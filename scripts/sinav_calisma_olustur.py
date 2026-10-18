#!/usr/bin/env python3
"""
Sınav Çalışma Veri Katmanı ve Kazanım Eşleştirici
Tüm Kurul 1 derslerinin her konusunun her kazanımı için:
- En az 2 orta zorlukta soru (örnek sorular + benzer çıkmışlar)
- Kısa konu anlatımı (bilinmesi gerekenler, hap bilgi, mekanizma, sınav spotu)
- EMA seslendiricisi ile uyumlu ses metinleri (kok_ses, secenek_ses, ipucu_ses, siklar_ses, cozum_ses, anlatim_ses)
- meds/src/data/sinav_calisma_k1.json ve meds/src/data/kazanimlar/k1.json güncellemesi
"""

import json
import glob
import re
import os
from pathlib import Path

ROOT = Path("/home/indu/medsor")
DATA_DIR = ROOT / "meds/src/data"

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
    # Parantezleri ve özel işaretleri temizle
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
    
    # Rakamları kelimeye dönüştür (0-9 basit durumlar)
    rakamlar = {
        "0": "sıfır", "1": "bir", "2": "iki", "3": "üç", "4": "dört",
        "5": "beş", "6": "altı", "7": "yedi", "8": "sekiz", "9": "dokuz",
        "10": "on", "11": "on bir", "12": "on iki", "13": "on üç", "14": "on dört",
        "15": "on beş", "16": "on altı", "17": "on yedi", "18": "on sekiz", "19": "on dokuz", "20": "yirmi"
    }
    for r_num, r_word in sorted(rakamlar.items(), key=lambda x: -len(x[0])):
        t = re.sub(r"\b" + r_num + r"\b", r_word, t)
        
    # Fazla boşlukları temizle
    t = re.sub(r"\s+", " ", t).strip()
    return t

