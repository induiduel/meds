import json, os, sys
from scripts.build_deck_48_full import build_full_deck, DECK_ID

def apply():
    deck = build_full_deck()
    
    # 1. Update interactive_learning_decks.json
    interactive_path = "src/data/interactive_learning_decks.json"
    with open(interactive_path, "r", encoding="utf-8") as f:
        decks = json.load(f)
        
    found = False
    for idx, d in enumerate(decks):
        if d.get("id") == DECK_ID:
            decks[idx] = deck
            found = True
            break
            
    if not found:
        decks.append(deck)
        
    with open(interactive_path, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print(f"Updated {interactive_path}")
    
    # 2. Update items/k1p-k1-48-vulva-vajen-ve-serviks-hastaliklari.json
    item_path = f"src/data/decks/items/{DECK_ID}.json"
    os.makedirs(os.path.dirname(item_path), exist_ok=True)
    with open(item_path, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    print(f"Updated {item_path}")
    
    # 3. Update catalog.json entry
    catalog_path = "src/data/decks/catalog.json"
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        for cat_item in catalog:
            if cat_item.get("id") == DECK_ID:
                cat_item["slidesCount"] = len(deck["slides"])
                cat_item["flashcardsCount"] = len(deck["flashcards"])
                cat_item["description"] = deck["description"]
                break
        with open(catalog_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"Updated {catalog_path}")

    # 4. Update packages/k1p-k1-48-vulva-vajen-ve-serviks-hastaliklari/deck.json
    pkg_path = f"../packages/{DECK_ID}/deck.json"
    if os.path.exists(os.path.dirname(pkg_path)):
        with open(pkg_path, "w", encoding="utf-8") as f:
            json.dump(deck, f, ensure_ascii=False, indent=2)
        print(f"Updated {pkg_path}")
        
    print("All sync targets updated successfully!")

if __name__ == '__main__':
    apply()
