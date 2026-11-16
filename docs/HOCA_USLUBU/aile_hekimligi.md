# Aile Hekimliği — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 53 tekil çıkmış soru · güven: **orta** · yıllar: {2018: 2, 2020: 24, 2021: 4, 2022: 2, 2023: 6, 2025: 1}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %47 (genel ortalama %40)
- **olumsuz**: %15 (genel ortalama %15)
- **onculu**: %15 (genel ortalama %8)
- **yanlis_bul**: %11 (genel ortalama %13)
- **tanim**: %4 (genel ortalama %1)
- **sayi**: %4 (genel ortalama %3)
- **dogru_ifade**: %2 (genel ortalama %6)

### Sorulan bilgi türü (neden sorulur)
- **onleme_halk_sagligi**: %43 (genel ortalama %5)
- **tanim_kavram**: %15 (genel ortalama %32)
- **tani_ayirici**: %13 (genel ortalama %12)
- **ilac_endikasyon**: %8 (genel ortalama %7)
- **prognoz_komplikasyon**: %6 (genel ortalama %2)
- **mekanizma**: %6 (genel ortalama %14)
- **siniflama_ad**: %4 (genel ortalama %9)

### Bilişsel düzey
- **L1_hatirlama**: %58 (genel ortalama %51)
- **L2_anlama_iliski**: %42 (genel ortalama %44)

### Biçim
- Kök uzunluğu: ort. 18.3 kelime (p25 10 · medyan 13 · p75 21).
- Şık: ort. 5.2 kelime; bileşik şık %33; sayısal şık %6; mutlak ifadeli çeldirici %6.
- Doğru şık tek başına en uzun: %15 (genel %19). Doğru şık konumu: {'A': 0.283, 'E': 0.245, 'C': 0.226, 'D': 0.132, 'B': 0.113}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.415, 'bilesik_yer_degistirmeli': 0.358, 'ayni_ailede_komsu_kavram': 0.302, 'sayisal_yakin_deger': 0.057, 'mutlak_ifade_tuzagi': 0.057}
- Aynı bilginin yeniden sorulması: soruların %6'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %47, olumsuz %15, onculu %15.
- Kök 10–21 kelime; şık ort. 5.2 kelime, uzunluklar birbirine yakın (CV≈0.25).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %58, L2_anlama_iliski %42.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Yaşlılık Döneminde Güvenli Yaşamın İlkeleri — 15 soru, yıllar [2018, 2020, 2023, 2025], güven dusuk
- **Neden:** onleme_halk_sagligi (%33) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.267, 'onculu': 0.2, 'yanlis_bul': 0.133, 'olumsuz': 0.133, 'tanim': 0.067, 'dogru_ifade': 0.067, 'en_tipik': 0.067, 'sayi': 0.067} · düzey {'L2_anlama_iliski': 0.667, 'L1_hatirlama': 0.333} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %13
- **Tekrar eden çekirdek kavramlar:** Yalnız II (2×, 1 yıl); Tuvaletlerin alçaltılması (2×, 1 yıl)

### Aile Hekimliğinde Periyodik Muayeneler 1 — 14 soru, yıllar [2020, 2021, 2022, 2023], güven dusuk
- **Neden:** onleme_halk_sagligi (%64) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.571, 'olumsuz': 0.143, 'yanlis_bul': 0.143, 'onculu': 0.071, 'sayi': 0.071} · düzey {'L1_hatirlama': 0.643, 'L2_anlama_iliski': 0.357} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %50
- **Tekrar eden çekirdek kavramlar:** Eklem bozuklukları (5×, 2 yıl); Anti-HAV testi (2×, 2 yıl); 4-12 ay arası (2×, 0 yıl)

### Aile Hekimliğine Yaklaşım — 11 soru, yıllar [2020, 2021, 2023], güven dusuk
- **Neden:** tanim_kavram (%27) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'onculu': 0.273, 'dogrudan': 0.273, 'olumsuz': 0.182, 'yanlis_bul': 0.182, 'tanim': 0.091} · düzey {'L1_hatirlama': 0.545, 'L2_anlama_iliski': 0.455} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %18
- **Tekrar eden çekirdek kavramlar:** I ve III (3×, 1 yıl); Homoseksüalite tedavisi (2×, 1 yıl)

### Nikotin Bağımlılığı ve Tedavisi — 9 soru, yıllar [2020, 2021, 2023], güven dusuk
- **Neden:** onleme_halk_sagligi (%33) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.889, 'olumsuz': 0.111} · düzey {'L1_hatirlama': 1.0} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %11
- **Tekrar eden çekirdek kavramlar:** Öğren - Öner - Ölç - Önderlik et - Örgütle (4×, 1 yıl)

### Aile Hekimliğinde Periyodik Muayeneler 2 — 4 soru, yıllar [2020, 2023], güven dusuk
- **Neden:** onleme_halk_sagligi (%75) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.5, 'olumsuz': 0.25, 'onculu': 0.25} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.5} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %50
