import json
import os
import re
import sys
import shutil

SCRATCH_DIR = (__import__('tempfile').gettempdir())
DECKS_JSON = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/src/data/interactive_learning_decks.json")

FILES = [
    ("deck_genital_enfeksiyonlar.json", "learn-genital-enfeksiyonlar", "1e6198aa-321f-46ce-b6d7-7b6bda17f3be"),
    ("deck_bobrek_tumorleri.json", "learn-bobrek-tumorleri", "5ebe233a-5e70-47ad-8110-a980d81223fb"),
    ("deck_mesane_tumorleri.json", "learn-mesane-hastaliklari-tumorleri", "e3e5492e-8ca9-4a67-a961-26a58e439909"),
    ("deck_glomeruler_nefrotik.json", "learn-glomeruler-hastaliklar-nefrotik", "3c2321ea-1fb1-4398-964b-1b9ea66482a7"),
    ("deck_glomeruler_nefritik.json", "learn-glomeruler-hastaliklar-nefritik", "8e5077c0-8f8e-4055-a70b-9587e801ff4c"),
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
    print("=== Batch 5 Integration & Validation Script ===")
    
    generated_decks = {}
    for filename, expected_id, conv_id in FILES:
        filepath = os.path.join(SCRATCH_DIR, filename)
        if not os.path.exists(filepath):
            # Check subagent scratch dir
            alt_path = rf"C:\Users\indui\.gemini\antigravity\brain\{conv_id}\scratch\{filename}"
            if os.path.exists(alt_path):
                print(f"[+] Copying {filename} from subagent dir: {alt_path}")
                shutil.copy(alt_path, filepath)
            else:
                print(f"[-] Missing file: {filepath} (and alt {alt_path})")
                sys.exit(1)
        
        with open(filepath, "r", encoding="utf-8") as f:
            deck_data = json.load(f)
            
        did = deck_data.get("id") or deck_data.get("deckId")
        if not did:
            did = expected_id
        deck_data["id"] = did
        deck_data["deckId"] = did
            
        slides = deck_data.get("slides", [])
        print(f"\n[+] Inspecting: {did}")
        print(f"    Title: {deck_data.get('title')}")
        print(f"    Slide count: {len(slides)}")
        
        if len(slides) != 24:
            print(f"[-] ERROR: Expected 24 slides, got {len(slides)}")
            sys.exit(1)
            
        total_chars = 0
        bad_count = 0
        q_count = 0
        
        for i, s in enumerate(slides):
            c = s.get("content") or s.get("synthesisNarrative") or ""
            s["content"] = c
            s["synthesisNarrative"] = c
            s["slideNumber"] = i + 1
            
            title = s.get("title", "")
            total_chars += len(c)
            
            for pat in BAD_PATTERNS:
                if re.search(pat, c) or re.search(pat, title):
                    print(f"    [-] Bad pattern '{pat}' found in slide {i+1} ({title})")
                    bad_count += 1
                    
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
                    
                if len(opts) == 5 and isinstance(ans, int) and 0 <= ans <= 4:
                    q_count += 1
                else:
                    print(f"    [-] Invalid question in slide {i+1}: options={len(opts)}, ans={ans} (raw={pq.get('correctAnswer')})")
            else:
                print(f"    [-] Missing practice question in slide {i+1}")
                
        avg_chars = total_chars / len(slides)
        print(f"    Avg content chars: {avg_chars:.1f}")
        print(f"    Valid practice questions: {q_count}/24")
        print(f"    Bad pattern matches: {bad_count}")
        
        if bad_count > 0:
            print("[-] Terminating due to bad patterns.")
            sys.exit(1)
        if avg_chars < 1400:
            print("[-] Terminating: average content length below threshold (1400).")
            sys.exit(1)
            
        generated_decks[did] = deck_data

    # Merge into main interactive_learning_decks.json
    with open(DECKS_JSON, "r", encoding="utf-8") as f:
        existing_decks = json.load(f)
        
    print(f"\nExisting decks in main file: {len(existing_decks)}")
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
            print(f"[+] Successfully replaced deck: {did}")
        else:
            updated_decks.append(d)
            
    for did, new_deck in generated_decks.items():
        if did not in updated_ids:
            updated_decks.append(new_deck)
            print(f"[+] Added new deck: {did}")
            
    with open(DECKS_JSON, "w", encoding="utf-8") as f:
        json.dump(updated_decks, f, ensure_ascii=False, indent=2)
        
    print(f"\n[+] Total decks after merge: {len(updated_decks)}")
    print("[+] Successfully wrote updated interactive_learning_decks.json!")

if __name__ == "__main__":
    main()
