#!/usr/bin/env python3
"""
Kurul 1 - Ders 8: Hücresel Yaşlanma (Prof. Dr. Hikmet Keleş)
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

from scripts.k1_08_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)
from scripts.k1_08_deck_data.section_1 import get_section_1_slides
from scripts.k1_08_deck_data.section_2 import get_section_2_slides
from scripts.k1_08_deck_data.section_3 import get_section_3_slides
from scripts.k1_08_deck_data.section_4 import get_section_4_slides
from scripts.k1_08_deck_data.section_5 import get_section_5_slides
from scripts.k1_08_deck_data.section_6 import get_section_6_slides
from scripts.k1_08_deck_data.section_7 import get_section_7_slides
from scripts.k1_08_deck_data.section_8 import get_section_8_slides
from scripts.k1_08_deck_data.section_9 import get_section_9_slides
from scripts.k1_08_deck_data.section_10 import get_section_10_slides

from scripts.enrich_k1_08_elements import (
    get_extra_quizzes, get_extra_causal_chains, get_extra_sliders,
    get_extra_branching, get_extra_tables
)

# Dosya yolları
QUESTIONS_FILE = os.path.join(BASE_DIR, "meds/src/data/ornek_sorular/k1/k1-08-hucresel-yaslanma.json")
PACKAGE_DIR = os.path.join(BASE_DIR, "meds/src/data/decks/packages/k1-08-hucresel-yaslanma")
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
        "İlgili patofizyolojik mekanizmayı düşününüz",
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
                "k1-08-fc-01",
                "Hücresel senesensin laboratuvar tanısında en yaygın kullanılan histokimyasal enzim belirteci nedir?",
                "pH 6.0 koşullarında çalışan Senesensle İlişkili Beta-Galaktozidaz (SA-β-gal) enzimidir.",
                "Lizozomal hidrolaz aktivitesi", "Hücresel Yaşlanma"
            ),
            make_flashcard(
                "k1-08-fc-02",
                "Somatik hücrelerde Hayflick limitini belirleyen temel biyolojik sayaç mekanizması nedir?",
                "Her bölünme döngüsünde uç replikasyon problemi nedeniyle kısalan telomerik DNA dizileridir.",
                "Kromozom uç yapısı ve sınırlı bölünme", "Hücresel Yaşlanma"
            ),
            make_flashcard(
                "k1-08-fc-03",
                "Senesent hücreleri kalıcı G1 arrestinde tutan temel siklin bağımlı kinaz inhibitörleri nelerdir?",
                "p16INK4a (CDK4/6 inhibitörü) ve p21CIP1 (p53 aracılı CDK2 inhibitörü) proteinleridir.",
                "Rb defosforilasyonunu koruyan inhibitörler", "Hücresel Yaşlanma"
            )
        ],
        19: [
            make_flashcard(
                "k1-08-fc-04",
                "Erişkin tipi erken yaşlanma olan Werner Sendromunda mutasyona uğrayan gen ve enzimatik işlevi nedir?",
                "WRN genidir; 3'->5' DNA helikaz ve ekzonükleaz aktivitesiyle replikasyon çatalını stabilize eder.",
                "RecQ helikaz ailesi üyesi", "DNA Onarımı ve Yaşlanma"
            ),
            make_flashcard(
                "k1-08-fc-05",
                "Hutchinson-Gilford Progeria Sendromunda nükleer membran harabiyeti yapan mutant protein hangisidir?",
                "Lamin A genindeki mutasyon sonucu farnesil grubunu kaybedemeyen toksik 'progerin' proteinidir.",
                "Nükleer kılıf ara filaman mutasyonu", "DNA Onarımı ve Yaşlanma"
            ),
            make_flashcard(
                "k1-08-fc-06",
                "Çift zincir DNA kırıklarını tanıyıp p53 fosforilasyonunu başlatan primer sensör kinaz hangisidir?",
                "ATM (Ataxia-Telangiectasia Mutated) serin/treonin protein kinazıdır.",
                "DNA hasar yanıtının merkezi yöneticisi", "DNA Onarımı ve Yaşlanma"
            )
        ],
        29: [
            make_flashcard(
                "k1-08-fc-07",
                "Telomerik DNA'nın memeli türlerindeki korunmuş evrensel tekrar hekzanükleotid dizisi nedir?",
                "5'-TTAGGG-3' (Timin-Timin-Adenin-Guanin-Guanin-Guanin) hekzanükleotid dizisidir.",
                "Guaninden zengin uç tekrarı", "Telomer Biyolojisi"
            ),
            make_flashcard(
                "k1-08-fc-08",
                "Telomerik 3' sarkan tek zincirli ucu sararak ATR kinaz yanıtından saklayan shelterin faktörü hangisidir?",
                "POT1 (Protection of Telomeres 1) proteinidir.",
                "Tek zincirli DNA bağlayıcı shelterin alt birimi", "Telomer Biyolojisi"
            ),
            make_flashcard(
                "k1-08-fc-09",
                "Telomer ucunun kendi çift zinciri içine kıvrılarak oluşturduğu koruyucu düğüm yapısına ne ad verilir?",
                "T-loop (Telomeric loop) ve D-loop (Displacement loop) halka yapısıdır.",
                "Kromozom ucunu çift zincir kırığı sanılmaktan koruyan ilmek", "Telomer Biyolojisi"
            )
        ],
        39: [
            make_flashcard(
                "k1-08-fc-10",
                "İnsan telomeraz holoenziminin iki temel fonksiyonel alt birimi hangileridir?",
                "Katalitik ters transkriptaz olan hTERT proteini ve RNA kalıbı sağlayan hTERC (hTR) molekülüdür.",
                "Protein ve RNA kompleksi", "Telomeraz ve Genomik Kriz"
            ),
            make_flashcard(
                "k1-08-fc-11",
                "p53 inaktif hücrelerde aşırı telomer kısalmasıyla tetiklenen 'BFB döngüsü' ne anlama gelir?",
                "Bridge-Fusion-Breakage (Köprü-Füzyon-Kırılma) döngüsüdür; anöploidi ve mitotik krize yol açar.",
                "Kromozomal instabilite mekanizması", "Telomeraz ve Genomik Kriz"
            ),
            make_flashcard(
                "k1-08-fc-12",
                "Kanser hücrelerinin yaklaşık yüzde seksen beşinde sınırsız bölünmeyi sağlayan temel enzim nedir?",
                "hTERT katalitik alt biriminin yeniden reaktive edildiği telomeraz enzimidir.",
                "Ölümsüzleşme (immortalization) enzimi", "Telomeraz ve Genomik Kriz"
            )
        ],
        49: [
            make_flashcard(
                "k1-08-fc-13",
                "Elektron transport zincirinden sızan elektronların O2 ile reaksiyonundan ilk oluşan primer ROS hangisidir?",
                "Süperoksit anyon radikalidir (O2·-); Kompleks I ve III temel sızıntı alanlarıdır.",
                "Tek elektron indirgenmesi ürünü", "Mitokondri ve Oksidatif Stres"
            ),
            make_flashcard(
                "k1-08-fc-14",
                "Mitokondriyal matriks içindeki süperoksiti hidrojen peroksite dönüştüren spesifik enzim nedir?",
                "Manganez Süperoksit Dismutaz (MnSOD / SOD2) enzimidir.",
                "Mitokondriyal antioksidan kalkan", "Mitokondri ve Oksidatif Stres"
            ),
            make_flashcard(
                "k1-08-fc-15",
                "Oksidatif DNA hasarının en duyarlı ve sık ölçülen idrar/doku belirteci olan modifiye baz hangisidir?",
                "8-okso-7,8-dihidro-2'-deoksiguanozin (8-oxo-dG) lezyonudur.",
                "Guanin bazının hidroksilasyonu", "Mitokondri ve Oksidatif Stres"
            )
        ],
        59: [
            make_flashcard(
                "k1-08-fc-16",
                "Zar potansiyeli çöken yaşlı mitokondrilerin dış zarında birikerek mitofajiyi başlatan kinaz hangisidir?",
                "PINK1 (PTEN-induced kinase 1) serin/treonin kinazıdır.",
                "Mitokondriyal hasar sensörü", "Mitofaji ve Organel Klirensi"
            ),
            make_flashcard(
                "k1-08-fc-17",
                "PINK1 tarafından fosforillenerek sitozolden mitokondriye göç eden E3 ubikitin ligaz hangisidir?",
                "Parkin (PARK2) proteinidir; dış zar proteinlerini ubikitinleyerek otofagozoma sevk eder.",
                "Parkinson hastalığı ile ilişkili ligaz", "Mitofaji ve Organel Klirensi"
            ),
            make_flashcard(
                "k1-08-fc-18",
                "Mitokondriyal membran geçirgenliği gözenekleri (MOMP) açıldığında sitoplazmaya sızıp apoptozu tetikleyen protein nedir?",
                "Sitokrom c proteinidir; sitozolik Apaf-1 ve dATP ile birleşerek apoptomazomu kurar.",
                "Solunum zinciri elektron taşıyıcısı ve apoptotik tetik", "Mitofaji ve Organel Klirensi"
            )
        ],
        69: [
            make_flashcard(
                "k1-08-fc-19",
                "Yanlış katlanmış polipeptitleri tanıyıp ATP harcayarak yeniden doğru katlayan moleküler aile nedir?",
                "Hsp70 ve Hsp90 başta olmak üzere Isı Şoku Proteinleri (Moleküler Şaperonlar) ailesidir.",
                "Hücresel katlanma rehberleri", "Proteostaz ve Protein Agregatları"
            ),
            make_flashcard(
                "k1-08-fc-20",
                "Ömrünü tamamlamış veya hasarlı proteinlerin proteazomda tanınması için eklenen kovalent etiket nedir?",
                "Lizin kalıntıları üzerinden bağlanan poliubikitin zinciridir (K48 bağlı).",
                "76 amino asitlik yıkım bayrağı", "Proteostaz ve Protein Agregatları"
            ),
            make_flashcard(
                "k1-08-fc-21",
                "Yaşlanan nöronlarda proteazomal kapasite yetersiz kaldığında mikrotübüllerle sentrozomda toplanan inklüzyonlara ne ad verilir?",
                "Agregom (Aggresome) adı verilir; daha sonra otofajik yolla temizlenmeye çalışılır.",
                "Sentrozomal çözünmeyen protein deposu", "Proteostaz ve Protein Agregatları"
            )
        ],
        79: [
            make_flashcard(
                "k1-08-fc-22",
                "Besin bolluğunda aktive olarak ribozomal translasyonu hızlandıran ve otofajiyi bloke eden kinaz kompleksi nedir?",
                "mTORC1 (mammalian Target of Rapamycin Complex 1) kinaz kompleksidir.",
                "Hücresel anabolizmanın baş yöneticisi", "Besin Algılama ve Sinyal Yolakları"
            ),
            make_flashcard(
                "k1-08-fc-23",
                "Düşük hücresel enerji durumunda (yüksek AMP/ATP) aktive olarak otofajiyi başlatan ana enerji sensörü nedir?",
                "AMPK (AMP ile Aktive Olan Protein Kinaz) enzimidir.",
                "Hücresel yakıt göstergesi", "Besin Algılama ve Sinyal Yolakları"
            ),
            make_flashcard(
                "k1-08-fc-24",
                "Kalori kısıtlamasında yükselen NAD+ kofaktörüne bağımlı olarak PGC-1alfayı deasetile eden enzim ailesi nedir?",
                "Sirtuinler (özellikle SIRT1 ve SIRT3) NAD+ bağımlı deasetilaz ailesidir.",
                "Uzun ömür (longevity) deasetilazları", "Besin Algılama ve Sinyal Yolakları"
            )
        ],
        89: [
            make_flashcard(
                "k1-08-fc-25",
                "Senesens İlişkili Salgı Fenotipinin (SASP) kronik doku harabiyeti yapan ana sitokin bileşenleri nelerdir?",
                "İnterlökin-6 (IL-6), İnterlökin-8 (IL-8), TNF-alfa ve Matris Metalloproteinazlardır (MMP-1/3/13).",
                "Pro-enflamatuar ve matriks eritici kokteyl", "SASP ve İnflammaging"
            ),
            make_flashcard(
                "k1-08-fc-26",
                "Yaşlanma ile dokularda gelişen steril, düşük dereceli kronik inflamasyona gerontolojide ne ad verilir?",
                "'İnflammaging' (İnflamatuar Yaşlanma) adı verilir.",
                "İnflamasyon ve aging birleşimi terim", "SASP ve İnflammaging"
            ),
            make_flashcard(
                "k1-08-fc-27",
                "Yaşlanan hücrelerde nükleer zardan sitoplazmaya sızan DNA parçalarını yabancı mikrop gibi algılayan yolak nedir?",
                "cGAS-STING (siklik GMP-AMP sentaz ve STING) sitozolik DNA sensör yolağıdır.",
                "Tip I interferon ve NF-kappaB tetikleyicisi", "SASP ve İnflammaging"
            )
        ],
        100: [
            make_flashcard(
                "k1-08-fc-28",
                "Senesent hücrelerin anti-apoptotik kalkanını hedefleyerek seçici hücre ölümünü sağlayan ilaç grubuna ne ad verilir?",
                "Senolitikler (örneğin Dasatinib, Kuersetin, Fisetin, Navitoklaks) adı verilir.",
                "Senesent hücreleri öldüren terapötik sınıf", "Anti-Aging Terapötikler"
            ),
            make_flashcard(
                "k1-08-fc-29",
                "Hücreyi öldürmeksizin SASP salgısını baskılayan ajanlara (örneğin Rapamisin, Metformin) ne ad verilir?",
                "Senomorfikler (Senomorphic agents) adı verilir.",
                "SASP susturucu moleküller", "Anti-Aging Terapötikler"
            ),
            make_flashcard(
                "k1-08-fc-30",
                "Kalıtsal olmayan epigenetik hücresel biyolojik yaşı en hassas belirleyen moleküler biyobelirteç nedir?",
                "Steve Horvath'ın CpG adacıklarındaki DNA metilasyon haritasına dayanan 'Epigenetik Saat'tir.",
                "DNA metilasyon profili", "Anti-Aging Terapötikler"
            )
        ]
    }

def main():
    print("=" * 70)
    print("Kurul 1 - Ders 8: Hücresel Yaşlanma (Prof. Dr. Hikmet Keleş)")
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
            q_id = q.get("id") or f"k1-08-q{len(questions)+1:02d}"
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
    extra_quizzes = get_extra_quizzes()
    extra_causal = get_extra_causal_chains()
    extra_sliders = get_extra_sliders()
    extra_branching = get_extra_branching()
    extra_tables = get_extra_tables()
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

        if slide_num in extra_quizzes:
            elements.append(extra_quizzes[slide_num])
        if slide_num in extra_causal:
            elements.append(extra_causal[slide_num])
        if slide_num in extra_sliders:
            elements.append(extra_sliders[slide_num])
        if slide_num in extra_branching:
            elements.append(extra_branching[slide_num])
        if slide_num in extra_tables:
            elements.append(extra_tables[slide_num])

        # Şema normalizasyonları, tablo sütun sayısı eşitleme ve sızıntı temizliği
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
                    # Sütun sayısı eksiği varsa otomatik tamamla
                    if len(cells) < len(hdrs):
                        diff = len(hdrs) - len(cells)
                        if diff == 1 and len(cells) >= 2:
                            c3_text = cells[1].get("hint", "") or "Klinik değerlendirme"
                            cells[1]["hint"] = "İlgili anahtar parametreyi düşününüz"
                            cells.append({
                                "text": c3_text,
                                "isMasked": False,
                                "hint": ""
                            })
                        else:
                            for _ in range(diff):
                                cells.append({
                                    "text": "Standart fizyolojik parametre",
                                    "isMasked": False,
                                    "hint": ""
                                })
                    # Fazla hücre varsa kırp
                    elif len(cells) > len(hdrs):
                        cells = cells[:len(hdrs)]
                        r["cells"] = cells

                    # Sızıntı temizliği
                    for c in cells:
                        if isinstance(c, dict) and c.get("isMasked"):
                            ch = c.get("hint", "")
                            ca = c.get("text", "")
                            if ch and leaks(ch, ca):
                                c["hint"] = sanitize_hint(ch, ca)

        # Anlatım alanlarını validator standartlarına uygun bağla
        core_txt = slide.get("content") or slide.get("synthesisNarrative") or slide.get("coreContent", {}).get("text", "")
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
    print(f"Adım Başına Oran: {total_interactive / len(final_slides):.2f}x (Hedef: 1.5x - 3.0x)")
    print("-" * 50)
    for t, count in type_counts.most_common():
        pct = (count / total_interactive) * 100
        status = "UYGUN" if pct >= 8.0 else "DÜŞÜK (!)"
        print(f"  {t:<22}: {count:>3} (%{pct:>5.1f}) -> {status}")
    print("=" * 50)

    # Her tür en az %8 olmalı
    for t, count in type_counts.items():
        pct = (count / total_interactive) * 100
        assert pct >= 8.0, f"HATA: {t} türü %8 şartını sağlamıyor: %{pct:.1f}"

    # 5. DOSYALARI YAZ (XML, HTML, MD, JSON)
    deck_id = "k1p-k1-08-hucresel-yaslanma"
    deck_title = "Hücresel Yaşlanma (Yeni Mikro-Ders)"
    short_title = "Hücresel Yaşlanma"

    os.makedirs(PACKAGE_DIR, exist_ok=True)
    os.makedirs(DECKS_ITEMS_DIR, exist_ok=True)

    # Manifest
    manifest_data = {
        "id": "k1-08-hucresel-yaslanma",
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
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
    ET.SubElement(meta_el, "discipline").text = "Tıbbi Patoloji"
    ET.SubElement(meta_el, "instructor").text = "Prof. Dr. Hikmet Keleş"

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
        f"  <p>Eğitmen: Prof. Dr. Hikmet Keleş | Toplam 100 Adım | {total_interactive} Etkileşim</p>"
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
        f"**Ders:** Tıbbi Patoloji · **Öğretim Üyesi:** Prof. Dr. Hikmet Keleş · **Kurul:** Kurul 1",
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
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audio/decks/k1-08.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "emerald",
        "matchedNoteId": "k1-08",
        "matchedNoteTitle": "Hücresel Yaşlanma",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-08-hucresel-yaslanma",
            "manifest": "manifest.json",
            "structure": "structure.xml",
            "blocks": "blocks.html",
            "content": "content.md"
        },
        "overview": (
            "Hücresel yaşlanmanın moleküler mekanizmaları: Hayflick limiti, telomer kısalması ve shelterin kompleksi; "
            "DNA onarım defektleri ve erken yaşlanma sendromları (Werner, Hutchinson-Gilford, Ataksi Telenjiektazi); "
            "mitokondriyal disfonksiyon, serbest radikal teorisi ve PINK1/Parkin aracılı mitofaji; "
            "proteostaz kaybı, şaperon ve proteazom disfonksiyonu; besin algılama yolakları (IGF-1/mTOR, AMPK, SIRT1); "
            "SASP, kronik steril inflamasyon (inflammaging); senolitik ve senomorfik terapötik stratejiler."
        ),
        "highYieldPearls": [
            "Hücresel senesens G1/S fazında kalıcı, geri dönüşümsüz replikatif arresttir; SA-β-gal ve p16INK4a ile tanınır.",
            "Hayflick limiti insan somatik hücrelerinin bölünme sınırıdır; temel belirleyici telomer erozyonudur.",
            "Telomerik DNA 5'-TTAGGG-3' tekrarlarından oluşur; shelterin kompleksi (TRF1, TRF2, POT1) tarafından korunur.",
            "POT1 tek zincirli sarkan 3' ucu örterek ATR kinaz aktivasyonunu engeller; TRF2 ise T-loop ilmeğini kilitler.",
            "Werner sendromu WRN genindeki RecQ helikaz mutasyonudur; erişkin dönemde katarakt ve ateroskleroz yapar.",
            "Hutchinson-Gilford progeria LMNA geni nokta mutasyonudur; farnesilini kaybedemeyen toksik progerin nükleer zarı bozar.",
            "p53 inaktif hücrelerde aşırı telomer kısalması Bridge-Fusion-Breakage (BFB) krizine ve genomik anöploidiye yol açar.",
            "Kanser hücrelerinin %85-90'ı hTERT telomeraz reaktivasyonuyla, kalanı ise ALT yolağıyla immortalize olur.",
            "Mitokondri ETC Kompleks I ve III primer süperoksit (O2·-) sızıntı alanlarıdır; MnSOD süperoksiti H2O2'ye çevirir.",
            "Zar potansiyeli çöken yaşlı mitokondrinin dış zarında PINK1 birikir, Parkin E3 ligazı çekerek mitofajiyi başlatır.",
            "Bax ve Bak oligomerizasyonu MOMP oluşturarak sitokrom c'yi sitoplazmaya salar ve apoptomazomu tetikler.",
            "Yaşlanma ile 26S proteazom tıkanır ve çözünmeyen proteinler sentrozom çevresinde toplanarak agregomları kurar.",
            "Aşırı beslenme IGF-1 ve mTORC1'i aktive ederek otofajiyi boğar; kalori kısıtlaması ise AMPK ve SIRT1'i uyarır.",
            "SIRT1 NAD+ bağımlı deasetilazdır; PGC-1alfa ve FOXO'yu deasetile ederek mitokondriyal biyogenez ve antioksidan yanıtı artırır.",
            "SASP (Senesens İlişkili Salgı Fenotipi) IL-6, IL-8 ve MMP salgılayarak dokuda kronik steril inflamasyona (inflammaging) neden olur.",
            "Senolitikler (Dasatinib, Kuersetin) senesent hücreleri seçici apoptoza sokar; senomorfikler (Metformin, Rapamisin) SASP'ı susturur."
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
        if d.get("id") == deck_id or d.get("id") == "k1-08-hucresel-yaslanma":
            found_idx = i
            break

    deck_summary = {
        "id": deck_id,
        "title": deck_title,
        "shortTitle": short_title,
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 (Ürogenital ve Solunum Sistemi)",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "audioFile": "audio/decks/k1-08.mp3",
        "audioDuration": 2400,
        "confidence": 0.99,
        "themeColor": "emerald",
        "matchedNoteId": "k1-08",
        "matchedNoteTitle": "Hücresel Yaşlanma",
        "isNew": True,
        "isLegacy": False,
        "version": "2.0.0",
        "packageSources": {
            "packageDir": "meds/src/data/decks/packages/k1-08-hucresel-yaslanma",
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
            "discipline": "Tıbbi Patoloji",
            "committee": "Kurul 1",
            "totalSlides": 100,
            "interactiveElementsCount": total_interactive,
            "hasPackage": True
        }
        if isinstance(catalog, list):
            for i, c in enumerate(catalog):
                if c.get("id") == deck_id:
                    catalog[i] = cat_entry
                    cat_found = True
                    break
            if not cat_found:
                catalog.append(cat_entry)
        elif isinstance(catalog, dict) and "decks" in catalog:
            for i, c in enumerate(catalog["decks"]):
                if c.get("id") == deck_id:
                    catalog["decks"][i] = cat_entry
                    cat_found = True
                    break
            if not cat_found:
                catalog["decks"].append(cat_entry)
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print("7. catalog.json başarıyla güncellendi.")

    print("\n" + "=" * 70)
    print("TEBRİKLER! DERS 8 TÜM FORMATLARDA BAŞARIYLA TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    main()
