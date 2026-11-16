# Beyin ve Sinir Cerrahisi — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 37 tekil çıkmış soru · güven: **dusuk** · yıllar: {2020: 16, 2022: 1, 2023: 2, 2024: 2}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %46 (genel ortalama %40)
- **dogru_ifade**: %19 (genel ortalama %6)
- **onculu**: %8 (genel ortalama %8)
- **en_tipik**: %8 (genel ortalama %8)
- **vaka**: %8 (genel ortalama %5)
- **olumsuz**: %5 (genel ortalama %15)
- **yanlis_bul**: %3 (genel ortalama %13)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %38 (genel ortalama %32)
- **mekanizma**: %22 (genel ortalama %14)
- **tani_ayirici**: %16 (genel ortalama %12)
- **siniflama_ad**: %11 (genel ortalama %9)
- **onleme_halk_sagligi**: %5 (genel ortalama %5)
- **ilac_endikasyon**: %3 (genel ortalama %7)
- **etiyoloji_risk**: %3 (genel ortalama %11)

### Bilişsel düzey
- **L1_hatirlama**: %54 (genel ortalama %51)
- **L2_anlama_iliski**: %38 (genel ortalama %44)
- **L3_uygulama**: %8 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 23.5 kelime (p25 9 · medyan 18 · p75 30).
- Şık: ort. 5.2 kelime; bileşik şık %28; sayısal şık %8; mutlak ifadeli çeldirici %8.
- Doğru şık tek başına en uzun: %22 (genel %19). Doğru şık konumu: {'B': 0.27, 'A': 0.27, 'C': 0.189, 'D': 0.135, 'E': 0.135}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.514, 'bilesik_yer_degistirmeli': 0.243, 'ayni_ailede_komsu_kavram': 0.162, 'mutlak_ifade_tuzagi': 0.081, 'sayisal_yakin_deger': 0.081}
- Aynı bilginin yeniden sorulması: soruların %5'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %46, dogru_ifade %19, onculu %8.
- Kök 9–30 kelime; şık ort. 5.2 kelime, uzunluklar birbirine yakın (CV≈0.21).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %54, L2_anlama_iliski %38, L3_uygulama %8.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Kafa ve Omurilik Yaralanmaları — 15 soru, yıllar [2020], güven dusuk
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.667, 'vaka': 0.133, 'en_tipik': 0.067, 'sayi': 0.067, 'olumsuz': 0.067} · düzey {'L2_anlama_iliski': 0.467, 'L1_hatirlama': 0.4, 'L3_uygulama': 0.133} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %40
- **Tekrar eden çekirdek kavramlar:** Transkraniyal ultrasonografi (2×, 1 yıl); Travmatik subdural kanama tanisında ilk yapılacak gõrüntüleme, perfüzyon MR görüntulemesid (2×, 1 yıl); 7 (2×, 0 yıl)

### Kafatasını oluşturan kemiklerin travmaları — 8 soru, yıllar [2020, 2024], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogru_ifade': 0.375, 'yanlis_bul': 0.125, 'onculu': 0.125, 'en_tipik': 0.125, 'dogrudan': 0.125, 'olumsuz': 0.125} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Kafa tabanı kırıklarında doğrudan travma olmadan, saatler sonra gelişen periorbital ekimoz (2×, 1 yıl)

### Medulla Spinalis lezyonları — 6 soru, yıllar [2020, 2023, 2024], güven dusuk
- **Neden:** siniflama_ad (%50) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.5, 'dogru_ifade': 0.5} · düzey {'L1_hatirlama': 1.0} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Büyük lezyonlarda dorsal kolonlar, tractus corticospinalis ve tractus spinothalamicus etki (2×, 1 yıl)

### İntrakraniyal Kitlelerde Belirti ve Bulgular — 4 soru, yıllar [2020, 2023], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.5, 'onculu': 0.25, 'en_tipik': 0.25} · düzey {'L1_hatirlama': 0.75, 'L2_anlama_iliski': 0.25} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %25

### Kafa travmasına eşlik eden erken dönem klinik sorunlar — 4 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** onleme_halk_sagligi (%50) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogru_ifade': 0.25, 'dogrudan': 0.25, 'onculu': 0.25, 'vaka': 0.25} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.25, 'L3_uygulama': 0.25} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0
