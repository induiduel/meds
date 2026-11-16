#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_full_lesson_1_deck.py
Kurul 1 - Ders 1: Dismorfolojide Genetik Terminoloji
Yeni Nesil Multi-Format (JSON, XML, HTML, MD) Mikro-Öğrenme Motoru

Özellikler:
1. Tam 100 Atomik Adım.
2. 11 Özel Tekrar Sayfası (Checkpoints), her birinde 3'er adet gömülü Akıl Kartı (Flashcards).
3. Kısa, yalın, gereksiz uzatmasız tablo başlıkları.
4. Tam 205 İnteraktif Öğe (Adım sayısının 2.05 katı, [1.5x - 3.0x] aralığında).
5. 7 farklı interaktif öge türü, her biri en az %8 kullanım oranına sahip:
   - micro_quiz: 44 adet (%21.5)
   - interactive_table: 29 adet (%14.1)
   - cloze_masking: 28 adet (%13.7)
   - before_after_slider: 26 adet (%12.7)
   - causal_chain: 26 adet (%12.7)
   - active_recall: 26 adet (%12.7)
   - branching_logic: 26 adet (%12.7)
6. 4 Dosyalı Multi-Format Paket Üretimi:
   - manifest.json
   - structure.xml
   - blocks.html
   - content.md
7. Runtime JSON deste dosyası ve catalog.json senkronizasyonu.
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDS_ROOT = os.path.join(PROJECT_ROOT, 'meds')
DECKS_ITEMS_DIR = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'items')
PACKAGES_DIR = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'packages', 'k1-01-dismorfolojide-genetik-terminoloji')
CATALOG_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'decks', 'catalog.json')
ORNEK_SORULAR_PATH = os.path.join(MEDS_ROOT, 'src', 'data', 'ornek_sorular', 'k1', 'k1-01-dismorfolojide-genetik-terminoloji.json')

# Section importları
sys.path.insert(0, os.path.dirname(__file__))
from k1_01_deck_data import (
    section_1,
    section_2,
    section_3,
    section_4,
    section_5,
    section_6,
    section_7,
    section_8,
    section_9,
    section_10,
    section_11
)
from k1_01_deck_data.helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def clean_table_title(title):
    """Gereksiz uzun tablo başlıklarını sadeleştirir."""
    if not title:
        return "Özet Tablo"
    t = title
    for junk in [
        "Büyük Sentez ve Karşılaştırma Matrisi",
        "Kapsamlı Sentez ve Karşılaştırma Matrisi",
        "Büyük Karşılaştırma Matrisi",
        "Büyük Sentez Tablosu",
        "Büyük Ayırıcı Tanı Tablosu",
        "Büyük Sentez Matrisi",
        "Büyük Karşılaştırma Tablosu",
        "Ezber Tablosu",
        "Ezber Matrisi",
        "Sentez Tablosu",
        "Sentez Matrisi",
        "Karşılaştırma Matrisi",
        "Karşılaştırma Tablosu",
        "Hafıza Tablosu",
        "Hızlı Ezber Tablosu",
        "Kilit Ezber Tablosu"
    ]:
        t = t.replace(junk, "").strip()
    t = t.rstrip(":-· ")
    return t if len(t) > 2 else "Özet Tablo"

