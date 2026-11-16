# Kalp ve Damar Cerrahisi — hoca üslubu ve kazanım haritası (otomatik; `scripts/hoca_profili/uslup_analiz.py`)

> 19 tekil çıkmış soru · güven: **dusuk** · yıllar: {2020: 4, 2022: 4, 2023: 1, 2025: 3}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %37 (genel ortalama %40)
- **olumsuz**: %32 (genel ortalama %15)
- **en_tipik**: %21 (genel ortalama %8)
- **yanlis_bul**: %5 (genel ortalama %13)
- **vaka**: %5 (genel ortalama %5)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %53 (genel ortalama %32)
- **siniflama_ad**: %21 (genel ortalama %9)
- **etiyoloji_risk**: %10 (genel ortalama %11)
- **tani_ayirici**: %5 (genel ortalama %12)
- **prognoz_komplikasyon**: %5 (genel ortalama %2)
- **ilac_endikasyon**: %5 (genel ortalama %7)

### Bilişsel düzey
- **L1_hatirlama**: %79 (genel ortalama %51)
- **L2_anlama_iliski**: %16 (genel ortalama %44)
- **L3_uygulama**: %5 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 11.4 kelime (p25 7 · medyan 10 · p75 12).
- Şık: ort. 3.5 kelime; bileşik şık %10; sayısal şık %0; mutlak ifadeli çeldirici %0.
- Doğru şık tek başına en uzun: %10 (genel %19). Doğru şık konumu: {'D': 0.263, 'A': 0.263, 'E': 0.211, 'B': 0.211, 'C': 0.053}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.947, 'bilesik_yer_degistirmeli': 0.053}
- Aynı bilginin yeniden sorulması: soruların %0'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %37, olumsuz %32, en_tipik %21.
- Kök 7–12 kelime; şık ort. 3.5 kelime, uzunluklar birbirine yakın (CV≈0.26).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %79, L2_anlama_iliski %16, L3_uygulama %5.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Göğüs duvarı anomalileri — 16 soru, yıllar [2020, 2022, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%62) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.375, 'olumsuz': 0.312, 'en_tipik': 0.25, 'yanlis_bul': 0.062} · düzey {'L1_hatirlama': 0.812, 'L2_anlama_iliski': 0.188} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %12
- **Tekrar eden çekirdek kavramlar:** Pektus ekskavatum (3×, 1 yıl); Kızlarda daha sık görülür (2×, 1 yıl)

### Enfektif endokardit ve damar içi katater enfeksiyonları — 3 soru, yıllar [2022], güven dusuk
- **Neden:** etiyoloji_risk (%67) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'olumsuz': 0.333, 'dogrudan': 0.333, 'vaka': 0.333} · düzey {'L1_hatirlama': 0.667, 'L3_uygulama': 0.333} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %33
