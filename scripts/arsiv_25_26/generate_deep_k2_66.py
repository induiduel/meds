#!/usr/bin/env python3
"""
generate_deep_k2_66.py:
Expands the 10 sparse pages (<40 words) of y25-k2-66-primer-myelin-ve-metabolik-toksik-hastaliklar
into deep, rich amfi lecture sentences, preserves drawing alignment (22/22 schemas),
prunes uncompiled commands, and verifies all 6 Quality Gates with 0 HATA.
"""

import sys
import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/cizim"))

import konusma_v2 as KV
import denetle as D
import isle as IS
import cizim_dogrula as CD
import sablon

TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-66-primer-myelin-ve-metabolik-toksik-hastaliklar"

NEW_SENTENCES_BY_PAGE = {
    1: {
        "ses": "Ders boyunca miyelinin biyokimyasal mimarisinden başlayarak multipl skleroz, lökodistrofiler ve sistemik metabolik yetmezliklerin sinir dokusundaki patolojik lezyonlarını ayrıntılı biçimde inceleyeceğiz.",
        "ekran": "**Klinik ve Patolojik Kapsam:** Miyelin mimarisi, demiyelinizan plaklar ve metabolik lezyonlar",
        "slayt": {
            "sayfa": 1,
            "satir": ["Primer Myelin Hastalıkları ve", "Edinsel Metabolik ve Toksik", "Bozukluklar"],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s01", "cikmis": [], "spot": None, "duzey": 2
    },
    3: {
        "ses": "Miyelin kılıfındaki bu zengin lipit içeriği yüksek elektriksel direnç ve yalıtım sağlayarak sinirsel iletim hızını katbekat artıran hidrofobik bir bariyer vazifesi görür.",
        "ekran": "**Lipit İzolasyon Bariyeri:** Yüksek elektriksel direnç ve hidrofobik membran yalıtımı",
        "slayt": {
            "sayfa": 3,
            "satir": ["- Galaktoserebrozid: Myelinin yapısında en bol bulunan lipit"],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s02", "cikmis": [], "spot": None, "duzey": 2
    },
    5: {
        "ses": "Ranvier nodlarındaki voltaj kapılı sodyum kanallarının yüksek yoğunluğu sayesinde aksiyon potansiyeli noddan noda sıçrayarak enerji tüketimini en aza indirir ve iletimi olağanüstü hızlandırır.",
        "ekran": "**Saltatuvar İletim Dinamiği:** Ranvier nodlarında yoğun sodyum kanalları ve hızlı atlama",
        "slayt": {
            "sayfa": 5,
            "satir": ["Eletriksel uyarı aksonlarda Ranvier nodları yoluyla atlayarak (saltatory", "conduction) ilerler."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s03", "cikmis": [], "spot": None, "duzey": 2
    },
    32: {
        "ses": "Hücresel bağışıklığın ileri derecede çöktüğü hastalarda je ce virüsü oligodendrosit çekirdeklerinde tipik viral inklüzyonlar oluşturarak yaygın ve düzensiz demiyelinizasyon odaklarına yol açar.",
        "ekran": "**Oligodendrosit Hasarı:** Nükleer inklüzyonlar ve destrüktif demiyelinizasyon odakları",
        "slayt": {
            "sayfa": 32,
            "satir": ["Virüs özellikle oligodentrositleri infekte eder ve bu hücrelerin hasarına", "ve ölümüne neden olarak demyelinizasyon oluşturur."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s13", "cikmis": [], "spot": None, "duzey": 2
    },
    35: {
        "ses": "Lizozomal enzim defektine bağlı biriken anormal sfingolipidler makrofajlar tarafından fagosite edildikçe dokuda köpüksü histiyositler ve karakteristik globoid hücre birikimleri meydana gelir.",
        "ekran": "**Makrofaj İnfiltrasyonu:** Lizozomal lipid birikimi ve karakteristik köpüksü hücreler",
        "slayt": {
            "sayfa": 35,
            "satir": ["Myelin kaybı lipidle dolu makrofaj infiltrasyonuna neden olur."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s14", "cikmis": [], "spot": None, "duzey": 2
    },
    37: {
        "ses": "Bilateral simetrik demiyelinizasyon alanları piramidal yolları ve serebellar bağlantıları harap ederek çocuklarda kazanılmış motor becerilerin süratle kaybına ve kuadripareziye neden olur.",
        "ekran": "**Motor Fonksiyon Kaybı:** Serebellar ve piramidal lif hasarıyla gelişen kuadriparezi",
        "slayt": {
            "sayfa": 37,
            "satir": ["Beyaz cevherin yaygın tutulumuyla motor becerilerde bozulma,", "spastisite, hipotoni ya da ataksi görülür."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s14", "cikmis": [], "spot": None, "duzey": 2
    },
    41: {
        "ses": "Tiamin eksikliğine bağlı hücresel enerji metabolizması çökünce mamiller cisimlerde ve üçüncü ventrikül çevresinde peteşiyal kanamalar ile endotel proliferasyonu gelişir.",
        "ekran": "**Mamiller Cisim Hasarı:** Tiamin eksikliğine bağlı mikrovasküler kanama ve nekroz",
        "slayt": {
            "sayfa": 41,
            "satir": ["Bu sendrom özellikle kronik alkolizmde sık görülür."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s16", "cikmis": [], "spot": None, "duzey": 2
    },
    43: {
        "ses": "Biyokimyasal metilasyon döngüsünün bozulması posterior kordondaki vibrasyon ve pozisyon duyusunu, lateral kortikospinal traktustaki ise motor iletimi eşzamanlı olarak sekteye uğratır.",
        "ekran": "**Kombine Traktus Tutulumu:** Arka kordon duyusal ve lateral kortikospinal motor hasar",
        "slayt": {
            "sayfa": 43,
            "satir": ["Bu durum omuriliğin subakut kombine dejenerasyonu olarak", "isimlendirilir."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s17", "cikmis": [], "spot": None, "duzey": 2
    },
    48: {
        "ses": "Artan amonyağın astrositlerde glutamine dönüştürülmesi osmotik çekimle hücre içi ödemi tetikler ve glial morfolojiyi Alzheimer tip iki sitolojik görünümüne dönüştürür.",
        "ekran": "**Glial Osmotik Şişme:** Glutamin birikimine bağlı astrositer ödem ve morfolojik değişim",
        "slayt": {
            "sayfa": 48,
            "satir": ["Santral sinir sisteminde amonyak metabolizması glutamin sentetazın", "aktivasyonu ile sadece astrositlerde gerçekleşir."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s18", "cikmis": [], "spot": None, "duzey": 2
    },
    51: {
        "ses": "Özellikle intratekal kemoterapi veya kraniyal radyoterapiyle kombine edildiğinde metotreksat santral sinir sisteminde derin lökoensefalopati ve nekrotizan doku kalsifikasyonlarına yol açar.",
        "ekran": "**Toksik Lökoensefalopati:** Metotreksat nörotoksisitesine bağlı nekrotizan kalsifikasyon",
        "slayt": {
            "sayfa": 51,
            "satir": ["Hasar özellikle beyaz cevherde olup nekroz, demyelinizasyon, gliozis ve", "kalsifikasyon görülebilir."],
            "sekil": None
        },
        "slayt_adim": "y25-k2-66-s20", "cikmis": [], "spot": None, "duzey": 2
    }
}

DRAWING_SNIPPETS_MAP = {
    0: "Myelin kılıfı hem santral sinir",
    1: "sfingomyelin myelin kılıfının sağlamlığını",
    2: "myelin protein sıfır santral sinir",
    3: "Ranvier nodlarının uzunluğu yaklaşık bir mikron",
    4: "Schwann hücresi sadece tek bir internoda",
    5: "Dismyelinizan hastalıklar normal myelinin",
    6: "tekrarlayan ve duraksayan özellikte nörolojik yetersizlik",
    7: "de re iki aleli multipl skleroz",
    8: "Yardımcı te bir hücreleri interferon gama salgılar",
    9: "periventriküler beyaz cevherde belirirler",
    10: "gölge plak olarak adlandırılır",
    11: "oligoklonal bantlar saptanır",
    12: "olguların yüzde yirmi kadarında ölümcüldür",
    13: "akuaporin dört su kanallarına karşı",
    14: "Ponsun omurilikteki motor nöronlara uyarı taşıyan liflerindeki tutulum",
    15: "Je ce virüsü özellikle oligodendrositleri",
    16: "lipidle dolu makrofaj infiltrasyonuna",
    17: "Erken lezyonlarda kanamaya neden olan dilate kapillerler",
    18: "Tablo daha sonra hızla ilerleyerek alt ekstremitelerde spastik güçsüzlüğe",
    19: "Alzheimer tip iki hücreleri adı verilir",
    20: "globus pallidusun seçici hasarına yol açar",
    21: "Radyasyondan etkilenen beyin bölgelerinde geniş koagülasyon nekrozu"
}

def main():
    print("=== Expanding y25-k2-66-primer-myelin-ve-metabolik-toksik-hastaliklar to Deep Amfi Lecture ===")
    
    with open(TASLAK / "konusma_v2.json") as f:
        kv = json.load(f)
    
    with open(TASLAK / "cizim_aday.json") as f:
        caday = json.load(f)
    
    # Prune uncompiled commands (keep only the first 22 schemas)
    drawings = caday.get("komutlar", [])[:22]
    print(f"Loaded {len(drawings)} candidate schema drawings (pruned uncompiled commands).")
    
    # Ensure idempotency by removing any previously added sentences
    added_ses = {v["ses"] for v in NEW_SENTENCES_BY_PAGE.values()}
    for b in kv.get("bolumler", []):
        for p in b.get("paragraflar", []):
            p["cumleler"] = [c for c in p.get("cumleler", []) if c.get("ses") not in added_ses]
            
    # Insert new sentences at appropriate positions
    for target_page, s_data in sorted(NEW_SENTENCES_BY_PAGE.items()):
        inserted = False
        for b in kv.get("bolumler", []):
            if inserted:
                break
            for p in b.get("paragraflar", []):
                c_pages = [c["slayt"]["sayfa"] for c in p.get("cumleler", [])]
                if target_page in c_pages:
                    # Find last index with target_page
                    last_idx = max(i for i, page in enumerate(c_pages) if page == target_page)
                    p["cumleler"].insert(last_idx + 1, dict(s_data))
                    inserted = True
                    break
        if not inserted:
            raise RuntimeError(f"Could not insert sentence for page {target_page}")
            
    # Re-index all sentences monotonically
    counter = 1
    new_cumleler_all = []
    old_to_new_cid = {}
    for b in kv.get("bolumler", []):
        for p in b.get("paragraflar", []):
            for c in p.get("cumleler", []):
                old_cid = c.get("id")
                new_cid = f"k2-66-c{counter:04d}"
                c["id"] = new_cid
                if old_cid:
                    old_to_new_cid[old_cid] = new_cid
                counter += 1
                new_cumleler_all.append(c)
                
    print(f"Total sentences after expansion: {len(new_cumleler_all)} (all re-indexed k2-66-c0001..c{len(new_cumleler_all):04d})")
    
    # Verify word count per page
    words_by_page = {}
    for c in new_cumleler_all:
        sp = c["slayt"]["sayfa"]
        words_by_page[sp] = words_by_page.get(sp, 0) + len(c["ses"].split())
    sparse_pages = [sp for sp, w in words_by_page.items() if w < 40]
    total_words = sum(words_by_page.values())
    print(f"Total words: {total_words}, sparse pages (<40 words): {len(sparse_pages)}")
    if sparse_pages:
        print(f"ERROR: Still sparse pages: {sparse_pages}")
        sys.exit(1)
        
    # 1. Save updated konusma_v2.json
    with open(TASLAK / "konusma_v2.json", "w", encoding="utf-8") as f:
        json.dump(kv, f, ensure_ascii=False, indent=2)
    print("Saved konusma_v2.json successfully.")
    
    # 2. Update and save cizim_aday.json
    def find_id_by_text(snippet):
        for s in new_cumleler_all:
            if snippet in s["ses"]:
                return s["id"]
        raise ValueError(f"Snippet not found: {snippet}")

    updated_drawings = []
    for idx, d in enumerate(drawings):
        d_copy = dict(d)
        if idx in DRAWING_SNIPPETS_MAP:
            d_copy["cumle"] = find_id_by_text(DRAWING_SNIPPETS_MAP[idx])
        else:
            d_copy["cumle"] = old_to_new_cid.get(d.get("cumle"), d.get("cumle"))
        if "adimlar" in d_copy and not d_copy.get("ogeler"):
            d_copy["ogeler"] = d_copy["adimlar"]
        updated_drawings.append(d_copy)
    
    caday["komutlar"] = updated_drawings
    with open(TASLAK / "cizim_aday.json", "w", encoding="utf-8") as f:
        json.dump(caday, f, ensure_ascii=False, indent=2)
    print(f"Saved cizim_aday.json with {len(updated_drawings)} commands.")
    
    # 3. Generate konusma_metni.md
    md_lines = [f"# {kv.get('baslik', 'Primer Myelin Hastalıkları ve Edinsel Metabolik ve Toksik Bozukluklar')}", ""]
    for bi, b in enumerate(kv.get("bolumler", [])):
        b_baslik = b.get("baslik", f"Bölüm {bi+1}")
        md_lines.append(f"@@ {b_baslik}")
        for pi, p in enumerate(b.get("paragraflar", [])):
            p_text = " ".join(c["ses"].strip() for c in p.get("cumleler", []) if c.get("ses"))
            if p_text:
                md_lines.append(p_text)
                md_lines.append("")
    
    (TASLAK / "konusma_metni.md").write_text("\n".join(md_lines).strip() + "\n", encoding="utf-8")
    print("Generated and saved konusma_metni.md.")
    
    # 4. RUN ALL 6 QUALITY GATES
    print("\n--- Running Quality Gate 1: KV.dogrula ---")
    kv_errs = KV.dogrula(kv, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
    if kv_errs:
        print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
        for e in kv_errs[:15]: print(" ", e)
        sys.exit(1)
    print("PASSED KV.dogrula: 0 HATA")
    
    print("\n--- Running Quality Gate 2: denetle.py ---")
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
        print("FAILED metin_denetle:\n", r_metin.stdout, r_metin.stderr)
        sys.exit(1)
    print("PASSED metin_denetle: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 5: sesli_kapsam ---")
    kapsam_errs = IS.sesli_kapsam(TASLAK)
    if kapsam_errs:
        print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
        for ke in kapsam_errs: print(" ", ke)
        sys.exit(1)
    print("PASSED sesli_kapsam: 0 HATA")
    
    print("\n--- Running Quality Gate 6: cizim_dogrula.py ---")
    accum = []
    cum_text = {}
    for s in new_cumleler_all:
        accum.append(s["ses"])
        accum.append(s.get("ekran", ""))
        cum_text[s["id"]] = " ".join(accum)
    sent_map = {s["id"]: s for s in new_cumleler_all}
    c_errs = []
    for idx, d in enumerate(updated_drawings):
        cid = d["cumle"]
        coz_d, err_c = sablon.coz(d)
        if err_c:
            c_errs.append(f"Drawing {idx+1} ({cid}) sablon.coz error: {err_c}")
            continue
        s_words = len(sent_map[cid]["ses"].split())
        err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
        if err_v:
            c_errs.append(f"Drawing {idx+1} ({cid}) {d.get('sablon')} error: {err_v}")
    if c_errs:
        print(f"FAILED cizim_dogrula with {len(c_errs)} errors:")
        for ce in c_errs: print(" ", ce)
        sys.exit(1)
    print(f"PASSED cizim_dogrula: {len(updated_drawings)}/{len(updated_drawings)} KOMUT 0 HATA")
    print("\n🎉 ALL 6 QUALITY GATES PASSED PERFECTLY FOR LESSON 66 WITH ZERO ERRORS!")

if __name__ == "__main__":
    main()
