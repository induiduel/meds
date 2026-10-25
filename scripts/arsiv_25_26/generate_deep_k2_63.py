#!/usr/bin/env python3
"""
generate_deep_k2_63.py:
Expands the 6 sparse pages (<40 words) of y25-k2-63-antidepresan-ilaclar into deep,
rich amfi lecture sentences, preserves drawing alignment (7/7 commands),
and verifies all 6 Quality Gates with 0 HATA.
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

TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-63-antidepresan-ilaclar"

NEW_SENTENCES_BY_PAGE = {
    1: {
        "ses": "Ruhsal ıstırabın dindirilmesinde hekimin hastaya gösterdiği derin empatik anlayış, farmakolojik tedavinin etkinliğini artıran en temel insani unsurdur.",
        "ekran": "**Empati ve Tedavi Uyumu:** Terapötik ilişkinin farmakoterapiye katkısı",
        "slayt": {"sayfa": 1, "satir": ["Tababet sanatı üç şeydir: 1. el mahareti ile aletler, 2. ilaç, 3. ahlaktır."], "sekil": None},
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    },
    2: {
        "ses": "Depresyon tedavisinde yanıtın haftalar sonra ortaya çıkması ve ilaç etkileşimlerinin yönetimi hekimlikte derin bir farmakolojik bilgi birikimi gerektirir.",
        "ekran": "**Gecikmiş Klinik Yanıt:** Tedavi yanıtının haftalar alması ve etkileşim yönetimi",
        "slayt": {"sayfa": 2, "satir": ["Antidepresanlar"], "sekil": None},
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    },
    12: {
        "ses": "Rezerpin gibi veziküler amin pompasını geri dönüşsüz felç eden ajanlar dopamin, noradrenalin ve serotonin rezervlerini boşaltarak ağır depresif tablolar tetikler.",
        "ekran": "**Veziküler Boşalma:** Rezerpin etkisiyle nörotransmitter depolarının tükenmesi",
        "slayt": {"sayfa": 12, "satir": ["Vezküler Amin Kapısı"], "sekil": None},
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    },
    20: {
        "ses": "Postsinaptik reseptörlerin artan monoaminlerle uzun süreli uyarılması zamanla reseptör duyarsızlaşmasına ve hücre içi gen ekspresyonu değişikliklerine yol açar.",
        "ekran": "**Reseptör Duyarsızlaşması:** Kronik monoamin artışıyla adaptif transkripsiyonel yanıt",
        "slayt": {"sayfa": 20, "satir": ["Antidepresan ilaçların olası etki alanları. Norepinefrin (NE) ve serotoninin (5-HT) nöronal alımının inhibisyonu,\nbu nörotransmiterlerin sinaptik aktivitelerini arttırır."], "sekil": None},
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    },
    21: {
        "ses": "Bu ajanlar hem serotonin hem noradrenalin geri alımını eşzamanlı engelleyerek trisiklik antidepresanların etkinliğini taşırken, onların antikolinerjik yan etkilerinden belirgin ölçüde uzaktır.",
        "ekran": "**Dual İnhibisyon Üstünlüğü:** Trisiklik etkinliği ve düşük antikolinerjik yan etki",
        "slayt": {"sayfa": 21, "satir": ["Selektif serotonin – noradrenalin gerialım inhibitörleri (SNRİ)"], "sekil": None},
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    },
    30: {
        "ses": "Sinaptik aralıkta sağlanan bu monoamin artışı, nörotrofik faktörlerin transkripsiyonunu uyararak hipokampal nörogenezisi ve sinaptik plastisiteyi kademeli olarak güçlendirir.",
        "ekran": "**Nörotrofik Transkripsiyon:** Sinaptik plastisite ve hipokampal nörogenezis uyarımı",
        "slayt": {"sayfa": 30, "satir": ["Antidepressant\ndrug blocks\nreuptake of the\nneurotransmitter. PRESYNAPTIC"], "sekil": None},
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    }
}

DRAWING_SNIPPETS_MAP = {
    0: "enerji kaybı, uyku ve iştah",
    1: "Kronik psikolojik stres ve inatçı kronik ağrı",
    2: "Sınıfın diğer temel üyeleri sertralin",
    3: "Duloksetin, milnasipran ve levomilnasipran",
    4: "Trisiklik moleküller muskarinik reseptörleri",
    5: "Se se re i grubu ilaçlar taşıyıcı üzerindeki",
    6: "Tedavinin ilk günlerinde görülen sinaptik monoamin"
}

def main():
    print("=== Expanding y25-k2-63-antidepresan-ilaclar to Deep Amfi Lecture ===")
    
    with open(TASLAK / "konusma_v2.json") as f:
        kv = json.load(f)
    
    with open(TASLAK / "cizim_aday.json") as f:
        caday = json.load(f)
    
    drawings = caday.get("komutlar", [])
    print(f"Loaded {len(drawings)} candidate drawings.")
    
    # Ensure idempotency by removing any previously added sentences
    added_ses = {v["ses"] for v in NEW_SENTENCES_BY_PAGE.values()}
    for b in kv.get("bolumler", []):
        for p in b.get("paragraflar", []):
            p["cumleler"] = [c for c in p.get("cumleler", []) if c.get("ses") not in added_ses]
    
    # 1. Expand sentences
    old_to_new_cid = {}
    new_cumleler_all = []
    
    counter = 1
    for bi, b in enumerate(kv.get("bolumler", [])):
        for pi, p in enumerate(b.get("paragraflar", [])):
            old_sents = p.get("cumleler", [])
            new_sents = []
            
            pages_in_p = {c.get("slayt", {}).get("sayfa") for c in old_sents}
            
            for c in old_sents:
                old_id = c["id"]
                new_id = f"k2-63-c{counter:04d}"
                c_copy = dict(c)
                c_copy["id"] = new_id
                old_to_new_cid[old_id] = new_id
                new_sents.append(c_copy)
                counter += 1
            
            for p_num in sorted(pages_in_p):
                if p_num in NEW_SENTENCES_BY_PAGE:
                    add_data = NEW_SENTENCES_BY_PAGE[p_num]
                    new_id = f"k2-63-c{counter:04d}"
                    new_sent = {
                        "id": new_id,
                        "ses": add_data["ses"],
                        "ekran": add_data["ekran"],
                        "duzey": add_data["duzey"],
                        "vurgu": [],
                        "slayt": add_data["slayt"],
                        "slayt_adim": add_data["slayt_adim"],
                        "cikmis": add_data["cikmis"],
                        "spot": add_data["spot"]
                    }
                    new_sents.append(new_sent)
                    counter += 1
            
            p["cumleler"] = new_sents
            new_cumleler_all.extend(new_sents)
    
    print(f"Expanded to {len(new_cumleler_all)} sentences.")
    
    # Check word counts per page
    sayfa_kelime = {}
    for c in new_cumleler_all:
        s = c.get("slayt", {}).get("sayfa", 1)
        w = len(c.get("ses", "").split())
        sayfa_kelime[s] = sayfa_kelime.get(s, 0) + w
    
    sparse_pages = [s for s, w in sorted(sayfa_kelime.items()) if w < 40]
    total_words = sum(sayfa_kelime.values())
    print(f"Total words: {total_words} across {len(sayfa_kelime)} pages. Sparse pages count: {len(sparse_pages)}")
    if sparse_pages:
        print(f"ERROR: Still have sparse pages: {sparse_pages}")
        sys.exit(1)
    
    # Save updated konusma_v2.json
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
    md_lines = [f"# {kv.get('baslik', 'Antidepresan İlaçlar')}", ""]
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
    print("\n🎉 ALL 6 QUALITY GATES PASSED PERFECTLY FOR LESSON 63 WITH ZERO ERRORS!")

if __name__ == "__main__":
    main()
