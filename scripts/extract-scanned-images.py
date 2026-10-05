r"""
MedSoru Scanned PDF Image Extractor
Extracts images from scanned PDFs in C:\Users\indui\Desktop\meds_database\meds_sorular
and saves them to C:\Users\indui\Desktop\meds_database\meds_sorular_images\[pdf_name]\
"""

import os
import sys
import pypdf
from PIL import Image

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')))
SORULAR_DIR = os.path.join(BASE_DIR, "meds_sorular")
IMAGES_DIR = os.path.join(BASE_DIR, "meds_sorular_images")

os.makedirs(IMAGES_DIR, exist_ok=True)

def process_pdf(pdf_path):
    pdf_name = os.path.basename(pdf_path)
    base_name = os.path.splitext(pdf_name)[0].strip()
    out_dir = os.path.join(IMAGES_DIR, base_name)
    os.makedirs(out_dir, exist_ok=True)

    print(f"\nProcessing PDF: {pdf_name}")
    try:
        reader = pypdf.PdfReader(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_name}: {e}")
        return []

    extracted_images = []
    img_counter = 0

    for page_idx, page in enumerate(reader.pages):
        try:
            for img in page.images:
                img_counter += 1
                out_path = os.path.join(out_dir, f"page_{page_idx+1:03d}_img_{img_counter:03d}.png")
                
                # Check if already extracted
                if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                    extracted_images.append(out_path)
                    continue

                with open(out_path, "wb") as f:
                    f.write(img.data)
                
                # Verify and filter out tiny icons/banners
                try:
                    with Image.open(out_path) as im:
                        w, h = im.size
                        # Only keep images that could be questions (at least 300x300)
                        if w < 250 or h < 250:
                            os.remove(out_path)
                            continue
                except Exception:
                    pass

                extracted_images.append(out_path)
        except Exception as e:
            print(f"  Warning on page {page_idx+1}: {e}")

    print(f"  ✓ {len(extracted_images)} valid question images extracted to: {out_dir}")
    return extracted_images

def main():
    if not os.path.exists(SORULAR_DIR):
        print(f"Directory not found: {SORULAR_DIR}")
        return

    # Target specific scanned/image-based PDFs or all scanned PDFs
    target_pdfs = [
        "3. Sınıf 1. Kurul.pdf",
        "3.sınıf 4.kurul .pdf",
        "2023-2024 DÖNEM 3 KURUL 4 ÇIKMIŞLAR _250311_151638.pdf",
        "sorular.pdf",
        "Final Sınavı Cevap Anahtarı.pdf",
        "Kurul 2 Cevap Anahtarı.pdf",
        "Kurul III Cevap Anahtarı.pdf",
        "Kurul IV Cevap Anahtarı.pdf",
        "Kurul V Cevap Anahtarı.pdf",
        "Kurul VI Cevap Anahtarı.pdf"
    ]

    total_all_images = 0
    for fname in target_pdfs:
        full_path = os.path.join(SORULAR_DIR, fname)
        if os.path.exists(full_path):
            imgs = process_pdf(full_path)
            total_all_images += len(imgs)
        else:
            # Try case-insensitive search
            found = False
            for real_f in os.listdir(SORULAR_DIR):
                if real_f.lower() == fname.lower():
                    imgs = process_pdf(os.path.join(SORULAR_DIR, real_f))
                    total_all_images += len(imgs)
                    found = True
                    break

    print(f"\n=======================================================")
    print(f"  Total Extracted Question Images: {total_all_images}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
