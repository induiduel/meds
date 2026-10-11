import json, os, sys

def apply_deck(deck):
    deck_id = deck["id"]
    print(f"Applying deck {deck_id}...")
    
    # Base directory for medsor
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    meds_dir = os.path.join(repo_root, "meds")
    
    # 1. Update interactive_learning_decks.json
    interactive_path = os.path.join(meds_dir, "src/data/interactive_learning_decks.json")
    if os.path.exists(interactive_path):
        with open(interactive_path, "r", encoding="utf-8") as f:
            decks = json.load(f)
            
        found = False
        for idx, d in enumerate(decks):
            if d.get("id") == deck_id:
                decks[idx] = deck
                found = True
                break
        if not found:
            decks.append(deck)
            
        with open(interactive_path, "w", encoding="utf-8") as f:
            json.dump(decks, f, ensure_ascii=False, indent=2)
        print(f"Updated {interactive_path}")
        
    # 2. Update src/data/decks/items/<id>.json
    item_path = os.path.join(meds_dir, f"src/data/decks/items/{deck_id}.json")
    os.makedirs(os.path.dirname(item_path), exist_ok=True)
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    print(f"Updated {item_path}")
    
    # 3. Update catalog.json
    catalog_path = os.path.join(meds_dir, "src/data/decks/catalog.json")
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        for cat_item in catalog:
            if cat_item.get("id") == deck_id:
                cat_item["slidesCount"] = len(deck["slides"])
                cat_item["flashcardsCount"] = len(deck.get("flashcards", []))
                cat_item["description"] = deck.get("description", "")
                cat_item["totalSlides"] = len(deck["slides"])
                cat_item["slideCount"] = len(deck["slides"])
                cat_item["isNew"] = True
                cat_item["version"] = "2.0"
                break
        with open(catalog_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"Updated {catalog_path}")

    # 4. Paketler tek kaynaktan yeniden üretilir (meds_export/deste_paketleri).
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_deck_packages.py')], check=False)

    print(f"Deck {deck_id} applied successfully!")

if __name__ == '__main__':
    print("Helper loaded.")
