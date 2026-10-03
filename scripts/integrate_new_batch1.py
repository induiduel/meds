import json
import os
import re
import sys
import shutil

SCRATCH_DIR = r"C:\Users\indui\.gemini\antigravity\brain\386176b3-c821-4f99-a837-6f25ae2aca35\scratch"
DECKS_JSON = r"c:\Users\indui\Desktop\meds\src\data\interactive_learning_decks.json"

FILES = [
    ("deck_asiri_duyarlilik.json", "learn-asiri-duyarlilik-ve-otoimmunite"),
    ("deck_tumor_biyolojisi.json", "learn-tumor-biyolojisi-terminolojisi"),
    ("deck_akut_enflamasyon.json", "deck-acute-inflammation-pathology"),
]

BAD_PATTERNS = [
    r'\uf0d8', r'', r'🔲',
    r'Morfolojik ve H[uü]cresel Bulgular',
    r'Temel Patofizyolojik Odak',
    r'Klinik Tan[iı] ve Ay[iı]r[iı]c[iı] Tan[iı]',
    r'Tedavi ve Y[oö]netim',
    r'S[iı]k Yap[iı]lan Hatalar',
]

def main():
    print("=== Yeni Mimari Batch 1 (3 Ders) Entegrasyon ve Doğrulama ===")
    
    generated_decks = {}
    for filename, expected_id in FILES:
        filepath = os.path.join(SCRATCH_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[-] Missing file: {filepath}")
            sys.exit(1)
        
        with open(filepath, "r", encoding="utf-8") as f:
            deck_data = json.load(f)
            
        did = deck_data.get("id") or deck_data.get("deckId")
        if not did:
            did = expected_id
        deck_data["id"] = did
        deck_data["deckId"] = did
            
        slides = deck_data.get("slides", [])
        print(f"\n[+] İnceleniyor: {did}")
        print(f"    Başlık: {deck_data.get('title')}")
        print(f"    Dinamik Slayt Sayısı: {len(slides)}")
        
        if len(slides) < 15:
            print(f"[-] UYARI: Çok az slayt üretilmiş: {len(slides)}")
            sys.exit(1)
            
        total_chars = 0
        bad_count = 0
        q_count = 0
        incomplete_sentence_warnings = 0
        
        for i, s in enumerate(slides):
            c = s.get("content") or s.get("synthesisNarrative") or ""
            s["content"] = c
            s["synthesisNarrative"] = c
            s["slideNumber"] = i + 1
            
            title = s.get("title", "")
            total_chars += len(c)
            
            # Bad patterns check
            for pat in BAD_PATTERNS:
                if re.search(pat, c) or re.search(pat, title):
                    print(f"    [-] Yasaklı kalıp '{pat}' bulundu: Slayt {i+1} ({title})")
                    bad_count += 1
            
            # Complete sentence check (prose shouldn't end abruptly without punctuation)
            stripped_c = c.strip()
            if stripped_c and not stripped_c.endswith(('.', '!', '?', ':', ')', '`', '*', '"', "'", '’', '”')):
                print(f"    [!] Slayt {i+1} metni yarım kalmış görünüyor (noktalama ile bitmiyor): ...{stripped_c[-40:]}")
                incomplete_sentence_warnings += 1
                    
            pq = s.get("practiceQuestion")
            if pq and isinstance(pq, dict):
                opts = pq.get("options", [])
                ans = pq.get("correctAnswer")
                if isinstance(ans, str) and ans.strip().upper() in ["A", "B", "C", "D", "E"]:
                    ans = ord(ans.strip().upper()) - ord("A")
                    pq["correctAnswer"] = ans
                elif ans is None and "answer" in pq:
                    ans_str = str(pq["answer"]).strip().upper()
                    if ans_str in ["A", "B", "C", "D", "E"]:
                        ans = ord(ans_str) - ord("A")
                        pq["correctAnswer"] = ans
                if "answer" not in pq and isinstance(ans, int) and 0 <= ans <= 4:
                    pq["answer"] = chr(ord("A") + ans)
                elif isinstance(ans, int) and 0 <= ans <= 4:
                    pq["answer"] = chr(ord("A") + ans)
                    
                q_text = pq.get("question", "").strip()
                exp = pq.get("explanation", "").strip()
                if len(opts) == 5 and isinstance(ans, int) and 0 <= ans <= 4 and len(q_text) > 20 and len(exp) > 20:
                    q_count += 1
                else:
                    print(f"    [-] Geçersiz / eksik soru Slayt {i+1}: opts={len(opts)}, ans={ans}, q_len={len(q_text)}, exp_len={len(exp)}")
            else:
                print(f"    [-] Eksik soru: Slayt {i+1}")
                
        avg_chars = total_chars / len(slides)
        print(f"    Ortalama İçerik Karakteri: {avg_chars:.1f} (Toplam: {total_chars:,} karakter)")
        print(f"    Geçerli Pekiştirme Sorusu: {q_count}/{len(slides)}")
        print(f"    Yasaklı Kalıp Eşleşmesi: {bad_count}")
        print(f"    Yarım Cümle Uyarısı: {incomplete_sentence_warnings}")
        
        if bad_count > 0:
            print("[-] Terminating due to bad patterns.")
            sys.exit(1)
        if avg_chars < 1500:
            print("[-] Terminating: average content length below threshold (1500).")
            sys.exit(1)
            
        generated_decks[did] = deck_data

    # Merge into main interactive_learning_decks.json
    with open(DECKS_JSON, "r", encoding="utf-8") as f:
        existing_decks = json.load(f)
        
    print(f"\nMevcut veritabanındaki toplam güverte: {len(existing_decks)}")
    updated_decks = []
    updated_ids = set()
    
    for d in existing_decks:
        did = d.get("id") or d.get("deckId")
        if did in generated_decks:
            new_deck = generated_decks[did]
            new_deck["id"] = did
            if "category" not in new_deck or not new_deck["category"]:
                new_deck["category"] = d.get("category", "Dönem 3 Kurul 1")
            updated_decks.append(new_deck)
            updated_ids.add(did)
            print(f"[+] Başarıyla güncellendi: {did} ({len(new_deck['slides'])} slayt)")
        else:
            updated_decks.append(d)
            
    for did, new_deck in generated_decks.items():
        if did not in updated_ids:
            updated_decks.append(new_deck)
            print(f"[+] Yeni güverte eklendi: {did} ({len(new_deck['slides'])} slayt)")
            
    with open(DECKS_JSON, "w", encoding="utf-8") as f:
        json.dump(updated_decks, f, ensure_ascii=False, indent=2)
        
    print(f"\n[+] Güncelleme sonrası toplam güverte: {len(updated_decks)}")
    print("[+] interactive_learning_decks.json başarıyla kaydedildi!")

if __name__ == "__main__":
    main()
