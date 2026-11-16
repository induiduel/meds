# Tıbbi Genetik — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 179 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 6, 2019: 1, 2020: 31, 2021: 11, 2022: 9, 2023: 8, 2024: 10, 2025: 25, 2026: 12}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %60 (genel ortalama %40)
- **yanlis_bul**: %9 (genel ortalama %13)
- **olumsuz**: %9 (genel ortalama %15)
- **en_tipik**: %8 (genel ortalama %8)
- **onculu**: %4 (genel ortalama %8)
- **dogru_ifade**: %3 (genel ortalama %6)
- **sayi**: %3 (genel ortalama %3)

### Sorulan bilgi türü (neden sorulur)
- **siniflama_ad**: %24 (genel ortalama %9)
- **mekanizma**: %22 (genel ortalama %14)
- **tanim_kavram**: %21 (genel ortalama %32)
- **tani_ayirici**: %18 (genel ortalama %12)
- **ilac_endikasyon**: %4 (genel ortalama %7)
- **onleme_halk_sagligi**: %3 (genel ortalama %5)
- **epidemiyoloji_sayi**: %3 (genel ortalama %2)

### Bilişsel düzey
- **L2_anlama_iliski**: %52 (genel ortalama %44)
- **L1_hatirlama**: %46 (genel ortalama %51)
- **L3_uygulama**: %2 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 18.3 kelime (p25 10 · medyan 17 · p75 24).
- Şık: ort. 4.6 kelime; bileşik şık %25; sayısal şık %16; mutlak ifadeli çeldirici %2.
- Doğru şık tek başına en uzun: %36 (genel %19). Doğru şık konumu: {'A': 0.43, 'C': 0.179, 'D': 0.162, 'B': 0.14, 'E': 0.089}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.654, 'bilesik_yer_degistirmeli': 0.212, 'sayisal_yakin_deger': 0.162, 'ayni_ailede_komsu_kavram': 0.117, 'mutlak_ifade_tuzagi': 0.017}
- Aynı bilginin yeniden sorulması: soruların %5'i birden çok kez çıkmış.

### Dönem kayması (2023 sonrası − öncesi, puan farkı)
- {'kalip': {'olumsuz': 0.081, 'yanlis_bul': -0.099, 'dogrudan': 0.099}, 'duzey': {'L2_anlama_iliski': 0.164, 'L1_hatirlama': -0.164}, 'tur': {'tani_ayirici': 0.267, 'siniflama_ad': -0.291}}

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %60, yanlis_bul %9, olumsuz %9.
- Kök 10–24 kelime; şık ort. 4.6 kelime, uzunluklar birbirine yakın (CV≈0.29).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L2_anlama_iliski %52, L1_hatirlama %46, L3_uygulama %2.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Doğumsal Kadın/Erkek Genital Gelişim Anomalileri — 22 soru, yıllar [2018, 2020, 2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tanim_kavram (%27) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.818, 'en_tipik': 0.091, 'yanlis_bul': 0.045, 'tanim': 0.045} · düzey {'L1_hatirlama': 0.591, 'L2_anlama_iliski': 0.409} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %23
- **Tekrar eden çekirdek kavramlar:** İnterseksüel (5×, 1 yıl); Konjenital adrenal hiperplazi (21-hidroksilaz eksikliği) (3×, 2 yıl); Swyer sendromu (3×, 1 yıl); Deksametazon (2×, 2 yıl)

### Prenatal Tanı Yöntemleri — 19 soru, yıllar [2018, 2019, 2020, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tani_ayirici (%47) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.579, 'onculu': 0.158, 'yanlis_bul': 0.105, 'en_tipik': 0.053, 'sayi': 0.053, 'olumsuz': 0.053} · düzey {'L2_anlama_iliski': 0.789, 'L1_hatirlama': 0.211} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** On bir ile on dördüncü haftalar arası (3×, 1 yıl); Yalnız II (2×, 2 yıl); 11-14. hafta (2×, 0 yıl)

### Nörolojik Hastalıklar — 15 soru, yıllar [2020], güven dusuk
- **Neden:** siniflama_ad (%40) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.8, 'dogru_ifade': 0.133, 'en_tipik': 0.067} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.333} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %20
- **Tekrar eden çekirdek kavramlar:** Duchenne ve Becker musküler distro- (5×, 1 yıl)

### Kalıtsal Metabolik Hastalıklar Genetiği — 11 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** siniflama_ad (%64) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'yanlis_bul': 0.364, 'dogrudan': 0.364, 'en_tipik': 0.091, 'dogru_ifade': 0.091, 'tanim': 0.091} · düzey {'L2_anlama_iliski': 0.545, 'L1_hatirlama': 0.455} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %9
- **Tekrar eden çekirdek kavramlar:** Etkilenen bebekler doğumdan itibaren anormaldir. (3×, 1 yıl); Otozomal resesif (OR) geçişli olan bu hastalığın tanısını hayatın ilk 6 ayından önce koyma (2×, 1 yıl)

### Yaşlanma Genetiği — 9 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** mekanizma (%89) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'olumsuz': 0.333, 'onculu': 0.222, 'dogrudan': 0.222, 'yanlis_bul': 0.111, 'sayi': 0.111} · düzey {'L2_anlama_iliski': 1.0} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %11
- **Tekrar eden çekirdek kavramlar:** Beta-galaktozidaz enzim aktivitesinde azalma (3×, 2 yıl)

