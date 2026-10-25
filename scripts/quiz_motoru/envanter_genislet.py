#!/usr/bin/env python3
"""Faz 2: Birleştirilmiş Derin Analiz ve Atomik Bilgi Envanteri Yardımcısı.

Sesli ders (Audio Lesson) ve Quiz motorunun ortak Single Source of Truth
olarak kullanacağı 'atomik_bilgi_envanteri.json' dosyasını derler, doğrular ve bağlar.
Mükerrer LLM çağrısını ve çifte analiz maliyetini kesin olarak engeller.
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List

MEDS = Path(__file__).resolve().parents[2]


def kategori_tahmin_et(terim: str, cumle: str) -> str:
    """Metin içeriğine göre atomik bilgi kategorisi önerir."""
    t_low = (terim + " " + cumle).casefold()
    if any(k in t_low for k in ["reseptör", "reseptoru", "alfa-", "beta-", "agonist", "antagonist", "blokör"]):
        return "receptor"
    if any(k in t_low for k in ["enzim", "az", "kinaz", "sentaz", "hidrolaz", "inhibitor", "indukte"]):
        return "enzyme"
    if any(k in t_low for k in ["klirens", "yarı ömür", "biyoyararlanım", "cyp", "adme", "eliminasyon", "dağılım hacmi"]):
        return "pharmacokinetics"
    if any(k in t_low for k in ["yan etki", "toksisite", "kontrendike", "advers", "zehirlenme", "teratojen"]):
        return "side_effect"
    if any(k in t_low for k in ["hastalık", "sendrom", "yetmezlik", "enfeksiyon", "hipertansiyon"]):
        return "disease"
    if any(k in t_low for k in ["semptom", "bulgu", "belirti", "triad"]):
        return "symptom"
    if any(k in t_low for k in ["grubu", "sınıfı", "türevi", "jenerasyonu"]):
        return "drug_class"
    if any(k in t_low for k in ["gen", "mutasyon", "polimorfizm"]):
        return "gene"
    if any(k in t_low for k in ["protein", "kanal", "pompa", "taşıyıcı"]):
        return "protein"
    if any(k in t_low for k in ["ilaç", "tedavi", "endikasyon", "kullanılır", "etken"]):
        return "drug"
    return "clinical_note"


def envanter_derle(taslak_klasoru: Path) -> Dict[str, Any]:
    """Taslak klasöründeki ders_paketi.json, sayfa_haritasi.json ve cikmis_baglantilari.json'dan
    tekil atomik bilgi envanterini derler veya doğrular."""
    ders_paketi_dosyasi = taslak_klasoru / "ders_paketi.json"
    if not ders_paketi_dosyasi.exists():
        raise FileNotFoundError(f"ders_paketi.json bulunamadı: {ders_paketi_dosyasi}")

    dp = json.loads(ders_paketi_dosyasi.read_text())
    ders_id = dp.get("id", taslak_klasoru.name)
    kurul = dp.get("kurul", 2)
    konu = dp.get("konu", "")
    ders_adi = dp.get("ders", "Tıbbi Farmakoloji")
    
    # Çıkmış soru bağları
    cikmis_map = {}
    cik_dosya = taslak_klasoru / "cikmis_baglantilari.json"
    if cik_dosya.exists():
        try:
            for c in json.loads(cik_dosya.read_text()):
                if c.get("ilgili"):
                    s_no = c.get("slideNumber") or c.get("kanit", {}).get("sayfa")
                    if s_no:
                        cikmis_map.setdefault(int(s_no), []).append(c.get("soru_id"))
        except Exception:
            pass

    # Mevcut bilgi_paketi maddeleri
    bilgi_paketi = dp.get("bilgi_paketi", [])
    atoms: List[Dict[str, Any]] = []

    for idx, b in enumerate(bilgi_paketi, start=1):
        atom_id = f"ka_{ders_id}_{idx:03d}"
        sayfa = b.get("kanit", {}).get("sayfa", 1)
        alinti = b.get("kanit", {}).get("alinti", "")
        bilgi_metni = b.get("bilgi", "")
        terim = b.get("varlik") or bilgi_metni.split(":")[0] if ":" in bilgi_metni else bilgi_metni.split(" ")[0]
        
        kat = b.get("kategori") or kategori_tahmin_et(terim, bilgi_metni)
        
        ilgili_cikmislar = cikmis_map.get(sayfa, [])
        has_past = len(ilgili_cikmislar) > 0
        
        atom = {
            "knowledge_atom_id": atom_id,
            "course_id": "pharmacology" if "farma" in ders_adi.casefold() else "general_medicine",
            "board_id": f"2026_2027_kurul_{kurul}",
            "schedule_ref": f"kurul_{kurul}_{ders_id}",
            "topic_id": ders_id,
            "audio_lesson_id": f"{ders_id}-sesli",
            "learning_objective_id": f"{ders_id}-lo-01",
            "category": kat,
            "title": terim.strip()[:60],
            "statement": bilgi_metni.strip(),
            "subtopic": b.get("alt_baslik") or konu,
            "page_number": sayfa,
            "evidence": {
                "page": sayfa,
                "quote": alinti
            },
            "past_exam_relevance": {
                "has_appeared": has_past,
                "question_ids": ilgili_cikmislar,
                "frequency": len(ilgili_cikmislar)
            },
            "tags": [kat, f"sayfa_{sayfa}"]
        }
        atoms.append(atom)

    envanter = {
        "course_id": "pharmacology" if "farma" in ders_adi.casefold() else "general_medicine",
        "board_id": f"2026_2027_kurul_{kurul}",
        "topic_id": ders_id,
        "audio_lesson_id": f"{ders_id}-sesli",
        "generated_at": dp.get("tarih", "2026-10-26"),
        "total_atoms": len(atoms),
        "atoms": atoms
    }

    cikti_yolu = taslak_klasoru / "atomik_bilgi_envanteri.json"
    cikti_yolu.write_text(json.dumps(envanter, ensure_ascii=False, indent=2))
    return envanter


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 envanter_genislet.py <taslak_klasoru>")
        sys.exit(1)
        
    klasor = Path(sys.argv[1])
    try:
        env = envanter_derle(klasor)
        print(f"BAŞARILI: {env['topic_id']} için {env['total_atoms']} atomik bilgi birimi envantere yazıldı.")
    except Exception as e:
        print(f"HATA: {e}")
        sys.exit(1)
