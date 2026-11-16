# FTR — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 132 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 2, 2020: 69, 2021: 11, 2022: 8, 2023: 5, 2024: 1}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %44 (genel ortalama %40)
- **dogru_ifade**: %14 (genel ortalama %6)
- **onculu**: %12 (genel ortalama %8)
- **yanlis_bul**: %9 (genel ortalama %13)
- **vaka**: %8 (genel ortalama %5)
- **en_tipik**: %6 (genel ortalama %8)
- **olumsuz**: %4 (genel ortalama %15)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %42 (genel ortalama %32)
- **tani_ayirici**: %17 (genel ortalama %12)
- **mekanizma**: %15 (genel ortalama %14)
- **siniflama_ad**: %9 (genel ortalama %9)
- **ilac_endikasyon**: %8 (genel ortalama %7)
- **onleme_halk_sagligi**: %6 (genel ortalama %5)
- **prognoz_komplikasyon**: %2 (genel ortalama %2)

### Bilişsel düzey
- **L1_hatirlama**: %46 (genel ortalama %51)
- **L2_anlama_iliski**: %46 (genel ortalama %44)
- **L3_uygulama**: %8 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 18.8 kelime (p25 8 · medyan 12 · p75 26).
- Şık: ort. 4.6 kelime; bileşik şık %25; sayısal şık %3; mutlak ifadeli çeldirici %1.
- Doğru şık tek başına en uzun: %21 (genel %19). Doğru şık konumu: {'A': 0.386, 'B': 0.174, 'C': 0.152, 'E': 0.144, 'D': 0.144}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.598, 'bilesik_yer_degistirmeli': 0.25, 'ayni_ailede_komsu_kavram': 0.242, 'sayisal_yakin_deger': 0.03, 'mutlak_ifade_tuzagi': 0.008}
- Aynı bilginin yeniden sorulması: soruların %12'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %44, dogru_ifade %14, onculu %12.
- Kök 8–26 kelime; şık ort. 4.6 kelime, uzunluklar birbirine yakın (CV≈0.27).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %46, L2_anlama_iliski %46, L3_uygulama %8.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Kas-iskelet sistemi hastalıklarında Non- farmakolojik Yaklaşımlar: Egzersiz — 25 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** ilac_endikasyon (%28) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.68, 'dogru_ifade': 0.16, 'yanlis_bul': 0.08, 'olumsuz': 0.04, 'onculu': 0.04} · düzey {'L1_hatirlama': 0.72, 'L2_anlama_iliski': 0.28} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %24
- **Tekrar eden çekirdek kavramlar:** Ani ve sistemik hastalıklar nedeniyle ölüm riskinin azalması (4×, 1 yıl); Eklem hareket açıklığına engel olan kemik yapısı (2×, 1 yıl); Proprio...egzersizi (2×, 1 yıl)

### Sık görülen nörolojik Hastalıklar ve Rehabilitasyonu — 19 soru, yıllar [2020, 2021, 2022, 2023], güven dusuk
- **Neden:** siniflama_ad (%32) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'en_tipik': 0.211, 'onculu': 0.211, 'dogrudan': 0.211, 'vaka': 0.105, 'dogru_ifade': 0.105, 'yanlis_bul': 0.105, 'sayi': 0.053} · düzey {'L2_anlama_iliski': 0.474, 'L1_hatirlama': 0.421, 'L3_uygulama': 0.105} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %11
- **Tekrar eden çekirdek kavramlar:** I ve III (2×, 2 yıl); Spastik (2×, 1 yıl); Omurilik yaralanmasında motor ve duyu kayıpları gözlenirken otonom sistem tutulumu gözlenm (2×, 1 yıl)

### Bel ağrılarına yaklaşım — 18 soru, yıllar [2020, 2021, 2023], güven dusuk
- **Neden:** tanim_kavram (%61) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.444, 'vaka': 0.222, 'dogru_ifade': 0.222, 'en_tipik': 0.056, 'onculu': 0.056} · düzey {'L1_hatirlama': 0.556, 'L3_uygulama': 0.222, 'L2_anlama_iliski': 0.222} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %28
- **Tekrar eden çekirdek kavramlar:** Spinal stenoz (3×, 1 yıl); Sabahları daha belirgin olup gün içinde hareketle rahatlayan bel ağrısı (3×, 1 yıl); Spondilolistezis (2×, 1 yıl); Ağrı arttığında kısa süreli istirahat iyi gelir (2×, 1 yıl)

### Yaşlılığa Özgü Hareket Sistemi Bozuklukları — 16 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.312, 'dogrudan': 0.25, 'olumsuz': 0.188, 'dogru_ifade': 0.125, 'onculu': 0.062, 'en_tipik': 0.062} · düzey {'L2_anlama_iliski': 0.625, 'L1_hatirlama': 0.375} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %12
- **Tekrar eden çekirdek kavramlar:** Senil osteoporozda kırık riski yoktur (3×, 1 yıl); Antiinflamatuar sitokinler sarkopeni gelişiminde etkilidir (2×, 1 yıl); I, II ve III (2×, 1 yıl)

### Üst ekstremitenin fonksiyonel anatomisi ve Muayene yöntemleri — 15 soru, yıllar [2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%47) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.4, 'onculu': 0.267, 'vaka': 0.267, 'eslestirme': 0.067} · düzey {'L2_anlama_iliski': 0.533, 'L3_uygulama': 0.267, 'L1_hatirlama': 0.2} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %47
- **Tekrar eden çekirdek kavramlar:** Karpal tünel sendromu (4×, 1 yıl); Yergason testi (2×, 2 yıl); I, II, III ve IV (2×, 1 yıl); De Quervain tendiniti (2×, 1 yıl)

### Alt ekstremitenin Fonksiyonel Anatomisi ve muayene yöntemleri — 14 soru, yıllar [2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.357, 'dogru_ifade': 0.214, 'olumsuz': 0.143, 'onculu': 0.143, 'yanlis_bul': 0.143} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.5} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %21
- **Tekrar eden çekirdek kavramlar:** Tibialis anterior (3×, 1 yıl); Trendelenburg yürüyüşü (3×, 1 yıl); II ve IV (2×, 1 yıl)

### Servikal ve lomber bölgenin fonksiyonel anatomisi ve değerlendirme — 13 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%77) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.385, 'dogru_ifade': 0.231, 'onculu': 0.231, 'yanlis_bul': 0.077, 'en_tipik': 0.077} · düzey {'L2_anlama_iliski': 0.538, 'L1_hatirlama': 0.462} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0

### Boyun ağrılarına yaklaşım — 9 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tani_ayirici (%33) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.778, 'vaka': 0.111, 'dogru_ifade': 0.111} · düzey {'L2_anlama_iliski': 0.556, 'L1_hatirlama': 0.333, 'L3_uygulama': 0.111} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %67
- **Tekrar eden çekirdek kavramlar:** Whiplash Sendromu (4×, 2 yıl)

### Nörolojik Rehabilitasyona Giriş ve Genel İlkeler — 3 soru, yıllar [2024], güven dusuk
- **Neden:** mekanizma (%100) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.667, 'en_tipik': 0.333} · düzey {'L2_anlama_iliski': 1.0} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %33
