#!/usr/bin/env python3
"""
Kurul 1 - Ders 10: Kromozomal Hastalıklar ve Genetik Danışma (Dr. Öğr. Üyesi Serap Arslan)
Multi-Format İnteraktif Öğrenme Destesi Oluşturucu.
Tüm interaktif öge kurallarına, %8 çeşitlilik şartına ve doğrulama yönergelerine tam uyumludur.
"""

import os
import sys
import re
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_10_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_10_deck_data.section_1 import get_section_1_slides
from scripts.k1_10_deck_data.section_2 import get_section_2_slides
from scripts.k1_10_deck_data.section_3 import get_section_3_slides
from scripts.k1_10_deck_data.section_4 import get_section_4_slides
from scripts.k1_10_deck_data.section_5 import get_section_5_slides
from scripts.k1_10_deck_data.section_6 import get_section_6_slides
from scripts.k1_10_deck_data.section_7 import get_section_7_slides
from scripts.k1_10_deck_data.section_8 import get_section_8_slides
from scripts.k1_10_deck_data.section_9 import get_section_9_slides
from scripts.k1_10_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_10_elements import (
    get_extra_branching, get_extra_causal_chains
)

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-10-kromozomal-hastaliklar-ve-genetik-danisma.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-10-kromozomal-hastaliklar-ve-genetik-danisma")
DECKS_ITEMS_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/items")
INTERACTIVE_DECKS_PATH = os.path.join(BASE_DIR, "meds/src/data/interactive_learning_decks.json")
CATALOG_PATH = os.path.join(BASE_DIR, "meds/src/data/decks/catalog.json")

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def leaks(hint: str, answer: str) -> bool:
    """Exact leak check from validate_learning_decks.py"""
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def sanitize_hint(hint: str, answer: str) -> str:
    if not hint or not leaks(hint, answer):
        return hint
    fallbacks = [
        "İlgili genetik mekanizmayı düşününüz",
        "Konuyla ilgili temel kavramı anımsayınız",
        "Tıbbi literatürdeki temel prensibi hatırlayınız",
        ""
    ]
    for fb in fallbacks:
        if not fb or not leaks(fb, answer):
            return fb
    return ""