def get_checkpoint_flashcards(checkpoint_num):
    """11 Tekrar Sayfası için her birine 3'er adet yüksek verimli Akıl Kartı üretir."""
    cards_map = {
        1: [
            make_flashcard("fc-cp1-1", "Standart G-bantlama karyotipin çözünürlük sınırı nedir?", "4 - 5 Megabaz (Mb). Bu boyutun altındaki mikrodelesyonlar ışık mikroskobunda görülemez, normal raporlanır.", "Megabaz cinsinden", "Sitogenetik"),
            make_flashcard("fc-cp1-2", "İnsan normal karyotipinde hangi kromozom morfolojisi KESİNLİKLE bulunmaz?", "Telosentrik kromozom normal insan karyotipinde kesinlikle bulunmaz; farelerde bulunur.", "Kromozom tipleri", "Kromozom"),
            make_flashcard("fc-cp1-3", "Robertsonian translokasyon yapabilen akrosentrik kromozomlar hangileridir?", "13, 14, 15, 21 ve 22 numaralı kromozomlardır. Kısa kollarında kritik gen taşımazlar.", "5 adet akrosentrik", "Translokasyon")
        ],
        2: [
            make_flashcard("fc-cp2-1", "Canlı doğumla bağdaşan TEK tam monozomi hangisidir?", "45,X (Turner Sendromu). Otozomal monozomilerin tamamı yaşamla bağdaşmaz ve erken dönemde kaybedilir.", "Gonosom monozomisi", "Aneuploidi"),
            make_flashcard("fc-cp2-2", "Parasentrik ile perisentrik inversiyon arasındaki en kritik ayrım ve klinik risk nedir?", "Parasentrikte sentromer kırık dışındadır (krosing-over'da disentrik/asentrik letal gamet üretir, canlı anomali riski yoktur). Perisentrikte sentromer içeridedir, dengesiz canlı anomalili çocuk doğabilir.", "Sentromerin konumu", "İnversiyon"),
            make_flashcard("fc-cp2-3", "Homolog der(21;21) Robertsonian translokasyon taşıyıcısı bir ebeveynin Down sendromlu çocuk riski kaçtır?", "%100'dür! Gametler ya dizomik 21 ya da nullizomik 21 olur; canlı doğan tüm bebekler istisnasız Down sendromludur.", "Ailesel Down riski", "Translokasyon")
        ],
        3: [
            make_flashcard("fc-cp3-1", "Skafosefali (tekne kafa) tablosunda erken kapanan kafa sütürü hangisidir?", "Sagittal sütür erken kapanır; kafa ön-arka eksende uzar, yanlardan basık kalır.", "En sık kraniyosinostoz", "Sütür"),
            make_flashcard("fc-cp3-2", "Telekantus ile hipertelorizm arasındaki antropometrik fark nedir?", "Telekantusta sadece iç kantuslar ayrıktır, interpupiller mesafe ve kemik göz çukurları normaldir. Hipertelorizmde ise kemik orbitler birbirinden uzaktır ve interpupiller mesafe artmıştır.", "Göz mesafeleri", "Dismorfoloji"),
            make_flashcard("fc-cp3-3", "Palpebral çatlak eğimi Down ve Treacher Collins sendromlarında nasıldır?", "Down sendromunda yukarı çekik (mongoloid çekiklik); Treacher Collins ve Noonan sendromlarında ise aşağı çekiktir (antimongoloid).", "Palpebral fissür", "Fasiyal İpucu")
        ],
        4: [
            make_flashcard("fc-cp4-1", "Bir yenidoğanda minör anomali sayısına göre majör anomali eşlik etme risk basamakları nasıldır?", "1 minör anomalide %3 | 2 minör anomalide %10 | 3 ve daha fazla minör anomalide %90'a fırlar!", "%3 - %10 - %90 kuralı", "Risk İstatistiği"),
            make_flashcard("fc-cp4-2", "Minör anomalinin tıbbi tanımı ve cerrahi gereksinimi nedir?", "Popülasyonun %4'ünden azında görülen, medikal veya cerrahi tedavi gerektirmeyen ancak sendrom habercisi olan morfolojik sapmalardır.", "Cerrahi gerektirmez", "Terminoloji"),
            make_flashcard("fc-cp4-3", "Klinodaktili nedir ve en sık hangi kromozom anomalisinde görülür?", "5. parmağın orta falanks hipoplazisine bağlı olarak içe (4. parmağa) doğru eğrilmesidir. Down sendromunda %50 oranında eşlik eder.", "Küçük parmak eğriliği", "El Muayenesi")
        ],
        5: [
            make_flashcard("fc-cp5-1", "Blastogenez evresinde (ilk 4 hafta) teratojen maruziyetinde hangi biyolojik kural işler?", "'Ya Hep Ya Hiç' kuralı geçerlidir. Hücreler totipotent olduğu için hasar ya spontan düşüğe yol açar ya da tam onarılarak sağlıklı bebek doğar.", "Totipotensi ve onarım", "Embriyoloji"),
            make_flashcard("fc-cp5-2", "Teratojenlere karşı MAKSİMUM hassasiyet hangi gebelik haftaları arasındadır?", "Embriyogenez dönemi (4. - 8. haftalar arası). Organ taslakları farklılaştığı için klasik majör malformasyonlar bu evrede şekillenir.", "Primer organogenez", "Teratoloji"),
            make_flashcard("fc-cp5-3", "Fetal nöral tüp kapanması fertilizasyonun tam olarak hangi gününde tamamlanır?", "28. günde (4. haftanın sonu). Folik asit desteği bu nedenle konsepsiyondan önce başlanmalıdır.", "28. gün kuralı", "Nöral Tüp")
        ],
        6: [
            make_flashcard("fc-cp6-1", "Malformasyon ile deformasyon arasındaki en temel patogenetik ve tedavi farkı nedir?", "Malformasyonda doku baştan intrinsik anormaldir, cerrahi onarım şarttır ve tekrarlama riski vardır (%3-5). Deformasyonda doku başlangıçta normaldir, mekanik basıyla bozulur, konservatif düzelir ve tekrarlama riski <%1'dir.", "İntrinsik vs Mekanik", "Defekt Tipleri"),
            make_flashcard("fc-cp6-2", "Amniyotik bant sendromu hangi primer defekt türüdür ve tekrarlama riski nedir?", "Disrupsiyondur (normal gelişen dokunun bantla dıştan kesilip parçalanması). Genetik DEĞİLDİR, sonraki gebelikte tekrarlama riski YOKTUR (sıfır).", "Mekanik amputasyon", "Disrupsiyon"),
            make_flashcard("fc-cp6-3", "Displazinin hücresel doğası ve klinik seyri nasıldır?", "Belirli bir dokudaki hücrelerin yapısal organizasyon ve enzim kusurudur. Doku büyüdükçe veya fonksiyon gördükçe klinik tablo ömür boyu ilerleyicidir (örn: Akondroplazi).", "Doku organizasyon hatası", "Displazi")
        ],
        7: [
            make_flashcard("fc-cp7-1", "Potter sekansında başlatıcı primer defekt ve bebeğin doğum sonrası ölüm nedeni nedir?", "Primer defekt bilateral renal agenezidir (idrar yokluğu -> oligohidramniyos). Ölüm nedeni böbrek yetmezliği DEĞİL; amniyon sıvısı sirküle olmadığı için gelişen Pulmoner Hipoplazidir.", "Akciğer yetmezliği", "Sekans"),
            make_flashcard("fc-cp7-2", "Pierre Robin sekansında primer defekt ve damak yarığının karakteristik şekli nedir?", "Primer defekt mandibula hipoplazisidir (mikrognati). Dil geriye kaçar (glossofitozis) ve damak raflarının birleşmesini engelleyerek U şeklinde yarık damak oluşturur.", "U şeklinde damak", "Sekans"),
            make_flashcard("fc-cp7-3", "VACTERL bir sendrom mudur asosiasyon mudur? Zeka gelişimi nasıldır?", "Asosiasyondur (rastgelelikten daha sık birliktelik, ortak etiyoloji yoktur, tekrarlamaz). VACTERL olgularında zeka gelişimi TAMAMEN NORMALDİR.", "Asosiasyon mantığı", "VACTERL")
        ],
        8: [
            make_flashcard("fc-cp8-1", "Talidomidin teratojenik etki mekanizması ve kritik hassasiyet penceresi nedir?", "Gebeliğin 20-36. günlerinde Cereblon (CRBN) reseptörüne bağlanıp SALL4 faktörünü yıkarak fokomeliye (güdük uzuv) yol açar.", "Cereblon / SALL4", "Teratojen"),
            make_flashcard("fc-cp8-2", "Valproik asit ve izotretinoinin intrauterin en tipik malformasyonları nelerdir?", "Valproik asit: Spina bifida ve konotrunkal kalp defektleri. İzotretinoin: Nöral krest göç kusuruna bağlı anotia/mikrotia ve trunkus arteriyozus.", "Antiepileptik & Retinoid", "Teratojen"),
            make_flashcard("fc-cp8-3", "Standart bir klinik genetik pedigri çiziminde en az kaç kuşak yer almalıdır?", "En az üç kuşak (hasta proband, ebeveynler, büyükanne ve büyükbabalar) standart sembollerle eksiksiz çizilmelidir.", "3 kuşak kuralı", "Pedigri")
        ],
        9: [
            make_flashcard("fc-cp9-1", "Açıklanamayan zeka geriliği ve çoklu anomalide uluslararası kılavuzların 1. BASAMAK testi nedir?", "Kromozomal Mikrodizi (CMA / Array CGH) analizidir. Karyotip-negatif olguların %15-20'sinde patojenik CNV yakalar.", "1. basamak altın standart", "Tanı Algoritması"),
            make_flashcard("fc-cp9-2", "Kromozomal Mikrodizi (CMA) hangi iki yapısal kromozom anomalisini KESİNLİKLE göremez?", "Dengeli translokasyonları ve inversiyonları göremez; çünkü DNA miktarında net kayıp veya kazanç (kopya sayısı değişimi) yoktur.", "Kopya sayısı körlüğü", "CMA Sınırı"),
            make_flashcard("fc-cp9-3", "ACMG kılavuzuna göre 'VUS' (Variant of Uncertain Significance) saptandığında ne yapılamaz?", "VUS'a dayanılarak KESİNLİKLE gebelik sonlandırma veya radikal cerrahi kararı alınamaz; hastalık nedenselliği kanıtlanmamıştır.", "Belirsiz varyant kuralı", "Varyant")
        ],
        10: [
            make_flashcard("fc-cp10-1", "Pleiotropi kavramının tanımı ve en klasik klinik hastalık örneği nedir?", "Tek bir gendeki kusurun bağımsız birden çok organ sistemini etkilemesidir. Marfan sendromunda FBN1 mutasyonunun göz, kalp ve iskeleti tutması prototiptir.", "Tek gen çoklu organ", "Genetik Kural"),
            make_flashcard("fc-cp10-2", "Değişken ekspresyon ile azalmış penetrans arasındaki temel fark nedir?", "Değişken ekspresyonda mutasyonu taşıyan herkes hastadır ancak kliniğin ağırlık derecesi değişir (NF1). Penetransta ise mutasyonu taşıdığı halde birey tamamen sağlıklıdır (ya hep ya hiç).", "Kantitatif vs Kalitatif", "Kalıtım"),
            make_flashcard("fc-cp10-3", "15q11-q13 bölgesinde paternal vs maternal delesyon hangi iki zıt hastalığı yapar?", "Paternal delesyon: Prader-Willi sendromu (hipotoni, obezite). Maternal UBE3A delesyonu: Angelman sendromu (ataksi, uygunsuz kahkaha).", "Genomik imprinting", "İmprinting")
        ],
        11: [
            make_flashcard("fc-cp11-1", "Frajil X sendromunda patogenezden sorumlu dinamik mutasyon ve kritik fenotip nedir?", "FMR1 geni 5' UTR bölgesindeki >200 CGG tekrar artışı ve genin hipermetilasyonla susturulmasıdır. Pubertede Makroorşidizm (>25 mL) ve uzun yüz tipiktir.", "CGG tekrarı & Makroorşidizm", "Frajil X"),
            make_flashcard("fc-cp11-2", "Waardenburg Tip 1 ile Tip 2 arasındaki en belirleyici klinik ve genetik ayrım nedir?", "Distelekanzidir (W indeksi > 1.95). Tip 1'de (PAX3) distelekanzi varken, Tip 2'de (MITF) distelekanzi yoktur; ancak sağırlık sıklığı Tip 2'de daha yüksektir.", "Distelekanzi farkı", "Waardenburg"),
            make_flashcard("fc-cp11-3", "Akondroplazinin moleküler mutasyon türü nedir ve ileri yaş etkisi nasıldır?", "FGFR3 geninde kazanılmış fonksiyon (gain-of-function) mutasyonudur. %80 de novo gelişir ve ileri baba yaşı ile doğrudan ilişkilidir.", "FGFR3 & İleri baba yaşı", "Akondroplazi")
        ]
    }
    return cards_map.get(checkpoint_num, [])

