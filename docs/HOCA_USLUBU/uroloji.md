# Üroloji — hoca üslubu ve kazanım haritası (otomatik; `scripts/hoca_profili/uslup_analiz.py`)

> 187 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 6, 2019: 20, 2020: 64, 2021: 25, 2022: 7, 2023: 21, 2024: 11, 2025: 15, 2026: 11}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %41 (genel ortalama %40)
- **olumsuz**: %27 (genel ortalama %15)
- **yanlis_bul**: %12 (genel ortalama %13)
- **vaka**: %5 (genel ortalama %5)
- **dogru_ifade**: %5 (genel ortalama %6)
- **sayi**: %4 (genel ortalama %3)
- **tanim**: %3 (genel ortalama %1)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %30 (genel ortalama %32)
- **etiyoloji_risk**: %23 (genel ortalama %11)
- **tani_ayirici**: %14 (genel ortalama %12)
- **ilac_endikasyon**: %13 (genel ortalama %7)
- **onleme_halk_sagligi**: %6 (genel ortalama %5)
- **siniflama_ad**: %6 (genel ortalama %9)
- **epidemiyoloji_sayi**: %4 (genel ortalama %2)

### Bilişsel düzey
- **L1_hatirlama**: %66 (genel ortalama %51)
- **L2_anlama_iliski**: %28 (genel ortalama %44)
- **L3_uygulama**: %5 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 13.0 kelime (p25 8 · medyan 10 · p75 14).
- Şık: ort. 4.4 kelime; bileşik şık %16; sayısal şık %6; mutlak ifadeli çeldirici %0.
- Doğru şık tek başına en uzun: %13 (genel %19). Doğru şık konumu: {'D': 0.251, 'C': 0.225, 'B': 0.209, 'A': 0.176, 'E': 0.139}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.754, 'ayni_ailede_komsu_kavram': 0.139, 'bilesik_yer_degistirmeli': 0.128, 'sayisal_yakin_deger': 0.059, 'mutlak_ifade_tuzagi': 0.005}
- Aynı bilginin yeniden sorulması: soruların %22'i birden çok kez çıkmış.

### Dönem kayması (2023 sonrası − öncesi, puan farkı)
- {'kalip': {'olumsuz': 0.178}, 'tur': {'tanim_kavram': 0.09, 'tani_ayirici': -0.098}}

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %41, olumsuz %27, yanlis_bul %12.
- Kök 8–14 kelime; şık ort. 4.4 kelime, uzunluklar birbirine yakın (CV≈0.29).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %66, L2_anlama_iliski %28, L3_uygulama %5.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etiyoloji ve Semptomatolojisi — 73 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven orta
- **Neden:** tanim_kavram (%38) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.438, 'olumsuz': 0.274, 'yanlis_bul': 0.11, 'dogru_ifade': 0.041, 'vaka': 0.041, 'tanim': 0.027, 'sayi': 0.027, 'onculu': 0.027, 'en_tipik': 0.014} · düzey {'L1_hatirlama': 0.726, 'L2_anlama_iliski': 0.233, 'L3_uygulama': 0.041} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %32
- **Tekrar eden çekirdek kavramlar:** Sıklık (frequency) (9×, 3 yıl); Soğuk iklim (7×, 3 yıl); Stres üriner inkontinans (7×, 2 yıl); Pelvik organ prolapsusu (7×, 1 yıl)

### Üriner Sistem Enfeksiyonları Lab. Bulguları ve Tedavi — 42 soru, yıllar [2019, 2020, 2021, 2022, 2023, 2024, 2025], güven orta
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.429, 'olumsuz': 0.405, 'tanim': 0.071, 'dogru_ifade': 0.048, 'onculu': 0.024, 'sayi': 0.024} · düzey {'L1_hatirlama': 0.786, 'L2_anlama_iliski': 0.214} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %48
- **Tekrar eden çekirdek kavramlar:** Bakteriüri (11×, 2 yıl); Non-komplike alt üriner sistem enfeksiyonu (5×, 2 yıl); Akut bakteriyel prostatit (4×, 1 yıl); Akut sistit (4×, 1 yıl)

### Enürezis Nokturna — 31 soru, yıllar [2019, 2020, 2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** ilac_endikasyon (%39) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'yanlis_bul': 0.323, 'dogrudan': 0.258, 'vaka': 0.226, 'sayi': 0.097, 'olumsuz': 0.065, 'en_tipik': 0.032} · düzey {'L2_anlama_iliski': 0.516, 'L1_hatirlama': 0.258, 'L3_uygulama': 0.226} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %26
- **Tekrar eden çekirdek kavramlar:** Tedavinin başarılı olması için 4 yaşından önce tedaviye başlanması gerekir. (5×, 2 yıl); Tam idrar tetkiki (4×, 1 yıl); Desmopressin ile tedaviye başlarım (2×, 1 yıl); Büyük çocuklarda tedavi vermeden enürezisin spontan rezolüsyonu beklenir (2×, 1 yıl)

### Üriner Sistemin Spesifik Enfeksiyonları — 15 soru, yıllar [2018, 2019, 2020, 2022, 2023, 2024, 2025], güven dusuk
- **Neden:** etiyoloji_risk (%27) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'olumsuz': 0.4, 'dogru_ifade': 0.2, 'yanlis_bul': 0.2, 'dogrudan': 0.133, 'en_tipik': 0.067} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.333} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Antiviral tedavi (7×, 1 yıl); Yaklaşık %70 oranında bilateral (iki taraflı) tutulum gösterir (2×, 2 yıl); Etkeni E. coli ve diğer üropatojen bakterilerdir (2×, 2 yıl); Echinococcus granulosus etrafı düzgün, yuvarlak, tek bir kist oluşturur. (2×, 1 yıl)

### Üriner Sistem Taş Hastalıkları Fizyopatolojisi — 12 soru, yıllar [2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** etiyoloji_risk (%33) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.75, 'olumsuz': 0.25} · düzey {'L1_hatirlama': 1.0} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Kalsiyum oksalat monohidrat (2×, 2 yıl)

### Üriner Obstrüksiyonun Fizyopatolojisi — 11 soru, yıllar [2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tanim_kavram (%27) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.636, 'olumsuz': 0.182, 'en_tipik': 0.091, 'dogru_ifade': 0.091} · düzey {'L1_hatirlama': 0.636, 'L2_anlama_iliski': 0.364} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %18
- **Tekrar eden çekirdek kavramlar:** Hidrojen-fosfat (HPO₄²⁻) ekskresyonunda (idrarla atılımında) artış (2×, 2 yıl); Hidrojen ve fosfat ekskresyonu artar (2×, 1 yıl)

### Üriner Sistem Enfeksiyonları: Laboratuvar Bulguları ve Tedavi — 3 soru, yıllar [2026], güven dusuk
- **Neden:** etiyoloji_risk (%33) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.333, 'sayi': 0.333, 'yanlis_bul': 0.333} · düzey {'L2_anlama_iliski': 0.667, 'L1_hatirlama': 0.333} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0
