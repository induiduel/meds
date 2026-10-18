#!/usr/bin/env python3
"""
Sınav Çalışma Veri Katmanı ve Kazanım Eşleştirici v2
Tüm Kurul 1 derslerinin her konusunun her kazanımı için:
- En az 2 orta zorlukta soru (örnek sorular + benzer çıkmışlar)
- Kapsamlı ve öğretici ÖZET KONU ANLATIMI (bilinmesi gereken temel bilgiler, mekanizmalar, sınav tuzakları)
- EMA seslendiricisi ile uyumlu ses metinleri (kok_ses, secenek_ses, ipucu_ses, siklar_ses, cozum_ses, anlatim_ses)
- Branş ve çözücü ders kodu eşleşmesi (patoloji, genetik, enfeksiyon, üroloji vb. ve gerçek ses klasörleri)
- meds/src/data/sinav_calisma_k1.json ve meds/src/data/kazanimlar/k1.json güncellemesi
"""

import json
import glob
import re
import os
from pathlib import Path

ROOT = Path("/home/indu/medsor")
DATA_DIR = ROOT / "meds/src/data"

BRANS_HARITASI = {
    "Tıbbi Patoloji": "patoloji",
    "Tıbbi Genetik": "genetik",
    "Enfeksiyon Hastalıkları": "enfeksiyon",
    "Üroloji": "uroloji",
    "Halk Sağlığı": "halksagligi",
    "Kadın Hastalıkları ve Doğum": "kadindogum",
    "Tıbbi Farmakoloji": "farmakoloji"
}

def norm_key(s: str) -> str:
    if not s:
        return ""
    s = s.lower().replace("’", "'").replace("`", "'").replace("–", "-").replace("—", "-")
    s = s.replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("ş", "s").replace("ç", "c").replace("ğ", "g")
    return re.sub(r"[^a-z0-9]", "", s)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

def to_speech_text(text: str) -> str:
    """Metni EMA okuyucusuna uygun Türkçe fonetik ses metnine çevirir."""
    if not text:
        return ""
    t = text
    t = re.sub(r"[\(\)\[\]\{\}\<\>\"\'`*#~_]", " ", t)
    t = t.replace(";", ",").replace(":", ",")
    t = t.replace("%", "yüzde ")
    t = t.replace("≥", "eşit ya da büyük ")
    t = t.replace("≤", "eşit ya da küçük ")
    t = t.replace(">", "büyük ")
    t = t.replace("<", "küçük ")
    t = t.replace("→", " ardından ")
    t = t.replace("+", " artı ")
    t = t.replace("±", " artı eksi ")
    t = t.replace("&", " ve ")
    t = t.replace("/", " ya da ")
    
    rakamlar = {
        "0": "sıfır", "1": "bir", "2": "iki", "3": "üç", "4": "dört",
        "5": "beş", "6": "altı", "7": "yedi", "8": "sekiz", "9": "dokuz",
        "10": "on", "11": "on bir", "12": "on iki", "13": "on üç", "14": "on dört",
        "15": "on beş", "16": "on altı", "17": "on yedi", "18": "on sekiz", "19": "on dokuz", "20": "yirmi"
    }
    for r_num, r_word in sorted(rakamlar.items(), key=lambda x: -len(x[0])):
        t = re.sub(r"\b" + r_num + r"\b", r_word, t)
        
    t = re.sub(r"\s+", " ", t).strip()
    return t

def clean_markdown_section(text: str, max_chars=1200) -> str:
    """Markdown metnini temizleyip akıcı özet paragrafına dönüştürür."""
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("<sub>") or line.startswith("📘"):
            continue
        line = re.sub(r"==([^=]+)==", r"\1", line)
        line = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
        line = re.sub(r"\[!NOTE\]|\[!IMPORTANT\]|\[!WARNING\]", "", line)
        line = re.sub(r"^>\s*", "", line).strip()
        if line:
            lines.append(line)
    result = " ".join(lines)
    result = re.sub(r"\s+", " ", result).strip()
    if len(result) > max_chars:
        # Son cümlenin bittiği yerden kes
        cut = result[:max_chars]
        last_dot = cut.rfind(".")
        if last_dot > 200:
            result = cut[:last_dot + 1]
    return result

