# Göğüs Hastalıkları — hoca üslubu ve kazanım haritası (otomatik; `scripts/hoca_profili/uslup_analiz.py`)

> 48 tekil çıkmış soru · güven: **orta** · yıllar: {2018: 1, 2019: 1, 2020: 17, 2021: 3, 2022: 7, 2023: 1, 2025: 3}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %23 (genel ortalama %40)
- **vaka**: %19 (genel ortalama %5)
- **yanlis_bul**: %15 (genel ortalama %13)
- **en_tipik**: %12 (genel ortalama %8)
- **olumsuz**: %12 (genel ortalama %15)
- **onculu**: %8 (genel ortalama %8)
- **sayi**: %6 (genel ortalama %3)

### Sorulan bilgi türü (neden sorulur)
- **tani_ayirici**: %29 (genel ortalama %12)
- **tanim_kavram**: %23 (genel ortalama %32)
- **ilac_endikasyon**: %12 (genel ortalama %7)
- **etiyoloji_risk**: %10 (genel ortalama %11)
- **mekanizma**: %8 (genel ortalama %14)
- **siniflama_ad**: %6 (genel ortalama %9)
- **epidemiyoloji_sayi**: %4 (genel ortalama %2)

### Bilişsel düzey
- **L2_anlama_iliski**: %46 (genel ortalama %44)
- **L1_hatirlama**: %35 (genel ortalama %51)
- **L3_uygulama**: %19 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 19.4 kelime (p25 9 · medyan 18 · p75 28).
- Şık: ort. 4.8 kelime; bileşik şık %25; sayısal şık %23; mutlak ifadeli çeldirici %2.
- Doğru şık tek başına en uzun: %21 (genel %19). Doğru şık konumu: {'A': 0.25, 'B': 0.229, 'D': 0.229, 'E': 0.208, 'C': 0.083}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.417, 'ayni_ailede_komsu_kavram': 0.312, 'bilesik_yer_degistirmeli': 0.25, 'sayisal_yakin_deger': 0.229, 'mutlak_ifade_tuzagi': 0.021}
- Aynı bilginin yeniden sorulması: soruların %4'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %23, vaka %19, yanlis_bul %15.
- Kök 9–28 kelime; şık ort. 4.8 kelime, uzunluklar birbirine yakın (CV≈0.27).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L2_anlama_iliski %46, L1_hatirlama %35, L3_uygulama %19.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Pnömoniler — 25 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2025], güven dusuk
- **Neden:** tanim_kavram (%24) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.28, 'en_tipik': 0.2, 'yanlis_bul': 0.16, 'vaka': 0.12, 'onculu': 0.08, 'sayi': 0.08, 'olumsuz': 0.08} · düzey {'L1_hatirlama': 0.44, 'L2_anlama_iliski': 0.44, 'L3_uygulama': 0.12} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %8
- **Tekrar eden çekirdek kavramlar:** Pnömoni için CURB-65 hesaplanırken nabız sayısı kullanılır. (4×, 1 yıl); Ampirik tedavi yaklaşımına göre sınıflandırma (3×, 1 yıl); Sağ orta lob (2×, 1 yıl); 48 saat (2×, 1 yıl)

### Plevral efüzyon ve ampiyem — 13 soru, yıllar [2020, 2021, 2022, 2023, 2025], güven dusuk
- **Neden:** tani_ayirici (%38) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'vaka': 0.462, 'onculu': 0.077, 'dogru_ifade': 0.077, 'dogrudan': 0.077, 'sayi': 0.077, 'en_tipik': 0.077, 'olumsuz': 0.077, 'tanim': 0.077} · düzey {'L3_uygulama': 0.462, 'L1_hatirlama': 0.308, 'L2_anlama_iliski': 0.231} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %15
- **Tekrar eden çekirdek kavramlar:** Eksüda plevral efüzyon (3×, 2 yıl); I, II, III ve IV (3×, 1 yıl); Kardiyotorasik oranın normalden yüksek ölçülmesi (2×, 1 yıl)

### Obstrüktif ve restriktif akciğer hastalıkları — 10 soru, yıllar [2020, 2022, 2025], güven dusuk
- **Neden:** tani_ayirici (%40) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'yanlis_bul': 0.3, 'dogrudan': 0.3, 'olumsuz': 0.3, 'onculu': 0.1} · düzey {'L2_anlama_iliski': 0.8, 'L1_hatirlama': 0.2} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %10
