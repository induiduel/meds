import os
import json
import re

DECKS_JSON = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/src/data/interactive_learning_decks.json")
CATALOG_TS = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/src/data/deckPdfCatalog.ts")
TXT_DIR = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')) + "/ders_notlari_txt")
OUTPUT_MAPPING_JSON = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/src/data/slidePdfMappings.json")

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def parse_catalog():
    # Read catalog from ts file
    with open(CATALOG_TS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to extract deck mappings
    pattern = r'"([^"]+)":\s*\{\s*"deckId":\s*"([^"]+)",\s*"deckTitle":\s*"([^"]+)",\s*"fileId":\s*"([^"]*)",\s*"fileName":\s*"([^"]*)",\s*"driveUrl":\s*"([^"]*)",\s*"localFileName":\s*"([^"]*)"'
    matches = re.findall(pattern, content)
    catalog = {}
    for m in matches:
        catalog[m[0]] = {
            "deckId": m[1],
            "deckTitle": m[2],
            "fileId": m[3],
            "fileName": m[4],
            "driveUrl": m[5],
            "localFileName": m[6] or m[4]
        }
    return catalog

def find_txt_file(pdf_name):
    clean_target = pdf_name.replace('.pdf', '').strip()
    files = os.listdir(TXT_DIR)
    # Direct match with .txt
    for f in files:
        if f.replace('.txt', '').strip().lower() == clean_target.lower():
            return os.path.join(TXT_DIR, f)
    # Fuzzy match
    target_words = set(re.findall(r'\w{3,}', clean_target.lower()))
    best_file = None
    best_score = 0
    for f in files:
        f_words = set(re.findall(r'\w{3,}', f.replace('.txt', '').lower()))
        score = len(target_words.intersection(f_words))
        if score > best_score and score >= 2:
            best_score = score
            best_file = f
    if best_file:
        return os.path.join(TXT_DIR, best_file)
    return None

def extract_pages_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    splits = re.split(r'---\s*\[SAYFA\s*(\d+)\]\s*---', text)
    pages = {}
    if len(splits) > 1:
        for i in range(1, len(splits), 2):
            p_num = int(splits[i])
            p_text = splits[i+1].strip()
            pages[p_num] = p_text
    return pages

def main():
    print("=== Slayt - Orijinal PDF Sayfa Eşleştirme Motoru ===")
    catalog = parse_catalog()
    print(f"Katalogda {len(catalog)} güverte meta verisi bulundu.")
    
    with open(DECKS_JSON, 'r', encoding='utf-8') as f:
        decks = json.load(f)
        
    master_mappings = {}
    updated_decks_count = 0
    
    for deck in decks:
        did = deck.get('id') or deck.get('deckId')
        slides = deck.get('slides', [])
        meta = catalog.get(did)
        
        if not meta or not slides:
            continue
            
        pdf_name = meta.get('localFileName') or meta.get('fileName')
        txt_path = find_txt_file(pdf_name) if pdf_name else None
        
        pages = {}
        total_pdf_pages = 0
        if txt_path and os.path.exists(txt_path):
            pages = extract_pages_from_txt(txt_path)
            total_pdf_pages = max(pages.keys()) if pages else 0
            
        # If no txt pages found, fallback to proportional
        n_slides = len(slides)
        if total_pdf_pages == 0:
            total_pdf_pages = max(n_slides * 2, 30)
            
        deck_mapping = {
            "deckId": did,
            "deckTitle": deck.get('title'),
            "fileName": pdf_name,
            "fileId": meta.get('fileId'),
            "driveUrl": meta.get('driveUrl'),
            "totalPdfPages": total_pdf_pages,
            "slides": {}
        }
        
        # Calculate matching scores for each slide
        prev_page = 1
        for i, slide in enumerate(slides):
            s_num = slide.get('slideNumber', i + 1)
            title = slide.get('title', '')
            content = slide.get('content', '') or slide.get('synthesisNarrative', '')
            
            # Significant keywords
            title_kw = set(re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ]{4,}', title.lower()))
            content_kw = set(re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ]{5,}', content.lower()[:350]))
            all_kw = title_kw.union(list(content_kw)[:15])
            
            scored_pages = []
            for p_num, p_text in pages.items():
                p_lower = p_text.lower()
                t_score = sum(3 for w in title_kw if w in p_lower)
                b_score = sum(1 for w in all_kw if w in p_lower)
                total_sc = t_score + b_score
                if total_sc > 0:
                    scored_pages.append((p_num, total_sc))
                    
            scored_pages.sort(key=lambda x: x[1], reverse=True)
            
            # Determine startPage and endPage with sequential smoothing
            if scored_pages and scored_pages[0][1] >= 2:
                top_pages = [p[0] for p in scored_pages[:4]]
                # Filter out outlier jumps backward if possible
                coherent_pages = [p for p in top_pages if p >= prev_page - 2]
                if coherent_pages:
                    primary_p = coherent_pages[0]
                else:
                    primary_p = top_pages[0]
            else:
                # Proportional estimate
                prop_p = int(round(1 + ((i) / max(1, n_slides - 1)) * (total_pdf_pages - 1)))
                primary_p = max(prev_page, min(prop_p, total_pdf_pages))
                
            # Define window around primary page
            # Usually 1 slide covers 1 to 3 PDF pages
            start_p = max(1, primary_p - 1 if primary_p > 1 and primary_p == prev_page else primary_p)
            end_p = min(total_pdf_pages, max(start_p, primary_p + 1))
            
            # Smooth forward progression
            start_p = max(start_p, prev_page)
            end_p = max(start_p, end_p)
            prev_page = start_p
            
            page_range = [start_p, end_p]
            citation_str = f"Sayfa {start_p}-{end_p}" if start_p != end_p else f"Sayfa {start_p}"
            
            deck_mapping["slides"][str(s_num)] = {
                "slideNumber": s_num,
                "title": title,
                "primaryPage": primary_p,
                "startPage": start_p,
                "endPage": end_p,
                "pageRange": page_range,
                "citation": citation_str,
                "fileName": pdf_name
            }
            
            # Update slide in deck
            slide["sourcePdf"] = {
                "fileName": pdf_name,
                "fileId": meta.get('fileId'),
                "startPage": start_p,
                "endPage": end_p,
                "primaryPage": primary_p,
                "citation": citation_str
            }
            slide["sourceCitation"] = citation_str
            slide["sourcePage"] = primary_p
            slide["sourcePageRange"] = page_range
            
        master_mappings[did] = deck_mapping
        updated_decks_count += 1
        print(f"[+] {did:38s}: {n_slides} slayt -> {total_pdf_pages} PDF sayfası eşleştirildi.")
        
    # Write slidePdfMappings.json
    with open(OUTPUT_MAPPING_JSON, 'w', encoding='utf-8') as f:
        json.dump(master_mappings, f, ensure_ascii=False, indent=2)
    print(f"\n[+] {len(master_mappings)} güverte eşleştirmesi {OUTPUT_MAPPING_JSON} dosyasına kaydedildi.")
    
    # Save updated decks
    with open(DECKS_JSON, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print(f"[+] {updated_decks_count} güverte interaktif veritabanında sourcePdf meta verileriyle güncellendi.")

if __name__ == "__main__":
    main()
