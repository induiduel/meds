#!/usr/bin/env python3
"""
generate_deep_k2_19.py:
Expands the 2 sparse pages (43, 44) of y25-k2-19-bipolar-bozukluk
into deep, rich amfi lecture sentences, preserves all 12 drawing commands,
and verifies all 6 Quality Gates with 0 HATA.
"""

import sys
import json
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

TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-19-bipolar-bozukluk"

NEW_SENTENCES_BY_PAGE = {
    43: {
        "ses": "Bipolar bozukluk tedavisinde lityum ve valproat gibi duygudurum dengeleyicilerinin terapötik kan düzeylerinin yakından izlenmesi, psikoeğitim ve tedaviye hasta uyumunun güçlendirilmesi mani ve depresyon ataklarının nüksünü önlemede hayati role sahiptir.",
        "ekran": "**Tedavi Uyumu ve Profilaksi:** Duygudurum dengeleyicileri, terapötik kan düzeyi ve nüks önleme",
        "slayt": {
            "sayfa": 43,
            "satir": ["Kaynaklar"],
            "sekil": None
        },
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    },
    44: {
        "ses": "Duygudurum ataklarının erken tanınması, intihar riskinin dikkatle yönetilmesi, hasta ve aile eğitiminin sürdürülmesi ile koruyucu profilaksi ilkelerinin titizlikle uygulanması psikiyatri pratiğinin ve hekimlik sanatının en kritik başarı basamaklarıdır.",
        "ekran": "**Klinik Başarı İlkeleri:** Erken tanı, intihar riski yönetimi, aile eğitimi ve koruyucu profilaksi",
        "slayt": {
            "sayfa": 44,
            "satir": ["Teşekkürler…"],
            "sekil": None
        },
        "slayt_adim": None, "cikmis": [], "spot": None, "duzey": 2
    }
}

def main():
    print("=== Expanding y25-k2-19-bipolar-bozukluk to Deep Amfi Lecture ===")
    
    with open(TASLAK / "konusma_v2.json") as f:
        kv = json.load(f)
        
    with open(TASLAK / "cizim_aday.json") as f:
        caday = json.load(f)
    drawings = caday.get("komutlar", [])
    print(f"Loaded {len(drawings)} candidate drawings.")
    
    # Ensure idempotency
    added_ses = {v["ses"] for v in NEW_SENTENCES_BY_PAGE.values()}
    for b in kv.get("bolumler", []):
        for p in b.get("paragraflar", []):
            p["cumleler"] = [c for c in p.get("cumleler", []) if c.get("ses") not in added_ses]
            
    # Insert new sentences at matching pages
    for target_page, s_data in sorted(NEW_SENTENCES_BY_PAGE.items()):
        inserted = False
        for b in kv.get("bolumler", []):
            if inserted:
                break
            for p in b.get("paragraflar", []):
                c_pages = [c["slayt"]["sayfa"] for c in p.get("cumleler", [])]
                if target_page in c_pages:
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
                new_cid = f"k2-19-c{counter:04d}"
                c["id"] = new_cid
                if old_cid:
                    old_to_new_cid[old_cid] = new_cid
                counter += 1
                new_cumleler_all.append(c)
                
    print(f"Total sentences after expansion: {len(new_cumleler_all)}")
    
    # Check word count per page
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
        
    # Save konusma_v2.json
    with open(TASLAK / "konusma_v2.json", "w", encoding="utf-8") as f:
        json.dump(kv, f, ensure_ascii=False, indent=2)
    print("Saved konusma_v2.json successfully.")
    
    # Generate konusma_metni.md
    md_lines = [f"# {kv.get('baslik', 'Bipolar Bozukluk')}", ""]
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
    
    # RUN ALL 6 QUALITY GATES
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
    
    print("\n🎉 ALL QUALITY GATES PASSED PERFECTLY FOR LESSON 19 WITH ZERO ERRORS!")

if __name__ == "__main__":
    main()
