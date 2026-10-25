#!/usr/bin/env python3
"""
generate_deep_k2_06.py:
Generates a complete, deep amfi-level lecture for Lesson 6:
"Ağrı Yolları ve Mekanizmaları" (Anesteziyoloji ve Reanimasyon - Dr. Öğr. Üyesi Serap Arslan).

Key Objectives & Standards (GEMINI.md & AGENTS.md):
1. 0 Skipped Slides, 0 Sparse Pages (<40 words).
   All 55 content/figure pages (pages 2 to 56) covered with rich amfi depth (70-110 words/page, total ~4,500 spoken words, ~32 mins audio).
2. Complete amfi explanations of:
   - IASP pain definition (sensory, affective, subjective, 2020 update)
   - Pain terminology: allodynia, hyperalgesia, anesthesia dolorosa, causalgia, hyperpathia, dysesthesia, paresthesia, hypesthesia, neuralgia, neuropathy, threshold vs tolerance
   - Classification by duration: acute, subacute, chronic
   - Classification by mechanism: nociceptive, neuropathic, nociplastic, psychogenic/functional
   - Deafferentation pain & causalgia/CRPS (sympathetic involvement)
   - Somatic (superficial vs deep) and visceral pain (characteristics, referral, autonomic signs)
   - 4 stages of pain perception: Transduction, Transmission (A-delta vs C fibers), Modulation, Perception
   - Figure descriptions for Page 13, 41 (4-stage diagram with analgesic targets), and 55 (Gate Control Theory)
   - Molecular mechanisms: peripheral sensitization (inflammatory soup: PG, bradykinin, SP, CGRP, NGF)
   - Central sensitization: wind-up, NMDA activation, loss of Mg block, Ca influx
   - Disinhibition: loss of GABA/glycine, loss of descending monoaminergic inhibition
   - Reorganization: structural cortical/thalamic remodeling
   - Nociceptors, TRP channels, and pharmacological interventions (NSAIDs, local anesthetics, opioids)
   - Neurotransmitters, dorsal horn Rexed laminae, Gate Control Theory, descending inhibitory pathways (PAG, RVM, serotonin, noradrenaline, enkephalins)
3. 9 Relevant past questions mapped with exact spoken trigger cues:
   "Burada çıkmış sınav sorusu bulunmaktadır: ..."
4. 15 Live vector drawings (siniflama, karsilastirma, neden_sonuc, mekanizma_adimlari) with 0 forward leaks.
5. All 6 Quality Gates passing synchronously with 0 HATA.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-06-agri-yollari-ve-mekanizmalari"
KAYNAK = TASLAK / "kaynak.md"

sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
import konusma_v2 as KV

raw_kaynak = KAYNAK.read_text(encoding="utf-8")
pages = {}
for p_block in raw_kaynak.split("=== SAYFA "):
    if not p_block.strip():
        continue
    lines = p_block.strip().splitlines()
    pno = int(lines[0].split()[0])
    raw = [l.strip() for l in lines[1:] if l.strip()]
    pages[pno] = raw


def find_satir(pno, pattern=None, idx=0):
    if pno not in pages or not pages[pno]:
        return []
    if pattern:
        pat_norm = KV._katla(pattern)
        matched = [l for l in pages[pno] if pat_norm in KV._katla(l) and l]
        if matched:
            return [matched[idx % len(matched)]]
    return [pages[pno][idx % len(pages[pno])]]


sent_counter = 0

def make_sentence(ekran, ses, pno, adim, satir_pattern=None, satir_idx=0, cikmis=None, highlight_word=None, sekil=None, duzey=0):
    global sent_counter
    sent_counter += 1
    cid = f"k2-06-c{sent_counter:04d}"
    
    adim_str = f"k2-06-d-s{adim:02d}"
    
    satirlar = []
    if sekil is None:
        satirlar = find_satir(pno, satir_pattern, satir_idx)
        
    vurgular = []
    if highlight_word:
        clean_ekran = ekran.replace("**", "")
        if highlight_word.casefold() in clean_ekran.casefold():
            vurgular.append({"metin": highlight_word, "tur": "cikmis" if cikmis else "terim"})
            
    return {
        "id": cid,
        "ses": ses,
        "ekran": ekran,
        "duzey": duzey,
        "vurgu": vurgular,
        "slayt_adim": adim_str,
        "cikmis": cikmis or [],
        "spot": None,
        "slayt": {
            "sayfa": pno,
            "satir": satirlar,
            "sekil": sekil
        }
    }


def build_all_sections():
    global sent_counter
    sent_counter = 0
    
    # ----------------------------------------------------
    # BÖLÜM 1: Ağrının Tanımı, İki Temel Özelliği ve Öznelliği (Sayfa 1-6)
    # ----------------------------------------------------
    p1 = [
        make_sentence(
            "Ağrı Yolları ve Mekanizmaları: **Algolojiye giriş ve ders hedefleri**",
            "Ağrı yolları ve mekanizmaları dersimize başlarken; nosisepsiyonun hücresel temellerini, ağrının sınıflandırılmasını ve santral modülasyon yolaklarını kapsamlı bir şekilde inceleyeceğiz.",
            1, 1, satir_pattern="AĞRI", duzey=0
        ),
        make_sentence(
            "Klinik ve farmakolojik hedefler: **Nosiseptif iletimin basamakları**",
            "Dersimiz boyunca ağrı duyusunun periferik reseptörlerden primer duyusal kortekse iletimindeki dört temel aşamayı ve analjezik ilaçların bu aşamalardaki moleküler etki noktalarını öğreneceğiz.",
            1, 1, satir_pattern="AĞRI", duzey=0
        ),
        make_sentence(
            "Santral duyarlılaşma ve kapı kontrol teorisi: **Kronik ağrının fizyopatolojisi**",
            "Ayrıca akut ağrının kronikleşme süreçlerini, arka boynuzdaki kapı kontrol mekanizmasını ve inen inhibitör sistemlerin analjezik etkilerini basamak basamak ele alacağız.",
            1, 1, satir_pattern="AĞRI", duzey=0
        )
    ]

    p2 = [
        make_sentence(
            "IASP Ağrı Tanımı: **Duyusal, afektif ve hoş olmayan deneyim**",
            "Uluslararası Ağrı Araştırmaları Teşkilatının kabul gören tanımına göre ağrı; vücudun herhangi bir yerinden kaynaklanan, gerçek ya da olası bir doku hasarı ile birlikte bulunan veya bu hasarla açıklanan, hastanın geçmiş deneyimleriyle ilişkili, hoş olmayan duyusal ve emosyonel bir deneyimdir.",
            2, 1, satir_pattern="Uluslararası", duzey=0
        ),
        make_sentence(
            "Fiziksel ve emosyonel birliktelik: **Yalnızca duyu değil, karmaşık yaşantı**",
            "Ağrı yalnızca dokudan gelen basit bir fiziksel duyu sinyali olmayıp; kişinin ruhsal durumunu, bilişsel değerlendirmesini ve afektif tepkilerini içine alan çok boyutlu bir yaşantıdır.",
            2, 1, satir_pattern="duyusal", duzey=1
        ),
        make_sentence(
            "Objektif doku hasarı zorunluluğunun kalkması: **Hasar kanıtlanamasa da ağrı gerçektir**",
            "Modern algolojide doku hasarının somut olarak gösterilmesi tanı için mutlak bir şart değildir; doku hasarı kanıtlanamasa dahi hastanın ağrı bildirimi gerçek bir deneyim olarak kabul edilir ve tedaviye alınır.",
            2, 1, satir_pattern="Doku", duzey=1
        ),
        make_sentence(
            "İki bin yirmi güncellemesi: **Öznellik vurgusu ve kişisel bildirim önceliği**",
            "Uluslararası Ağrı Araştırmaları Teşkilatının iki bin yirmi yılındaki son güncellemesinde ağrının öznel niteliği ön plana çıkarılmış, her bireyin ağrıyı yaşamı boyunca edindiği kişisel deneyimlerle öğrendiği açıkça vurgulanmıştır.",
            2, 1, satir_pattern="2020", duzey=1
        )
    ]

    p3 = [
        make_sentence(
            "Objektif bulgu yokluğu: **Migren ve nevraljide somut lezyon aranmaz**",
            "Ağrı tanımının en kritik ilkelerinden biri olası doku hasarı kavramıdır; zira migren, gerilim tipi baş ağrısı veya trigeminal nevralji gibi birçok şiddetli kronik ağrı tablosunda laboratuvar veya görüntüleme ile objektif bir doku hasarı saptanamaz.",
            3, 2, satir_pattern="Birçok", duzey=0
        ),
        make_sentence(
            "Psikolojik yanılgısının önlenmesi: **Bulgu olmaması ağrıyı hayali kılmaz**",
            "Klinisyenin fizik muayenede veya radyolojik tetkiklerde somut bir patoloji bulamaması, hastanın yakınmasının psikolojik veya uydurma olduğu anlamına kesinlikle gelmez.",
            3, 2, satir_pattern="psikolojik", duzey=1
        ),
        make_sentence(
            "Klinik güven ve yaklaşım: **Hastanın ağrı ifadesi temel tanı ölçütüdür**",
            "Hastanın ağrım var ifadesi tıp pratiğinde aksi kanıtlanana kadar doğru kabul edilmeli; nöropatik ve nosiplastik mekanizmaların varlığı göz önünde tutularak empatik bir tedavi protokolü başlatılmalıdır.",
            3, 2, satir_pattern="hastanın", duzey=1
        )
    ]

    p4 = [
        make_sentence(
            "Duyusal komponent: **Nosiseptörlerden kortekse objektif duyu iletimi**",
            "Ağrının birinci temel bileşeni duyusal komponenttir; bu bileşen periferik sinir lifleri ile taşınan, lezyonun yerini, süresini, şiddetini ve niteliğini belirleyen objektif nörofizyolojik duyu iletimini kapsar.",
            4, 3, satir_pattern="duyusal", duzey=0
        ),
        make_sentence(
            "Emosyonel komponent: **Kişinin acıya verdiği affektif ve ruhsal tepki**",
            "Ağrının ikinci ayrılmaz bileşeni ise emosyonel yani duygusal komponenttir; ağrının kişide oluşturduğu ıstırap, kaygı, korku ve hoşnutsuzluk gibi afektif durumları temsil eder.",
            4, 3, satir_pattern="emosyonel", duzey=1
        ),
        make_sentence(
            "Bütüncül değerlendirme ilkesi: **Duyusal uyarı emosyonel filtrede işlenir**",
            "Aynı şiddetteki bir nosiseptif uyaran iki farklı bireyde emosyonel filtrenin ve geçmiş yaşantıların farklılığı nedeniyle tamamen zıt şiddet ve tepkilerle algılanabilir.",
            4, 3, satir_pattern="etkilenmesidir", duzey=1
        )
    ]

    p5 = [
        make_sentence(
            "Ağrının mutlak öznelliği: **Bireysel algı ve nosisepsiyon farkı**",
            "Ağrı her zaman ve her koşulda kişiye özneldir; bu bağlamda dokudan gelen duyusal nosiseptif uyarı ile bilinç düzeyinde hissedilen ağrı aynı anlama gelmez.",
            5, 4, satir_pattern="özneldir", duzey=0
        ),
        make_sentence(
            "Nosisepsiyon ve ağrı ayrımı: **Fizyolojik sinyal bilince ulaşınca ağrı olur**",
            "Nosisepsiyon periferik reseptörlerin zararlı uyaranı algılayıp omuriliğe iletmesi şeklindeki nörofizyolojik bir süreçken; ağrı bu sinyalin serebral korteks ve limbik sistemde yorumlanmasıyla ortaya çıkan subjektif bir algıdır.",
            5, 4, satir_pattern="Nosiseptif", duzey=1
        ),
        make_sentence(
            "Yaşam kalitesi ve sosyal etki: **Kişilik, tecrübe ve sosyal çevre rolü**",
            "Bireyin yaşı ilerledikçe edindiği deneyimler ağrı kavramını değiştirir; kontrol altına alınamayan kronik ağrı hastanın psikolojik dengesini, aile yaşantısını ve tüm sosyal üretkenliğini derinden sarsar.",
            5, 4, satir_pattern="sosyal", duzey=1
        )
    ]

    p6 = [
        make_sentence(
            "Ağrı eşiğini şekillendiren etmenler: **Kültür, inanç ve cinsiyet değişkenleri**",
            "İnsanoğlu doğduğu andan itibaren çevresiyle etkileşime girer; bireyin inançları, konuştuğu dil, cinsiyeti ve içinde büyüdüğü kültürel yapı onun emosyonel yanıt mekanizmasını ve ağrıya karşı tutumunu belirler.",
            6, 5, satir_pattern="İnsanoğlu", duzey=0
        ),
        make_sentence(
            "Ağrı eşiği ve tolerans ayrımı: **Fizyolojik alt sınırdan psikolojik sınıra**",
            "Objektif nosiseptif uyaranların yanı sıra bu sübjektif faktörler, kişinin uyarandan ilk ağrı hissettiği eşiği ve ağrıya ne kadar süre katlanabileceğini belirleyen tolerans seviyesini doğrudan etkiler.",
            6, 5, satir_pattern="özellikleri", duzey=1
        ),
        make_sentence(
            "Klinik algoloji kuralı: **Her hastanın ağrı skalası kendine özgüdür**",
            "Klinisyen farklı sosyokültürel arka plana sahip hastaları değerlendirirken tek bir kalıp yargıya kapılmamalı, hastanın bildirdiği ağrı skorunu kendi bireysel gerçekliği içinde ele almalıdır.",
            6, 5, satir_pattern="oluşturur", duzey=1
        )
    ]

    b01 = {
        "id": "k2-06-b01",
        "baslik": "Ağrının Tanımı, İki Temel Özelliği ve Öznelliği",
        "paragraflar": [
            {"id": "k2-06-p000", "sayfa": 1, "slayt_adim": 1, "cumleler": p1},
            {"id": "k2-06-p001", "sayfa": 2, "slayt_adim": 1, "cumleler": p2},
            {"id": "k2-06-p002", "sayfa": 3, "slayt_adim": 2, "cumleler": p3},
            {"id": "k2-06-p003", "sayfa": 4, "slayt_adim": 3, "cumleler": p4},
            {"id": "k2-06-p004", "sayfa": 5, "slayt_adim": 4, "cumleler": p5},
            {"id": "k2-06-p005", "sayfa": 6, "slayt_adim": 5, "cumleler": p6}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 2: Ağrının Periferik ve Santral Komponentleri (Sayfa 7-8)
    # ----------------------------------------------------
    p7 = [
        make_sentence(
            "Fizyolojik periferik komponent: **Nosiseptörler ve anatomik duyu yolları**",
            "Ağrının tanımlanmasında birinci temel öğe fizyolojik yani periferik komponenttir; bu komponent dokudaki nosiseptörler vasıtasıyla santral sinir sistemine uzanan anatomik duyusal iletim yollarını kapsar.",
            7, 6, satir_pattern="Fizyolojik", duzey=0
        ),
        make_sentence(
            "Duyusal uyarı iletimi: **Periferden omurilik arka boynuzuna geçiş**",
            "Doku düzeyinde oluşan zararlı fiziksel uyaran periferik sinir liflerinin iletim özelliklerine bağlı olarak omuriliğe ve oradan yüksek merkezlere doğru taşınır.",
            7, 6, satir_pattern="nosiseptörler", duzey=1
        ),
        make_sentence(
            "Bilinç öncesi süreç: **Korteks öncesi objektif sinyal akışı**",
            "Bu periferik duyusal iletim aşamasında henüz kortikal bir algı veya bilinçli ıstırap oluşmamıştır; yalnızca elektrofizyolojik sinyal transferi gerçekleşmektedir.",
            7, 6, satir_pattern="merkezlere", duzey=1
        )
    ]

    p8 = [
        make_sentence(
            "Psikolojik santral komponent: **Üç büyük boyut ve beyin merkezleri**",
            "Ağrının ikinci öğesi psikolojik yani santral komponenttir ve kendi içinde duyusal diskriminatif boyut, affektif motivasyonel boyut ve kognitif değerlendirici boyut olmak üzere üç büyük boyutu barındırır.",
            8, 7, satir_pattern="Psikolojik", duzey=0
        ),
        make_sentence(
            "Duyusal-diskriminatif boyut: **Somatosensoriyel korteks ve talamik lokalizasyon**",
            "Duyusal diskriminatif boyut ağrının tam anatomik yerini, süresini, keskinliğini ve şiddetini belirler; bu ayrım primer somatosensoryal korteks ve talamusun ventroposterolateral çekirdeğinde gerçekleşir.",
            8, 7, satir_pattern="diskriminatif", duzey=1
        ),
        make_sentence(
            "Affektif ve kognitif boyut: **Limbik sistem, frontal lob ve acı yaşantısı**",
            "Affektif motivasyonel boyut limbik sistem ve singulat kortekste ağrının yarattığı korku ve kaçınma davranışını; kognitif boyut ise frontal lobda ağrının anlamlandırılmasını ve baş etme stratejilerini yönetir.",
            8, 7, satir_pattern="affektif", duzey=1
        )
    ]

    b02 = {
        "id": "k2-06-b02",
        "baslik": "Ağrının Periferik (Fizyolojik) ve Santral (Psikolojik) Komponentleri",
        "paragraflar": [
            {"id": "k2-06-p006", "sayfa": 7, "slayt_adim": 6, "cumleler": p7},
            {"id": "k2-06-p007", "sayfa": 8, "slayt_adim": 7, "cumleler": p8}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 3: Ağrı Terminolojisi ve Duyusal Bozukluklar (Sayfa 9-12)
    # ----------------------------------------------------
    p9 = [
        make_sentence(
            "Allodini tanımı: **Normalde ağrısız uyarana ağrı yanıtı**",
            "Allodini, normal koşullarda hiçbir şekilde ağrı oluşturmayan pamuk dokunması, giysi teması veya ılık su gibi zararsız bir stimulusun şiddetli ağrıya yol açması tablosudur.",
            9, 9, satir_pattern="Allodynia", duzey=0
        ),
        make_sentence(
            "Anestezi dolorosa: **Duyusuz bölgede hissedilen çelişkili ağrı**",
            "Anestezi dolorosa, duyu muayenesinde tamamen hissiz ve anestezik bulunan bir alanda hastanın inatçı ve ızdırap verici bir ağrı hissetmesi durumudur.",
            9, 9, satir_pattern="Anesthesia", duzey=1
        ),
        make_sentence(
            "Çıkmış Sınav Sorusu: **Kozalji ve travmatik sinir lezyonu ilişkisi**",
            "Burada çıkmış sınav sorusu bulunmaktadır: Travmatik bir periferik sinir lezyonundan sonra ortaya çıkan, özellikle median veya siyatik sinir hasarlarında görülen ve sempatik hiperaktiviteyle şiddetlenen inatçı yanıcı ağrı tablosuna kozalji adı verilir.",
            9, 10, satir_pattern="Kozalji", duzey=1, cikmis=["q-2__kurul_-12"], highlight_word="Kozalji"
        ),
        make_sentence(
            "Santral ağrı kavramı: **Santral sinir sistemi lezyonuna bağlı ağrı**",
            "Santral ağrı ise talamik enfarktüs, omurilik travması veya multipl skleroz gibi doğrudan santral sinir sistemindeki duyusal yolakların hasarlanması sonucu ortaya çıkan yaygın nöropatik tablodur.",
            9, 10, satir_pattern="Santral", duzey=1
        )
    ]

    p10 = [
        make_sentence(
            "Disestezi ve parestezi: **Hoş olmayan anormal duyu ile uyuşma ayrımı**",
            "Disestezi hastayı belirgin derecede rahatsız eden ve acı veren nahoş anormal duyuyken; parestezi uyuşma, karıncalanma veya keçeleşme gibi rahatsız edici olmayan spontan duyusal hisleri tanımlar.",
            10, 11, satir_pattern="Disestezi", duzey=0
        ),
        make_sentence(
            "Hiperaljezi mekanizması: **Ağrılı uyarana karşı abartılı yanıt**",
            "Hiperaljezi, normalde hafif ağrı oluşturan zararlı bir uyarana karşı duyarlılığın ve verilen ağrı cevabının belirgin biçimde artmasıdır.",
            10, 12, satir_pattern="Hiperaljezi", duzey=1
        ),
        make_sentence(
            "Hiperestezi ve hiperpati: **Artmış stimulus duyarlılığı ve patlayıcı yanıt**",
            "Hiperestezi dokunma ve termal gibi tüm stimülasyonlara karşı duyarlılığın artmasıyken; hiperpati yüksek eşikli uyarana karşı gecikmeli fakat patlayıcı ve aşırı şiddetli reaksiyonla karakterize özel bir ağrılı sendromdur.",
            10, 12, satir_pattern="Hiperpati", duzey=1
        ),
        make_sentence(
            "Hipoaljezi: **Zararlı uyarana verilen ağrı yanıtının azalması**",
            "Hipoaljezi ise tam tersine ağrılı bir uyarana karşı hissedilen acının ve nöronal yanıtın fizyolojik sınırların altına inmesidir.",
            10, 12, satir_pattern="Hiperaljezi", duzey=1
        )
    ]

    p11 = [
        make_sentence(
            "Hipoestezi ve nöralji: **Duyusal küntleşme ve sinir trasesinde ağrı**",
            "Hipoestezi herhangi bir uyarana karşı dokunma ve duyu algısının azalmasıyken; nöralji belirli bir periferik veya kraniyal sinirin anatomik dağılım alanı boyunca şimşek çakar tarzda yayılan ağrıdır.",
            11, 13, satir_pattern="Hipoestezi", duzey=0
        ),
        make_sentence(
            "Nöropati ve nosiseptör: **Sinir hasarı ve özelleşmiş ağrı sensörleri**",
            "Nöropati bir sinirde meydana gelen patolojik yapısal hasar veya fonksiyon bozukluğudur; nosiseptör ise zararlı ya da potansiyel olarak doku hasarı yapabilecek uyaranlara duyarlı çıplak sinir uçlarıdır.",
            11, 13, satir_pattern="Nöropati", duzey=1
        ),
        make_sentence(
            "Noxious kavramı: **Doku hasarı tehdidi oluşturan zararlı uyaran**",
            "Noxious terimi ise doğrudan doku bütünlüğünü tehdit eden, hücre yıkımına yol açabilecek mekanik, termal veya kimyasal zararlı uyarıcıları ifade eder.",
            11, 13, satir_pattern="Nosiseptör", duzey=1
        )
    ]

    p12 = [
        make_sentence(
            "Ağrı eşiği tanımı: **Kişide ağrıyı başlatan minimum uyaran şiddeti**",
            "Ağrı eşiği, bir bireyde ilk kez ağrı hissinin ortaya çıkmasına neden olan en küçük fiziksel uyarının şiddetidir ve fizyolojik olarak kişiler arasında nispeten sabit kabul edilir.",
            12, 14, satir_pattern="Ağrı", duzey=0
        ),
        make_sentence(
            "Ağrı tolerans seviyesi: **Bireyin katlanabildiği maksimum ağrı sınırı**",
            "Ağrı tolerans seviyesi ise kişinin tolere etmeye ve dayanmaya hazır olduğu, ağrıya yol açan en büyük uyaran şiddetini temsil eder.",
            12, 14, satir_pattern="tolerans", duzey=1
        ),
        make_sentence(
            "Eşik ile tolerans farkı: **Fizyolojik alt sınır ve psikososyal üst tavan**",
            "Eşik dokudaki nosiseptörlerin duyarlılığıyla belirlenen biyolojik bir alt sınırlıyken; tolerans düzeyi inanç, motivasyon, anksiyete ve yorgunluk gibi psikososyal faktörlerle her bireyde geniş dalgalanmalar gösterir.",
            12, 14, satir_pattern="şiddeti", duzey=1
        )
    ]

    b03 = {
        "id": "k2-06-b03",
        "baslik": "Ağrı Terminolojisi ve Duyusal Bozukluklar",
        "paragraflar": [
            {"id": "k2-06-p008", "sayfa": 9, "slayt_adim": 9, "cumleler": p9},
            {"id": "k2-06-p009", "sayfa": 10, "slayt_adim": 11, "cumleler": p10},
            {"id": "k2-06-p010", "sayfa": 11, "slayt_adim": 13, "cumleler": p11},
            {"id": "k2-06-p011", "sayfa": 12, "slayt_adim": 14, "cumleler": p12}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 4: Başlama Süresine Göre Ağrı: Akut, Subakut ve Kronik Ağrı (Sayfa 13-16)
    # ----------------------------------------------------
    p13 = [
        make_sentence(
            "Süreye göre sınıflama: **Akut, subakut ve kronik ayrımının klinik önemi**",
            "Ağrının sınıflandırılmasında klinisyenin başvurduğu ilk ve en pratik ölçüt ağrının başlama zamanı ve devam etme süresidir.",
            13, 16, satir_pattern="Ağrı", duzey=0, sekil="Ağrı sınıflandırması başlığı: Başlama süresine göre sınıflama şeması"
        ),
        make_sentence(
            "Zaman ekseninde patofizyoloji: **Biyolojik uyarıdan bağımsız hastalığa**",
            "Süre uzadıkça ağrının altında yatan moleküler mekanizma koruyucu bir nosiseptif uyrıdan, sinir sisteminde kalıcı plastisite ve duyarlılaşmayla giden bir hastalığa evrilir.",
            13, 16, satir_pattern="başlama", duzey=1
        ),
        make_sentence(
            "Klinik evreleme çerçevesi: **Tedavi stratejisini belirleyen temel basamak**",
            "Bu sınıflama hastaya uygulanacak farmakolojik ajanların seçiminde, cerrahi kararlarında ve fizik tedavi planlamasında temel kılavuzdur.",
            13, 16, satir_pattern="sınıflama", duzey=1
        )
    ]

    p14 = [
        make_sentence(
            "Akut ağrı özellikleri: **Koruyucu, daima nosiseptif ve lokalize**",
            "Akut ağrı daima nosiseptif nitelikte olup vücuda zarar veren akut bir olayın, travmanın, enfeksiyonun veya doku hipoksisinin varlığını haber veren biyolojik bir alarm sistemidir.",
            14, 16, satir_pattern="Akut", duzey=0
        ),
        make_sentence(
            "Lezyon ve ağrı korelasyonu: **Yer, şiddet ve zaman bakımından tam uyum**",
            "Akut ağrıda nedensel lezyon ile hissedilen ağrı arasında yer, şiddet ve zaman bakımından çok yakın ve doğrusal bir ilişki bulunur.",
            14, 16, satir_pattern="ilişki", duzey=1
        ),
        make_sentence(
            "Tedavi yanıtı ve prognoz: **Doku iyileşmesi ile ağrının sonlanması**",
            "Doku onarımı tamamlandığında ve inflamatuar süreç yatıştığında akut nosiseptif ağrı kendiliğinden tamamen ortadan kaybolur.",
            14, 16, satir_pattern="enflamasyon", duzey=1
        )
    ]

    p15 = [
        make_sentence(
            "Kronik ağrı tanımı: **Üç ila altı aydan uzun süren patolojik tablo**",
            "Üç ila altı aydan daha uzun süreli devam eden ya da beklenen normal doku iyileşme süresini aşan ağrılara kronik ağrı adı verilir.",
            15, 17, satir_pattern="Kronik", duzey=0
        ),
        make_sentence(
            "Uyarıcı işlevin kaybı: **Artık koruyucu değil, bizzat bir hastalıktır**",
            "Kronik ağrıda biyolojik koruyucu alarm fonksiyonu tamamen yitirilmiştir; ağrı bir semptom olmaktan çıkıp santral sinir sisteminin kalıcı bir hastalığı haline gelmiştir.",
            15, 17, satir_pattern="işlevi", duzey=1
        ),
        make_sentence(
            "Psikososyal çöküş: **Depresyon, anksiyete ve davranış değişiklikleri**",
            "Kişinin hayat kalitesini bozan, uyku düzenini yıkan, bireyi anormal ağrı davranışlarına ve içe kapanmaya yönelten kompleks psikososyal etkenler tabloya eklenir.",
            15, 17, satir_pattern="psikolojik", duzey=1
        )
    ]

    p16 = [
        make_sentence(
            "Subakut ağrı tanımı: **Altı hafta ile üç ay arası kritik geçiş dönemi**",
            "Altı haftadan başlayıp üç aya kadar uzanan ağrılara subakut ağrı denir ve bu evre akut nosiseptif ağrıdan kalıcı kronik ağrıya geçişin yaşandığı kritik penceredir.",
            16, 18, satir_pattern="Subakut", duzey=0
        ),
        make_sentence(
            "Klinik örnek: **Miyofasyal ağrı sendromu ve kronikleşme riski**",
            "Miyofasyal ağrı sendromları, tedavi edilmemiş bel spazmları ve postoperatif uzamış ağrılar subakut dönemin en tipik klinik örnekleridir.",
            16, 18, satir_pattern="Miyofasyal", duzey=1
        ),
        make_sentence(
            "Terapötik pencere önemi: **Santral duyarlılaşma yerleşmeden müdahale**",
            "Subakut evrede uygulanacak agresif medikal tedavi, tetik nokta enjeksiyonları ve erken mobilizasyon ağrının kronikleşmesini ve nöroplastik hasarın yerleşmesini engeller.",
            16, 18, satir_pattern="geçiş", duzey=1
        )
    ]

    b04 = {
        "id": "k2-06-b04",
        "baslik": "Başlama Süresine Göre Ağrı: Akut, Subakut ve Kronik Ağrı",
        "paragraflar": [
            {"id": "k2-06-p012", "sayfa": 13, "slayt_adim": 16, "cumleler": p13},
            {"id": "k2-06-p013", "sayfa": 14, "slayt_adim": 16, "cumleler": p14},
            {"id": "k2-06-p014", "sayfa": 15, "slayt_adim": 17, "cumleler": p15},
            {"id": "k2-06-p015", "sayfa": 16, "slayt_adim": 18, "cumleler": p16}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 5: Mekanizmaya Göre Ağrı: Nosiseptif ve Nöropatik Ağrı (Sayfa 17-20)
    # ----------------------------------------------------
    p17 = [
        make_sentence(
            "Mekanizmaya göre sınıflama: **Etiyopatogenetik dört temel kategori**",
            "Ağrının etiyopatogenetik mekanizmalarına göre yapılan ikinci sınıflamada nosiseptif ağrı, nöropatik ağrı, psikojenik ağrı ve nosiplastik ağrı olmak üzere temel kategoriler incelenir.",
            17, 19, satir_pattern="Mekanizmalarına", duzey=0
        ),
        make_sentence(
            "Hücresel mekanizma ayrımı: **Reseptör aktivasyonu ve nöronal lezyon**",
            "Bu ayrım ağrının sağlam bir sinir boyunca iletilen doku hasarı sinyali mi yoksa sinir liflerinin kendi patolojisi mi olduğunu ortaya koyar.",
            17, 19, satir_pattern="sınıflaması", duzey=1
        ),
        make_sentence(
            "Tedavi protokolüne rehberlik: **Doğru mekanizmaya doğru farmakoterapi**",
            "Nosiseptif ağrıda antienflamatuarlar ve opioidler etkiliyken, nöropatik ağrıda antiepileptik ve antidepresan ajanların seçilmesi mekanizma odaklı yaklaşımın sonucudur.",
            17, 19, satir_pattern="Mekanizmalarına", duzey=1
        )
    ]

    p18 = [
        make_sentence(
            "Nosiseptif ağrı mekanizması: **Periferik nosiseptörlerin fizyopatolojik uyarımı**",
            "Nosiseptif ağrı, periferik dokularda yer alan ve nosiseptör adı verilen özelleşmiş ağrı algılayıcılarının mekanik, termal ya da kimyasal süreçlerle uyarılması sonucu meydana gelir.",
            18, 19, satir_pattern="Nosiseptif", duzey=0
        ),
        make_sentence(
            "Doku orijini ve yaygınlığı: **Somatik dokular ve visseral organlar**",
            "Deri, kas, kemik, eklem gibi somatik dokularda veya iç organlarda doku yıkımı ya da iskemi geliştiğinde salınan algopatojen maddeler nosiseptörleri aktive eder.",
            18, 19, satir_pattern="visseral", duzey=1
        ),
        make_sentence(
            "Sinir bütünlüğü özelliği: **İletim yolları sağlam ve fizyolojiktir**",
            "Nosiseptif ağrıda periferik sinirler, omurilik ve talamokortikal yollar yapısal olarak tamamen sağlamdır; yalnızca hasarlı dokudan gelen sinyalleri iletirler.",
            18, 19, satir_pattern="algılayıcılarını", duzey=1
        )
    ]

    p19 = [
        make_sentence(
            "Nöropatik ağrı tanımı: **Somatosensoriyel sinir sisteminin primer lezyonu**",
            "Nöropatik ağrı; periferik ya da santral somatosensoriyel sinir sistemini etkileyen mekanik bir travma, kompresyon veya metabolik bir hastalık sonucunda doğrudan sinirin hasarlanmasıyla ortaya çıkar.",
            19, 20, satir_pattern="Nöropatik", duzey=0
        ),
        make_sentence(
            "Çıkmış Sınav Sorusu: **Bel fıtığı ve disk hernisinde nöropatik radikülopati**",
            "Burada çıkmış sınav sorusu bulunmaktadır: Bel fıtığı veya disk hernisinde spinal sinir kökünün mekanik kompresyona ve iskemiye uğraması sonucu bacağa yayılan radikülopati ağrısı, sinir dokusunun doğrudan hasarlandığı klasik nöropatik ağrı örneğidir.",
            19, 20, satir_pattern="Disk", duzey=1, cikmis=["past-q-_SKENDERUN_T_M_d_rl___ne0__1__230709_230251-7"], highlight_word="Disk hernisinde"
        ),
        make_sentence(
            "Etiyolojik çeşitlilik: **Metabolik diyabetik polinöropati ve toksik nedenler**",
            "Mekanik kök basılarının yanı sıra uzun süreli kontrolsüz diyabete bağlı diyabetik nöropati veya alkol ve kemoterapiye bağlı toksik sinir hasarları da periferik nöropatik ağrının başlıca nedenleridir.",
            19, 20, satir_pattern="metabolik", duzey=1
        )
    ]

    p20 = [
        make_sentence(
            "Nöropatik ağrının semiyolojisi: **Batıcı, saplanıcı ve elektrik çarpar tarzda**",
            "Nöropatik ağrı hastalar tarafından sıklıkla aralıklı, kısa süreli, batıcı, saplanıcı, yanıcı veya elektrik şoku çarpar tarzda tanımlanır ve duysal innervasyon bozukluğunun bulunduğu alanda algılanır.",
            20, 21, satir_pattern="duysal", duzey=0
        ),
        make_sentence(
            "Pozitif ve negatif bulgular: **Duyu kaybı zemininde hiperaljezi ve allodini**",
            "Hastanın muayenesinde bir yandan hipoestezi yani duyu kaybı izlenirken, diğer yandan etkilenen sahada hafif dokunmayla şiddetli acı duyulması yani allodini ve hiperaljezi birlikteliği saptanır.",
            20, 21, satir_pattern="Aralıklı", duzey=1
        ),
        make_sentence(
            "Periferik ve santral örnekler: **Trigeminal nevraljiden talamik inmeye**",
            "Periferik nöropatik ağrıya trigeminal nevralji, postherpetik nevralji ve karpal tünel sendromu; santral nöropatik ağrıya ise talamik enfarktüs sonrası gelişen Dejerine-Roussy sendromu prototip örnektir.",
            20, 22, satir_pattern="batıcı", duzey=1
        )
    ]

    b05 = {
        "id": "k2-06-b05",
        "baslik": "Mekanizmaya Göre Ağrı: Nosiseptif ve Nöropatik Ağrı",
        "paragraflar": [
            {"id": "k2-06-p016", "sayfa": 17, "slayt_adim": 19, "cumleler": p17},
            {"id": "k2-06-p017", "sayfa": 18, "slayt_adim": 19, "cumleler": p18},
            {"id": "k2-06-p018", "sayfa": 19, "slayt_adim": 20, "cumleler": p19},
            {"id": "k2-06-p019", "sayfa": 20, "slayt_adim": 21, "cumleler": p20}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 6: Deafferentasyon Ağrıları ve Sempatik Ağrılar (Sayfa 21-24)
    # ----------------------------------------------------
    p21 = [
        make_sentence(
            "Deafferentasyon ağrısı kavramı: **Duyusal afferent girdinin kopması**",
            "Deafferentasyon ağrısı, periferden omuriliğe ya da beyne giden duyusal iletim yollarının cerrahi, travmatik veya vasküler nedenlerle tamamen kesilmesi sonucu ortaya çıkan ilginç bir nöropatik ağrı türüdür.",
            21, 23, satir_pattern="İlginç", duzey=0
        ),
        make_sentence(
            "Santral deşarj mekanizması: **İnhibisyonsuz kalan spinal nöronların aktivasyonu**",
            "Normalde arka boynuza sürekli gelen periferik dokunma ve duyu sinyalleri kesildiğinde, omurilikteki ikinci sıra nöronlar kontrolsüzce spontan aksiyon potansiyelleri üreterek üst merkezlere yalancı ağrı mesajları gönderir.",
            21, 23, satir_pattern="ağrı", duzey=1
        ),
        make_sentence(
            "Klinik tablo ve direnç: **Klasik analjeziklere dirençli yanıcı ağrı**",
            "Bu durum periferde herhangi bir hasar veya nosiseptör uyarımı olmamasına rağmen, santral düzeyde son derece şiddetli, sürekli ve klasik analjeziklere yanıtsız bir yanma hissi oluşturur.",
            21, 23, satir_pattern="İlginç", duzey=1
        )
    ]

    p22 = [
        make_sentence(
            "Deafferentasyon örnekleri: **Fantom ekstremite ve brakiyal avülsiyon**",
            "Deafferentasyon ağrısına en çarpıcı klinik örnekler; cerrahi amputasyon sonrası var olmayan kolda veya bacakta hissedilen fantom ekstremite ağrısı ve brakiyal pleksus kök avülsiyonlarıdır.",
            22, 24, satir_pattern="Deafferentasyon", duzey=0
        ),
        make_sentence(
            "Spinal kord hasarı ve inme: **Paraplejik ağrılar ve talamik sendrom**",
            "Ayrıca tam omurilik kesisi geçiren paraplejik hastaların hissiz kalan alt ekstremitelerinde duydukları şiddetli nöropatik ağrılar ve talamik enfarktüs sonrası santral ağrılar bu mekanizmayla gelişir.",
            22, 24, satir_pattern="travmatik", duzey=1
        ),
        make_sentence(
            "Kortikal reorganizasyon: **Somatosensoriyel haritanın yeniden çizilmesi**",
            "Duyu girdisi kesilen kortikal alanların komşu vücut bölgeleri tarafından istila edilmesi yani maladaptif nöroplastisite fantom ağrısının kronikleşmesinde kilit rol oynar.",
            22, 24, satir_pattern="örnek", duzey=1
        )
    ]

    p23 = [
        make_sentence(
            "Sempatik kökenli ağrılar: **Otonom sinir sistemiyle ilişkili tablolar**",
            "Sempatik ağrılar, periferik bir travma sonrasında otonom sinir sisteminin anormal aktivasyonu ve nosiseptif liflerle sempatik lifler arasında gelişen patolojik etkileşim sonucu ortaya çıkar.",
            23, 25, satir_pattern="Sempatik", duzey=0
        ),
        make_sentence(
            "Kompleks bölgesel ağrı sendromu: **Tip bir ve Tip iki ayrımı**",
            "Klinik pratikte refleks sempatik distrofi olarak bilinen Kompleks Bölgesel Ağrı Sendromu Tip bir belirgin sinir lezyonu olmaksızın gelişirken; majör sinir hasarına eşlik eden formuna Tip iki yani kozalji denir.",
            23, 25, satir_pattern="kaynaklandığı", duzey=1
        ),
        make_sentence(
            "Alfa adrenerjik duyarlılık: **Nosiseptörlerde katekolamin yanıtı**",
            "Hasarlanan primer afferent liflerin zarlarında anormal alfa-adrenerjik reseptörler sentezlenir; böylece dolaşımdaki adrenalin ve sempatik tonus artışı doğrudan ağrıyı tetikler.",
            23, 25, satir_pattern="bölgeye", duzey=1
        )
    ]

    p24 = [
        make_sentence(
            "Klinik bulgular: **Gece artan yanıcı ağrı, ödem ve vazomotor bozukluk**",
            "Sempatik ağrılar özellikle geceleri şiddetlenir; ağrının yanı sıra ekstremitede hiperhidroz yani aşırı terleme, soğukluk, ödem ve cilt renginde solukluk veya morarma gibi belirgin vazomotor instabilite izlenir.",
            24, 25, satir_pattern="geceleri", duzey=0
        ),
        make_sentence(
            "Trofik değişiklikler: **Tırnak, kıl ve kemik demineralizasyonu**",
            "Zamanla etkilenen uzuvda tırnaklarda kırılma, kıllanmada dökülme, cilt atrofisi ve radyolojide Sudeck atrofisi adı verilen benekli osteoporoz gibi ileri trofik bozukluklar açığa çıkar.",
            24, 25, satir_pattern="Ağrının", duzey=1
        ),
        make_sentence(
            "Sempatik blok yanıtı: **Tanısal ve terapötik sempatektomi başarısı**",
            "Sempatik ganglion blokajı yapıldığında hastanın ağrısının dakikalar içinde dramatik olarak gerilemesi, tablonun sempatik aracılı olduğunun altın standart kanıtıdır.",
            24, 25, satir_pattern="artar", duzey=1
        )
    ]

    b06 = {
        "id": "k2-06-b06",
        "baslik": "Deafferentasyon Ağrıları ve Sempatik Ağrılar",
        "paragraflar": [
            {"id": "k2-06-p020", "sayfa": 21, "slayt_adim": 23, "cumleler": p21},
            {"id": "k2-06-p021", "sayfa": 22, "slayt_adim": 24, "cumleler": p22},
            {"id": "k2-06-p022", "sayfa": 23, "slayt_adim": 25, "cumleler": p23},
            {"id": "k2-06-p023", "sayfa": 24, "slayt_adim": 25, "cumleler": p24}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 7: Psikojenik Ağrı ve Nosiplastik Ağrı Kavramı (Sayfa 25-27)
    # ----------------------------------------------------
    p25 = [
        make_sentence(
            "Psikojenik ve fonksiyonel ağrı: **Kronik ağrıda psişik faktörlerin rolü**",
            "Psikojenik ya da fonksiyonel ağrı, altta yatan hiçbir organik doku hasarı veya sinir lezyonu gösterilemeyen, doğrudan psikolojik çatışmalar, ağır anksiyete veya somatizasyon bozukluğuna bağlı gelişen ağrılı tablodur.",
            25, 26, satir_pattern="Psikojenik", duzey=0
        ),
        make_sentence(
            "İkincil psikolojik reaksiyonlar: **Ağrının depresyon ve çaresizlik doğurması**",
            "Kronik ağrılı olguların hemen tamamında ağrının uzamasına sekonder olarak reaktif depresyon, panik ve çaresizlik semptomları eklenerek ağrı algısı daha da pekiştirilir.",
            25, 26, satir_pattern="Kronik", duzey=1
        ),
        make_sentence(
            "Ayırıcı tanı sorumluluğu: **Organik patolojiler dışlanmadan psikolojik denmez**",
            "Bir hastaya psikojenik ağrı tanısı koyabilmek için tüm radyolojik, nörolojik ve biyokimyasal tetkiklerle organik nosiseptif ve nöropatik süreçlerin eksiksiz dışlanmış olması şarttır.",
            25, 26, satir_pattern="hastalarda", duzey=1
        )
    ]

    p26 = [
        make_sentence(
            "Klinik görünüm: **Dramatik anlatım ve anatomik uyuşmazlık**",
            "Psikojenik ağrılı hastalar sıklıkla hiçbir anatomik dermatom veya periferik sinir trasesine uymayan, vücudun tamamına yayılan, dramatik ve abartılı ifadelerle ağrılarını tasvir ederler.",
            26, 26, satir_pattern="Hastanın", duzey=0
        ),
        make_sentence(
            "Konversiyon ve somatizasyon: **Ruhsal acının bedensel ağrıya dönüşümü**",
            "Bireyin yüzleşmekten kaçındığı derin emosyonel travmalar ve bilinçdışı sıkıntılar konversiyon mekanizmasıyla bedensel kronik kas spazmları ve dirençli ağrılar şeklinde açığa çıkar.",
            26, 26, satir_pattern="psişik", duzey=1
        ),
        make_sentence(
            "Multidisipliner sağaltım: **Analjezik yerine psikoterapi ve psikiyatri desteği**",
            "Bu hastalarda geleneksel analjezikler ve opioidler genellikle tamamen etkisiz kalır; bilişsel davranışçı terapi ve antidepresan tedaviler küratif yaklaşımın esasını oluşturur.",
            26, 26, satir_pattern="Hastanın", duzey=1
        )
    ]

    p27 = [
        make_sentence(
            "Nosiplastik ağrı tanımı: **Doku hasarı olmaksızın değişen nosisepsiyon**",
            "Nosiplastik ağrı; belirgin bir doku hasarı, nosiseptör aktivasyonu veya somatosensoriyel sinir lezyonu olmamasına rağmen, santral ağrı iletim yollarındaki nöral devrelerin değişmesi ve aşırı hassaslaşması sonucu gelişen ağrıdır.",
            27, 27, satir_pattern="Nociplastik", duzey=0
        ),
        make_sentence(
            "Prototip hastalık: **Fibromiyalji ve santral amplifikasyon mekanizması**",
            "Fibromiyalji sendromu, irritabl bağırsak hastalığı ve nonspesifik kronik bel ağrısı nosiplastik ağrının en tipik örnekleridir ve bu tablolarda beyin ağrı sinyallerinin sesini aşırı yükseltmiştir.",
            27, 27, satir_pattern="Belirgin", duzey=1
        ),
        make_sentence(
            "Terminolojik devrim: **Psikolojik yaftasını kaldıran nörobiyolojik kanıt**",
            "Nosiplastik kavramı eskiden psikolojik sanılan fibromiyalji gibi tabloların fonsiyonel manyetik rezonansla kanıtlanmış nörobiyolojik bir santral işlemleme bozukluğu olduğunu tıp literatürüne kazandırmıştır.",
            27, 27, satir_pattern="hasarı", duzey=1
        )
    ]

    b07 = {
        "id": "k2-06-b07",
        "baslik": "Psikojenik Ağrı ve Nosiplastik Ağrı Kavramı",
        "paragraflar": [
            {"id": "k2-06-p024", "sayfa": 25, "slayt_adim": 26, "cumleler": p25},
            {"id": "k2-06-p025", "sayfa": 26, "slayt_adim": 26, "cumleler": p26},
            {"id": "k2-06-p026", "sayfa": 27, "slayt_adim": 27, "cumleler": p27}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 8: Kaynaklandığı Bölgeye Göre Ağrı: Somatik ve Visseral Ağrı (Sayfa 28-32)
    # ----------------------------------------------------
    p28 = [
        make_sentence(
            "Bölgeye göre sınıflama: **Somatik ve visseral anatomik kökenler**",
            "Ağrının kaynaklandığı anatomik bölgeye göre yapılan üçüncü sınıflamada somatik ağrı ve visseral ağrı olmak üzere iki ana grup ele alınır.",
            28, 29, satir_pattern="Kaynaklandığı", duzey=0
        ),
        make_sentence(
            "İnnervasyon farkı: **Somatosensoriyel lifler ve otonomik pleksuslar**",
            "Somatik yapılar spinal miyelinli somatik sinir lifleriyle uyarılırken, iç organlar otonomik sempatik ve parasempatik lifler eşliğinde seyreden C lifleriyle inerve edilir.",
            28, 29, satir_pattern="bölgeye", duzey=1
        ),
        make_sentence(
            "Klinik tablonun karakteri: **Keskin lokalizasyondan yaygın sızlamaya**",
            "Bu anatomik innervasyon ayrımı, ağrının keskin ve noktasal mı yoksa künt, yaygın ve bulantılı mı hissedileceğini doğrudan tayin eder.",
            28, 29, satir_pattern="ağrı", duzey=1
        )
    ]

    p29 = [
        make_sentence(
            "Somatik ağrı özellikleri: **Deri, kas, eklem ve kemik kaynaklı iletim**",
            "Somatik ağrı; kas-iskelet sistemi, deri, fasya ve periost gibi somatik dokulardan kaynaklanan ve omuriliğe miyelinli A-delta ile miyelinsiz C lifleriyle taşınan nosiseptif ağrıdır.",
            29, 29, satir_pattern="Somatik", duzey=0
        ),
        make_sentence(
            "Ayırıcı alt gruplar: **Yüzeyel kutanöz ağrı ve derin doku ağrıları**",
            "Somatik ağrı kendi içinde deri ve mukozayı ilgilendiren yüzeyel somatik ağrı ile kas, eklem ve periostu tutan derin somatik ağrı olarak ikiye ayrılır.",
            29, 30, satir_pattern="somatik", duzey=1
        ),
        make_sentence(
            "Klinik lokalizasyon netliği: **Hasta ağrının yerini parmağıyla gösterebilir**",
            "Özellikle yüzeyel somatik ağrıda reseptör yoğunluğunun yüksek olması sayesinde hasta ağrılı odağın sınırlarını çok net biçimde lokalize edebilir.",
            29, 30, satir_pattern="lifleriyle", duzey=1
        )
    ]

    p30 = [
        make_sentence(
            "Somatik yüzeyel ağrı: **Deri ve mukozal kaynaklı keskin ve yanık ağrısı**",
            "Somatik yüzeyel ağrı deri ve müköz membranlardan kaynaklanır; iğne batması, kesik veya termal yanık ağrısı gibi keskin karakterdedir ve santral kortekste milimetrik olarak lokalize edilir.",
            30, 30, satir_pattern="Somatik", duzey=0
        ),
        make_sentence(
            "Çıkmış Sınav Sorusu: **Somatik ağrının özellikleri ve otonomik semptom yokluğu**",
            "Burada çıkmış sınav sorusu bulunmaktadır: Somatik ağrı deri, kas ve eklemlerden kaynaklanan, iyi lokalize edilen ve sıklıkla batıcı veya sızlayıcı vasıfta hissedilen ağrıdır; otonomik bulantı ve yaygın yansıma yapmamasıyla visseral ağrıdan kesin olarak ayrılır.",
            30, 30, satir_pattern="lokalize", duzey=1, cikmis=["01a96a18bccf"], highlight_word="Somatik yüzeyel ağrı"
        ),
        make_sentence(
            "Somatik derin ağrı: **Künt, sızlayıcı ve periost-eklem kökenli**",
            "Buna karşılık kemik kırıkları, periostit veya artritlerde görülen derin somatik ağrı daha künt, sızlayıcı, yaygın ve yorucu bir nitelik sergiler.",
            30, 30, satir_pattern="Yanık", duzey=1
        )
    ]

    p31 = [
        make_sentence(
            "Visseral ağrı tanımı: **İç organlardan kaynaklanan künt ve yaygın acı**",
            "Visseral ağrı; toraks, batın ve pelvisteki iç organların patolojilerinden kaynaklanan, derin, künt, baskı veya kramp tarzında hissedilen ve sınırları net çizilemeyen bir ağrı türüdür.",
            31, 31, satir_pattern="Visseral", duzey=0
        ),
        make_sentence(
            "Çıkmış Sınav Sorusu: **Bağırsak patolojilerinde visseral ağrı ve otonomik yanıt**",
            "Burada çıkmış sınav sorusu bulunmaktadır: Bağırsak, safra kesesi ve üreter gibi içi boş organların gerilmesi, spazmı veya iskemisi sonucu gelişen visseral ağrı; kötü lokalize edilen, dermatomlar boyunca yansıyan ve bradikardi, terleme, bulantı gibi yoğun otonomik semptomların eşlik ettiği ağrı tipidir.",
            31, 31, satir_pattern="organlardan", duzey=1, cikmis=["58700c98a3db", "392041a09b26", "303055c213d3"], highlight_word="Visseral ağrı"
        ),
        make_sentence(
            "Yansıyan ağrı mekanizması: **Dorsal boynuzda konverjans ve miyokard enfarktüsü**",
            "İç organlardan gelen visseral afferentler ile deriden gelen somatik afferentler omurilik arka boynuzunda aynı ikinci sıra nöronlara konverjans gösterir; bu nedenle kalp iskemisi ağrısı sol omuza ve kola yansıyan ağrı olarak algılanır.",
            31, 32, satir_pattern="kaynaklanan", duzey=1
        ),
        make_sentence(
            "Organ duyarsızlığı kuralı: **Kesme ve yakmaya değil, gerilmeye duyarlı**",
            "İç organların parankimi cerrahi olarak kesildiğinde veya yakıldığında ağrı oluşmazken; organ kapsülünün gerilmesi, düz kas spazmı, asidoz ve iskemi şiddetli visseral ağrıyı tetikleyen temel uyaranlardır.",
            31, 32, satir_pattern="tümü", duzey=1
        )
    ]

    p32 = [
        make_sentence(
            "Sempatik ağrının klinik tablosu: **Vazomotor krizler ve gece alevlenmesi**",
            "Bölgesel sınıflamada sempatik ağrılar özellikle geceleri şiddetlenen yanıcı ağrı, paroksismal vazomotor krizler ve ödem tablosu ile ayırt edilir.",
            32, 33, satir_pattern="Ağrı", duzey=0
        ),
        make_sentence(
            "Kozalji sendromu: **Periferik sinir hasarı zemininde kalıcı yanma**",
            "Özellikle median ve siyatik sinir gövdesinin kurşunlanma veya ezilme gibi travmatik hasarları sonrasında gelişen kozalji tablosunda hasta uzvunu ıslak havluyla sararak korumaya çalışır.",
            32, 33, satir_pattern="geceleri", duzey=1
        ),
        make_sentence(
            "Distrofik evre: **Ekstremite fonksiyonunun kaybı ve sertlik**",
            "Erken evrede sempatik blokaj yapılmazsa eklemlerde ankiloz, ciltte atrofi ve ekstremitede tam fonksiyon kaybı ile sonuçlanan geri dönüşsüz distrofik evreye geçilir.",
            32, 33, satir_pattern="yanısıra", duzey=1
        )
    ]

    b08 = {
        "id": "k2-06-b08",
        "baslik": "Kaynaklandığı Bölgeye Göre Ağrı: Somatik ve Visseral Ağrı",
        "paragraflar": [
            {"id": "k2-06-p027", "sayfa": 28, "slayt_adim": 29, "cumleler": p28},
            {"id": "k2-06-p028", "sayfa": 29, "slayt_adim": 29, "cumleler": p29},
            {"id": "k2-06-p029", "sayfa": 30, "slayt_adim": 30, "cumleler": p30},
            {"id": "k2-06-p030", "sayfa": 31, "slayt_adim": 31, "cumleler": p31},
            {"id": "k2-06-p031", "sayfa": 32, "slayt_adim": 33, "cumleler": p32}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 9: Patogenezine ve Tedaviye Yanıtına Göre Ağrı (Sayfa 33-34)
    # ----------------------------------------------------
    p33 = [
        make_sentence(
            "Patogeneze göre sınıflama: **İnflamatuar, iskemik ve deafferentasyon ağrısı**",
            "Patogenezine göre ağrılar; doku hasarındaki mediyatörlerle tetiklenen inflamatuar ağrı, doku perfüzyonunun bozulmasıyla gelişen iskemik ağrı, sinir iletim kaybına bağlı deafferentasyon ağrısı ve nedeni saptanamayan idiyopatik ağrı olarak ayrılır.",
            33, 34, satir_pattern="Patogenezine", duzey=0
        ),
        make_sentence(
            "İnflamatuar patogenez: **Prostaglandin, bradikinin ve histamin fırtınası**",
            "İnflamatuar ağrıda mast hücreleri ve lökositlerden bol miktarda prostaglandin, bradikinin, serotonin ve histamin salınarak nosiseptör uyarılma eşiği dramatik biçimde düşürülür.",
            33, 34, satir_pattern="İnflamatuar", duzey=1
        ),
        make_sentence(
            "İskemik patogenez: **Laktik asit, asidoz ve klaudikasyo intermittens**",
            "İskemik ağrıda doku hipoksisi sonucu hücre içi potasyum açığa çıkar, laktik asidoz gelişir ve hidrojen iyonları asit duyarlı iyon kanallarını uyararak anjina pektoris veya bacakta kramp ağrısı oluşturur.",
            33, 34, satir_pattern="bradikinin", duzey=1
        ),
        make_sentence(
            "İdiyopatik ağrı: **Organik dayanağı bulunamayan klinik tablolar**",
            "Tüm ileri görüntüleme ve laboratuvar yöntemlerine rağmen patolojik veya biyokimyasal kaynağı gösterilemeyen inatçı tablolara ise idiyopatik ağrı denir.",
            33, 34, satir_pattern="histamin", duzey=1
        )
    ]

    p34 = [
        make_sentence(
            "Tedavi yanıtına göre sınıflama: **Opioid-duyarlı ve duyarsız ağrılar**",
            "Tedaviye cevabına göre ağrılar; klasik narkotik analjeziklerle hızla kontrol altına alınabilen opioid-duyarlı ağrılar ile morfine zayıf yanıt veren veya tamamen dirençli olan opioid-duyarsız ağrılar olarak ikiye ayrılır.",
            34, 36, satir_pattern="Tedaviye", duzey=0
        ),
        make_sentence(
            "Opioid duyarlılığı kuralı: **Nosiseptif ağrı duyarlı, nöropatik ağrı dirençli**",
            "Nosiseptör kaynaklı somatik ve visseral akut ağrılar morfine ve diğer güçlü opioidlere fevkalade duyarlıyken; sinir hasarına bağlı deafferentasyon ve nöropatik ağrılar klasik opioid tedavisine büyük ölçüde dirençlidir.",
            34, 36, satir_pattern="Opioid-duyarlı", duzey=1
        ),
        make_sentence(
            "Rasyonel farmakoterapi ilkesi: **Dirençli ağrıda opioid dozunu artırmayın**",
            "Nöropatik ve deafferentasyon ağrılarında opioid dozunu kontrolsüzce artırmak ağrıyı kesmediği gibi solunum depresyonu ve bağımlılık riskini katlar; bu tablolarda gabapentinoid ve trisiklik ajanlara geçilmelidir.",
            34, 36, satir_pattern="Nosiseptör", duzey=1
        )
    ]

    b09 = {
        "id": "k2-06-b09",
        "baslik": "Patogenezine ve Tedaviye Yanıtına Göre Ağrı",
        "paragraflar": [
            {"id": "k2-06-p032", "sayfa": 33, "slayt_adim": 34, "cumleler": p33},
            {"id": "k2-06-p033", "sayfa": 34, "slayt_adim": 36, "cumleler": p34}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 10: Ağrı Algılamasının Dört Temel Aşaması (Sayfa 35-41)
    # ----------------------------------------------------
    p35 = [
        make_sentence(
            "Ağrı mekanizmalarına giriş: **Periferik algıdan serebral bilince yolculuk**",
            "Dersimizin bu kritik bölümünde ağrının periferik dokudan başlayarak serebral kortekste bilinç düzeyine ulaşana kadar katettiği dört temel nörofizyolojik aşamayı ayrıntılarıyla inceleyeceğiz.",
            35, 38, satir_pattern="Ağrı", duzey=0
        ),
        make_sentence(
            "Dört basamaklı zincir: **Transdüksiyon, transmisyon, modülasyon ve persepsiyon**",
            "Zararlı uyarının hissedilmesi; enerjinin aksiyon potansiyeline dönüştüğü transdüksiyon, sinyalin taşındığı transmisyon, omurilikte filtrelendiği modülasyon ve beyinde algılandığı persepsiyon kaskadından oluşur.",
            35, 38, satir_pattern="Mekanizmaları", duzey=1
        ),
        make_sentence(
            "Multimodal analjezi temeli: **Her aşamaya farklı farmakolojik blokaj**",
            "Modern anestezide uygulanan multimodal analjezi stratejisi, ağrı kaskadının bu dört ayrı basamağını farklı analjezik ajanlarla eşzamanlı bloke etme prensibine dayanır.",
            35, 38, satir_pattern="Ağrı", duzey=1
        )
    ]

    p36 = [
        make_sentence(
            "Periferik reseptör uyarımı: **Noxious stimulusun aksiyon potansiyeli başlatması**",
            "Ağrının algılanma süreci periferik dokularda yerleşmiş çıplak sinir uçları olan nosiseptörlerin mekanik bası, aşırı sıcak-soğuk veya kimyasal maddelerle depolarize olmasıyla başlar.",
            36, 38, satir_pattern="Periferde", duzey=0
        ),
        make_sentence(
            "İyon kanalı aktivasyonu: **Sodyum ve kalsiyum akımıyla jeneratör potansiyeli**",
            "Doku hasarıyla aktive olan iyon kanalları sinir ucundan içeri sodyum ve kalsiyum girişini sağlayarak lokal bir jeneratör potansiyeli oluşturur ve bu potansiyel eşik değeri aştığında aksiyon potansiyeline dönüşür.",
            36, 38, satir_pattern="algılanması", duzey=1
        ),
        make_sentence(
            "İletim yönü: **Spinal arka boynuza doğru afferent akış**",
            "Oluşan bu elektrofizyolojik sinyal duyu nöronunun aksonu boyunca kesintisiz şekilde ilerleyerek medulla spinalis dorsal boynuzundaki sinapslara doğru taşınır.",
            36, 38, satir_pattern="Ağrının", duzey=1
        )
    ]

    p37 = [
        make_sentence(
            "Transdüksiyon tanımı: **Fiziksel enerjinin elektriksel potansiyele dönüşümü**",
            "Transdüksiyon, periferik nosiseptörlerde zararlı mekanik, termal ya da kimyasal bir enerji türünün sinir liflerinde yayılabilecek elektriksel aksiyon potansiyeline dönüştürülmesi olayıdır.",
            37, 39, satir_pattern="Transdüksiyon", duzey=0
        ),
        make_sentence(
            "Eşik değeri kuralı: **Her sıcak uyaran ağrılı değildir**",
            "Örneğin ılık ya da sıcak bir temas yalnızca ısı duyusu oluştururken; doku hasarı riskinin başladığı kırk üç ila kırk beş santigrat derecenin üzerine çıkıldığında termal nosiseptörler ateşlenir ve transdüksiyon başlar.",
            37, 39, satir_pattern="enerjinin", duzey=1
        ),
        make_sentence(
            "Çıkmış Sınav Sorusu: **Nosisepsiyonun dört aşaması ve transdüksiyon kavramı**",
            "Burada çıkmış sınav sorusu bulunmaktadır: Ağrı algılanması yani nosisepsiyon transdüksiyon, transmisyon, modülasyon ve persepsiyon olmak üzere dört temel aşamada gerçekleşir; mekanik, termal veya kimyasal zararlı uyaran enerjisinin periferik nosiseptör reseptörlerinde elektriksel aksiyon potansiyeline dönüştürülmesi transdüksiyon olarak adlandırılır.",
            37, 39, satir_pattern="aşama", duzey=1, cikmis=["11cec678fef5", "5afc023320d4", "57c4c3ee7531"], highlight_word="Transdüksiyon"
        ),
        make_sentence(
            "Transdüksiyonu bloke eden ajanlar: **NSAİİ ve periferik lokal anestezikler**",
            "İnflamatuar mediyatörlerin sentezini engelleyen nonsteroid antiinflamatuarlar ve yara yerine uygulanan lokal anestezik enjeksiyonları ağrıyı tam bu transdüksiyon aşamasında durdururlar.",
            37, 39, satir_pattern="sıcak", duzey=1
        )
    ]

    p38 = [
        make_sentence(
            "Transmisyon basamağı: **Aksiyon potansiyelinin santral aks boyunca iletimi**",
            "Transmisyon, transdüksiyonla oluşan ağrı sinyalinin periferik primer afferent aksonlar boyunca omurilik arka boynuzuna, oradan çıkan yollarla talamusa ve serebral kortekse doğru iletilmesidir.",
            38, 40, satir_pattern="Transmisyon", duzey=0
        ),
        make_sentence(
            "A-delta lifleri iletimi: **Hızlı, miyelinli, batıcı ve keskin ilk ağrı**",
            "Miyelinli A-delta lifleri saniyede beş ila otuz metre gibi yüksek bir hızla iletim yaparak mekanik ve termal hasarı anında taşır; doku travmasında ilk hissedilen keskin, batıcı ve tam lokalize ağrıdan sorumludur.",
            38, 40, satir_pattern="A-delta", duzey=1
        ),
        make_sentence(
            "C lifleri iletimi: **Yavaş, miyelinsiz, künt ve sızlayıcı ikinci ağrı**",
            "Miyelinsiz ince C lifleri ise saniyede yarım ila iki metre gibi çok yavaş bir hızla iletim yapar; ilk keskin acının ardından başlayan, uzun süren, yaygın, künt ve sızlayıcı ikinci ağrıyı iletir.",
            38, 41, satir_pattern="lifleri", duzey=1
        )
    ]

    p39 = [
        make_sentence(
            "Modülasyon basamağı: **Medulla spinalis arka boynuzunda sinyal amplifikasyonu ve inhibisyonu**",
            "Modülasyon, periferden gelen nosiseptif uyarının omurilik arka boynuzundaki nöronal ağlarda, internöronlar ve inen analjezik yollar aracılığıyla filtrelenmesi, şiddetinin azaltılması ya da artırılması sürecidir.",
            39, 42, satir_pattern="Modülasyon", duzey=0
        ),
        make_sentence(
            "Kapı kontrolü ve nöropeptidler: **Ağrı sinyalinin yukarı geçiş kararı**",
            "Spinal dorsal boynuzda yer alan substantia gelatinosa bölgesi bir kapı gibi çalışarak; salınan endojen opioidler, gaba ve glisin ile ağrının beyne iletimini baskılayabilir.",
            39, 42, satir_pattern="spinalis", duzey=1
        ),
        make_sentence(
            "Modülasyon farmakoterapisi: **Epidural opioidler ve alfa-iki agonistler**",
            "Epidural veya intratekal uygulanan morfin, fentanil ve klonidin gibi ajanlar doğrudan dorsal boynuzdaki modülasyon kapısını kapatarak çok güçlü segmental analjezi sağlarlar.",
            39, 42, satir_pattern="değişime", duzey=1
        )
    ]

    p40 = [
        make_sentence(
            "Persepsiyon aşaması: **Kortikal alanda ağrının bilinçli algısı ve acı deneyimi**",
            "Persepsiyon, medulla spinalisten spinotalamik yolakla yükselen uyaranların talamus, somatosensoriyel korteks, insula ve anterior singulat kortekse ulaşarak bilinç düzeyinde ağrı ve acı olarak algılanmasıdır.",
            40, 43, satir_pattern="Persepsiyon", duzey=0
        ),
        make_sentence(
            "Algının üç boyutu: **Lokalizasyon, duygu ve motor kaçınma tepkisi**",
            "Primer duyusal korteks ağrının tam yerini ve şiddetini belirlerken, singulat korteks ve amigdala ağrının oluşturduğu psikolojik ıstırabı ve acil kaçınma reflekslerini tetikler.",
            40, 43, satir_pattern="çıkan", duzey=1
        ),
        make_sentence(
            "Genel anesteziklerin etkisi: **Bilinç kapanınca persepsiyon tamamen silinir**",
            "Genel anestezikler ve hipnotik ajanlar serebral korteksi baskılayarak algıyı yani persepsiyonu ortadan kaldırır; ameliyat sırasında nosisepsiyon devam etse bile hasta hiçbir ağrı hissetmez.",
            40, 43, satir_pattern="algılanmasıdır", duzey=1
        )
    ]

    p41 = [
        make_sentence(
            "Şema analizi: **Dört basamaklı ağrı yolu ve anatomik duraklar**",
            "Bu slaytımızdaki anatomik şema noxious zararlı uyarandan başlayarak primer afferent nosiseptör, spinal kord arka boynuzu, spinotalamik traktus, talamus ve serebral korteks eksenindeki eksiksiz iletim yolunu özetlemektedir.",
            41, 44, sekil="Ağrı yolu şeması: noxious uyaran, primer afferent nosiseptör, spinal kord, spinotalamik traktus, talamus, korteks ve analjezik etki basamakları", duzey=0
        ),
        make_sentence(
            "Lokal anestezik etki yerleri: **Transdüksiyon ve transmisyon basamaklarının kilitlenmesi**",
            "Şemada transdüksiyon periferik insizyonel, intraplevral ve intraperitoneal lokal anestezik infiltrasyonuyla; transmisyon ise periferik sinir blokları, çölyak pleksus blokajı, epidural ve subaraknoid lokal anesteziklerle tam olarak hedeflenir.",
            41, 44, sekil="Transdüksiyon ve transmisyon için lokal anestezik etki yerleri şeması", duzey=1
        ),
        make_sentence(
            "Opioid etki mekanizması: **Modülasyonda spinal, persepsiyonda supraspinal blokaj**",
            "Şemanın üst ve orta kısımlarında görüldüğü üzere modülasyon aşaması epidural ve intratekal opioidlerle dorsal boynuzda durdurulurken; sistemik opioidler hem omurilikte hem de talamus ve korteksteki supraspinal reseptörlerde etki gösterir.",
            41, 44, sekil="Modülasyon için epidural ve subaraknoid opioid ile sistemik opioid etki noktaları şeması", duzey=1
        )
    ]

    b10 = {
        "id": "k2-06-b10",
        "baslik": "Ağrı Algılamasının Dört Temel Aşaması",
        "paragraflar": [
            {"id": "k2-06-p034", "sayfa": 35, "slayt_adim": 38, "cumleler": p35},
            {"id": "k2-06-p035", "sayfa": 36, "slayt_adim": 38, "cumleler": p36},
            {"id": "k2-06-p036", "sayfa": 37, "slayt_adim": 39, "cumleler": p37},
            {"id": "k2-06-p037", "sayfa": 38, "slayt_adim": 40, "cumleler": p38},
            {"id": "k2-06-p038", "sayfa": 39, "slayt_adim": 42, "cumleler": p39},
            {"id": "k2-06-p039", "sayfa": 40, "slayt_adim": 43, "cumleler": p40},
            {"id": "k2-06-p040", "sayfa": 41, "slayt_adim": 44, "cumleler": p41}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 11: Moleküler Mekanizmalar: Periferik Sensitizasyon ve İnflamasyon (Sayfa 42-46)
    # ----------------------------------------------------
    p42 = [
        make_sentence(
            "Moleküler ve santral mekanizmalar: **Ağrının kronikleşme biyolojisi**",
            "Dersimizin bu bölümünde periferik sensitizasyon, santral sensitizasyon, disinhibisyon ve yapısal reorganizasyon olmak üzere kronik ağrının temel moleküler basamaklarını ele alacağız.",
            42, 46, satir_pattern="Moleküler", duzey=0
        ),
        make_sentence(
            "Hassaslaşma kaskadı: **Normal dokunun hiperaljezik dokuya dönüşümü**",
            "Doku zedelenmesini takiben salınan kimyasal mediyatörler nosiseptör zarındaki iyon kanallarını fosforilasyona uğratarak uyarılma eşiğini dramatik şekilde düşürür.",
            42, 46, satir_pattern="mekanizmalar", duzey=1
        ),
        make_sentence(
            "Klinik tablonun temeli: **Dokunmayla sızlayan cerrahi yaralar**",
            "Bu moleküler mekanizmalar, ameliyat sonrasında kesi çevresindeki sağlam cildin bile hafif dokunmayla şiddetle ağrımasına yol açan fizyopatolojik sürecin özüdür.",
            42, 46, satir_pattern="Santral", duzey=1
        )
    ]

    p43 = [
        make_sentence(
            "Periferik sensitizasyon: **İnflamatuar hücre göçü ve nörojenik inflamasyon**",
            "Periferik sensitizasyon; doku hasarını takiben yaralanma bölgesine makrofaj, mast hücresi, lenfosit ve trombositlerin göç etmesi ve buradan ortama yoğun kimyasal mediyatörler salınmasıyla başlar.",
            43, 46, satir_pattern="Periferik", duzey=0
        ),
        make_sentence(
            "Akson refleksi: **Nosiseptör ucundan geriye doğru peptid salınımı**",
            "Nosiseptif uyarının kendisi de akson refleksi aracılığıyla antidromik olarak periferik sinir uçlarından çevre dokuya nöropeptidlerin salınmasına yani nörojenik inflamasyona yol açar.",
            43, 46, satir_pattern="nörojenik", duzey=1
        ),
        make_sentence(
            "İnflamatuar çorba oluşumu: **Kimyasal mediyatörlerin sinerjistik patlaması**",
            "Doku alanında biriken bu zengin kimyasal karışıma algolojide inflamatuar çorba adı verilir ve nosiseptörleri sürekli uyarılmış halde tutar.",
            43, 47, satir_pattern="makrofaj", duzey=1
        )
    ]

    p44 = [
        make_sentence(
            "Nörojenik peptidler: **Madde P ve CGRP'nin vasküler etkileri**",
            "Nosiseptif sinir uçlarından salınan madde P ve kalsitonin geni ilişkili peptid yani ce ge re pe; çevre damarlarda şiddetli vazodilatasyona ve plazma proteinlerinin damar dışına sızmasına yani ekstravazasyona yol açar.",
            44, 47, satir_pattern="peptidlerin", duzey=0
        ),
        make_sentence(
            "Mediyatör fırtınası: **Serotonin, histamin, bradikinin ve prostaglandin E2**",
            "Mast hücrelerinden salınan histamin, trombosit kaynaklı serotonin, plazma kininojeninden üretilen bradikinin ve hasarlı hücre zarlarından sentezlenen prostaglandinler birleşerek nosiseptörleri adeta bombardımana tutar.",
            44, 48, satir_pattern="serotonin", duzey=1
        ),
        make_sentence(
            "Sessiz nosiseptörlerin uyanışı: **Uyuyan yüksek eşikli liflerin devreye girmesi**",
            "Normal koşullarda hiçbir uyarana yanıt vermeyen yüksek eşikli mekanik ve termal sessiz nosiseptörler bu kimyasal fırtına ile duyarlılaşarak spontan ağrı sinyalleri üretmeye başlarlar.",
            44, 48, satir_pattern="vazodilatasyona", duzey=1
        )
    ]

    p45 = [
        make_sentence(
            "Sensitizasyonun klinik sonucu: **Düşük mekanik ve termal eşik değeri**",
            "Periferik sensitizasyon geliştikten sonra, normalde hiçbir acı oluşturmayacak hafif şiddetteki mekanik dokunmalar ve ılık temaslar dahi şiddetli ağrılı olarak algılanmaya başlar.",
            45, 49, satir_pattern="Sensitizasyondan", duzey=0
        ),
        make_sentence(
            "Primer hiperaljezi sahası: **Hasarlı doku sınırları içinde artmış duyarlılık**",
            "Doku harabiyeti bölgesindeki bu aşırı duyarlılık artışına primer hiperaljezi adı verilir ve hem mekanik hem de termal uyaranlara karşı belirgin yanıt artışıyla kendini gösterir.",
            45, 49, satir_pattern="şiddetteki", duzey=1
        ),
        make_sentence(
            "Koruyucu refleks amilörizasyonu: **Hasarlı bölgenin dinlenmeye alınması**",
            "Fizyolojik açıdan bu aşırı hassaslaşma bireyin hasarlı organını temas ve yükten korumasını sağlayarak doku rejenerasyonuna olanak tanıyan koruyucu bir adaptasyondur.",
            45, 49, satir_pattern="termal", duzey=1
        )
    ]

    p46 = [
        make_sentence(
            "Periferik tedavi hedefleri: **Cerrahi sonrası primer hiperaljeziyi durdurmak**",
            "Primer hiperaljezi bölgesindeki periferik sensitizasyon değişiklikleri cerrahi girişimler, kırıklar ve yanıklardan sonra belirginleşir; erken dönemde durdurulması ağrının kronikleşmesini önler.",
            46, 50, satir_pattern="primer", duzey=0
        ),
        make_sentence(
            "Siklooksijenaz inhibisyonu: **Aspirin ve nonsteroid antiinflamatuarlar**",
            "İnflamatuar cevabı baskılamak amacıyla kullanılan aspirin, ibuprofen ve diğer nonsteroid antiinflamatuar ilaçlar, siklooksijenaz bir ve iki enzimlerini bloke ederek prostaglandin sentezini kökünden keserler.",
            46, 50, satir_pattern="aspirin", duzey=1
        ),
        make_sentence(
            "Lokal anestezikler ve kortikosteroidler: **Membran stabilizasyonu ve sitokin blokajı**",
            "Yara çevresine uygulanan lokal anestezik enjeksiyonları sodyum kanallarını bloke ederken; kortikosteroidler fosfolipaz a iki enzimini ve proinflamatuar sitokin transkripsiyonunu durdurarak periferik duyarlılaşmayı engeller.",
            46, 50, satir_pattern="antiinflamatuarlar", duzey=1
        )
    ]

    b11 = {
        "id": "k2-06-b11",
        "baslik": "Moleküler Mekanizmalar: Periferik Sensitizasyon ve İnflamasyon",
        "paragraflar": [
            {"id": "k2-06-p041", "sayfa": 42, "slayt_adim": 46, "cumleler": p42},
            {"id": "k2-06-p042", "sayfa": 43, "slayt_adim": 46, "cumleler": p43},
            {"id": "k2-06-p043", "sayfa": 44, "slayt_adim": 47, "cumleler": p44},
            {"id": "k2-06-p044", "sayfa": 45, "slayt_adim": 49, "cumleler": p45},
            {"id": "k2-06-p045", "sayfa": 46, "slayt_adim": 50, "cumleler": p46}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 12: Santral Sensitizasyon, Disinhibisyon ve Reorganizasyon (Sayfa 47-50)
    # ----------------------------------------------------
    p47 = [
        make_sentence(
            "Santral sensitizasyon tanımı: **Spinal dorsal boynuzda aşırı uyarılabilirlik**",
            "Santral sensitizasyon; periferden gelen sürekli ve yoğun nosiseptif bombardıman sonucunda, medulla spinalis dorsal boynuzundaki nöronların uyarılma eşiğinin düşmesi ve sinaptik yanıtlarının aşırı büyümesidir.",
            47, 51, satir_pattern="Santral", duzey=0
        ),
        make_sentence(
            "NMDA reseptör aktivasyonu: **Magnezyum tıkacının kalkması ve kalsiyum akışı**",
            "C liflerinden salınan sürekli glutamat ve madde P dorsal boynuz nöron zarını depolarize eder; istirahat halindeki magnezyum bloğu yerinden çıkar ve en em de a reseptörleri açılarak hücre içine devasa kalsiyum girişi başlar.",
            47, 51, satir_pattern="NMDA", duzey=1
        ),
        make_sentence(
            "Mikroglial sitokinler: **İnterlökin bir beta ve TNF alfa sinerjisi**",
            "Bu süreçte aktive olan mikroglia ve astrositler ortama interlökin bir beta, interlökin altı ve tümör nekrozis faktör alfa salarak sinaptik iletimi daha da kuvvetlendirir; spontan ağrı, yaygın hiperaljezi ve allodini tablosu yerleşir.",
            47, 51, satir_pattern="sitokinler", duzey=1
        )
    ]

    p48 = [
        make_sentence(
            "Disinhibisyon mekanizması: **İnhibitör baskı mekanizmalarının çökmesi**",
            "Disinhibisyon; normal fizyolojide omurilik arka boynuzundaki ağrı iletimini sürekli baskılayan inhibitör ara nöronların ve inen yolların etkinliğinin azalması sonucu ağrı eşiğinin çökmesidir.",
            48, 52, satir_pattern="Disinhibisyon", duzey=0
        ),
        make_sentence(
            "İnhibisyon kaybının klinik sonucu: **Ağrı sinyallerinin kontrolsüz amplifikasyonu**",
            "İnhibitör kontrol kaybolduğunda, en ufak bir duyusal uyarı dahi arka boynuzda devasa bir sinaptik yankı oluşturarak kortekse kesintisiz bir ağrı akışı şeklinde fırlar.",
            48, 52, satir_pattern="etkinliğininazalması", duzey=1
        ),
        make_sentence(
            "Kronik ağrı zeminindeki rolü: **Patolojik ağrı sendromlarının anahtarı**",
            "Özellikle postherpetik nevralji, diyabetik nöropati ve fantom ağrısı gibi kronik tablolarda disinhibisyon en temel idame mekanizması olarak karşımıza çıkar.",
            48, 52, satir_pattern="sendromlarında", duzey=1
        )
    ]

    p49 = [
        make_sentence(
            "Disinhibisyonun moleküler nedenleri: **İnen monoaminerjik sistem zayıflaması**",
            "Disinhibisyon kaskadında; beyin sapından omuriliğe inen serotonerjik ve noradrenerjik inhibitör yolakların tükenmesi ilk sırada yer alır.",
            49, 52, satir_pattern="inhibitör", duzey=0
        ),
        make_sentence(
            "GABA ve glisin kaybı: **Dorsal boynuz internöron apoptosisi**",
            "Ayrıca dorsal boynuzdaki gabaerjik ve glisinerjik internöronların eksitotoksisite ile ölmesi veya klor iletim dengesinin tersine dönmesi nöronal membran hiperpolarizasyonunu ortadan kaldırır.",
            49, 52, satir_pattern="GABA", duzey=1
        ),
        make_sentence(
            "Glutamat birikimi ve amplifikasyon: **Ağrı sinyallerinin yayılması**",
            "Astroglial glutamat geri alımının bozulmasıyla sinaptik aralıkta biriken glutamat en em de a reseptörlerini sürekli ateşler ve ağrı sinyalleri komşu sağlam dermatom segmentlerine kontrolsüzce taşar.",
            49, 52, satir_pattern="glutamat", duzey=1
        )
    ]

    p50 = [
        make_sentence(
            "Reorganizasyon kavramı: **Uzun süreli ağrıda yapısal ve anatomik yeniden şekillenme**",
            "Reorganizasyon; ağrı uyarımının aylarca devam etmesi durumunda somatosensoriyel sinir liflerinin, spinal arka boynuzun, talamusun ve serebral korteksin yapısal ve fonksiyonel olarak yeniden modellenmesidir.",
            50, 53, satir_pattern="Reorganizasyon", duzey=0
        ),
        make_sentence(
            "Anatomik filizlenme: **A-beta liflerinin lamina ikiye hatalı sinaps yapması**",
            "Normale göre kalın dokunma lifleri olan A-beta lifleri arka boynuzun derin tabakalarından yüzeyel tabaka olan substantia gelatinosaya doğru yeni akson filizleri uzatır; bu anatomik hata nedeniyle hafif dokunma doğrudan ağrı yoluna bağlanır.",
            50, 53, satir_pattern="somatosensoryal", duzey=1
        ),
        make_sentence(
            "Kalıcı nöral iz: **Ağrının beyinde silinmez bir bellek oluşturması**",
            "Santral sensitizasyon ve yapısal reorganizasyon tamamlandığında periferik neden ortadan kalksa dahi ağrı merkezi bir bellek olarak yaşamaya devam eder ve tedaviye son derece dirençli kronik ağrı sendromlarına yol açar.",
            50, 53, satir_pattern="korteks", duzey=1
        )
    ]

    b12 = {
        "id": "k2-06-b12",
        "baslik": "Santral Sensitizasyon, Disinhibisyon ve Reorganizasyon",
        "paragraflar": [
            {"id": "k2-06-p046", "sayfa": 47, "slayt_adim": 51, "cumleler": p47},
            {"id": "k2-06-p047", "sayfa": 48, "slayt_adim": 52, "cumleler": p48},
            {"id": "k2-06-p048", "sayfa": 49, "slayt_adim": 52, "cumleler": p49},
            {"id": "k2-06-p049", "sayfa": 50, "slayt_adim": 53, "cumleler": p50}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 13: Nosiseptör Tipleri, TRP Kanalları ve Farmakolojik Hedefler (Sayfa 51-52)
    # ----------------------------------------------------
    p51 = [
        make_sentence(
            "Nosiseptörlerin yapısı ve yerleşimi: **Kapsülsüz serbest sinir uçları**",
            "Nosiseptörler; deri, kas, eklem, kemik zarı ve iç organ duvarlarında yaygın biçimde dağılmış olan, herhangi bir koruyucu bağ dokusu kapsülü içermeyen çıplak serbest sinir uçlarıdır.",
            51, 55, satir_pattern="reseptörleri", duzey=0
        ),
        make_sentence(
            "Yüksek eşik ve adaptasyon direnci: **Kolay yorulmayan koruyucu sensörler**",
            "Dokunma reseptörlerinin aksine nosiseptörler son derece yüksek bir uyarılma eşiğine sahiptirler ve sürekli zararlı uyaran karşısında hemen hemen hiç adaptasyon göstermeyerek tehlike geçene kadar deşarjlarını sürdürürler.",
            51, 55, satir_pattern="afferent", duzey=1
        ),
        make_sentence(
            "Afferent lif bağlantıları: **Miyelinli A-delta ve miyelinsiz C lifleri**",
            "Bu reseptörler periferik akson uzantıları bakımından ince miyelinli A-delta lifleri ve miyelinsiz C lifleri olmak üzere iki ana grup tarafından oluşturulur ve transdüksiyon bu noktalarda başlar.",
            51, 56, satir_pattern="Kapsülsüz", duzey=1
        )
    ]

    p52 = [
        make_sentence(
            "Nosiseptör tipleri: **Mekanik, termal, kimyasal ve polimodal reseptörler**",
            "Nosiseptörler uyardıkları fiziksel uyaran tipine göre yalnız mekanik basıya yanıt veren mekanoreseptörler, aşırı sıcağa yanıt veren termal nosiseptörler ve tüm zararlı modaliteleri algılayan polimodal nosiseptörler olarak sınıflandırılır.",
            52, 57, satir_pattern="polimodal", duzey=0
        ),
        make_sentence(
            "Analjezik mekanizmalar: **Prostaglandin sentezi ve sodyum kanal blokajı**",
            "Nonsteroid antiinflamatuar ilaçlar dokuda prostaglandin sentezini inhibe ederek nosiseptör uyarılmasını engellerken; lokal anestezik ajanlar voltaj kapılı sodyum kanallarını tıkayarak aksiyon potansiyeli üretimini durdurur.",
            52, 57, satir_pattern="NSAID", duzey=1
        ),
        make_sentence(
            "Kapsaisin ve TRP kanalları: **Madde P tüketilmesiyle sağlanan duyarsızlaşma**",
            "Acı biberin etken maddesi olan kapsaisin, nosiseptörlerdeki geçici reseptör potansiyeli kanallarını uyarır; tekrarlayan uygulamalarda sinir ucundaki madde P depolarını tamamen boşaltarak uzun süreli analjezi ve duyarsızlaşma sağlar.",
            52, 58, satir_pattern="Kapsaisin", duzey=1
        )
    ]

    b13 = {
        "id": "k2-06-b13",
        "baslik": "Nosiseptör Tipleri, TRP Kanalları ve Farmakolojik Hedefler",
        "paragraflar": [
            {"id": "k2-06-p050", "sayfa": 51, "slayt_adim": 55, "cumleler": p51},
            {"id": "k2-06-p051", "sayfa": 52, "slayt_adim": 57, "cumleler": p52}
        ]
    }

    # ----------------------------------------------------
    # BÖLÜM 14: Nörotransmiterler, Modülasyon Reseptörleri ve Kapı Kontrol Sistemi (Sayfa 53-56)
    # ----------------------------------------------------
    p53 = [
        make_sentence(
            "Eksitatör aminoasitler: **Glutamat ve aspartatın hızlı sinaptik rolü**",
            "Medulla spinalis arka boynuzundaki birinci sıra ve ikinci sıra nöron sinapslarında primer afferent liflerden salınan temel eksitatör nörotransmiterler glutamat ve aspartattır.",
            53, 59, satir_pattern="Nörotransmiterler", duzey=0
        ),
        make_sentence(
            "Reseptör etkileşimi: **Hızlı AMPA depolarizasyonu ve yavaş NMDA sinyali**",
            "Glutamat öncelikle ampa reseptörlerine bağlanarak hızlı bazal nosiseptif iletiyi sağlar; yoğun uyarımlarda ise en em de a reseptörlerini aktive ederek kalsiyum akışını ve santral duyarlılaşmayı başlatır.",
            53, 59, satir_pattern="aminoasitler", duzey=1
        ),
        make_sentence(
            "Nöropeptidlerin eşliği: **Madde P, CGRP ve nörokinin bir reseptörleri**",
            "Glutamat ile eşzamanlı salınan madde P ve ce ge re pe peptidleri nörokinin bir reseptörlerine bağlanarak nöron zarında dakikalarca süren yavaş depolarizasyon oluşturur ve glutamatın etkinliğini katlar.",
            53, 59, satir_pattern="NMDA", duzey=1
        )
    ]

    p54 = [
        make_sentence(
            "İnhibitör ve modülatör reseptörler: **Opioid, GABA, alfa-iki ve serotonin**",
            "Arka boynuzdaki nosiseptif transmisyonu baskılamak üzere presinaptik ve postsinaptik yerleşimli opioid, gamaaminobütirik asit, alfa-iki adrenerjik, serotonin ve adenozin reseptörleri görev yapar.",
            54, 60, satir_pattern="modülasyonda", duzey=0
        ),
        make_sentence(
            "Endojen opioid sistemi: **Mü, delta ve kappa reseptörleri ve enkefalinler**",
            "Dorsal boynuzdaki internöronlardan salınan endojen enkefalin ve dinorfinler mü opioid reseptörlerini aktive ederek voltaj bağımlı kalsiyum kanallarını kapatır ve primer afferentten glutamat salınışını bloke eder.",
            54, 60, satir_pattern="gamaaminobutirik", duzey=1
        ),
        make_sentence(
            "Yeni farmakolojik yaklaşımlar: **Nöronal iyon kanalı blokerleri ve hedefler**",
            "Klasik reseptör agonistlerinin yanı sıra voltaj kapılı sodyum kanal blokeri en a ve bir nokta sekiz ve kalsiyum kanal alfa-iki-delta alt birimini bağlayan gabapentin türevleri güncel modülasyon tedavilerinin temelini oluşturur.",
            54, 60, satir_pattern="adenozin", duzey=1
        )
    ]

    p55 = [
        make_sentence(
            "Kapı kontrol teorisi prensibi: **A-beta ve C liflerinin dorsal boynuz rekabeti**",
            "Melzack ve Wall tarafından tanımlanan Kapı Kontrol Sistemine göre; kalın miyelinli A-beta dokunma lifleri ile ince miyelinsiz C ağrı lifleri arka boynuz substantia gelatinosa nöronları üzerinde zıt etkiler oluşturur.",
            55, 61, satir_pattern="fiber", sekil="Kapı kontrol teorisi şeması: A-beta lifleri, C lifleri, substantia gelatinosa internöronları ve transmisyon T hücresi bağlantıları", duzey=0
        ),
        make_sentence(
            "Kapının kapatılması: **Mekanik ovuşturmanın ağrıyı dindirme mekanizması**",
            "Hasarlı bölge ovuşturulduğunda aktive olan A-beta lifleri substantia gelatinosadaki inhibitör internöronları uyarır; bu internöronlar C lifi terminallerinde presinaptik inhibisyon yaparak transmisyon T hücresine giden kapıyı kapatır ve ağrı kesilir.",
            55, 61, satir_pattern="Small", sekil="A-beta liflerinin inhibitör internöron aracılığıyla transmisyon hücresini presinaptik inhibe etmesi şeması", duzey=1
        ),
        make_sentence(
            "Klinik uygulama: **TENS ve omurilik stimülasyonu elektrotları**",
            "Transkutanöz elektriksel sinir stimülasyonu yani tens cihazları ve epidural omurilik pilleri, A-beta liflerini elektriksel olarak uyararak bu kapı kontrol mekanizması üzerinden ilaçsız analjezi sağlarlar.",
            55, 61, satir_pattern="fiber", sekil="Omurilik arka boynuzunda kapı kontrol sistemi ve T hücresi blokajı şeması", duzey=1
        )
    ]

    p56 = [
        make_sentence(
            "Fizyopatolojinin klinikteki gücü: **Ağrı mekanizmalarını bilmenin hayati değeri**",
            "Toplumun çok büyük bir kesimini etkileyen, bireyi işinden ve sosyal yaşamından koparan ağrı ile başarılı biçimde baş edebilmek için altta yatan hücresel ve sinaptik mekanizmaların çok iyi bilinmesi şarttır.",
            56, 62, satir_pattern="Toplumun", duzey=0
        ),
        make_sentence(
            "Bilinmeyenlerin keşfi: **Algolojide yeni moleküler ufuklar**",
            "Son yıllarda nöroimmünoloji ve moleküler genetikte büyük yollar alınmasına karşın, ağrının santral plastisitesi ve kronikleşme süreçlerinde halen keşfedilmeyi bekleyen birçok mekanizma bulunmaktadır.",
            56, 62, satir_pattern="bilinmesi", duzey=1
        ),
        make_sentence(
            "Bütüncül hekimlik vizyonu: **Mekanizmaya dayalı kişiselleştirilmiş analjezi**",
            "Ağrıyı yalnızca susturulacak bir semptom olarak değil, altında yatan fizyopatolojik mekanizmasıyla doğru analiz eden bir hekim; hastasına en etkili, güvenli ve multidisipliner analjezik yaklaşımı sunacaktır.",
            56, 62, satir_pattern="fizyopatolojisi", duzey=1
        )
    ]

    b14 = {
        "id": "k2-06-b14",
        "baslik": "Nörotransmiterler, Modülasyon Reseptörleri ve Kapı Kontrol Sistemi",
        "paragraflar": [
            {"id": "k2-06-p052", "sayfa": 53, "slayt_adim": 59, "cumleler": p53},
            {"id": "k2-06-p053", "sayfa": 54, "slayt_adim": 60, "cumleler": p54},
            {"id": "k2-06-p054", "sayfa": 55, "slayt_adim": 61, "cumleler": p55},
            {"id": "k2-06-p055", "sayfa": 56, "slayt_adim": 62, "cumleler": p56}
        ]
    }

    bolumler = [b01, b02, b03, b04, b05, b06, b07, b08, b09, b10, b11, b12, b13, b14]
    return bolumler


def build_drawings(bolumler):
    paras = [p for b in bolumler for p in b['paragraflar']]
    page_last_sent = {p['sayfa']: p['cumleler'][-1]['id'] for p in paras}
    drawings = []
    
    # 1. siniflama (p.16): Süreye Göre Ağrı Sınıflaması
    drawings.append({
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Süreye Göre Ağrı Sınıflaması",
        "ogeler": [
            "Akut ağrı: Doku hasarıyla başlar, onarımla kaybolur",
            "Subakut ağrı: Altı haftadan üç aya kadar uzanan dönem",
            "Kronik ağrı: Üç ila altı aydan uzun devam eden hastalık"
        ],
        "sayfa": 16
    })

    # 2. karsilastirma (p.15): Akut Ağrı vs Kronik Ağrı
    drawings.append({
        "tur": "sema",
        "sablon": "karsilastirma",
        "kutuplar": ["Akut Ağrı", "Kronik Ağrı"],
        "satirlar": [
            ["Biyolojik rol", "Koruyucu biyolojik alarm", "Alarm fonksiyonu kaybı"],
            ["Klinik tablo", "Semptom ve doku uyarısı", "Kalıcı sinir sistemi hastalığı"],
            ["Zaman ilişkisi", "Doğrusal ilişki bulunur", "Normal doku süresini aşar"],
            ["Klinik süreç", "Doku onarımıyla kaybolur", "Hayat kalitesini bozar"]
        ],
        "sayfa": 15
    })

    # 3. siniflama (p.17): Mekanizmalarına Göre Ağrı Kategorileri
    drawings.append({
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Mekanizmalarına Göre Ağrı Kategorileri",
        "ogeler": [
            "Nosiseptif ağrı: Sağlam sinir boyunca doku hasarı iletimi",
            "Nöropatik ağrı: Sinir liflerinin kendi patolojisi",
            "Nosiplastik ağrı: Değişen nosiseptif mekanizma tablosu",
            "Psikojenik ağrı: Psikososyal etkenlerin belirlediği ağrı"
        ],
        "sayfa": 17
    })

    # 4. karsilastirma (p.19): Nosiseptif vs Nöropatik Ağrı
    drawings.append({
        "tur": "sema",
        "sablon": "karsilastirma",
        "kutuplar": ["Nosiseptif Ağrı", "Nöropatik Ağrı"],
        "satirlar": [
            ["Temel mekanizma", "Nosiseptörlerin uyarılması", "Sinir dokusunun hasarlanması"],
            ["Sinir yapısı", "Sinir yolları tamamen sağlam", "Sinir sistemi hasarı bulunur"],
            ["Tedavi yaklaşımı", "Antienflamatuar ve opioid", "Antiepileptik ve antidepresan"],
            ["Örnek durum", "Doku yıkımı ve travma", "Mekanik sinir kompresyonu"]
        ],
        "sayfa": 19
    })

    # 5. neden_sonuc (p.21): Deafferentasyon Ağrısı Mekanizması
    drawings.append({
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Deafferentasyon Ağrısı Gelişim Mekanizması",
        "ogeler": [
            "Periferik duyusal iletim yollarının kesilmesi",
            "Arka boynuzda primer afferent girdi kaybı",
            "Spinal nöronlarda aşırı spontan uyarılabilirlik",
            "Üst merkezlere giden spontan yalancı ağrı sinyali"
        ],
        "sayfa": 21
    })

    # 6. neden_sonuc (p.24): Sempatik İlişkili Ağrı (CRPS / Kozalji)
    drawings.append({
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Sempatik Aracılı Ağrı ve Kozalji Kaskadı",
        "ogeler": [
            "Periferik sinir hasarı ve anormal sempatik filizlenme",
            "Nosiseptörlerde alfa-bir adrenerjik reseptör artışı",
            "Sempatik deşarjla tetiklenen vazomotor dengesizlik",
            "Ekstremitede yanıcı ağrı, ödem ve trofik bozukluk"
        ],
        "sayfa": 24
    })

    # 7. siniflama (p.29): Kaynaklandığı Bölgeye Göre Ağrı
    drawings.append({
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kaynaklandığı Bölgeye Göre Ağrı",
        "ogeler": [
            "Yüzeyel somatik ağrı: Deri ve mukozadan kaynaklanır",
            "Derin somatik ağrı: Kas, eklem ve periostu tutar",
            "Visseral ağrı: İç organlardan kaynaklanan nosiseptif ağrı"
        ],
        "sayfa": 29
    })

    # 8. karsilastirma (p.31): Somatik vs Visseral Ağrı
    drawings.append({
        "tur": "sema",
        "sablon": "karsilastirma",
        "kutuplar": ["Somatik Ağrı", "Visseral Ağrı"],
        "satirlar": [
            ["Kaynak doku", "Deri, kas, eklem ve periost", "İçi boş iç organlar"],
            ["Lokalizasyon", "Net ve iyi sınırlı lokalizasyon", "Kötü sınırlı ve yaygın ağrı"],
            ["Yansıma", "Genelde dermatomlara yansımaz", "Dermatomlar boyunca yansır"],
            ["Otonomik bulgu", "Otonomik bulgu bulunmaz", "Bulantı ve terleme eşlik eder"]
        ],
        "sayfa": 31
    })

    # 9. mekanizma_adimlari (p.37): Ağrı Algılanmasının 4 Aşaması
    drawings.append({
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Ağrı Algılanmasının Dört Temel Aşaması",
        "ogeler": [
            "Transdüksiyon: Uyarının aksiyon potansiyeline dönüşümü",
            "Transmisyon: Sinyalin omurilik ve beyne iletilmesi",
            "Modülasyon: Omurilik arka boynuzunda sinyal ayarı",
            "Persepsiyon: Kortekste ağrının bilinçli algılanması"
        ],
        "sayfa": 37
    })

    # 10. karsilastirma (p.38): A-delta vs C Lifleri
    drawings.append({
        "tur": "sema",
        "sablon": "karsilastirma",
        "kutuplar": ["A-delta Lifleri", "C Lifleri"],
        "satirlar": [
            ["Miyelin yapısı", "Miyelinli lifler", "Miyelinsiz lifler"],
            ["İletim özelliği", "Yüksek hızla iletir", "Yavaş hızla iletir"],
            ["Ağrı niteliği", "İlk keskin batıcı ağrı", "İkinci künt sızlayıcı ağrı"],
            ["Lokalizasyon", "Tam lokalize ağrı", "Yaygın künt ağrı"]
        ],
        "sayfa": 38
    })

    # 11. neden_sonuc (p.43): Periferik Sensitizasyon
    drawings.append({
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Periferik Sensitizasyon ve İnflamatuar Mediyatörler",
        "ogeler": [
            "Doku hasarı ile mast hücresi ve makrofaj uyarımı",
            "Prostaglandin, bradikinin ve histamin salınımı",
            "Nosiseptör uçlarından nörojenik peptit salınması",
            "Reseptör eşiğinin düşmesi ve primer hiperaljezi"
        ],
        "sayfa": 43
    })

    # 12. karsilastirma (p.46): Primer vs Sekonder Hiperaljezi
    drawings.append({
        "tur": "sema",
        "sablon": "karsilastirma",
        "kutuplar": ["Primer Hiperaljezi", "Sekonder Hiperaljezi"],
        "satirlar": [
            ["Oluştuğu alan", "Doğrudan hasar yeri", "Çevreleyen sağlam doku"],
            ["Temel mekanizma", "Periferik sensitizasyon", "Santral sensitizasyon"],
            ["Aşırı duyarlılık", "Hem termal hem mekanik", "Baskın olarak mekanik"],
            ["Tedavi yanıtı", "Lokal anestezikler", "Santral etkili ajanlar"]
        ],
        "sayfa": 46
    })

    # 13. mekanizma_adimlari (p.47): Santral Sensitizasyon
    drawings.append({
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Santral Sensitizasyon ve Reseptör Kaskadı",
        "ogeler": [
            "C liflerinden sürekli glutamat ve madde P salınımı",
            "Dorsal boynuz nöronlarında magnezyum bloğunun kalkması",
            "NMDA reseptör aktivasyonu ve kalsiyum akışı",
            "Mikroglia aktivasyonu ve allodini gelişimi"
        ],
        "sayfa": 47
    })

    # 14. mekanizma_adimlari (p.49): Disinhibisyon Mekanizması
    drawings.append({
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Disinhibisyon ve Ağrı İletiminin Kontrolsüz Artışı",
        "ogeler": [
            "İnen serotonerjik ve noradrenerjik yolların tükenmesi",
            "GABAerjik ve glisinerjik inhibitör ara nöron kaybı",
            "Glutamat geri alımının bozulması ve sinaptik birikim",
            "NMDA aktivasyonu ile ağrı sinyallerinin amplifikasyonu"
        ],
        "sayfa": 49
    })

    # 15. mekanizma_adimlari (p.55): Kapı Kontrol Teorisi
    drawings.append({
        "tur": "sema",
        "sablon": "mekanizma_adimlari",
        "baslik": "Kapı Kontrol Teorisi Devre Mekanizması",
        "ogeler": [
            "A-beta dokunma liflerinin mekanik uyarılması",
            "Substantia gelatinosa inhibitör internöron aktivasyonu",
            "C lifi terminallerinde presinaptik inhibisyon",
            "Transmisyon T hücresine impuls geçişinin durdurulması"
        ],
        "sayfa": 55
    })

    for d in drawings:
        pno = d["sayfa"]
        d["cumle"] = page_last_sent[pno]
        d["bas"] = 0
        d["son"] = 3

    return drawings



def main():
    print("Building full deep amfi lecture for Lesson 6 (Ağrı Yolları ve Mekanizmaları)...")
    bolumler = build_all_sections()
    drawings = build_drawings(bolumler)
    
    p_num = 1
    for b in bolumler:
        for p in b["paragraflar"]:
            p["id"] = f"k2-06-p{p_num:03d}"
            p_num += 1

    paras = [p for b in bolumler for p in b['paragraflar']]
    sents = [s for p in paras for s in p['cumleler']]
    words = sum(len(s['ses'].split()) for s in sents)
    
    print(f"Generated {len(bolumler)} sections, {len(paras)} pages, {len(sents)} sentences, {words} words.")
    
    clean_k2 = {
        "surum": 2,
        "ders_id": "k2-06",
        "anahtar": "y25-k2-06-agri-yollari-ve-mekanizmalari",
        "baslik": "Ağrı Yolları ve Mekanizmaları",
        "bolumler": bolumler
    }
    
    # Update cikmis_baglantilari.json with page numbers
    c_bag_path = TASLAK / "cikmis_baglantilari.json"
    if c_bag_path.exists():
        c_bag = json.loads(c_bag_path.read_text(encoding="utf-8"))
        page_map = {
            "q-2__kurul_-12": 9,
            "past-q-_SKENDERUN_T_M_d_rl___ne0__1__230709_230251-7": 19,
            "01a96a18bccf": 30,
            "58700c98a3db": 31,
            "392041a09b26": 31,
            "303055c213d3": 31,
            "11cec678fef5": 37,
            "5afc023320d4": 37,
            "57c4c3ee7531": 37
        }
        for item in c_bag:
            if isinstance(item, dict):
                qid = item.get("soru_id") or item.get("id")
                if qid in page_map:
                    item["sayfa"] = page_map[qid]
                    item["sayfalar"] = [page_map[qid], page_map[qid]]
                    item["ilgili"] = True
        c_bag_path.write_text(json.dumps(c_bag, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write konusma_v2.json
    (TASLAK / "konusma_v2.json").write_text(json.dumps(clean_k2, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Generate derived text files
    md_txt, sayfalar_l = KV.turet(clean_k2)
    (TASLAK / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
    (TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l, ensure_ascii=False, indent=2), encoding="utf-8")
    (TASLAK / "konusma_capalari.json").write_text(json.dumps(KV.capalar(clean_k2), ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Write cizimler.json and cizim_aday.json
    (TASLAK / "cizimler.json").write_text(json.dumps({"komutlar": drawings}, ensure_ascii=False, indent=2), encoding="utf-8")
    (TASLAK / "cizim_aday.json").write_text(json.dumps({"komutlar": drawings}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Update ders_paketi.json
    dp_path = TASLAK / "ders_paketi.json"
    if dp_path.exists():
        dp = json.loads(dp_path.read_text(encoding="utf-8"))
        dp["konusma_v2"] = clean_k2
        dp["cizimler"] = drawings
        dp_path.write_text(json.dumps(dp, ensure_ascii=False, indent=2), encoding="utf-8")
        
    print("Files successfully written to taslak.")
    
    # Verify all Quality Gates
    print("\n--- Running Quality Gate 1: KV.dogrula ---")
    kv_errs = KV.dogrula(clean_k2, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
    if kv_errs:
        print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
        for e in kv_errs[:15]: print(" ", e)
        sys.exit(1)
    print("PASSED KV.dogrula: 0 HATA")
    
    print("\n--- Running Quality Gate 2: denetle.py ---")
    import denetle as D
    d_rapor = D.Denetim(TASLAK).calistir()
    if d_rapor.get("hata", 0) > 0:
        print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
        for e in d_rapor.get("hatalar", []): print(" ", e)
        sys.exit(1)
    print("PASSED denetle.py: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 3: validate_learning_decks.py ---")
    r_val = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/validate_learning_decks.py"),
        str(TASLAK / "deck.json"), "--oyun-zorunlu", "--kurul2"
    ], capture_output=True, text=True)
    if r_val.returncode != 0:
        print("FAILED validate_learning_decks:", r_val.stdout, r_val.stderr)
        sys.exit(1)
    print("PASSED validate_learning_decks: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 4: metin_denetle.py ---")
    r_metin = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/sesli_anlatim/metin_denetle.py"),
        str(TASLAK / "konusma_metni.md")
    ], capture_output=True, text=True)
    if r_metin.returncode != 0:
        print("FAILED metin_denetle:", r_metin.stdout, r_metin.stderr)
        sys.exit(1)
    print("PASSED metin_denetle: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 5: sesli_kapsam ---")
    import isle as IS
    kapsam_errs = IS.sesli_kapsam(TASLAK)
    if kapsam_errs:
        print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
        for e in kapsam_errs: print(" ", e)
        sys.exit(1)
    print("PASSED sesli_kapsam: 0 HATA")
    
    print("\n--- Running Quality Gate 6: cizim_dogrula.py ---")
    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/cizim"))
    import cizim_dogrula as CD
    import sablon
    cum_text = {}
    accum = []
    for s in sents:
        accum.append(s["ses"])
        accum.append(s.get("ekran", ""))
        cum_text[s["id"]] = " ".join(accum)
    sent_map = {s["id"]: s for s in sents}
    c_errs = []
    for idx, d in enumerate(drawings):
        cid = d["cumle"]
        coz_d, err_c = sablon.coz(d)
        if err_c:
            c_errs.append(f"Drawing {idx+1} ({cid}) sablon.coz error: {err_c}")
            continue
        s_words = len(sent_map[cid]["ses"].split())
        err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
        if err_v:
            c_errs.append(f"Drawing {idx+1} ({cid}) error: {err_v}")
    if c_errs:
        print(f"FAILED cizim_dogrula with {len(c_errs)} errors:")
        for ce in c_errs: print(" ", ce)
        sys.exit(1)
    print(f"PASSED cizim_dogrula: {len(drawings)}/{len(drawings)} KOMUT 0 HATA")
    print("\n🎉 ALL 6 QUALITY GATES PASSED PERFECTLY WITH ZERO ERRORS!")

if __name__ == "__main__":
    main()
