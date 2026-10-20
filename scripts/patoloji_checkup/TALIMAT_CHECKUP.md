# Patoloji Hızlı Check Up — Kurul 2+ (Claude, otomatik hat)

Görev: bir kurulun **yayımlanmış ve bağımsız denetimden geçmiş** patoloji derslerinden, sınav öncesi hızlı tekrar için
karşılaştırmalı tablolar kurmak. Biçim ve üslup Kurul 1'deki `src/data/patoloji_checkup/01…12-*.json` ile aynıdır
(önce 2 tanesini oku). Çıktı: `src/data/patoloji_checkup/k<N>/NN-<slug>.json` (bölüm başına bir dosya).

## Girdiler
- `meds_temp/spot_cozucu/k<N>patoloji/pdf_metin/<kod>.md` — ders PDF metni (`=== SAYFA n ===`). **Tek bilgi kaynağı.**
- `meds_temp/spot_cozucu/k<N>patoloji/onayli.json` — yalnız bu kodlar kullanılır.
- `meds_temp/spot_cozucu/k<N>patoloji/onem/<kod>.json` — sınav önemi (puanı yüksek bilgiler tablolarda mutlaka yer alır).
- `meds/src/data/dersler/k<N>.json` — ders adları (kod → konu).

## Kurallar
1. **Bölümler konu konu** (ör. SSS: ödem/herniasyon, serebrovasküler, enfeksiyonlar, tümörler, nörodejeneratif). Bölüm
   sayısı ders sayısına göre (3–12). Var olan bölüm dosyası varsa **güncelle** (tablo `id`'leri kalıcı; silme yok).
2. **Tablo:** `{id, baslik, k: ["2p03:12", …], sutun: [...], satir: [[...]]}` — her satır sütun sayısı kadar dolu hücre;
   `k` = bilginin geldiği `kod:sayfa` listesi (yalnız `onayli.json`'daki kodlar, sayfa PDF'te var). Karşılaştırma odaklı:
   tip/neden/mekanizma/morfoloji/klinik/sınav ipucu gibi sütunlar.
3. **Notlar:** `{m: "kısa sınav notu", k: "2p03:14"}`.
4. **Sadakat:** yalnız PDF'teki bilgi; çıkarım/ekleme yok. Türkçe üslup standardı (`meds/docs/TURKCE_USLUP_STANDARDI.md`),
   iç süreç dili yok.
5. Bitince `python3 meds/scripts/patoloji_checkup/dogrula.py --kurul <N>` → 0 HATA olana kadar düzelt.
