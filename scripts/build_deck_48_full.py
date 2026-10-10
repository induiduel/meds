import json, os, sys

import scripts.build_k1_48_data.gen_s1 as s1
import scripts.build_k1_48_data.gen_s2 as s2
import scripts.build_k1_48_data.gen_s3 as s3
import scripts.build_k1_48_data.gen_s4 as s4
import scripts.build_k1_48_data.gen_s5 as s5
import scripts.build_k1_48_data.gen_s6 as s6
import scripts.build_k1_48_data.gen_s7 as s7
import scripts.build_k1_48_data.gen_s8 as s8
import scripts.build_k1_48_data.gen_s9 as s9
import scripts.build_k1_48_data.gen_s10 as s10
from scripts.build_k1_48_data.flashcards_48 import get_deck_48_flashcards

DECK_ID = "k1p-k1-48-vulva-vajen-ve-serviks-hastaliklari"

def build_full_deck():
    all_sections = [
        s1.get_s1_slides(),
        s2.get_s2_slides(),
        s3.get_s3_slides(),
        s4.get_s4_slides(),
        s5.get_s5_slides(),
        s6.get_s6_slides(),
        s7.get_s7_slides(),
        s8.get_s8_slides(),
        s9.get_s9_slides(),
        s10.get_s10_slides()
    ]
    
    slides = []
    for sec in all_sections:
        slides.extend(sec)
        
    assert len(slides) == 100, f"Expected 100 slides, got {len(slides)}"
    
    # 16 learning outcomes mapped to syllabus
    learning_outcomes = [
        "Vulvanın anatomik ve histolojik katmanlarını (labia majora kıllı derisi ve labia minora mukozası) tanımlamak.",
        "Vulvitin irritan ve enfeksiyöz nedenlerini ayırmak, Bartholin bezi kisti ve apse komplikasyonunu açıklamak.",
        "Liken sklerozun histopatolojisini (epidermis incelmesi, dermal fibrozis) ve skuamöz hiperplaziden (akantoz) farkını bilmek.",
        "Vulva lökoplakisinde biyopsi zorunluluğunu ve lökoplaki yapan premalign/benign süreçleri kavramak.",
        "Kondiloma akuminatum (HPV 6/11, koilositoz) ile kondiloma lata (Treponema pallidum) ayrımını yapmak.",
        "Vulvar skuamöz karsinomun iki patogenetik yolunu (HPV pozitif bazaloid vs HPV negatif keratinize) karşılaştırmak.",
        "Diferansiye VIN (dVIN) lezyonunun histopatolojik tuzaklarını ve p53 mutasyonu ilişkisini açıklamak.",
        "Ekstramammary Paget hastalığının klinik taklit özelliğini ve meme Paget'inden temel farkını tanımlamak.",
        "Vajinanın Gartner kanal kistinin embriyolojik kökenini (Wolffian kalıntısı) ve yerleşimini bilmek.",
        "Üç majör vajinit etkenini (Candida hifleri, Trichomonas hareketli paraziti, Gardnerella clue cells) mikroskobik olarak ayırt etmek.",
        "Vajinal skuamöz karsinomun risk faktörlerini (önceki serviks Ca) ve lenfatik drenajını kavramak.",
        "Embriyonel rabdomiyosarkomun (Sarkoma Botryoides) pediatrik klinik tablosunu, kambiyum tabakasını ve Desmin/Miyogenin pozitifliğini bilmek.",
        "Serviks histolojisini, skuamöz metaplaziyi ve transformasyon zonunun karsinogenezdeki kilit rolünü kavramak.",
        "Yüksek riskli HPV E6 ve E7 onkoproteinlerinin p53 ve pRb inaktivasyon mekanizmalarını açıklamak.",
        "Pap smear taramasını, Bethesda sınıflamasını (LSIL/CIN 1 vs HSIL/CIN 2-3) ve kolposkopi biyofiziğini (asetobeyaz epitel, Schiller testi) bilmek.",
        "İnvaziv serviks karsinomunun doğrudan pelvik yayılımını, üreter obstrüksiyonunu ve en sık ölüm nedeni olan üremiyi açıklamak."
    ]
    
    flashcards = get_deck_48_flashcards()
    
    deck = {
        "id": DECK_ID,
        "title": "Vulva, Vajen ve Serviks Hastalıkları",
        "description": "Kurul 1 Tıbbi Patoloji amfi ders notu ve Robbins referanslarıyla tam uyumlu; vulva, vajen ve serviksin inflamatuvar, premalign ve malign patolojilerini, HPV karsinogenezini ve tarama ilkelerini kapsayan 100 slaytlık master modül.",
        "courseCode": "TIP 310",
        "curriculumPeriod": "Dönem 3 · Kurul 1",
        "committee": "Ürogenital ve Obstetrik Kurulu",
        "date": "07.10.2026",
        "instructor": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji ABD)",
        "sourcePdf": "meds_database_v2/ders_notlari_k1/notlar/48_vulva_vajen_ve_serviks_hastaliklari.md",
        "learningOutcomes": learning_outcomes,
        "flashcards": flashcards,
        "slides": slides
    }
    
    return deck

if __name__ == '__main__':
    deck = build_full_deck()
    print(f"Deck built successfully:")
    print(f" - Title: {deck['title']}")
    print(f" - Slides: {len(deck['slides'])}")
    print(f" - Flashcards: {len(deck['flashcards'])}")
    print(f" - Learning outcomes: {len(deck['learningOutcomes'])}")