### Kromozomal Hastalıklar ve Genetik Danışma — 8 soru, yıllar [2018, 2023, 2025, 2026], güven dusuk
- **Neden:** mekanizma (%25) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.75, 'olumsuz': 0.125, 'yanlis_bul': 0.125} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %25
- **Tekrar eden çekirdek kavramlar:** Cri du chat sendromu (kedi miyavlaması sendromu) (2×, 2 yıl)

### Nörodejeneratif Hastalıklar Genetiği — 8 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** mekanizma (%50) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.625, 'yanlis_bul': 0.25, 'dogru_ifade': 0.125} · düzey {'L2_anlama_iliski': 0.875, 'L1_hatirlama': 0.125} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %25
- **Tekrar eden çekirdek kavramlar:** Parkinson hastalığının hareket ile ilişkili semptomları L-dihidroksifenilalanin (L-DOPA) t (2×, 1 yıl)

### Tümör Mikro Çevresi, İnvazyon ve Metastaz — 8 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** siniflama_ad (%38) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.625, 'sayi': 0.125, 'olumsuz': 0.125, 'dogru_ifade': 0.125} · düzey {'L1_hatirlama': 0.75, 'L2_anlama_iliski': 0.25} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %0

### Preimplantasyon Genetik Tanı (PGD) — 7 soru, yıllar [2022, 2024, 2025], güven dusuk
- **Neden:** tani_ayirici (%57) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.571, 'olumsuz': 0.429} · düzey {'L2_anlama_iliski': 0.571, 'L1_hatirlama': 0.429} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0

### Dismorfolojide Genetik Terminoloji — 7 soru, yıllar [2022, 2025, 2026], güven dusuk
- **Neden:** tanim_kavram (%86) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.571, 'olumsuz': 0.429} · düzey {'L1_hatirlama': 1.0} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Yarık damak/dudak (2×, 2 yıl); Rahim içi basıya bağlı kraniyofasiyal şekil bozukluğu (kafatası ve yüzün şeklinin değişmes (2×, 2 yıl)

### Ateroskleroz Genetiği — 7 soru, yıllar [2025], güven dusuk
- **Neden:** mekanizma (%57) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'olumsuz': 0.286, 'dogrudan': 0.143, 'sayi': 0.143, 'en_tipik': 0.143, 'vaka': 0.143, 'yanlis_bul': 0.143} · düzey {'L2_anlama_iliski': 0.714, 'L3_uygulama': 0.143, 'L1_hatirlama': 0.143} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %14

### Ürogenital Sistem Tümörlerinde Genetik Belirteçler ve Kliniğe Yansımaları — 6 soru, yıllar [2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tani_ayirici (%67) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 1.0} · düzey {'L2_anlama_iliski': 0.833, 'L1_hatirlama': 0.167} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Testis tümörü (germ hücreli tümör) (3×, 2 yıl)

### Kardiyovasküler Hastalıkların Genetiği — 6 soru, yıllar [2022], güven dusuk
- **Neden:** siniflama_ad (%50) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.5, 'en_tipik': 0.167, 'yanlis_bul': 0.167, 'vaka': 0.167} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.333, 'L3_uygulama': 0.167} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %17

### Konjenital Kardiyovasküler Bozukluklarda Genetik Mekanizmalar — 6 soru, yıllar [], güven dusuk
- **Neden:** siniflama_ad (%67) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'en_tipik': 0.5, 'vaka': 0.167, 'dogrudan': 0.167, 'onculu': 0.167} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.333, 'L3_uygulama': 0.167} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %33

### Metabolik Hastalıklarda Dismorfik Bulgular ve Veziküler Trafik Bozuklukları — 6 soru, yıllar [2021], güven dusuk
- **Neden:** siniflama_ad (%67) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 1.0} · düzey {'L1_hatirlama': 0.833, 'L2_anlama_iliski': 0.167} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %33

### Gastrointestinal Tümörlerin Genetiği — 5 soru, yıllar [2020, 2022, 2025], güven dusuk
- **Neden:** siniflama_ad (%40) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'yanlis_bul': 0.6, 'dogrudan': 0.2, 'sayi': 0.2} · düzey {'L2_anlama_iliski': 0.8, 'L1_hatirlama': 0.2} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0

### Beyin ve İskelet Sistemi Gelişimi Genetiği — 5 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%60) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 1.0} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %40
- **Tekrar eden çekirdek kavramlar:** Arnold-Chiari malformasyonu (2×, 1 yıl)

### Lösemi genetik özellikler ve prognostik belirteçler — 5 soru, yıllar [2022], güven dusuk
- **Neden:** tani_ayirici (%40) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.8, 'onculu': 0.2} · düzey {'L2_anlama_iliski': 0.6, 'L1_hatirlama': 0.4} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %20

### Kan Hastalıklarının Genetiği — 5 soru, yıllar [], güven dusuk
- **Neden:** siniflama_ad (%40) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.6, 'en_tipik': 0.4} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %0

### Gastrointestinal Hastalıkların Genetiği — 4 soru, yıllar [2020, 2023], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.5, 'onculu': 0.25, 'en_tipik': 0.25} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %25

### Endokrin Hastalıklar ve Genetik — 4 soru, yıllar [2021], güven dusuk
- **Neden:** mekanizma (%50) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.5, 'en_tipik': 0.25, 'olumsuz': 0.25} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %0
