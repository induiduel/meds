# Kadın Hastalıkları ve Doğum — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 46 tekil çıkmış soru · güven: **orta** · yıllar: {2019: 8, 2020: 11, 2021: 6, 2022: 2, 2023: 5, 2024: 2, 2025: 5, 2026: 4}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %35 (genel ortalama %40)
- **vaka**: %15 (genel ortalama %5)
- **yanlis_bul**: %15 (genel ortalama %13)
- **olumsuz**: %11 (genel ortalama %15)
- **en_tipik**: %6 (genel ortalama %8)
- **onculu**: %6 (genel ortalama %8)
- **dogru_ifade**: %4 (genel ortalama %6)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %61 (genel ortalama %32)
- **tani_ayirici**: %13 (genel ortalama %12)
- **prognoz_komplikasyon**: %11 (genel ortalama %2)
- **onleme_halk_sagligi**: %4 (genel ortalama %5)
- **siniflama_ad**: %4 (genel ortalama %9)
- **epidemiyoloji_sayi**: %2 (genel ortalama %2)
- **ilac_endikasyon**: %2 (genel ortalama %7)

### Bilişsel düzey
- **L1_hatirlama**: %52 (genel ortalama %51)
- **L2_anlama_iliski**: %33 (genel ortalama %44)
- **L3_uygulama**: %15 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 20.0 kelime (p25 11 · medyan 16 · p75 28).
- Şık: ort. 3.6 kelime; bileşik şık %12; sayısal şık %33; mutlak ifadeli çeldirici %0.
- Doğru şık tek başına en uzun: %9 (genel %19). Doğru şık konumu: {'B': 0.261, 'A': 0.217, 'D': 0.196, 'C': 0.174, 'E': 0.152}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.435, 'ayni_ailede_komsu_kavram': 0.37, 'sayisal_yakin_deger': 0.326, 'bilesik_yer_degistirmeli': 0.109}
- Aynı bilginin yeniden sorulması: soruların %24'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %35, vaka %15, yanlis_bul %15.
- Kök 11–28 kelime; şık ort. 3.6 kelime, uzunluklar birbirine yakın (CV≈0.17).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %52, L2_anlama_iliski %33, L3_uygulama %15.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Gebelik Terminolojisi/Kavramları — 30 soru, yıllar [2019, 2020, 2021, 2022, 2023, 2024, 2025], güven dusuk
- **Neden:** tanim_kavram (%77) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.4, 'yanlis_bul': 0.2, 'olumsuz': 0.133, 'vaka': 0.133, 'onculu': 0.067, 'sayi': 0.033, 'dogru_ifade': 0.033} · düzey {'L1_hatirlama': 0.567, 'L2_anlama_iliski': 0.3, 'L3_uygulama': 0.133} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Chadwick belirtisi (5×, 1 yıl); 10.02.2021 (4×, 2 yıl); Goodell (4×, 1 yıl); Anti-streptolizin O (3×, 2 yıl)

### Abortus — 13 soru, yıllar [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tanim_kavram (%31) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'en_tipik': 0.231, 'vaka': 0.231, 'dogrudan': 0.231, 'onculu': 0.077, 'dogru_ifade': 0.077, 'sayi': 0.077, 'yanlis_bul': 0.077} · düzey {'L1_hatirlama': 0.462, 'L2_anlama_iliski': 0.308, 'L3_uygulama': 0.231} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %31
- **Tekrar eden çekirdek kavramlar:** Otozomal trizomi (5×, 2 yıl); Düşük tehdidi (3×, 1 yıl); Abortus imminens (2×, 1 yıl)

### Gebelik Terminolojisi ve Kavramları — 3 soru, yıllar [2026], güven dusuk
- **Neden:** tani_ayirici (%67) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'tanim': 0.333, 'olumsuz': 0.333, 'dogrudan': 0.333} · düzey {'L2_anlama_iliski': 0.667, 'L1_hatirlama': 0.333} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0