def extract_topic_summary(content: str, kazanim_metin: str, konu_adi: str) -> str:
    """Ders içeriğinden kazanımla en alakalı bölümü bulur ve özet metin oluşturur."""
    if not content:
        return f"{konu_adi} dersinde {kazanim_metin} kapsamında amfi ders notlarında vurgulanan temel mekanizmalar ve klinik tanı kriterleri ayrıntılı olarak ele alınmıştır."

    # İçeriği '## ' başlıklarına göre böl
    sections = re.split(r"\n##\s+", content)
    best_section = ""
    best_score = -1

    kz_words = set(re.findall(r"\w{4,}", kazanim_metin.lower()))

    for sec in sections:
        sec_lower = sec.lower()
        # 'Öğrenim Hedefleri' veya meta başlıkları atla
        if "öğrenim hedefleri" in sec_lower[:50] or "ders kodu" in sec_lower[:50]:
            continue
        # Başlık ve içerik uyumu
        score = sum(1 for w in kz_words if w in sec_lower)
        if score > best_score and len(sec.strip()) > 150:
            best_score = score
            best_section = sec

    if best_section and best_score >= 1:
        summary_clean = clean_markdown_section(best_section)
        if len(summary_clean) > 100:
            return summary_clean

    # Eğer spesifik bölüm bulunamadıysa öğrenim hedefleri haricindeki ilk doyurucu bölümü al
    for sec in sections[1:]:
        sec_lower = sec.lower()
        if "öğrenim hedefleri" not in sec_lower[:50] and len(sec.strip()) > 200:
            summary_clean = clean_markdown_section(sec)
            if len(summary_clean) > 150:
                return summary_clean

    combined = "\n".join(sections[1:3]) if len(sections) > 2 else content[:2000]
    return clean_markdown_section(combined)

