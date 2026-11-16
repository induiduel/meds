# Nöroloji — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 94 tekil çıkmış soru · güven: **orta** · yıllar: {2020: 52, 2021: 7, 2022: 7, 2023: 1}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %68 (genel ortalama %40)
- **vaka**: %10 (genel ortalama %5)
- **olumsuz**: %7 (genel ortalama %15)
- **sayi**: %5 (genel ortalama %3)
- **onculu**: %4 (genel ortalama %8)
- **yanlis_bul**: %3 (genel ortalama %13)
- **en_tipik**: %1 (genel ortalama %8)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %47 (genel ortalama %32)
- **tani_ayirici**: %16 (genel ortalama %12)
- **siniflama_ad**: %15 (genel ortalama %9)
- **mekanizma**: %13 (genel ortalama %14)
- **onleme_halk_sagligi**: %3 (genel ortalama %5)
- **ilac_endikasyon**: %3 (genel ortalama %7)
- **epidemiyoloji_sayi**: %2 (genel ortalama %2)

### Bilişsel düzey
- **L1_hatirlama**: %61 (genel ortalama %51)
- **L2_anlama_iliski**: %30 (genel ortalama %44)
- **L3_uygulama**: %10 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 17.8 kelime (p25 9 · medyan 15 · p75 21).
- Şık: ort. 2.9 kelime; bileşik şık %9; sayısal şık %8; mutlak ifadeli çeldirici %2.
- Doğru şık tek başına en uzun: %15 (genel %19). Doğru şık konumu: {'B': 0.234, 'D': 0.223, 'A': 0.213, 'C': 0.213, 'E': 0.117}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.681, 'ayni_ailede_komsu_kavram': 0.202, 'sayisal_yakin_deger': 0.085, 'bilesik_yer_degistirmeli': 0.064, 'mutlak_ifade_tuzagi': 0.021}
- Aynı bilginin yeniden sorulması: soruların %8'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %68, vaka %10, olumsuz %7.
- Kök 9–21 kelime; şık ort. 2.9 kelime, uzunluklar birbirine yakın (CV≈0.22).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %61, L2_anlama_iliski %30, L3_uygulama %10.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Periferik Nöropati — 16 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.812, 'yanlis_bul': 0.125, 'olumsuz': 0.062} · düzey {'L1_hatirlama': 0.812, 'L2_anlama_iliski': 0.188} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %19
- **Tekrar eden çekirdek kavramlar:** Nöronopati (2×, 2 yıl); Guillain-Barre sendromu (2×, 1 yıl); Basit mononöropati (2×, 1 yıl); En sık hedef antijeni presinaptik kalsiyum kanallarıdır. (2×, 1 yıl)

### Nörolojik Muayene — 16 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%62) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.938, 'olumsuz': 0.062} · düzey {'L1_hatirlama': 0.812, 'L2_anlama_iliski': 0.188} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Fasikülasyon (2×, 1 yıl)

### Bilinç Bozukluğu Olan Hastaya Yaklaşım — 12 soru, yıllar [2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tani_ayirici (%42) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.5, 'sayi': 0.25, 'olumsuz': 0.167, 'vaka': 0.083} · düzey {'L1_hatirlama': 0.583, 'L2_anlama_iliski': 0.333, 'L3_uygulama': 0.083} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Letarji (5×, 1 yıl); Kremaster refleksi (3×, 2 yıl)

### Baş ağrısına Yaklaşım — 10 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** tani_ayirici (%50) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.7, 'en_tipik': 0.1, 'onculu': 0.1, 'vaka': 0.1} · düzey {'L2_anlama_iliski': 0.6, 'L1_hatirlama': 0.3, 'L3_uygulama': 0.1} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %70
- **Tekrar eden çekirdek kavramlar:** Erkek cinsiyet (2×, 1 yıl); Subaraknoid kanama (SAK) (2×, 0 yıl)

### Kraniyal Sinir Muayenesi — 10 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%70) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.7, 'vaka': 0.2, 'onculu': 0.1} · düzey {'L1_hatirlama': 0.6, 'L3_uygulama': 0.2, 'L2_anlama_iliski': 0.2} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %10
- **Tekrar eden çekirdek kavramlar:** Sağ nervus hypoglossus (5×, 2 yıl); Sol medial longitudinal fasikulus (3×, 1 yıl)

### Bazal Gangliyonlar ve Ekstrapiramidal Sistem — 7 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** mekanizma (%71) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.857, 'dogru_ifade': 0.143} · düzey {'L2_anlama_iliski': 0.714, 'L1_hatirlama': 0.286} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %71
- **Tekrar eden çekirdek kavramlar:** Asetilkolin (2×, 1 yıl)

### Nörolojik Hastaya Yaklaşım — 7 soru, yıllar [2020], güven dusuk
- **Neden:** siniflama_ad (%29) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.714, 'vaka': 0.286} · düzey {'L1_hatirlama': 0.714, 'L3_uygulama': 0.286} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %29
- **Tekrar eden çekirdek kavramlar:** Parkinson hastalığı (2×, 1 yıl); Multipl skleroz (MS) (2×, 1 yıl)

### Medulla Spinalis Hastalıkları — 6 soru, yıllar [2020], güven dusuk
- **Neden:** tanim_kavram (%83) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.5, 'olumsuz': 0.333, 'vaka': 0.167} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.167, 'L3_uygulama': 0.167} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Spinal şok döneminde refleksler artmıştır (2×, 1 yıl)

### Felçler — 6 soru, yıllar [2020], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'vaka': 0.333, 'sayi': 0.167, 'yanlis_bul': 0.167, 'dogrudan': 0.167, 'onculu': 0.167} · düzey {'L1_hatirlama': 0.333, 'L3_uygulama': 0.333, 'L2_anlama_iliski': 0.333} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %17

### Epilepsi — 4 soru, yıllar [2020], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'onculu': 0.25, 'sayi': 0.25, 'dogrudan': 0.25, 'olumsuz': 0.25} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %25