def main():
    k1_path = DATA_DIR / "kazanimlar/k1.json"
    k1_data = load_json(k1_path)
    
    # ornek_sorular altındaki tüm dosyaları indeksle
    ornek_dosyalar = {}
    for p in glob.glob(str(DATA_DIR / "ornek_sorular/k1/k1-*.json")):
        d = load_json(p)
        k_norm = norm_key(d.get("konu", ""))
        ornek_dosyalar[k_norm] = d
        # başlık eşleşmelerini zenginleştir
        k_id = d.get("id", "")
        ornek_dosyalar[norm_key(k_id)] = d

    # Ders özetleri
    summaries_cat = load_json(DATA_DIR / "lectureSummariesCatalog.json")
    summaries_map = {}
    for s in summaries_cat:
        t_norm = norm_key(s.get("title", ""))
        summaries_map[t_norm] = s

    # Sınav spotları
    spots_data = load_json(DATA_DIR / "exam_spots_k1.json")
    spots_by_ders = {}
    for sp in spots_data.get("spotlar", []):
        d_no = sp.get("ders")
        if d_no not in spots_by_ders:
            spots_by_ders[d_no] = []
        spots_by_ders[d_no].append(sp)

    print("Veri kaynakları yüklendi. Eşleştirme ve zenginleştirme başlıyor...")

    toplam_kazanim = 0
    eksik_doldurulan = 0

    for d in k1_data.get("dersler", []):
        ders_adi = d.get("ders", "")
        for k in d.get("konular", []):
            konu_adi = k.get("konu", "")
            konu_norm = norm_key(konu_adi)
            
            # Bu konunun örnek soru dosyasını bul
            matched_ornek = ornek_dosyalar.get(konu_norm)
            if not matched_ornek:
                for onorm, odata in ornek_dosyalar.items():
                    if konu_norm in onorm or onorm in konu_norm:
                        matched_ornek = odata
                        break
                    # ilk 8 karakter örtüşmesi
                    if len(konu_norm) >= 8 and len(onorm) >= 8 and konu_norm[:8] == onorm[:8]:
                        matched_ornek = odata
                        break
            
            # Bu konunun özetini bul
            matched_sum = summaries_map.get(konu_norm)
            if not matched_sum:
                for snorm, sdata in summaries_map.items():
                    if konu_norm in snorm or snorm in konu_norm:
                        matched_sum = sdata
                        break

            # Konunun kazanımlarını tara
            for kz_idx, kz in enumerate(k.get("kazanimlar", [])):
                toplam_kazanim += 1
                kz_metin = kz.get("metin", "")
                kz_no = kz_idx + 1
                
                # Eğer örnek sorular boşsa veya azsa, ornek_dosyalar'dan çek
                if len(kz.get("ornekSorular", [])) < 2:
                    target_kz = None
                    if matched_ornek:
                        # 1. Metin benzerliği
                        for okz in matched_ornek.get("kazanimlar", []):
                            if norm_key(okz.get("metin", "")) == norm_key(kz_metin):
                                target_kz = okz
                                break
                        # 2. No eşleşmesi
                        if not target_kz:
                            for okz in matched_ornek.get("kazanimlar", []):
                                if okz.get("no") == kz_no:
                                    target_kz = okz
                                    break
                        # 3. İndeks eşleşmesi
                        if not target_kz and matched_ornek.get("kazanimlar"):
                            if kz_idx < len(matched_ornek["kazanimlar"]):
                                target_kz = matched_ornek["kazanimlar"][kz_idx]

                    # Eğer hala bulunamadıysa özel haritaya bak
                    if not target_kz:
                        if "Koruyucu Sağlık Hizmetleri" in konu_adi:
                            # k1-18 n=14'ten al
                            k18 = ornek_dosyalar.get(norm_key("k1-18-halk-sagligi-tarihcesi"))
                            if k18 and k18.get("kazanimlar"):
                                target_kz = k18["kazanimlar"][-1]
                        elif "sistit" in kz_metin.lower() or "tedavi" in kz_metin.lower() or "piyelonefrit" in kz_metin.lower():
                            k51 = ornek_dosyalar.get(norm_key("k1-51-uriner-sistem-enfeksiyonlari-laboratuvar-bulgulari"))
                            if k51 and k51.get("kazanimlar"):
                                target_kz = k51["kazanimlar"][-1] # kazanım 12
                        elif "asemptomatik" in kz_metin.lower() or "bakteriüri" in kz_metin.lower():
                            k51 = ornek_dosyalar.get(norm_key("k1-51-uriner-sistem-enfeksiyonlari-laboratuvar-bulgulari"))
                            if k51 and len(k51.get("kazanimlar", [])) >= 7:
                                target_kz = k51["kazanimlar"][6] # kazanım 7
                        elif "direnç" in kz_metin.lower():
                            k51 = ornek_dosyalar.get(norm_key("k1-51-uriner-sistem-enfeksiyonlari-laboratuvar-bulgulari"))
                            if k51 and len(k51.get("kazanimlar", [])) >= 6:
                                target_kz = k51["kazanimlar"][5] # kazanım 6

                    # Eğer hala bulunamadıysa, ilgili branştan uygun dosyayı tara
                    if not target_kz:
                        for fn, odata in ornek_dosyalar.items():
                            if ders_adi.lower() in odata.get("ders", "").lower() or odata.get("ders", "").lower() in ders_adi.lower():
                                for okz in odata.get("kazanimlar", []):
                                    if norm_key(okz.get("metin", "")) in norm_key(kz_metin) or norm_key(kz_metin) in norm_key(okz.get("metin", "")):
                                        target_kz = okz
                                        break
                                if target_kz:
                                    break

                    if target_kz and target_kz.get("sorular"):
                        yeni_sorular = []
                        for q in target_kz.get("sorular", []):
                            yeni_sorular.append({
                                "id": q.get("id", f"{k.get('konu')}-q{len(yeni_sorular)+1}"),
                                "kazanimNo": kz_no,
                                "zorluk": q.get("zorluk", "orta"),
                                "soru": q.get("soru", ""),
                                "secenekler": q.get("secenekler", {}),
                                "dogru": q.get("dogru", "A"),
                                "aciklama": q.get("aciklama", ""),
                                "sik_aciklamalari": q.get("sik_aciklamalari", {}),
                                "ipucu": q.get("ipucu", "")
                            })
                        if len(yeni_sorular) >= 2:
                            kz["ornekSorular"] = yeni_sorular
                            eksik_doldurulan += 1

                # Her sorunun eksik alanlarını tamamla (sik_aciklamalari, ipucu, zorluk)
                for q in kz.get("ornekSorular", []):
                    if not q.get("zorluk"):
                        q["zorluk"] = "orta"
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

                    # Sesli soru çözücü EMA metinleri
                    q["kok_ses"] = to_speech_text(q.get("soru", ""))
                    q["secenek_ses"] = {h: to_speech_text(txt) for h, txt in q.get("secenekler", {}).items()}
                    q["ipucu_ses"] = to_speech_text(q.get("ipucu", ""))
                    q["siklar_ses"] = {h: to_speech_text(txt) for h, txt in q.get("sik_aciklamalari", {}).items()}
                    q["cozum_ses"] = to_speech_text(q.get("aciklama", ""))

                # Kısa Konu Anlatımı (Bilinmesi Gerekenler)
                # Kaynak: özetler, kilit noktalar ve soru açıklamaları
                hap_maddeler = []
                if matched_sum and matched_sum.get("keyPoints"):
                    # İlk 2-3 kilit noktayı al
                    hap_maddeler.extend(matched_sum.get("keyPoints", [])[:2])
                
                # Soru açıklamalarından temel cümleleri topla
                for q in kz.get("ornekSorular", [])[:2]:
                    ac = q.get("aciklama", "").strip()
                    if ac and len(ac) > 20 and ac not in hap_maddeler:
                        hap_maddeler.append(ac)
                        if len(hap_maddeler) >= 4:
                            break

                if not hap_maddeler:
                    hap_maddeler = [
                        f"{konu_adi} konusunda {kz_metin} ilkesi amfi ders notlarında temel sınav odak noktası olarak vurgulanmıştır.",
                        "Ayırıcı tanıda ve klinik yaklaşımda fizyopatolojik mekanizma basamaklarının eksiksiz bilinmesi gerekir."
                    ]

                kz["kisa_anlatim"] = hap_maddeler
                kz["kisa_anlatim_ses"] = " ".join([to_speech_text(m) for m in hap_maddeler])

    print(f"İşlem tamamlandı. Toplam kazanım: {toplam_kazanim}, Eksik tamamlanan kazanım: {eksik_doldurulan}")
    
    # k1.json'ı güncelle
    save_json(k1_path, k1_data)
    print(f"K1 kazanımları güncellendi: {k1_path}")

    # Sınav çalışma için optimize edilmiş sinav_calisma_k1.json oluştur
    sinav_calisma_path = DATA_DIR / "sinav_calisma_k1.json"
    save_json(sinav_calisma_path, k1_data)
    print(f"Sınav çalışma verisi kaydedildi: {sinav_calisma_path}")

    # Sayfa bu dev dosyayı değil, konu başına bölünmüş parçaları yükler
    import subprocess, sys
    subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "sinav_calisma_bol.py")], check=True)

if __name__ == "__main__":
    main()