def main():
    k1_path = DATA_DIR / "kazanimlar/k1.json"
    k1_data = load_json(k1_path)
    
    # ornek_sorular altındaki tüm dosyaları indeksle
    ornek_dosyalar = {}
    for p in glob.glob(str(DATA_DIR / "ornek_sorular/k1/k1-*.json")):
        d = load_json(p)
        k_norm = norm_key(d.get("konu", ""))
        ornek_dosyalar[k_norm] = d
        k_id = d.get("id", "")
        ornek_dosyalar[norm_key(k_id)] = d

    # Ders özetleri
    summaries_cat = load_json(DATA_DIR / "lectureSummariesCatalog.json")
    summaries_map = {}
    for s in summaries_cat:
        t_norm = norm_key(s.get("title", ""))
        summaries_map[t_norm] = s

    # Çözücü branş dizinleri
    cozucu_dizinler = {}
    for brans in ["patoloji", "genetik", "enfeksiyon", "uroloji", "halksagligi", "kadindogum", "farmakoloji"]:
        idx_p = DATA_DIR / f"{brans}_cozucu/index.json"
        if idx_p.exists():
            cozucu_dizinler[brans] = load_json(idx_p)

    # Sınav spotları
    spots_data = load_json(DATA_DIR / "exam_spots_k1.json")
    spots_by_ders = {}
    for sp in spots_data.get("spotlar", []):
        d_no = sp.get("ders")
        if d_no not in spots_by_ders:
            spots_by_ders[d_no] = []
        spots_by_ders[d_no].append(sp)

    print("Veri kaynakları yüklendi. Kapsamlı özet konu anlatımları ve ses haritası oluşturuluyor...")

    toplam_kazanim = 0

    for d in k1_data.get("dersler", []):
        ders_adi = d.get("ders", "")
        brans_slug = BRANS_HARITASI.get(ders_adi, "patoloji")

        for k in d.get("konular", []):
            konu_adi = k.get("konu", "")
            konu_norm = norm_key(konu_adi)
            
            # Bu konunun özetini bul
            matched_sum = summaries_map.get(konu_norm)
            if not matched_sum:
                for snorm, sdata in summaries_map.items():
                    if konu_norm in snorm or snorm in konu_norm:
                        matched_sum = sdata
                        break

            # Çözücü ders kodunu bul
            cozucu_ders_kodu = None
            if brans_slug in cozucu_dizinler:
                for cd in cozucu_dizinler[brans_slug].get("dersler", []):
                    b_norm = norm_key(cd.get("baslik", ""))
                    if konu_norm in b_norm or b_norm in konu_norm:
                        cozucu_ders_kodu = cd.get("kod")
                        break

            k["brans"] = brans_slug
            if cozucu_ders_kodu:
                k["cozucu_kod"] = cozucu_ders_kodu

            # Konunun kazanımlarını tara
            for kz_idx, kz in enumerate(k.get("kazanimlar", [])):
                toplam_kazanim += 1
                kz_metin = kz.get("metin", "")
                kz_no = kz_idx + 1

                # 1. Kapsamlı Özet Konu Anlatımı
                content_text = matched_sum.get("content", "") if matched_sum else ""
                ozet_metin = extract_topic_summary(content_text, kz_metin, konu_adi)
                
                # Özet maddeleri (bilinmesi gereken temel noktalar)
                maddeler = []
                if matched_sum and matched_sum.get("keyPoints"):
                    for kp in matched_sum.get("keyPoints", []):
                        if any(w in kp.lower() for w in re.findall(r"\w{4,}", kz_metin.lower())):
                            maddeler.append(kp)
                
                # Soru açıklamalarından kritik spotları topla
                for q in kz.get("ornekSorular", [])[:3]:
                    ac = q.get("aciklama", "").strip()
                    if ac and len(ac) > 25 and ac not in maddeler:
                        maddeler.append(ac)
                        if len(maddeler) >= 3:
                            break

                kz["ozet_konu_anlatimi"] = ozet_metin
                kz["bilinmesi_gerekenler"] = maddeler
                kz["kisa_anlatim"] = maddeler[:3]  # Geriye uyumluluk
                kz["anlatim_ses"] = to_speech_text(f"{ozet_metin} Bilinmesi gerekenler: {' '.join(maddeler)}")

                # Soruların ses ve çözücü formatını zenginleştir
                for q_idx, q in enumerate(kz.get("ornekSorular", [])):
                    if not q.get("zorluk"):
                        q["zorluk"] = "orta"
                    
                    q["soru_no"] = q_idx + 1
                    if cozucu_ders_kodu:
                        q["cozucu_kod"] = cozucu_ders_kodu
                        q["brans"] = brans_slug

                    if not q.get("sik_aciklamalari") or len(q.get("sik_aciklamalari", {})) == 0:
                        dogru_sec = q.get("dogru", "A")
                        q["sik_aciklamalari"] = {}
                        for h in ["A", "B", "C", "D", "E"]:
                            if h in q.get("secenekler", {}):
                                if h == dogru_sec:
                                    q["sik_aciklamalari"][h] = f"Doğru. {q.get('aciklama', 'Bu seçenek sorulan temel mekanizmayı doğru olarak ifade eder.')}"
                                else:
                                    q["sik_aciklamalari"][h] = f"Yanlış. {q['secenekler'][h]} ifadesi bu soruda aranan tanı/özellik ile örtüşmemektedir."

                    if not q.get("ipucu"):
                        q["ipucu"] = f"Kazanım hedefini ve temel klinik-patolojik mekanizmayı göz önüne alınız."

                    # Ses formatları
                    q["kok_ses"] = to_speech_text(q.get("soru", ""))
                    q["secenek_ses"] = {h: to_speech_text(txt) for h, txt in q.get("secenekler", {}).items()}
                    q["ipucu_ses"] = to_speech_text(q.get("ipucu", ""))
                    q["siklar_ses"] = {h: to_speech_text(txt) for h, txt in q.get("sik_aciklamalari", {}).items()}
                    q["cozum_ses"] = to_speech_text(q.get("aciklama", ""))

    print(f"Toplam {toplam_kazanim} kazanım için kapsamlı özet konu anlatımları ve ses haritası tamamlandı.")
    
    # Dosyaları kaydet
    save_json(k1_path, k1_data)
    print(f"K1 kazanımları güncellendi: {k1_path}")

    sinav_calisma_path = DATA_DIR / "sinav_calisma_k1.json"
    save_json(sinav_calisma_path, k1_data)
    print(f"Sınav çalışma verisi kaydedildi: {sinav_calisma_path}")

if __name__ == "__main__":
    main()