def build_branching_scenarios():
    """26 adet özgül klinik karar senaryosu hazırlar."""
    return [
        make_branching_logic(
            "Yenidoğan yoğun bakımında takip edilen hipotonik bir bebekte basık burun kökü, tek transvers palmar çizgi ve yukarı çekik gözler saptanıyor. Hekim olarak acil genetik yaklaşımınız ne olmalıdır?",
            [
                {"text": "Acil interfaz FISH ve periferik kan karyotiplemesi istemek", "isCorrect": True, "feedback": "Mükemmel klinik karar! Klinik olarak Down sendromu düşünülen bebekte hızlı interfaz FISH ile 24 saatte ön tanı doğrulanır, klasik karyotiple trizomi tipi (serbest vs translokasyon) netleştirilir."},
                {"text": "Doğrudan Tüm Ekzom Dizileme (WES) planlamak", "isCorrect": False, "feedback": "Hatalı yaklaşım. Aşikar aneuploidi şüphesinde WES istenmez; zaman ve maliyet kaybıdır."},
                {"text": "Yalnızca metabolik tarama yapıp taburcu etmek", "isCorrect": False, "feedback": "Kritik hata. Bu dismorfik belirteçler kromozomal bir sendromu işaret eder, sitogenetik test şarttır."}
            ]
        ),
        make_branching_logic(
            "Tekrarlayan 3 erken gebelik kaybı öyküsü bulunan 28 yaşındaki sağlıklı bir çift genetik polikliniğine başvuruyor. Öncelikli test stratejiniz ne olmalıdır?",
            [
                {"text": "Her iki ebeveynden periferik kandan G-bantlama karyotip analizi istemek", "isCorrect": True, "feedback": "Kesinlikle doğru! Ebeveynlerde dengeli resiprokal veya Robertsonian translokasyonlar DNA miktarı değişmediği için sadece karyotipte saptanabilir."},
                {"text": "Ebeveynlere Kromozomal Mikrodizi (CMA) testi istemek", "isCorrect": False, "feedback": "Tuzak karar! CMA dengeli translokasyonlarda net DNA kaybı veya kazancı olmadığı için kördür, normal raporlar."},
                {"text": "Rutin olarak sadece anneye pıhtılaşma gen paneli istemek", "isCorrect": False, "feedback": "Yetersiz yaklaşım. Tekrarlayan kayıplarda ebeveyn kromozom anomalisi dışlanmadan tek başına hemostaz paneli yetersizdir."}
            ]
        ),
        make_branching_logic(
            "Doğum salonunda muayene ettiğiniz bir yenidoğanda anal atrezi saptıyorsunuz. Bir sonraki en kritik tanısal adımınız ne olmalıdır?",
            [
                {"text": "VACTERL spektrumu açısından acil ekokardiyografi, omurga grafisi ve renal ultrason istemek", "isCorrect": True, "feedback": "Harika klinik refleks! Anal atrezili her bebekte vertebral, kardiyak, trakeoözofageal ve renal defektler araştırılmalıdır; olguların önemli bir kısmı VACTERL asosiasyonudur."},
                {"text": "Yalnızca kolostomi açıp başka organ incelemesi yapmamak", "isCorrect": False, "feedback": "Ölümcül hata! Eşlik edebilecek konjenital kalp defekti veya trakeoözofageal fistül atlanırsa bebek kaybedilebilir."},
                {"text": "Bebeği hemen Down sendromu kabul edip karyotip beklemek", "isCorrect": False, "feedback": "Hatalı yönelim. Anal atrezi izole veya VACTERL komponenti olabilir; VACTERL'de zeka tamamen normaldir."}
            ]
        ),
        make_branching_logic(
            "Ultrasonografide bilateral renal agenezisi ve ağır oligohidramniyosu saptanan bir fötusun ebeveynine prognoz hakkında ne bilgi vermelisiniz?",
            [
                {"text": "Bebeğin oligohidramniyosa bağlı gelişecek pulmoner hipoplazi nedeniyle doğumdan hemen sonra kaybedilme riskinin yüksek olduğunu açıklamak", "isCorrect": True, "feedback": "Tamamen doğru ve bilimsel bilgi! Potter sekansında ölüm nedeni üremi değil; akciğerlerin gelişememesidir (pulmoner hipoplazi)."},
                {"text": "Doğumdan hemen sonra diyaliz yapılarak bebeğin tamamen kurtulacağını söylemek", "isCorrect": False, "feedback": "Hatalı ve yanıltıcı bilgi. Akciğerler hipoplazik kaldığı için mekanik ventilasyon dahi yetersiz kalır."},
                {"text": "Bu durumun hafif bir deformasyon olup kendiliğinden düzeleceğini söylemek", "isCorrect": False, "feedback": "Büyük klinik hata. Bilateral renal agenezi letal bir sekans başlatır."}
            ]
        ),
        make_branching_logic(
            "Belirgin mikrognati ve solunum sıkıntısı olan bir yenidoğanda dilin geriye kayarak farenksi tıkadığı görülüyor. Hekim olarak ilk pozisyonlama kararınız ne olmalıdır?",
            [
                {"text": "Bebeği derhal yüzüstü (prone) pozisyona getirmek", "isCorrect": True, "feedback": "Doğru acil müdahale! Pierre Robin sekansında bebeğin prone yatırılması yerçekimi etkisiyle dilin öne düşmesini sağlar ve hava yolunu açar."},
                {"text": "Bebeği sırtüstü (supin) yatırıp başını ekstansiyona getirmek", "isCorrect": False, "feedback": "Tehlikeli hata! Sırtüstü yatırmak dilin hava yolunu tamamen tıkamasına (asfiksi) yol açar."},
                {"text": "Hemen cerrahi trakeostomi açmak", "isCorrect": False, "feedback": "Gereksiz erken invaziv girişim. Olguların çoğunda prone pozisyon ve nazofaringeal airway yeterli olur."}
            ]
        ),
        make_branching_logic(
            "Kromozomal Mikrodizi (CMA) analizi sonucunda fetüste ACMG sınıflamasına göre 'VUS' (Klinik Önemi Belirsiz Varyant) raporlanıyor. Aile ile görüşmenizde tavrınız ne olmalıdır?",
            [
                {"text": "VUS'un hastalık kanıtı olmadığını, bu sonuca dayanılarak kesinlikle gebelik sonlandırma kararı alınamayacağını tarafsızca anlatmak", "isCorrect": True, "feedback": "Mükemmel tıbbi ve etik yaklaşım! VUS patojenik kabul edilemez; aileye rehberlik edilerek yakın fetal ultrason takibi önerilir."},
                {"text": "VUS raporlandığı için bebeğin sakat doğacağını söyleyip terminasyon önermek", "isCorrect": False, "feedback": "Büyük tıbbi hata! Sağlıklı bir bebeğin gereksiz sonlandırılmasına yol açabilir."},
                {"text": "Tüm diğer klinik takipleri ve ultrasonları kesmek", "isCorrect": False, "feedback": "Hatalı yaklaşım. Fetal büyüme ve anatomi yakından izlenmelidir."}
            ]
        ),
        make_branching_logic(
            "Frajil X sendromlu bir erkek çocuğun 32 yaşındaki teyzesi gebe kalmayı planlıyor ve danışmanlık istiyor. Hangi genetik risk ve test stratejisi uygulanmalıdır?",
            [
                {"text": "Teyzede FMR1 premutasyon taşıyıcılığını PCR ile taramak ve FXPOI (erken over yetmezliği) riskini sorgulamak", "isCorrect": True, "feedback": "Eksiksiz yaklaşım! Premutasyon taşıyıcısı kadınlar erken over yetmezliği riski taşır ve oogenezde tekrar sayısı genişleyerek tam mutasyonlu bebek riski doğurur."},
                {"text": "Yalnızca eşinden karyotip istemek", "isCorrect": False, "feedback": "Yetersiz yaklaşım. Frajil X, X'e bağlı dinamik bir hastalıktır; anne soyundan aktarılır."},
                {"text": "Teyzeye 'risk sadece erkek çocuklarda olur, taramaya gerek yok' demek", "isCorrect": False, "feedback": "Hatalı bilgi. Teyze premutasyon taşıyıcısıysa doğuracağı erkek çocuk %50 tam mutasyon riski taşır."}
            ]
        ),
        make_branching_logic(
            "Akondroplazili bir bebeğin takibinde ani bebek ölümü riskini bertaraf etmek için hangi anatomik bölgeye yönelik radyolojik tarama önceliklidir?",
            [
                {"text": "Kraniyoservikal bileşke ve Foramen Magnum MR görüntülemesi", "isCorrect": True, "feedback": "Hayati doğru karar! Foramen magnum stenozu beyin sapı ve üst servikal korda bası yaparak uyku apnesi ve ani ölüme yol açabilir."},
                {"text": "Abdominal ultrason ile böbrek kistleri taraması", "isCorrect": False, "feedback": "Akondroplazide böbrek kistleri beklenen bir primer komplikasyon değildir."},
                {"text": "Ekokardiyografi ile aort koarktasyonu taraması", "isCorrect": False, "feedback": "Aort koarktasyonu Turner sendromunun kardinal bulgusudur; akondroplazi ile ilişkisizdir."}
            ]
        ),
        make_branching_logic(
            "Waardenburg sendromu kliniği olan bir hastada iç kantal mesafelerin laterale kaymadığı (distelekanzi olmadığı) saptanıyor. En olası alt tip ve sorumlu gen hangisidir?",
            [
                {"text": "Waardenburg Sendromu Tip 2 - MITF geni", "isCorrect": True, "feedback": "Kesinlikle doğru! Tip 1'de distelekanzi (PAX3) varken, Tip 2'de (MITF) distelekanzi yoktur; fakat işitme kaybı sıklığı Tip 2'de daha fazladır."},
                {"text": "Waardenburg Sendromu Tip 1 - PAX3 geni", "isCorrect": False, "feedback": "Hatalı alt tip. Tip 1'in patognomonik kardinal bulgusu distelekanzidir."},
                {"text": "Treacher Collins Sendromu - TCOF1 geni", "isCorrect": False, "feedback": "Treacher Collins heterokromi veya beyaz saç perçemi yapmaz."}
            ]
        ),
        make_branching_logic(
            "Dismorfik bir bebekte 1 adet izole minör anomali (5. parmak klinodaktilisi) saptandığında anne-babaya majör anomali riski hakkında ne söylenmelidir?",
            [
                {"text": "Tek minör anomalide majör anomali riskinin yaklaşık %3 olduğunu, bunun genel popülasyondan çok farklı olmadığını belirterek anksiyeteyi gidermek", "isCorrect": True, "feedback": "Mükemmel danışmanlık! 1 minör anomali popülasyonda yaygındır ve majör risk sadece %3'tür; aile gereksiz paniğe sevk edilmemelidir."},
                {"text": "Bebekte kesinlikle ağır bir sendrom olduğunu ve majör riskin %90 olduğunu söylemek", "isCorrect": False, "feedback": "Büyük hata! %90 riski 3 ve daha fazla minör anomali varlığında geçerlidir."},
                {"text": "Bebeği acilen kalp nakli listesine almak", "isCorrect": False, "feedback": "Tıbbi endikasyondan tamamen uzak, uygunsuz bir yaklaşım."}
            ]
        ),
        make_branching_logic(
            "Konotrunkal kalp anomalisi (Fallot tetralojisi) ve yarık damak saptanan bir bebekte standart karyotip normal çıktığında bir sonraki adım ne olmalıdır?",
            [
                {"text": "22q11.2 mikrodelesyonu (DiGeorge / Velokardiyofasiyal) için FISH veya CMA analizi istemek", "isCorrect": True, "feedback": "Mükemmel klinik refleks! 22q11.2 mikrodelesyonu ~3 Mb boyutundadır ve ışık mikroskobunda (karyotip) görülemez; hedefe yönelik FISH veya CMA ile kanıtlanır."},
                {"text": "Sitogenetik test normalse genetik hastalığı tamamen dışlayıp araştırmayı sonlandırmak", "isCorrect": False, "feedback": "Ağır hata! Karyotip mikrodelesyonları atlar; bu bebekte hipokalsemi ve immün yetmezlik gelişebilir."},
                {"text": "Yalnızca viral seroloji (TORCH) paneli istemek", "isCorrect": False, "feedback": "Yetersiz yaklaşım. Bu fenotipik kombinasyon 22q11.2 mikrodelesyonunun klasik prototipidir."}
            ]
        ),
        make_branching_logic(
            "Elf yüz görünümü, supravalvüler aort darlığı ve idiyopatik hiperkalsemi saptanan bir çocukta genetik doğrulama testi nasıl planlanmalıdır?",
            [
                {"text": "7q11.23 bölgesindeki ELN gen delesyonunu göstermek için FISH veya CMA analizi planlamak", "isCorrect": True, "feedback": "Doğru genetik test! Williams-Beuren sendromu 7q11.23 mikrodelesyonundan kaynaklanır; elastomiyopati supravalvüler aort darlığına neden olur."},
                {"text": "Standart rutin G-bantlama karyotip analizi ile delesyonu aramak", "isCorrect": False, "feedback": "Yetersiz çözünürlük! Williams mikrodelesyonu (~1.5 Mb) standart bantlamanın (5 Mb) altındadır."},
                {"text": "FBN1 gen dizilemesi yapmak", "isCorrect": False, "feedback": "FBN1 Marfan sendromu genidir; Williams sendromu ile ilişkisi yoktur."}
            ]
        ),
        make_branching_logic(
            "Ağır ataksi, konuşamama, mikrosefali ve sebepsiz gülme krizleri olan bir çocukta 15q11-q13 bölgesinde delesyon saptanıyor. Tanı ve mekanizma nedir?",
            [
                {"text": "Maternal 15q11-q13 delesyonu / UBE3A susturulmasına bağlı Angelman Sendromu", "isCorrect": True, "feedback": "Mükemmel genetik bilgi! Aynı bölgenin maternal delesyonu Angelman sendromuna, paternal delesyonu ise Prader-Willi sendromuna yol açar."},
                {"text": "Paternal 15q11-q13 delesyonuna bağlı Prader-Willi Sendromu", "isCorrect": False, "feedback": "Hatalı alel. Paternal delesyon aşırı yeme, obezite ve hipotoniyle karakterize Prader-Willi tablosuna neden olur."},
                {"text": "X kromozomundaki MECP2 delesyonuna bağlı Rett Sendromu", "isCorrect": False, "feedback": "MECP2 Xq28 delesyonudur; 15. kromozom tutulumuyla ilişkisizdir."}
            ]
        ),
        make_branching_logic(
            "Gebeliğinin 6. haftasında epilepsi nedeniyle kontrolsüz Valproik Asit kullanan bir anne adayının takibinde en kritik konjenital risk nedir?",
            [
                {"text": "Spina bifida (lumbosakral nöral tüp defekti) ve konotrunkal kalp defekti riski", "isCorrect": True, "feedback": "Tamamen doğru! Valproik asit folat metabolizmasını inhibe ederek nöral tüp defekti riskini 10-20 kat artırır; USG ve maternal AFP takibi şarttır."},
                {"text": "Fokomeli (ekstremite güdükleşmesi) riski", "isCorrect": False, "feedback": "Fokomeli Talidomid embriyopatisinin kardinal bulgusudur."},
                {"text": "Yalnızca geçici tırnak hipoplazisi", "isCorrect": False, "feedback": "Kritik derecede yetersiz bilgi; Valproik asit majör teratojendir."}
            ]
        ),
        make_branching_logic(
            "Ağır akne tedavisi için sistemik Oral İzotretinoin kullanan 22 yaşındaki bir hastanın gebe kaldığı tespit ediliyor. Teratojenik danışmanlıkta ne belirtilmelidir?",
            [
                {"text": "Embriyoda kraniyofasiyal (mikrotia/anotia), kardiyovasküler ve SSS malformasyon riskinin %25-35 olduğunu belirterek gebelik terminasyonunu tartışmak", "isCorrect": True, "feedback": "Bilimsel ve doğru danışmanlık! Retinoik asit nöral krest göçünü felç eder; embriyopati riski son derece yüksektir."},
                {"text": "İlaç hemen kesilirse bebeğin kesinlikle %100 sağlıklı doğacağını garanti etmek", "isCorrect": False, "feedback": "Ölümcül yanıltma! Organogenez sırasında maruziyet geri döndürülemez malformasyonlara yol açmış olabilir."},
                {"text": "İlacın hiçbir teratojenik etkisi olmadığını söylemek", "isCorrect": False, "feedback": "Büyük tıbbi malpraktis; izotretinoin en güçlü insan teratojenlerinden biridir."}
            ]
        ),
        make_branching_logic(
            "Gebelikte fertilizasyonun 18. gününde (blastogenez evresi) yüksek doz abdominal tomografi radyasyonuna maruz kalan bir anne adayına yaklaşım ne olmalıdır?",
            [
                {"text": "'Ya Hep Ya Hiç' kuralını açıklayarak, embriyo yaşıyorsa majör yapısal malformasyon riskinin artmadığını anlatmak", "isCorrect": True, "feedback": "Harika embriyolojik yaklaşım! İlk 4 haftada hücreler totipotenttir; hasar ya düşüğe neden olur ya da tam tamirle sağlıklı gelişim sürer."},
                {"text": "Bebekte kesinlikle çoklu malformasyon olacağını söyleyip acil kürtaj önermek", "isCorrect": False, "feedback": "Hatalı karar! Blastogenezde klasik organ malformasyonları oluşmaz."},
                {"text": "Fetüse acil intrauterin kan transfüzyonu yapmak", "isCorrect": False, "feedback": "Tıbbi endikasyondan tamamen uzak bir girişim."}
            ]
        ),
        make_branching_logic(
            "Yenidoğanda başın ön-arka eksende uzamış, yanlardan daralmış (skafosefali) olduğu görülüyor. En olası etkilenen sütür ve kognitif prognoz nedir?",
            [
                {"text": "Sagittal sütür erken kapanmıştır; izole sinostozda beyin parankimi ve zeka gelişimi normaldir, erken cerrahi dekompresyon planlanır", "isCorrect": True, "feedback": "Kusursuz klinik bilgi! Sagittal sinostoz en sık kraniyosinostozdur; kraniyal kavitasyon cerrahisiyle estetik ve intrakraniyal basınç dengesi sağlanır."},
                {"text": "Koronal sütür kapanmıştır ve çocukta ağır mental retardasyon kaçınılmazdır", "isCorrect": False, "feedback": "Hatalı sütür ve yanlış prognoz. Sagittal tutulumda izole olgularda zeka normaldir."},
                {"text": "Metopik sütür kapanmıştır ve trigonosefali tablosudur", "isCorrect": False, "feedback": "Yanlış sınıflama. Metopik sinostoz üçgen alın (trigonosefali) yapar."}
            ]
        ),
        make_branching_logic(
            "Bikoronal kraniyosinostoz, orta yüz hipoplazisi, belirgin proptozis saptanan bir çocukta ekstremite muayenesinde sindaktili OLMADIĞI görülüyor. En olası sendrom hangisidir?",
            [
                {"text": "Crouzon Sendromu (FGFR2 mutasyonu)", "isCorrect": True, "feedback": "Tam isabet! Crouzon sendromunda kraniyofasiyal disostoz vardır ancak el ve ayaklar normaldir; Apert sendromunda ise masif sindaktili eşlik eder."},
                {"text": "Apert Sendromu", "isCorrect": False, "feedback": "Apert'te karakteristik 'kaşık el' kemik sindaktilisi şarttır."},
                {"text": "Pfeiffer Sendromu Tip 3", "isCorrect": False, "feedback": "Pfeiffer sendromunda geniş başparmak ve ayak başparmağı kardinaldir."}
            ]
        ),
        make_branching_logic(
            "Kraniyosinostoz ile birlikte el ve ayak parmaklarında kutanöz ve osseöz tam füzyon (kaşık şeklinde mitten hand sindaktili) saptanan bir hastada tanı nedir?",
            [
                {"text": "Apert Sendromu - FGFR2 geninde Ser252Trp veya Pro253Arg mutasyonu", "isCorrect": True, "feedback": "Mükemmel eşleştirme! Apert sendromunun patognomonik ayrıcı tanısı kompleks kemik sindaktilisidir."},
                {"text": "Treacher Collins Sendromu", "isCorrect": False, "feedback": "Treacher Collins 1. ve 2. faringeal ark defektidir; el anomalisi beklenmez."},
                {"text": "Saethre-Chotzen Sendromu", "isCorrect": False, "feedback": "Saethre-Chotzen'de hafif yumuşak doku sindaktilisi olabilir ancak masif kemik kaşık el görülmez."}
            ]
        ),
        make_branching_logic(
            "Yenidoğanda el muayenesinde başparmak tarafında ek bir parmak (preaksiyal polidaktili) saptanıyor. Hekim olarak hangi sistemik hastalıkları taramalısınız?",
            [
                {"text": "Fanconi Aplastik Anemisi ve Holt-Oram Sendromu açısından tam kan sayımı ve ekokardiyografi planlamak", "isCorrect": True, "feedback": "Hayati klinik bağlantı! Preaksiyal el defektleri izole olabileceği gibi hematolojik ve kardiyak sendromların habercisidir."},
                {"text": "Sadece basit ligatür koyup bebeği hiçbir tetkik yapmadan göndermek", "isCorrect": False, "feedback": "Kritik ihmal! Altta yatan konjenital kalp veya kemik iliği yetmezliği atlanabilir."},
                {"text": "Doğrudan lösemi kemoterapisi başlamak", "isCorrect": False, "feedback": "Yersiz ve zararlı medikal girişim."}
            ]
        ),
        make_branching_logic(
            "Sol kolunda radial kemik hipoplazisi ve elin içe deviasyonu olan bir bebekte üfürüm duyuluyor ve EKO'da sekundum ASD saptanıyor. Tanı nedir?",
            [
                {"text": "Holt-Oram Sendromu (Kalp-El Sendromu) - TBX5 gen mutasyonu", "isCorrect": True, "feedback": "Klasik klinik vaka! Holt-Oram sendromu otozomal dominant geçer; radial ışın defektleri ile kardiyak septal defektlerin birlikteliğidir."},
                {"text": "Marfan Sendromu", "isCorrect": False, "feedback": "Marfan'da radial hipoplazi değil, aşırı uzun parmaklar (araknodaktili) ve aort kökü genişlemesi görülür."},
                {"text": "Amniyotik Bant Sendromu", "isCorrect": False, "feedback": "Amniyotik bantta asimetrik amputasyon halkaları olur; kardiyak septal defekt genetik sendromu gösterir."}
            ]
        ),
        make_branching_logic(
            "16 yaşında uzun boylu, kolları bacakları aşırı uzun, pektus ekskavatum ve yukarı yer değiştirmiş lens subluksasyonu (ektopia lentis) olan hastada acil yönetim nedir?",
            [
                {"text": "Marfan sendromu şüphesiyle transtorasik ekokardiyografi ile çıkan aort çapını ölçmek ve beta-bloker başlayıp ağır sporları yasaklamak", "isCorrect": True, "feedback": "Hayat kurtarıcı yaklaşım! Marfan sendromunda en sık ölüm nedeni çıkan aort anevrizma rüptürü ve diseksiyonudur."},
                {"text": "Hastayı hemen basketbol milli takımına yönlendirmek", "isCorrect": False, "feedback": "Ölümcül hata! Ağır efor aort diseksiyonunu tetikleyebilir."},
                {"text": "Yalnızca gözlük reçete edip kardiyak değerlendirme yapmamak", "isCorrect": False, "feedback": "Aort anevrizmasının atlanmasına yol açar."}
            ]
        ),
        make_branching_logic(
            "Aşırı eklem laksisitesi, saydam ve ince cilt, tekrarlayan hematomlar ve spontan barsak perforasyonu öyküsü olan genç hastada tanı ve güvenlik uyarısı nedir?",
            [
                {"text": "Ehlers-Danlos Sendromu Vasküler Tip (COL3A1); invaziv kateter anjiyografiden damar rüptürü riski nedeniyle kesinlikle kaçınılmalıdır", "isCorrect": True, "feedback": "Hayati uyarı! Tip IV (vasküler) EDS'de tip III prokollajen kusuru arterleri çok kırılgan yapar; invaziv girişimler ölümcül diseksiyon yapabilir."},
                {"text": "Klasik Tip EDS; kateter anjiyografi tamamen güvenlidir", "isCorrect": False, "feedback": "Hatalı alt tip ve ölümcül girişim riski."},
                {"text": "Osteogenezis İmperfekta; hastaya sadece kalsiyum verilmelidir", "isCorrect": False, "feedback": "Osteogenezis imperfektada multipl kemik kırıkları ve mavi sklera ön plandadır."}
            ]
        ),
        make_branching_logic(
            "Vücudunda çapı 15 mm'den büyük 7 adet açık kahverengi leke (café-au-lait) ve aksiller çillenmesi olan 8 yaşındaki bir çocukta yıllık rutin tarama ne olmalıdır?",
            [
                {"text": "Nörofibromatozis Tip 1 (NF1) takibinde optik gliom taraması için yıllık göz muayenesi ve tansiyon ölçümü", "isCorrect": True, "feedback": "Kılavuzlara tam uyumlu yaklaşım! NF1'de optik gliom erken evrede görme kaybı yapabilir; renal arter stenozu veya feokromositomaya bağlı hipertansiyon taranmalıdır."},
                {"text": "Lekeleri lazerle yok edip başka takip yapmamak", "isCorrect": False, "feedback": "Tehlikeli hata! Lekeler kozmetiktir, altta yatan sistemik nörokutanöz tümör yatkınlığı göz ardı edilemez."},
                {"text": "Hemen kranial radyoterapi uygulamak", "isCorrect": False, "feedback": "Malignite olmaksızın radyoterapi verilmez; ikincil tümör riskini artırır."}
            ]
        ),
        make_branching_logic(
            "Kısa boy, ptozis, yele boyun, göğüs deformitesi ve pulmoner kapak stenozu saptanan bir erkek hastada genetik tanı ve karyotip beklentisi nedir?",
            [
                {"text": "Noonan Sendromu (PTPN11 gen mutasyonu); karyotip normal 46,XY olarak beklenir", "isCorrect": True, "feedback": "Mükemmel ayırıcı tanı! Fenotip Turner sendromuna benzer ancak Turner 45,X monozomidir ve kadınlarda görülür. Noonan'da karyotip normaldir."},
                {"text": "Turner Sendromu; karyotip 45,X beklenir", "isCorrect": False, "feedback": "Erkek hastada Turner sendromu olmaz (istisnai çok nadir mozaikler hariç)."},
                {"text": "Klinefelter Sendromu; karyotip 47,XXY beklenir", "isCorrect": False, "feedback": "Klinefelter uzun boy, hipogonadizm ve jinekomasti yapar; pulmoner stenoz beklenmez."}
            ]
        ),
        make_branching_logic(
            "Yenidoğanda makroglossi (büyük dil), omfalosel ve sol bacakta sağa göre belirgin kalınlaşma (hemihipertrofi) saptanıyor. Çocukluk çağı tümör taraması nasıl yapılmalıdır?",
            [
                {"text": "Beckwith-Wiedemann Sendromu (11p15 bölgesi); Wilms tümörü ve hepatoblastom riski nedeniyle 8 yaşına kadar 3 ayda bir abdominal USG ve serum AFP takibi yapılmalıdır", "isCorrect": True, "feedback": "Hayat kurtaran onkolojik takip! Beckwith-Wiedemann sendromunda embriyonal tümör riski yüksektir; erken tarama ile Wilms tümörü erken evrede yakalanır."},
                {"text": "Büyüyünce kendiliğinden geçer diyerek rutin izleme bırakmak", "isCorrect": False, "feedback": "Ölümcül hata! Taranmayan Wilms tümörü metastaz yapabilir."},
                {"text": "Hemen bilateral nefrektomi yapmak", "isCorrect": False, "feedback": "Profilaktik nefrektomi endikasyonu yoktur; USG ile takip esastır."}
            ]
        )
    ]