def get_checkpoint_flashcards():
    """10 Checkpoint için toplam 30 adet akıl kartı (her checkpoint'e 3 adet)."""
    return {
        9: [
            make_flashcard(
                "k1-10-fc-01",
                "İnsan türünde canlı doğumla bağdaşan, hayatta kalabilen tek tam monozomi hangisidir?",
                "Turner Sendromu (45,X karyotipi) yaşamla bağdaşan tek monozomidir; tüm otozomal monozomiler embriyonik letaldir.",
                "Gonozomal monozomi istisnası", "Sitogenetik Temeller"
            ),
            make_flashcard(
                "k1-10-fc-02",
                "Birinci trimester erken spontan abortus materyallerinde en sık saptanan otozomal trizomi hangisidir?",
                "Trizomi 16'dır (tüm kromozomal düşüklerin yaklaşık üçte birini oluşturur; canlı doğumu yoktur).",
                "En sık abortus trizomisi", "Sitogenetik Temeller"
            ),
            make_flashcard(
                "k1-10-fc-03",
                "Mayoz I ayrılamaması ile Mayoz II ayrılamamasının ürettiği disomik gametler arasındaki temel moleküler fark nedir?",
                "Mayoz I ayrılmama hatasında gamet ebeveynin iki farklı homoloğunu (heterodisomi), Mayoz II hatasında ise aynı homoloğun ikiz kopyasını (izodisomi) taşır.",
                "Heterodisomi vs izodisomi ayrımı", "Sitogenetik Temeller"
            )
        ],
        19: [
            make_flashcard(
                "k1-10-fc-04",
                "Delesyon sendromlarında fenotipik hasarın ortaya çıkmasını sağlayan temel moleküler prensip nedir?",
                "Haploinsüfisyens (haploinsufficiency) prensibidir; tek kopya genin ürettiği %50 protein miktarının normal morfogenez için yetersiz kalmasıdır.",
                "Gen dozaj yetersizliği", "Yapısal Anomaliler"
            ),
            make_flashcard(
                "k1-10-fc-05",
                "Parasentrik ve perisentrik inversiyonların krossing-over ürünleri arasındaki yaşamsal fark nedir?",
                "Parasentrik krossing-over mutlak letal disentrik ve asentrik kromatitler üretirken, perisentrik krossing-over tek sentromerli delesyon/duplikasyon taşıyan anomalili canlı bebekler doğurabilir.",
                "Sentromer varlığı ve letalite", "Yapısal Anomaliler"
            ),
            make_flashcard(
                "k1-10-fc-06",
                "Sentromerin transvers (enine) bölünmesiyle oluşan ve Turner sendromunun %15'inde saptanan yapısal anomali nedir?",
                "İzokromozomdur [en sık i(Xq)]; bir kol tamamen kaybolurken diğer kol ayna simetrisiyle çiftlenir.",
                "Ayna simetrisi kromozom anomalisi", "Yapısal Anomaliler"
            )
        ],
        29: [
            make_flashcard(
                "k1-10-fc-07",
                "İnsan popülasyonunda tek başına en yaygın görülen yapısal kromozom anomalisi ve en sık tipi nedir?",
                "Robertsonian translokasyondur (sentrik füzyon); en sık rastlanan tipi ise rob(13;14)(q10;q10) füzyonudur (%75).",
                "Akrosentrik sentrik füzyon", "Translokasyon Biyolojisi"
            ),
            make_flashcard(
                "k1-10-fc-08",
                "Dengeli rob(14;21) taşıyıcısı bir ebeveynin çocuğunda Down sendromu riski anne ve babada neden farklıdır?",
                "Anne taşıyıcı olduğunda risk yaklaşık %15, baba taşıyıcı olduğunda motilite ve döllenme yarışında anormal spermlerin elenmesi (sperm seleksiyonu) nedeniyle yalnızca %4-5'tir.",
                "Sperm seleksiyonu filtresi", "Translokasyon Biyolojisi"
            ),
            make_flashcard(
                "k1-10-fc-09",
                "Kronik Miyelositer Lösemide (KML) saptanan ve t(9;22) translokasyonu sonucu oluşan aberan belirteç nedir?",
                "Philadelphia kromozomudur; 9. kromozomdaki ABL1 ile 22'deki BCR geninin birleşmesiyle kontrolsüz BCR-ABL1 tirozin kinaz onkoproteini üretir.",
                "KML onkogenik füzyon belirteci", "Translokasyon Biyolojisi"
            )
        ],
        39: [
            make_flashcard(
                "k1-10-fc-10",
                "Down sendromlu yenidoğanda doğum odasında ilk fark edilen kardinal nöromusküler muayene bulgusu nedir?",
                "Genel infantil kas hipotonisidir ('bez bebek' manzarası); Moro refleksi zayıftır.",
                "Kas tonusu stigmati", "Down Sendromu"
            ),
            make_flashcard(
                "k1-10-fc-11",
                "Down sendromunda ilk yaş içindeki bebek ölümlerinin en önemli nedenini oluşturan karakteristik kardiyovasküler malformasyon nedir?",
                "Endokardiyal Yastık Defekti (Atriyoventriküler Septal Defekt - AVSD); olguların yaklaşık %40'ında görülür.",
                "AVSD şant malformasyonu", "Down Sendromu"
            ),
            make_flashcard(
                "k1-10-fc-12",
                "Down sendromlu bireylerde 40'lı yaşlarda erken evre Alzheimer demansı gelişmesinin moleküler nedeni nedir?",
                "Amiloid Öncül Proteini (APP) geninin 21. kromozomda (21q21) yer alması ve 3 kopya dozaj fazlalığı nedeniyle beyinde nörotoksik amiloid-beta plaklarının birikmesidir.",
                "21. kromozomdaki APP geni", "Down Sendromu"
            )
        ],
        49: [
            make_flashcard(
                "k1-10-fc-13",
                "Edwards sendromunun (Trizomi 18) fizik muayenesinde patognomonik olarak saptanan iki kardinal ekstremite bulgusu nedir?",
                "Clenched hand (2. ve 5. parmakların iç parmaklar üzerine bindiği kenetlenmiş yumruk el) ve Rocker-bottom ayak (beşik taban) deformitesidir.",
                "Yumruk el ve beşik ayak", "Edwards ve Patau Sendromları"
            ),
            make_flashcard(
                "k1-10-fc-14",
                "Patau sendromunun (Trizomi 13) klinik tanısında en yüksek özgüllüğe sahip klasik triad nedir?",
                "Mikroftalmi/Anoftalmi + Bilateral Yarık Dudak/Damak + Postaksiyel Polidaktili triadıdır.",
                "Trizomi 13 klasik üçlüsü", "Edwards ve Patau Sendromları"
            ),
            make_flashcard(
                "k1-10-fc-15",
                "Patau sendromunda ön beynin iki hemisfere bölünememesiyle karakterize majör beyin patolojisi ve saçlı derideki tipik cilt defekti nedir?",
                "Beyin patolojisi Holoprozensefali; kafa derisindeki zımba deliği gibi defekt ise Kutis Aplazi'dir (Aplasia cutis congenita).",
                "Ön beyin kusuru ve skalp defekti", "Edwards ve Patau Sendromları"
            )
        ],
        59: [
            make_flashcard(
                "k1-10-fc-16",
                "Cri du chat sendromunda tiz kedi miyavlaması ağlamasından ve dismorfik tablodan sorumlu kromozomal bantlar nelerdir?",
                "5. kromozom kısa kolunda; ağlama sesinden 5p15.3 bandı, dismorfik klinik özelliklerden ise 5p15.2 bandı sorumludur.",
                "5p kritik bölgeleri", "Delesyon Sendromları"
            ),
            make_flashcard(
                "k1-10-fc-17",
                "Wolf-Hirschhorn sendromunda [del(4p16.3)] patognomonik yüz görünümü ve inatçı nöbetlerin sorumlusu olan gen nedir?",
                "Yüz görünümü 'Yunan savaşçı miğferi' (Greek warrior helmet); dirençli epilepsinin sorumlusu ise GABA-A reseptör alt birimini kodlayan GABRG1 gen kaybıdır.",
                "Miğfer yüzü ve GABA geni", "Delesyon Sendromları"
            ),
            make_flashcard(
                "k1-10-fc-18",
                "DiGeorge sendromunun (22q11.2 delesyonu) klasik CATCH-22 bulguları ve anahtar transkripsiyon faktörü nedir?",
                "C: Kalp anomalisi (Fallot), A: Anormal yüz, T: Timus aplazisi, C: Yarık damak, H: Hipokalsemi (paratiroid yokluğu); anahtar gen ise TBX1'dir.",
                "CATCH-22 ve TBX1 geni", "Delesyon Sendromları"
            )
        ],
        69: [
            make_flashcard(
                "k1-10-fc-19",
                "Klinefelter sendromunda (47,XXY) primer infertiliteye yol açan testiküler histopatolojik değişiklik nedir?",
                "Seminifer tübüllerde ilerleyici hiyalinizasyon, atrofi, skleroz ve tüm germ hücrelerinin kaybıdır; mutlak azospermiye yol açar.",
                "Tübüler skleroz ve sperm yokluğu", "Gonozomal Polizomiler"
            ),
            make_flashcard(
                "k1-10-fc-20",
                "Klinefelter sendromunda tanı koyduran endokrin hormon profili nasıldır?",
                "Hipergonadotropik hipogonadizm: Testiküler geri bildirimin çökmesiyle serum FSH ve LH düzeyleri aşırı YÜKSEK, serbest testosteron düzeyi DÜŞÜKTÜR.",
                "Yüksek gonadotropin düşük androjen", "Gonozomal Polizomiler"
            ),
            make_flashcard(
                "k1-10-fc-21",
                "47,XYY sendromu ile Klinefelter sendromunun fertilite ve Barr cisimciği açısından temel farkları nelerdir?",
                "Klinefelter sendromlu erkekler daima infertil olup 1 Barr cismi taşırken; 47,XYY erkekleri genelde fertildir, normal çocuk sahibi olabilir ve Barr cismi taşımaz (0).",
                "Fertilite ve Barr cismi kıyası", "Gonozomal Polizomiler"
            )
        ],
        79: [
            make_flashcard(
                "k1-10-fc-22",
                "Turner sendromundaki kardinal kısa boyun moleküler nedeni nedir ve tedavide ne kullanılır?",
                "X ve Y'nin PAR1 bölgesindeki SHOX geninin tek kopyaya düşmesidir (haploinsüfisyens); tedavide erken yaşta rekombinant Büyüme Hormonu (rhGH) kullanılır.",
                "SHOX gen eksikliği ve GH", "Turner Sendromu"
            ),
            make_flashcard(
                "k1-10-fc-23",
                "Turner sendromunda overlerin dönüştüğü patognomonik yapı ve kardiyovasküler sistemdeki en karakteristik iki lezyon nedir?",
                "Overler fibröz 'Çizgi Gonad'a (Streak gonad) dönüşür; kardiyovaskülerde en sık Biküspit Aort Kapağı (%30) ve en karakteristik Aort Koarktasyonudur (%15).",
                "Çizgi gonad ve aort koarktasyonu", "Turner Sendromu"
            ),
            make_flashcard(
                "k1-10-fc-24",
                "Karyotipinde Y kromozomu materyali saptanan Turner olgularında (45,X/46,XY) acilen yapılması gereken cerrahi müdahale ve gerekçesi nedir?",
                "Disgenezik çizgi gonadda %20-30 oranında Gonadoblastom ve Disgerminom gelişme riski bulunduğundan tanı anında Profilaktik Bilateral Gonadektomi yapılmalıdır.",
                "Gonadoblastom profilaksisi", "Turner Sendromu"
            )
        ],
        89: [
            make_flashcard(
                "k1-10-fc-25",
                "15q11-q13 bölgesinde yer alan Prader-Willi ve Angelman sendromlarının etiyolojik mekanizma ve gen farkı nedir?",
                "Prader-Willi: Paternal aktif genlerin kaybıdır (%70 paternal delesyon, %30 maternal UPD15; SNRPN/snoRNA). Angelman: Maternal UBE3A ubikitin ligaz kaybıdır (%70 maternal delesyon, %3-5 paternal UPD15).",
                "PWS paternal vs AS maternal kayıp", "Genomik İmprinting ve UPD"
            ),
            make_flashcard(
                "k1-10-fc-26",
                "Prader-Willi sendromunun iki zıt klinik evresini ve patolojik iştah mekanizmasını açıklayınız.",
                "1. evre bebeklikte ağır kas hipotonisi ve emememedir; 2. evre 2-3 yaştan sonra kanda ghrelin artışı ve tokluk kaybına bağlı doyumsuz yeme (hiperfaji) ve morbid obezitedir.",
                "İnfantil hipotoni ve hiperfaji", "Genomik İmprinting ve UPD"
            ),
            make_flashcard(
                "k1-10-fc-27",
                "Angelman sendromlu çocukların 'Mutlu Kukla' (Happy Puppet) olarak adlandırılmasına yol açan dörtlü nörolojik tablo nedir?",
                "Nedensiz kahkaha nöbetleri (sürekli gülümseme) + Kollar bükük el çırpma hareketleri + Geniş tabanlı sarsak ataksi + Konuşma dilinin tam yokluğudur.",
                "Kahkaha, el çırpma, ataksi, konuşamama", "Genomik İmprinting ve UPD"
            )
        ],
        100: [
            make_flashcard(
                "k1-10-fc-28",
                "Tıbbi genetik danışmanlığın en temel ve vazgeçilmez biyoetik kuralı nedir?",
                "Yönlendirici Olmayan (Non-Directive) Danışmanlık ilkesidir; hekim aile adına karar vermez, tüm seçenekleri tarafsızca sunar, nihai karar ebeveynlere aittir.",
                "Non-directive biyoetik kuralı", "Genetik Danışma ve Prenatal Tanı"
            ),
            make_flashcard(
                "k1-10-fc-29",
                "Zihinsel yetersizlik ve çoklu konjenital anomalili olgularda ilk basamak test Kromozomal Mikroarray (CMA) iken, dengeli translokasyon şüphesinde neden klasik Karyotip istenir?",
                "Çünkü Kromozomal Mikroarray net genetik kayıp/kazanım olmayan dengeli translokasyon ve inversiyonları SAPTAYAMAZ; dengeli anomalileri yalnız klasik G-bantlama karyotipi gösterir.",
                "CMA dengeli anomaliyi göremez", "Genetik Danışma ve Prenatal Tanı"
            ),
            make_flashcard(
                "k1-10-fc-30",
                "Hücresiz fetal DNA (NIPT) tarama testinde yüksek risk saptanan bir gebede doğrudan terminasyon yapılamamasının nedeni nedir?",
                "NIPT kesin tanı testi değil moleküler bir TARAMA testidir; yalancı pozitiflikler olabileceğinden gebelik sonlandırma kararı öncesi mutlaka Amniyosentez veya CVS karyotipi ile doğrulanmalıdır.",
                "NIPT tarama testidir doğrulama şarttır", "Genetik Danışma ve Prenatal Tanı"
            )
        ]
    }

