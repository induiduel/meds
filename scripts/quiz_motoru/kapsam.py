#!/usr/bin/env python3
"""Quiz Motoru Kapsam ve Öncelik Kilidi Denetleyicisi.

Faz 1: Kapsam Kilidi (Scope Lock)
- Kullanıcı kararı 2026-10-27: Quiz üretimi HER ders için aktiftir (eski Farmakoloji kilidi kalktı).
- Ders-bağımsız (course-agnostic) mimari: MEDS_QUIZ_ETKIN_KURSLAR ortam değişkeni
  veya yapılandırma ile diğer branşlar (patoloji, mikrobiyoloji vb.) tek satırla etkinleştirilebilir.

Faz 3: Sesli Ders Tamamlanma Kilidi (Priority Lock)
- Bir dersin sesli anlatımı (Audio Lesson) 'COMPLETED' durumuna geçmeden
  Quiz soru üretim ajanları KESİNLİKLE tetiklenemez.
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS.parent

# Varsayılan: her ders etkin (kullanıcı kararı 2026-10-27). Kısıtlamak için MEDS_QUIZ_ETKIN_KURSLAR=a,b
TUM_DERSLER = True


def quiz_etkin_mi(brans_veya_kurs: str) -> bool:
    """Verilen branş veya kurs kimliği için quiz üretiminin etkin olup olmadığını döner."""
    if not brans_veya_kurs:
        return False
    
    # Ortam değişkeninden özel liste varsa oku
    ozel = os.environ.get("MEDS_QUIZ_ETKIN_KURSLAR")
    if ozel:
        etkinler = {x.strip().casefold() for x in ozel.split(",") if x.strip()}
        if "*" in etkinler or "tum" in etkinler:
            return True
        return brans_veya_kurs.strip().casefold() in etkinler

    return TUM_DERSLER


def sesli_ders_tamamlandi_mi(ders_id: str, taslak_klasor: Optional[Path] = None) -> bool:
    """Sesli dersin (Audio Lesson) tamamlanıp COMPLETED durumunda olup olmadığını doğrular.
    
    Kontrol kriterleri:
    1. Taslak klasöründe 'konusma_v2.json' (veya türetilmiş konusma_metni.md) var mı?
    2. Sesli ders metin denetimi (metin_denetle.py / konusma_v2.py --dogrula) 0 HATA ile geçmiş mi?
    3. hat/dersler/<ders_id>.json içinde 'ses' veya 'yayin' adımı başarılı mı?
    """
    if taslak_klasor and taslak_klasor.exists():
        v2 = taslak_klasor / "konusma_v2.json"
        metin = taslak_klasor / "konusma_metni.md"
        oturum_sesli = taslak_klasor / "oturum_sesli.json"
        
        # konusma_v2.json veya konusma_metni.md bulunmalı
        yayinli = (MEDS / "data/sesli_anlatim/metin" / f"{ders_id}.md").exists() and (MEDS / "data/sesli_anlatim/cumle_zaman" / f"{ders_id}.json").exists()  # elle üretilen dersler: yayınlanmış sesli ders = COMPLETED
        if not (v2.exists() or metin.exists() or yayinli):
            return False
            
        # Denetim dosyası veya oturumda hata var mı kontrol et
        if (taslak_klasor / "hata_sesli.txt").exists():
            return False

        # Eğer karar.json varsa ve onaylanmamışsa tamamlanmış sayılmaz
        karar_dosyasi = taslak_klasor / "karar.json"
        if karar_dosyasi.exists():
            try:
                k = json.loads(karar_dosyasi.read_text())
                if k.get("karar") not in ("onayla", "onaylandi"):
                    return False
            except Exception:
                return False

        return True

    # Taslak klasörü verilmemişse durum kayıtlarından kontrol et
    durum_dosyasi = KOK / f"meds_temp/hat/dersler/{ders_id}.json"
    if durum_dosyasi.exists():
        try:
            d = json.loads(durum_dosyasi.read_text())
            adimlar = d.get("adimlar", {})
            # sesli metin veya yayın adımı 0 ile tamamlanmış olmalı
            for adim in ("sesli_ders_metni", "yayin", "ses"):
                if adim in adimlar and adimlar[adim].get("kod") == 0:
                    return True
        except Exception:
            pass

    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 kapsam.py <brans_veya_kurs> [ders_id] [taslak_yolu]")
        sys.exit(1)
        
    brans = sys.argv[1]
    etkin = quiz_etkin_mi(brans)
    print(f"Quiz Etkinlik ({brans}): {'EVET (Aktif)' if etkin else 'HAYIR (Kapsam Dışı)'}")
    
    if len(sys.argv) >= 3:
        d_id = sys.argv[2]
        t_yol = Path(sys.argv[3]) if len(sys.argv) >= 4 else None
        sesli = sesli_ders_tamamlandi_mi(d_id, t_yol)
        print(f"Sesli Ders Durumu ({d_id}): {'COMPLETED' if sesli else 'BEKLİYOR (Kilitli)'}")