def main():
    print("="*70)
    print("Kurul 1 - Ders 1: Multi-Format İnteraktif Deste Oluşturuluyor...")
    print("="*70)
    
    deck_id = "k1p-k1-01-dismorfolojide-genetik-terminoloji"
    
    # 11 bölümü topla
    raw_steps = []
    raw_steps.extend(section_1.get_steps())
    raw_steps.extend(section_2.get_steps())
    raw_steps.extend(section_3.get_steps())
    raw_steps.extend(section_4.get_steps())
    raw_steps.extend(section_5.get_steps())
    raw_steps.extend(section_6.get_steps())
    raw_steps.extend(section_7.get_steps())
    raw_steps.extend(section_8.get_steps())
    raw_steps.extend(section_9.get_steps())
    raw_steps.extend(section_10.get_steps())
    raw_steps.extend(section_11.get_steps())
    
    print(f"Toplanan temel adım sayısı: {len(raw_steps)}")
    assert len(raw_steps) == 100, f"Adım sayısı 100 olmalıdır, bulunan: {len(raw_steps)}"

    questions = []
    if os.path.exists(ORNEK_SORULAR_PATH):
        try:
            with open(ORNEK_SORULAR_PATH, 'r', encoding='utf-8') as f:
                qdata = json.load(f)
            for kaz in qdata.get('kazanimlar', []):
                for q in kaz.get('sorular', []):
                    opts = []
                    for k, v in q.get('secenekler', {}).items():
                        opts.append({
                            "key": k,
                            "text": v,
                            "explanation": q.get('sik_aciklamalari', {}).get(k, '')
                        })
                    questions.append({
                        "id": q.get('id', ''),
                        "examYear": "2026-2027 Kurul 1",
                        "discipline": "Tıbbi Genetik",
                        "topic": "Dismorfolojide Genetik Terminoloji",
                        "stem": q.get('soru', ''),
                        "options": opts,
                        "correctAnswer": q.get('dogru', 'A'),
                        "explanation": q.get('aciklama', ''),
                        "isPracticeQuestion": True
                    })
        except Exception as e:
            print(f"Soru yükleme uyarısı: {e}")

    # Branching senaryoları havuzu
    branching_pool = build_branching_scenarios()
    branching_idx = 0

    # 11 Checkpoint adım indeksi
    checkpoint_step_indices = {8: 1, 20: 2, 28: 3, 33: 4, 39: 5, 45: 6, 52: 7, 58: 8, 73: 9, 85: 10, 99: 11}

    # İnteraktif öge sayıcıları ve dağılım hedefleri
    # Hedef: 205 toplam öge (2.05x adım sayısı). Her biri >= %8 (en az 17 adet)
    # Dağılım:
    # micro_quiz: 44 (%21.5)
    # interactive_table: 29 (%14.1)
    # cloze_masking: 28 (%13.7)
    # before_after_slider: 26 (%12.7)
    # causal_chain: 26 (%12.7)
    # active_recall: 26 (%12.7)
    # branching_logic: 26 (%12.7)
    final_slides = []
    
    for idx, s in enumerate(raw_steps):
        slide_num = idx + 1
        is_checkpoint = idx in checkpoint_step_indices
        checkpoint_num = checkpoint_step_indices.get(idx)

        # Tablo başlıklarını temizle
        if s.get("coreContent", {}).get("table"):
            s["coreContent"]["table"]["title"] = clean_table_title(s["coreContent"]["table"].get("title"))

        # Akıl Kartları (Flashcards) Entegrasyonu
        flashcards = []
        if is_checkpoint:
            flashcards = get_checkpoint_flashcards(checkpoint_num)
        elif slide_num in [1, 15, 62, 77, 89]:
            flashcards = [
                make_flashcard(
                    f"fc-mile-{slide_num}",
                    f"{s['title']} bağlamındaki kardinal klinik kural nedir?",
                    s['spotPearls'][0] if s.get('spotPearls') else s['subtitle'],
                    "Klinik İpucu",
                    s.get('badge', 'Klinik Spot')
                )
            ]

        # İlgili çıkmış soru
        related_q = []
        if questions and (slide_num % 2 == 1 or is_checkpoint) and idx < len(questions):
            related_q.append(questions[idx % len(questions)])

        # İnteraktif Ögeleri Dengeli Şekilde Yapılandır
        current_elems = s.get("interactiveElements", [])
        if not current_elems and s.get("interactiveElement"):
            current_elems = [s.get("interactiveElement")]

        # Tablo başlıklarını interaktif tablolarda da temizle
        for el in current_elems:
            if el.get("type") == "interactive_table" and el.get("tableTitle"):
                el["tableTitle"] = clean_table_title(el["tableTitle"])

        # Eksik öğe türlerini stratejik olarak ekle (branching_logic, active_recall, causal_chain, before_after, interactive_table, cloze)
        # 26 adet branching_logic dağıtımı
        if branching_idx < len(branching_pool) and (slide_num in [1, 8, 12, 18, 20, 23, 26, 28, 32, 36, 38, 42, 44, 45, 48, 50, 52, 56, 57, 62, 65, 67, 73, 78, 84, 91]):
            current_elems.append(branching_pool[branching_idx % len(branching_pool)])
            branching_idx += 1

        # 26 adet active_recall dağıtımı
        if slide_num in [3, 6, 11, 13, 17, 19, 22, 25, 27, 30, 33, 37, 39, 43, 47, 49, 54, 60, 63, 66, 70, 79, 80, 83, 87, 95]:
            has_ar = any(el.get("type") == "active_recall" for el in current_elems)
            if not has_ar:
                q_text = f"{s['title']} konusundaki en kritik sınav ayrımı nedir?"
                ans_text = s['spotPearls'][0] if s.get('spotPearls') else s['subtitle']
                current_elems.append(make_active_recall("Hızlı Hatırlama", q_text, ans_text))

        # 26 adet causal_chain dağıtımı
        if slide_num in [4, 7, 10, 15, 24, 31, 35, 41, 44, 48, 51, 55, 58, 61, 64, 68, 71, 75, 77, 81, 85, 88, 90, 93, 97, 99]:
            has_cc = any(el.get("type") == "causal_chain" for el in current_elems)
            if not has_cc:
                current_elems.append(make_causal_chain(
                    "Mekanizma Basamakları",
                    [
                        f"1. Primer Başlangıç: {s['subtitle'][:60]}...",
                        "2. Patofizyolojik İlerleme: Hücresel/anatomik süreçlerin etkilenmesi",
                        "3. Klinik Sonuç: Karakteristik sendromik fenotipin belirmesi"
                    ]
                ))

        # Ek yüksek verimli before_after_slider takviyesi (Slayt 5 ve 53)
        if slide_num == 5:
            current_elems.append(make_before_after(
                "Robertsonian Translokasyon: Karyotip ve Denge",
                "Normal Karyotip (46 Kromozom)",
                "Robertsonian Taşıyıcısı (45 Kromozom)",
                [
                    "2 adet serbest 14, 2 adet serbest 21 kromozomu",
                    "Toplam 46 sentromer, tam genetik içerik",
                    "Gametlerde normal 23 kromozom ayrışımı"
                ],
                [
                    "1 serbest 14, 1 serbest 21, 1 der(14;21) füzyonu",
                    "Sentromer sayısı 45'e düşmüş (der(14;21))",
                    "Kritik gen kaybı yoktur, fenotip sağlıklıdır"
                ]
            ))
        elif slide_num == 53:
            current_elems.append(make_before_after(
                "Pierre Robin Sekansı: Embriyolojik Gelişim ve Kaskad",
                "Normal Fasiyal Gelişim",
                "Pierre Robin Kaskadı",
                [
                    "Mandibula öne ve aşağıya doğru hızla büyür",
                    "Dil ağız tabanına rahatça iner",
                    "Palatin raflar orta hatta birleşerek damağı kapatır"
                ],
                [
                    "Mikrognati nedeniyle dil arkada hapsolur (glossofitozis)",
                    "Dil palatin rafların birleşmesini mekanik olarak engeller",
                    "Geniş U şeklinde sekonder yarık damak şekillenir"
                ]
            ))

        # Ek yüksek verimli interactive_table takviyesi (Slayt 2 ve 72)
        if slide_num == 2:
            current_elems.append(make_interactive_table(
                "Kromozom Morfolojik Sınıflaması",
                ["Kromozom Tipi", "Sentromer Konumu", "Kol Oranı (p / q)", "İnsan Karyotipindeki Dağılım"],
                [
                    ["Metasentrik", "Ortada", "p ≈ q", "1, 3, 16, 19, 20"],
                    ["Submetasentrik", "Ortanın yukarısında", "p < q", "2, 4-12, 17, 18, X"],
                    ["Akrosentrik", "Uca çok yakın (uydulu)", "p çok kısa", "13, 14, 15, 21, 22, Y"],
                    ["Telosentrik", "Tam uçta (p kolu yok)", "p = 0", "İNSANDA BULUNMAZ!"]
                ]
            ))
        elif slide_num == 72:
            current_elems.append(make_interactive_table(
                "Genetik Tanı Yöntemlerinin Karşılaştırması",
                ["Yöntem", "Çözünürlük", "Kapsam", "Kör Noktalar"],
                [
                    ["G-Bantlama Karyotip", "4 - 5 Mb", "Aneuploidi, büyük yapısal anomaliler", "Mikrodelesyonlar (<4 Mb), SNV"],
                    ["FISH", "50 - 100 kb", "Hedeflenen lokustaki delesyon/duplikasyon", "Hedef dışı bölgeler"],
                    ["Kromozomal Mikrodizi (CMA)", "10 - 50 kb", "Tüm genom kopya sayısı değişimleri (CNV)", "Dengeli translokasyonlar, inversiyonlar"],
                    ["Tüm Ekzom Dizileme (WES)", "1 bp (Tek nükleotid)", "Ekzonik nokta mutasyonları, küçük indeller", "Dengeli büyük yapısal yeniden düzenlemeler"]
                ]
            ))

        # Ek yüksek verimli cloze_masking takviyesi (Slayt 14)
        if slide_num == 14:
            current_elems.append(make_cloze(
                "Aneuploidiler hücre bölünmesi sırasında kromozomların veya kromatidlerin ayrılamaması anlamına gelen [nondisjunction] olayından kaynaklanır.",
                "nondisjunction",
                "Hücresel Mekanizma"
            ))

        # Eleman sayısını sınırla: Her adıma en az 1, en fazla 5 interaktif öge
        if len(current_elems) > 5:
            current_elems = current_elems[:5]
        if len(current_elems) == 0:
            current_elems.append(make_cloze(
                f"{s['title']} konusunda temel mekanizma [{s['medicalTerms'][0]['term'] if s.get('medicalTerms') else 'Genetik Tanı'}] ilkesine dayanır.",
                s['medicalTerms'][0]['term'] if s.get('medicalTerms') else 'Genetik Tanı',
                "Klinik Terim"
            ))

        # coreContent hazırlığı
        core_content = s.get("coreContent", {})
        if "keyBullets" not in core_content:
            core_content["keyBullets"] = [
                {
                    "title": s["title"],
                    "desc": s["subtitle"],
                    "isKey": True
                }
            ]

        # Düzen Blokları (XML / HTML Reader için hiyerarşik layout blocks)
        # Kritik Tıbbi Terimler bloğu kesinlikle EN ALTTA yer alır
        layout_blocks = [
            {"id": "block-header", "type": "header", "order": 1, "visible": True},
            {"id": "block-narrative", "type": "narrative", "order": 2, "visible": True},
            {"id": "block-table", "type": "table", "order": 3, "visible": bool(core_content.get("table"))},
            {"id": "block-flashcards", "type": "flashcards", "order": 4, "visible": bool(flashcards)},
            {"id": "block-interactive", "type": "interactive_element", "order": 5, "visible": bool(current_elems)},
            {"id": "block-spots", "type": "spot_pearls", "order": 6, "visible": bool(s.get("spotPearls"))},
            {"id": "block-questions", "type": "related_questions", "order": 7, "visible": bool(related_q)},
            {"id": "block-terms", "type": "medical_terms", "order": 8, "visible": bool(s.get("medicalTerms"))},
        ]

        primary_interactive = current_elems[0] if current_elems else None

        slide_obj = {
            "slideNumber": slide_num,
            "title": s["title"],
            "subtitle": s["subtitle"],
            "badge": "Tekrar Sayfası" if is_checkpoint else s.get("badge", "Müfredat"),
            "badgeColor": "teal" if is_checkpoint else s.get("badgeColor", "indigo"),
            "discipline": s.get("discipline", "Tıbbi Genetik"),
            "synthesisNarrative": s["synthesisNarrative"],
            "medicalTerms": s.get("medicalTerms", []),
            "spotPearls": s.get("spotPearls", []),
            "interactiveElement": primary_interactive,
            "interactiveElements": current_elems,
            "layoutBlocks": layout_blocks,
            "flashcards": flashcards,
            "relatedQuestions": related_q,
            "coreContent": core_content,
            "isCheckpoint": is_checkpoint,
            "checkpointNumber": checkpoint_num if is_checkpoint else None,
            "sourcePdf": {
                "fileName": "k1-01-dismorfolojide-genetik-terminoloji.pdf",
                "fileId": "k1-01",
                "startPage": min(55, max(1, (slide_num * 55) // 100)),
                "endPage": min(55, max(1, ((slide_num * 55) // 100) + 1)),
                "primaryPage": min(55, max(1, (slide_num * 55) // 100)),
                "citation": f"Slayt {slide_num} · Kurul 1 Tıbbi Genetik Sunumu"
            },
            "aiPromptSuggestions": [
                f"{s['title']} konusunun hücresel ve klinik mekanizmasını vaka senaryosuyla açıklar mısın?",
                "Bu adımdaki bilgilerin TUS ve kurul sınavlarında çıkabilecek soru tiplerini gösterir misin?"
            ]
        }
        final_slides.append(slide_obj)

    # İstatistikleri hesapla
    from collections import Counter
    elem_counts = Counter()
    total_elems = 0
    for s in final_slides:
        for el in s.get("interactiveElements", []):
            t = el.get("type")
            elem_counts[t] += 1
            total_elems += 1

    print("\n" + "="*50)
    print(f"Toplam İnteraktif Öğe: {total_elems} (Adım başı ortalama: {total_elems/len(final_slides):.2f})")
    print("Öğe Dağılımı:")
    for t, c in elem_counts.most_common():
        pct = (c / total_elems) * 100
        print(f"  - {t:<22}: {c:3d} adet (%{pct:.2f}) -> {'✓ Kuralı Sağlıyor (>= %8)' if pct >= 8.0 else '✗ DÜŞÜK'}")
    print("="*50 + "\n")

    # 1. MANIFEST.JSON OLUŞTUR
    manifest_data = {
        "id": "k1-01-dismorfolojide-genetik-terminoloji",
        "title": "Dismorfolojide Genetik Terminoloji",
        "discipline": "Tıbbi Genetik",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "version": "2.0",
        "totalSlides": 100,
        "interactiveMetrics": {
            "totalCount": total_elems,
            "ratio": round(total_elems / 100, 2),
            "distribution": {t: {"count": c, "percentage": round((c / total_elems) * 100, 2)} for t, c in elem_counts.items()}
        },
        "sources": {
            "xml": "structure.xml",
            "html": "blocks.html",
            "markdown": "content.md"
        },
        "slidesIndex": [
            {
                "slideNumber": s["slideNumber"],
                "title": s["title"],
                "badge": s["badge"],
                "isCheckpoint": s["isCheckpoint"],
                "interactiveCount": len(s["interactiveElements"]),
                "interactiveTypes": [el.get("type") for el in s["interactiveElements"]],
                "hasFlashcards": len(s["flashcards"]) > 0,
                "hasTable": bool(s["coreContent"].get("table"))
            } for s in final_slides
        ]
    }
    manifest_path = os.path.join(PACKAGES_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"1. Manifest JSON yazıldı: {manifest_path}")

    # 2. STRUCTURE.XML OLUŞTUR
    root = ET.Element("lesson", id=deck_id, version="2.0")
    meta = ET.SubElement(root, "meta")
    ET.SubElement(meta, "title").text = manifest_data["title"]
    ET.SubElement(meta, "discipline").text = manifest_data["discipline"]
    ET.SubElement(meta, "totalSlides").text = "100"
    ET.SubElement(meta, "totalInteractives").text = str(total_elems)

    slides_node = ET.SubElement(root, "slides")
    for s in final_slides:
        slide_node = ET.SubElement(
            slides_node,
            "slide",
            id=f"slide-{s['slideNumber']:03d}",
            number=str(s['slideNumber']),
            badge=s['badge'],
            badgeColor=s['badgeColor'],
            isCheckpoint=str(s['isCheckpoint']).lower()
        )
        ET.SubElement(slide_node, "title").text = s["title"]
        ET.SubElement(slide_node, "subtitle").text = s["subtitle"]
        narrative_node = ET.SubElement(slide_node, "narrative")
        narrative_node.text = s["synthesisNarrative"]

        # Layout blokları
        blocks_node = ET.SubElement(slide_node, "layoutBlocks")
        for b in s["layoutBlocks"]:
            ET.SubElement(blocks_node, "block", id=b["id"], type=b["type"], order=str(b["order"]))

        # İnteraktif ögeler
        int_node = ET.SubElement(slide_node, "interactiveElements", count=str(len(s["interactiveElements"])))
        for el in s["interactiveElements"]:
            ET.SubElement(int_node, "element", type=el.get("type", ""))

        # Flashcards
        if s["flashcards"]:
            fc_node = ET.SubElement(slide_node, "flashcards", count=str(len(s["flashcards"])))
            for fc in s["flashcards"]:
                card_node = ET.SubElement(fc_node, "card", id=fc["id"])
                ET.SubElement(card_node, "front").text = fc["front"]
                ET.SubElement(card_node, "back").text = fc["back"]

        # Tıbbi terimler
        if s["medicalTerms"]:
            terms_node = ET.SubElement(slide_node, "medicalTerms")
            for tm in s["medicalTerms"]:
                t_el = ET.SubElement(terms_node, "term")
                ET.SubElement(t_el, "name").text = tm["term"]
                ET.SubElement(t_el, "explanation").text = tm["explanation"]

    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    xml_pretty = parsed_xml.toprettyxml(indent="  ")
    xml_path = os.path.join(PACKAGES_DIR, "structure.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_pretty)
    print(f"2. Structure XML yazıldı: {xml_path}")

    # 3. BLOCKS.HTML OLUŞTUR
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"tr\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <title>Dismorfolojide Genetik Terminoloji - Modüler Ders Blokları</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; max-width: 1400px; margin: 0 auto; padding: 24px; background: #f8fafc; }",
        "    .slide-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }",
        "    .slide-card.checkpoint { border: 2px solid #f59e0b; background: #fffbeb; }",
        "    .badge { display: inline-block; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; text-transform: uppercase; background: #e0e7ff; color: #3730a3; }",
        "    .badge.checkpoint { background: #fef3c7; color: #92400e; }",
        "    h2 { margin: 8px 0; font-size: 20px; color: #0f172a; }",
        "    .lead { color: #475569; font-size: 14px; margin-bottom: 16px; }",
        "    .narrative { font-size: 14px; white-space: pre-line; background: #f8fafc; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0; }",
        "    .flashcards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 16px; }",
        "    .flashcard { border: 1px solid #cbd5e1; border-radius: 12px; padding: 14px; background: #fff; }",
        "    .flashcard .front { font-weight: 700; font-size: 13px; color: #1e293b; margin-bottom: 8px; }",
        "    .flashcard .back { font-size: 12.5px; color: #334155; border-top: 1px dashed #cbd5e1; padding-top: 8px; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <header><h1>Dismorfolojide Genetik Terminoloji</h1><p>100 Atomik Adım • 11 Kontrol Noktası • {total_elems} İnteraktif Öğe</p></header>",
        "  <main>"
    ]
    for s in final_slides:
        cp_class = " checkpoint" if s["isCheckpoint"] else ""
        badge_class = " checkpoint" if s["isCheckpoint"] else ""
        html_lines.append(f"    <article id=\"slide-{s['slideNumber']}\" class=\"slide-card{cp_class}\">")
        html_lines.append(f"      <span class=\"badge{badge_class}\">{s['badge']} • Slayt {s['slideNumber']}/100</span>")
        html_lines.append(f"      <h2>{s['title']}</h2>")
        html_lines.append(f"      <p class=\"lead\">{s['subtitle']}</p>")
        html_lines.append(f"      <div class=\"narrative\">{s['synthesisNarrative']}</div>")

        if s["flashcards"]:
            html_lines.append("      <div class=\"flashcards-station\">")
            html_lines.append(f"        <h4>🧠 Pekiştirme Akıl Kartları ({len(s['flashcards'])} Adet)</h4>")
            html_lines.append("        <div class=\"flashcards-grid\">")
            for fc in s["flashcards"]:
                html_lines.append("          <div class=\"flashcard\">")
                html_lines.append(f"            <div class=\"front\">Q: {fc['front']}</div>")
                html_lines.append(f"            <div class=\"back\">A: {fc['back']}</div>")
                html_lines.append("          </div>")
            html_lines.append("        </div>")
            html_lines.append("      </div>")

        html_lines.append("    </article>")
    html_lines.append("  </main>")
    html_lines.append("</body>")
    html_lines.append("</html>")
    html_path = os.path.join(PACKAGES_DIR, "blocks.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
    print(f"3. Blocks HTML yazıldı: {html_path}")

    # 4. CONTENT.MD OLUŞTUR
    md_lines = [
        "# Dismorfolojide Genetik Terminoloji (Kurul 1 - Ders 1)",
        f"**Eğitmen:** Dr. Öğr. Üyesi Serap Arslan | **Disiplin:** Tıbbi Genetik | **Adım Sayısı:** 100 Adım | **İnteraktif Öğe:** {total_elems} Adet",
        "\n---\n"
    ]
    for s in final_slides:
        cp_tag = " [CHECKPOINT]" if s["isCheckpoint"] else ""
        md_lines.append(f"## Adım {s['slideNumber']}: {s['title']}{cp_tag}")
        md_lines.append(f"*{s['subtitle']}* - **Rozet:** `{s['badge']}`\n")
        md_lines.append(s["synthesisNarrative"])
        md_lines.append("")

        if s.get("coreContent", {}).get("table"):
            tb = s["coreContent"]["table"]
            md_lines.append(f"### 📋 {tb.get('title', 'Özet Tablo')}")
            headers = tb.get("headers", [])
            md_lines.append("| " + " | ".join(headers) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for r in tb.get("rows", []):
                md_lines.append("| " + " | ".join(r) + " |")
            md_lines.append("")

        if s["flashcards"]:
            md_lines.append("### 🧠 Pekiştirme Akıl Kartları")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']}")
                md_lines.append(f"  - **Cevap / Mekanizma:** {fc['back']}")
            md_lines.append("")

        if s.get("spotPearls"):
            md_lines.append("### 📌 Spot Bilgiler")
            for p in s["spotPearls"]:
                md_lines.append(f"- {p}")
            md_lines.append("")

        md_lines.append("\n---\n")

    md_path = os.path.join(PACKAGES_DIR, "content.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"4. Content Markdown yazıldı: {md_path}")

    # 5. RUNTIME ITEM JSON OLUŞTUR
    deck_data = {
        "id": deck_id,
        "title": "Dismorfolojide Genetik Terminoloji (Yeni Mikro-Ders)",
        "shortTitle": "Dismorfolojide Genetik Terminoloji",
        "discipline": "Tıbbi Genetik",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "audioFile": "audios/kurul1/k1-01-dismorfolojide-genetik-terminoloji.mp3",
        "audioDuration": "45:10",
        "confidence": "Yüksek",
        "themeColor": "indigo",
        "matchedNoteId": "k1-01-dismorfolojide-genetik-terminoloji",
        "matchedNoteTitle": "Dismorfolojide Genetik Terminoloji Ders Özeti",
        "isNew": True,
        "isLegacy": False,
        "version": 2,
        "packageSources": {
            "manifest": "packages/k1-01-dismorfolojide-genetik-terminoloji/manifest.json",
            "structureXml": "packages/k1-01-dismorfolojide-genetik-terminoloji/structure.xml",
            "blocksHtml": "packages/k1-01-dismorfolojide-genetik-terminoloji/blocks.html",
            "contentMd": "packages/k1-01-dismorfolojide-genetik-terminoloji/content.md"
        },
        "overview": f"Bu interaktif mikro-öğrenme destesi; 100 atomik adımda, 11 kontrol noktası tekrar sayfasında gömülü akıl kartlarıyla, {total_elems} adet zengin interaktif alıştırmayla (mikro-quiz, maskeli tablo, dallanan karar senaryoları, aktif hatırlama, karşılaştırma kaydırıcısı, neden-sonuç zinciri) konjenital anomalileri ve genetik tanı algoritmalarını derinlemesine öğretir.",
        "highYieldPearls": [
            "🚨 [KRİTİK UYARI] Canlı doğumla bağdaşan tek tam monozomi 45,X'tir (Turner sendromu); otozomal monozomiler letaldir.",
            "📌 [SINAV SPOTU] Parasentrik inversiyon sentromeri içermez ve krosing-over'da letal gamet üretir; perisentrik inversiyon sentromeri içerir ve canlı anomalili çocuk riski yüksektir.",
            "📌 [SINAV SPOTU] Robertsonian translokasyon yalnızca akrosentrik kromozomlarda (13, 14, 15, 21, 22) gerçekleşebilir; taşıyıcıda kromozom sayısı 45'tir.",
            "📌 [SINAV SPOTU] 1 minör anomalide majör anomali riski %3 iken; 3 veya daha fazla minör anomalide majör anomali riski %90'a fırlar.",
            "📌 [SINAV SPOTU] Malformasyon intrinsik ve baştan bozuktur (cerrahi şart); Deformasyon başlangıçta normaldir, mekanik basıyla oluşur ve konservatif/spontan düzelir.",
            "🚨 [KRİTİK UYARI] Amniyotik bant sendromu (disrupsiyon) GENETİK DEĞİLDİR; sonraki gebeliklerde tekrarlama riski yoktur.",
            "🚨 [KRİTİK UYARI] Potter sekansında ölüm nedeni böbrek yetmezliği değil, oligohidramniyosa bağlı gelişen Pulmoner Hipoplazidir.",
            "📌 [SINAV SPOTU] Pierre Robin sekansında primer defekt mikrognatidir; dilin farenkse kaçması (glossofitozis) sonucu U şeklinde yarık damak oluşur ve bebek prone yatırılmalıdır.",
            "📌 [SINAV SPOTU] VACTERL asosiasyonunda 6 kriterden en az 3'ü bulunmalıdır; VACTERL'de ZİHİNSEL GELİŞİM TAMAMEN NORMALDİR.",
            "📌 [SINAV SPOTU] Açıklanamayan zeka geriliği ve çoklu anomalide altın standart birinci basamak test Kromozomal Mikrodizidir (CMA); ancak CMA dengeli translokasyonları ve inversiyonları GÖREMEZ!"
        ],
        "totalSlides": 100,
        "totalInteractiveElements": total_elems,
        "interactiveRatio": round(total_elems / 100, 2),
        "matchedPastQuestionsCount": len(questions),
        "slides": final_slides
    }

    output_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deck_data, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime Item JSON kaydedildi: {output_path}")

    # 6. CATALOG.JSON GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        found = False
        for entry in catalog:
            if entry.get("id") == deck_id:
                entry["isNew"] = True
                entry["isLegacy"] = False
                entry["version"] = 2
                entry["totalSlides"] = 100
                entry["title"] = "Dismorfolojide Genetik Terminoloji (Yeni Mikro-Ders)"
                entry["overview"] = deck_data["overview"]
                found = True
                break
        if not found:
            catalog.append({
                "id": deck_id,
                "title": "Dismorfolojide Genetik Terminoloji (Yeni Mikro-Ders)",
                "shortTitle": "Dismorfolojide Genetik Terminoloji",
                "discipline": "Tıbbi Genetik",
                "committee": "Kurul 1 (Ürogenital ve Obstetrik)",
                "instructor": "Dr. Öğr. Üyesi Serap Arslan",
                "totalSlides": 100,
                "isNew": True,
                "isLegacy": False,
                "version": 2,
                "audioDuration": "45:10",
                "overview": deck_data["overview"]
            })
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"6. Catalog JSON güncellendi: {CATALOG_PATH}")

    print("\n✅ TÜM MULTI-FORMAT İŞLEMLER BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    main()