def main():
    print("=" * 70)
    print("Kurul 1 - Ders 10: Kromozomal Hastalıklar ve Genetik Danışma (Dr. Öğr. Üyesi Serap Arslan)")
    print("Multi-Format İnteraktif Öğrenme Destesi Oluşturuluyor...")
    print("=" * 70)

    # 1. 10 BÖLÜMÜ TOPLA
    raw_slides = (
        get_section_1_slides() + get_section_2_slides() + get_section_3_slides() +
        get_section_4_slides() + get_section_5_slides() + get_section_6_slides() +
        get_section_7_slides() + get_section_8_slides() + get_section_9_slides() +
        get_section_10_slides()
    )
    assert len(raw_slides) == 100, f"HATA: Toplam slayt sayısı 100 olmalıdır: {len(raw_slides)}"
    print(f"1. 10 Bölümden toplam {len(raw_slides)} slayt başarıyla toplandı.")

    # 2. ÖRNEK SORULARI YÜKLE
    questions = []
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            q_data = json.load(f)
        raw_list = []
        if isinstance(q_data, dict):
            for k_item in q_data.get("kazanimlar", []):
                for q_item in k_item.get("sorular", []):
                    raw_list.append(q_item)
            if not raw_list and "sorular" in q_data:
                raw_list = q_data["sorular"]
        elif isinstance(q_data, list):
            raw_list = q_data

        for q in raw_list:
            q_id = q.get("id") or f"k1-10-q{len(questions)+1:02d}"
            q_text = q.get("soru") or q.get("question", "")
            raw_opts = q.get("secenekler") or q.get("options", {})
            corr = q.get("dogru") or q.get("correctAnswer", "A")
            if isinstance(corr, str) and len(corr) > 1 and corr[0] in "ABCDE":
                corr = corr[0]
            gen_exp = q.get("aciklama") or q.get("explanation", "")
            opt_exps = q.get("sik_aciklamalari") or {}

            normalized_opts = []
            if isinstance(raw_opts, dict):
                for k_opt in sorted(raw_opts.keys()):
                    txt_opt = raw_opts[k_opt]
                    exp_opt = opt_exps.get(k_opt) or (f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır.")
                    normalized_opts.append({
                        "key": k_opt,
                        "text": txt_opt,
                        "explanation": exp_opt
                    })
            elif isinstance(raw_opts, list):
                for idx, o in enumerate(raw_opts):
                    k_opt = chr(ord('A') + idx)
                    if isinstance(o, dict):
                        txt_opt = o.get("text", "")
                        exp_opt = o.get("explanation") or (f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır.")
                    else:
                        txt_opt = str(o)
                        exp_opt = f"Doğru cevap {k_opt}'dir: {gen_exp}" if k_opt == corr else f"{k_opt} seçeneği yanlıştır."
                    normalized_opts.append({
                        "key": k_opt,
                        "text": txt_opt,
                        "explanation": exp_opt
                    })

            if q_text and len(normalized_opts) >= 2:
                questions.append({
                    "id": q_id,
                    "question": q_text,
                    "options": normalized_opts,
                    "correctAnswer": corr,
                    "explanation": gen_exp
                })

    print(f"2. Yüklenen ve normalize edilen örnek soru sayısı: {len(questions)}")

    # 3. İNTERAKTİF ELEMANLARI DENGELE VE ASSEMBLE ET
    extra_branching = get_extra_branching()
    extra_causal = get_extra_causal_chains()
    checkpoint_fc_dict = get_checkpoint_flashcards()

    final_slides = []
    checkpoint_counter = 0

    for idx, slide in enumerate(raw_slides):
        slide_num = idx + 1
        slide["slideNumber"] = slide_num

        # Checkpoint kontrolü (Adım 9, 19, 29, 39, 49, 59, 69, 79, 89, 100)
        is_cp = (slide_num in [9, 19, 29, 39, 49, 59, 69, 79, 89, 100])
        if is_cp:
            checkpoint_counter += 1
            slide["isCheckpoint"] = True
            slide["checkpointNumber"] = checkpoint_counter
            if slide_num in checkpoint_fc_dict:
                slide["flashcards"] = checkpoint_fc_dict[slide_num]
            elif not slide.get("flashcards"):
                print(f"UYARI: Slayt {slide_num} checkpoint ancak flashcard yok!")
        else:
            slide.pop("isCheckpoint", None)
            slide.pop("checkpointNumber", None)
            slide.pop("flashcards", None)

        # Ekstra elemanları ilgili slaytlara ekle
        elements = list(slide.get("interactiveElements", []))

        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_causal:
            elements.append(extra_causal[slide_num])

        # Şema normalizasyonları ve sızıntı temizliği
        for el in elements:
            t = el.get("type")
            if t == "branching_logic":
                if "options" not in el and "branchingOptions" in el:
                    el["options"] = el["branchingOptions"]
                elif "branchingOptions" not in el and "options" in el:
                    el["branchingOptions"] = el["options"]
                for o in el.get("options", []):
                    if "isCorrect" in o and "isOptimal" not in o:
                        o["isOptimal"] = o["isCorrect"]
                    elif "isOptimal" in o and "isCorrect" not in o:
                        o["isCorrect"] = o["isOptimal"]
            elif t == "before_after_slider":
                lt = el.get("leftTitle") or el.get("beforeState", {}).get("label") or "Durum A"
                rt = el.get("rightTitle") or el.get("afterState", {}).get("label") or "Durum B"
                ld = el.get("leftPoints") or el.get("beforeState", {}).get("description") or ""
                rd = el.get("rightPoints") or el.get("afterState", {}).get("description") or ""
                lp = [ld] if isinstance(ld, str) else list(ld)
                rp = [rd] if isinstance(rd, str) else list(rd)
                el["leftTitle"] = lt
                el["rightTitle"] = rt
                el["leftPoints"] = lp
                el["rightPoints"] = rp
                if "beforeState" not in el:
                    el["beforeState"] = {"label": lt, "description": lp[0] if lp else ""}
                if "afterState" not in el:
                    el["afterState"] = {"label": rt, "description": rp[0] if rp else ""}
            elif t == "cloze_masking":
                h = el.get("hint", "")
                a = el.get("maskedTerm", "")
                if h and leaks(h, a):
                    el["hint"] = sanitize_hint(h, a)
            elif t == "interactive_table":
                hdrs = el.get("tableHeaders", [])
                rows = el.get("tableRows", [])
                for r in rows:
                    cells = r.get("cells", [])
                    if len(cells) < len(hdrs):
                        diff = len(hdrs) - len(cells)
                        for _ in range(diff):
                            cells.append({
                                "text": "Standart sitogenetik parametre",
                                "isMasked": False,
                                "hint": ""
                            })
                    elif len(cells) > len(hdrs):
                        cells = cells[:len(hdrs)]
                        r["cells"] = cells

                    for c in cells:
                        if isinstance(c, dict) and c.get("isMasked"):
                            ch = c.get("hint", "")
                            ca = c.get("text", "")
                            if ch and leaks(ch, ca):
                                c["hint"] = sanitize_hint(ch, ca)

        # Anlatım alanlarını validator standartlarına uygun bağla
        core_txt = slide.get("coreContent", {}).get("text", "")
        slide["synthesisNarrative"] = core_txt
        slide["content"] = core_txt
        if not slide.get("coreContent", {}).get("keyBullets"):
            slide.setdefault("coreContent", {})["keyBullets"] = [
                {"title": slide["title"], "desc": slide.get("subtitle", ""), "isKey": True}
            ]

        # İlgili soruları dağıt
        start_q_idx = ((slide_num - 1) * len(questions)) // 100
        end_q_idx = (slide_num * len(questions)) // 100
        step_questions = questions[start_q_idx:end_q_idx]
        if not step_questions and questions:
            step_questions = [questions[(slide_num - 1) % len(questions)]]

        slide["interactiveElements"] = elements
        slide["matchedPastQuestions"] = step_questions
        if step_questions:
            slide["matchedPastQuestion"] = step_questions[0]

        final_slides.append(slide)

    # 4. İSTATİSTİKLERİ HESAPLA VE DOĞRULA
    type_counts = Counter()
    for s in final_slides:
        for el in s.get("interactiveElements", []):
            type_counts[el.get("type")] += 1

    total_interactive = sum(type_counts.values())
    print("\n" + "=" * 50)
    print(f"Toplam İnteraktif Öğe: {total_interactive}")
    print(f"Adım Başına Oran: {total_interactive / len(final_slides):.2f}x (Hedef: 1.5x - 3.5x)")
    print("-" * 50)
    for t, count in type_counts.most_common():
        pct = (count / total_interactive) * 100
        status = "UYGUN" if pct >= 8.0 else "DÜŞÜK (!)"
        print(f"  {t:<22}: {count:>3} (%{pct:>5.1f}) -> {status}")
    print("=" * 50)

    for t, count in type_counts.items():
        pct = (count / total_interactive) * 100
        assert pct >= 8.0, f"HATA: {t} türü %8 şartını sağlamıyor: %{pct:.1f}"

    # 5. DOSYALARI YAZ (XML, HTML, MD, JSON)
    deck_id = "k1p-k1-10-kromozomal-hastaliklar-ve-genetik-danisma"
    deck_title = "Kromozomal Hastalıklar ve Genetik Danışma (Yeni Mikro-Ders)"
    short_title = "Kromozomal Hastalıklar ve Danışma"

    os.makedirs(PACKAGE_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

    # Manifest
    manifest_data = {
        "id": "k1-10-kromozomal-hastaliklar-ve-genetik-danisma",
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Genetik",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "version": "2.0.0",
        "formatVersion": "1.0",
        "totalSlides": 100,
        "totalInteractiveElements": total_interactive,
        "interactiveRatio": round(total_interactive / 100, 2),
        "interactiveDistribution": {t: {"count": c, "percentage": round(c / total_interactive * 100, 1)} for t, c in type_counts.items()},
        "files": {
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        }
    }
    manifest_path = os.path.join(PACKAGE_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"\n1. Paket Manifest kaydedildi: {manifest_path}")

    # Structure XML
    root = ET.Element("learningDeck", {
        "id": deck_id,
        "version": "2.0.0",
        "totalSlides": "100"
    })
    meta_el = ET.SubElement(root, "metadata")
    ET.SubElement(meta_el, "title").text = deck_title
    ET.SubElement(meta_el, "discipline").text = "Tıbbi Genetik"
    ET.SubElement(meta_el, "instructor").text = "Dr. Öğr. Üyesi Serap Arslan"

    slides_el = ET.SubElement(root, "slides")
    for s in final_slides:
        s_el = ET.SubElement(slides_el, "slide", {
            "number": str(s["slideNumber"]),
            "badge": s.get("badge", ""),
            "isCheckpoint": str(s.get("isCheckpoint", False)).lower()
        })
        ET.SubElement(s_el, "title").text = s["title"]
        ET.SubElement(s_el, "subtitle").text = s.get("subtitle", "")
        inter_el = ET.SubElement(s_el, "interactiveElements", {"count": str(len(s.get("interactiveElements", [])))})
        for el in s.get("interactiveElements", []):
            ET.SubElement(inter_el, "element", {"type": el.get("type", "")})

    xml_raw = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_raw)
    xml_path = os.path.join(PACKAGE_DIR, "structure.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(parsed.toprettyxml(indent="  "))
    print(f"2. Paket Structure XML kaydedildi: {xml_path}")

    # Blocks HTML
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"tr\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{deck_title} - İnteraktif Bloklar</title>",
        "  <style>",
        "    .slide-block { margin-bottom: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 1rem; }",
        "    .badge { font-weight: bold; color: #2563eb; }",
        "    .checkpoint { background: #fef2f2; border: 1px solid #f87171; padding: 1rem; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>{deck_title}</h1>",
        f"  <p>Eğitmen: Dr. Öğr. Üyesi Serap Arslan | Toplam 100 Adım | {total_interactive} Etkileşim</p>"
    ]
    for s in final_slides:
        cp_cls = " checkpoint" if s.get("isCheckpoint") else ""
        html_lines.append(f"  <div class=\"slide-block{cp_cls}\" id=\"slide-{s['slideNumber']}\">")
        html_lines.append(f"    <span class=\"badge\">Adım {s['slideNumber']} · {s.get('badge','')}</span>")
        html_lines.append(f"    <h2>{s['title']}</h2>")
        html_lines.append(f"    <h3>{s.get('subtitle','')}</h3>")
        html_lines.append(f"    <div class=\"narrative\">{s.get('synthesisNarrative','').replace(chr(10), '<br>')}</div>")
        html_lines.append("  </div>")
    html_lines.append("</body></html>")
    html_path = os.path.join(PACKAGE_DIR, "blocks.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
    print(f"3. Paket Blocks HTML kaydedildi: {html_path}")

    # Content MD
    md_lines = [
        f"# {deck_title}",
        f"**Ders:** Tıbbi Genetik · **Öğretim Üyesi:** Dr. Öğr. Üyesi Serap Arslan · **Kurul:** Kurul 1",
        f"**Adım Sayısı:** 100 · **İnteraktif Eleman:** {total_interactive} · **Oran:** {total_interactive/100:.2f}x\n",
        "---"
    ]
    for s in final_slides:
        md_lines.append(f"\n## Adım {s['slideNumber']}: {s['title']}")
        md_lines.append(f"*{s.get('subtitle', '')}* | **Rozet:** `{s.get('badge', '')}`\n")
        md_lines.append(s.get('synthesisNarrative', ''))
        if s.get("spotPearls"):
            md_lines.append("\n**Spot İnciler:**")
            for sp in s["spotPearls"]:
                md_lines.append(f"- {sp}")
        if s.get("flashcards"):
            md_lines.append("\n**Akıl Kartları (Flashcards):**")
            for fc in s["flashcards"]:
                md_lines.append(f"- **Soru:** {fc['front']} | **Cevap:** {fc['back']}")
    md_path = os.path.join(PACKAGE_DIR, "content.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"4. Paket Content MD kaydedildi: {md_path}")

    # Runtime Item JSON
    full_deck_item = {
        "id": deck_id,
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Genetik",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "audioFile": "audio/decks/k1-10.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "indigo",
        "matchedNoteId": "k1-10",
        "matchedNoteTitle": "Kromozomal Hastalıklar ve Genetik Danışma",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-10-kromozomal-hastaliklar-ve-genetik-danisma",
            "manifest": "manifest.json",
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        },
        "overview": (
            "Kromozomal hastalıkların ve genetik danışmanın kapsamlı klinik kılavuzu: normal karyotip, sayısal ve yapısal anomaliler; "
            "anöploidi mekanizmaları (mayotik ayrılamama, anafaz gecikmesi); dengeli ve dengesiz yeniden düzenlenmeler; "
            "resiprokal ve Robertsonian translokasyonlar (rob(13;14), rob(14;21)); canlı doğan otozomal trizomiler (Down, Edwards, Patau); "
            "klasik delesyonlar (Cri du chat 5p15, Wolf-Hirschhorn 4p16.3); mikrodelesyonlar (DiGeorge 22q11.2, Williams 7q11.23); "
            "gonozomal polizomiler (Klinefelter 47,XXY, 47,XYY); tek canlı monozomi Turner Sendromu (45,X); "
            "genomik imprinting ve uniparental dizomi (Prader-Willi, Angelman); yönlendirici olmayan genetik danışmanlık ve prenatal tanı."
        ),
        "highYieldPearls": [
            "Normal insan somatik karyotipi 46 kromozomdur (44 otozom, 2 gonozom); akrosentrikler 13, 14, 15, 21 ve 22'dir.",
            "Canlı doğumların yaklaşık %1'inde kromozom anomalisi bulunur; en sık klinik anomali anöploididir.",
            "Turner Sendromu (45,X) insan türünde yaşamla bağdaşan TEK tam monozomidir ve anne yaşından bağımsızdır.",
            "Spontan abortuslarda en sık saptanan otozomal trizomi Trizomi 16'dır (asla canlı doğamaz, mutlak letal).",
            "Mayoz I ayrılamaması heterodisomi (farklı homologlar), Mayoz II ayrılamaması izodisomi (özdeş kromatitler) üretir.",
            "Robertsonian translokasyon insanlarda EN YAYGIN yapısal kromozom anomalisidir; taşıyıcı 45 kromozomludur ve dengelidir.",
            "rob(14;21) taşıyıcısı ANNE ise Down riski %15, BABA ise sperm seleksiyonu nedeniyle %4-5'tir; rob(21;21) riski %100'dür.",
            "Down sendromu (%95 klasik, %4 translokasyon); infantil hipotoni, endokardiyal yastık defekti (AVSD) ve duodenal atrezi ile seyreder.",
            "Translokasyon Down sendromu ANNE YAŞINA BAĞLI DEĞİLDİR ve ebeveynlere mutlaka karyotip analizi yapılmalıdır.",
            "Edwards sendromu (Trizomi 18): İnfantil hipertonisite, clenched hand, rocker-bottom ayak, çıkıntılı oksiput; %80 kızdır.",
            "Patau sendromu (Trizomi 13): Holoprozensefali + mikroftalmi + yarık damak + polidaktili triadı ve kutis aplazidir.",
            "Cri du chat sendromu [del(5p15)]: Tiz kedi miyavlaması ağlaması (erişkinlikte kaybolur), ay yüz, mikrosefali.",
            "Wolf-Hirschhorn sendromu [del(4p16.3)]: Yunan savaşçı miğferi yüzü, balık ağzı ve GABRG1 kaybına bağlı dirençli epilepsidir.",
            "DiGeorge sendromu [del(22q11.2)]: En sık mikrodelesyon; TBX1 geni; CATCH-22 (Fallot, Timus aplazisi, neonatal hipokalsemi).",
            "Williams sendromu [del(7q11.23)]: Elastin (ELN) geni kaybı, Supravalvüler Aort Stenozu (SVAS), elfin yüzü ve kokteyl partisi kişiliği.",
            "17p12 duplikasyonu CMT-1A demiyelinizan nöropatisine, 17p12 delesyonu ise Basınca Duyarlı Nöropatiye (HNPP) yol açar.",
            "Klinefelter sendromu (47,XXY): 1 Barr cismi, önökoid uzun boy, seminifer tübül hiyalinizasyonu, azospermi, infertilite, yüksek FSH/LH.",
            "47,XYY sendromu paternal Mayoz II hatasıyla oluşur; uzun boyludurlar ancak FERTİLDİRLER (0 Barr cismi).",
            "Prader-Willi sendromu: Paternal 15q11-q13 kaybı (%70 delesyon, %30 mUPD15); bebeklikte hipotoni, 2 yaştan sonra hiperfaji ve obezite.",
            "Angelman sendromu: Maternal 15q11-q13 kaybı (%70 delesyon, %3-5 pUPD15); UBE3A geni; mutlu kukla, uygunsuz kahkaha, konuşamama.",
            "Genetik danışma HİÇBİR ZAMAN YÖNLENDİRİCİ OLMAMALIDIR (non-directive); karar tamamen aileye aittir.",
            "Zihinsel engellilik ve çoklu anomalide İLK BASAMAK test Kromozomal Mikroarray'dir (CMA); ancak dengeli anomalileri GÖREMEZ."
        ],
        "totalSlides": 100,
        "totalInteractiveElements": total_interactive,
        "interactiveRatio": round(total_interactive / 100, 2),
        "matchedPastQuestionsCount": len(questions),
        "slides": final_slides
    }
    output_path = os.path.join(DECKS_ITEMS_DIR, f"{deck_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_deck_item, f, ensure_ascii=False, indent=2)
    print(f"5. Runtime Item JSON kaydedildi: {output_path}")

    # 6. INTERACTIVE_LEARNING_DECKS.JSON GÜNCELLE
    with open(INTERACTIVE_DECKS_PATH, "r", encoding="utf-8") as f:
        decks_meta = json.load(f)

    found_idx = -1
    for i, d in enumerate(decks_meta):
        if d.get("id") == deck_id or d.get("id") == "k1-10-kromozomal-hastaliklar-ve-genetik-danisma" or d.get("id") == "learn-kromozomal-hastaliklar-ve":
            found_idx = i
            break

    deck_summary = {
        "id": deck_id,
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Genetik",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "audioFile": "audio/decks/k1-10.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "indigo",
        "matchedNoteId": "k1-10",
        "matchedNoteTitle": "Kromozomal Hastalıklar ve Genetik Danışma",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-10-kromozomal-hastaliklar-ve-genetik-danisma",
            "manifest": "manifest.json",
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        },
        "overview": full_deck_item["overview"],
        "highYieldPearls": full_deck_item["highYieldPearls"],
        "totalSlides": 100,
        "totalInteractiveElements": total_interactive,
        "interactiveRatio": round(total_interactive / 100, 2),
        "slides": final_slides
    }

    if found_idx >= 0:
        decks_meta[found_idx] = deck_summary
        print(f"6. interactive_learning_decks.json indeksi {found_idx} yerinde güncellendi.")
    else:
        decks_meta.append(deck_summary)
        print("6. interactive_learning_decks.json sonuna eklendi.")

    with open(INTERACTIVE_DECKS_PATH, "w", encoding="utf-8") as f:
        json.dump(decks_meta, f, ensure_ascii=False, indent=2)

    # 7. CATALOG.JSON GÜNCELLE
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        cat_found = False
        cat_entry = {
            "id": deck_id,
            "title": deck_title,
            "discipline": "Tıbbi Genetik",
            "committee": "Kurul 1",
            "totalSlides": 100,
            "interactiveElementsCount": total_interactive,
            "hasPackage": True
        }
        if isinstance(catalog, list):
            for i, c in enumerate(catalog):
                if c.get("id") == deck_id or c.get("id") == "k1-10-kromozomal-hastaliklar-ve-genetik-danisma":
                    catalog[i] = cat_entry
                    cat_found = True
                    break
            if not cat_found:
                catalog.append(cat_entry)
        elif isinstance(catalog, dict) and "decks" in catalog:
            for i, c in enumerate(catalog["decks"]):
                if c.get("id") == deck_id or c.get("id") == "k1-10-kromozomal-hastaliklar-ve-genetik-danisma":
                    catalog["decks"][i] = cat_entry
                    cat_found = True
                    break
            if not cat_found:
                catalog["decks"].append(cat_entry)
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print("7. catalog.json başarıyla güncellendi.")

    print("\n" + "=" * 70)
    print("TEBRİKLER! DERS 10 TÜM FORMATLARDA BAŞARIYLA TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    main()
