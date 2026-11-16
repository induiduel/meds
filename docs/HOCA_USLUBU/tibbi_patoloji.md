# Tıbbi Patoloji — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 1526 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 126, 2019: 27, 2020: 693, 2021: 192, 2022: 70, 2023: 87, 2024: 40, 2025: 24, 2026: 21}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %42 (genel ortalama %40)
- **olumsuz**: %15 (genel ortalama %15)
- **yanlis_bul**: %14 (genel ortalama %13)
- **en_tipik**: %13 (genel ortalama %8)
- **dogru_ifade**: %5 (genel ortalama %6)
- **onculu**: %4 (genel ortalama %8)
- **vaka**: %3 (genel ortalama %5)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %37 (genel ortalama %32)
- **siniflama_ad**: %13 (genel ortalama %9)
- **mekanizma**: %12 (genel ortalama %14)
- **etiyoloji_risk**: %10 (genel ortalama %11)
- **tani_ayirici**: %10 (genel ortalama %12)
- **tanimlayici_bulgu**: %9 (genel ortalama %3)
- **prognoz_komplikasyon**: %3 (genel ortalama %2)

### Bilişsel düzey
- **L1_hatirlama**: %57 (genel ortalama %51)
- **L2_anlama_iliski**: %40 (genel ortalama %44)
- **L3_uygulama**: %3 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 13.9 kelime (p25 7 · medyan 10 · p75 16).
- Şık: ort. 4.2 kelime; bileşik şık %17; sayısal şık %4; mutlak ifadeli çeldirici %3.
- Doğru şık tek başına en uzun: %18 (genel %19). Doğru şık konumu: {'A': 0.225, 'D': 0.21, 'C': 0.201, 'B': 0.183, 'E': 0.181}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.709, 'bilesik_yer_degistirmeli': 0.159, 'ayni_ailede_komsu_kavram': 0.132, 'sayisal_yakin_deger': 0.035, 'mutlak_ifade_tuzagi': 0.031}
- Aynı bilginin yeniden sorulması: soruların %13'i birden çok kez çıkmış.

### Dönem kayması (2023 sonrası − öncesi, puan farkı)
- {'tur': {'etiyoloji_risk': -0.087, 'mekanizma': 0.089}}

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %42, olumsuz %15, yanlis_bul %14.
- Kök 7–16 kelime; şık ort. 4.2 kelime, uzunluklar birbirine yakın (CV≈0.29).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %57, L2_anlama_iliski %40, L3_uygulama %3.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Aşırı Duyarlılık ve Otoimmünite — 68 soru, yıllar [2018, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven orta
- **Neden:** tanim_kavram (%34) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.485, 'onculu': 0.176, 'olumsuz': 0.147, 'dogru_ifade': 0.103, 'en_tipik': 0.074, 'eslestirme': 0.015} · düzey {'L1_hatirlama': 0.559, 'L2_anlama_iliski': 0.441} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %15
- **Tekrar eden çekirdek kavramlar:** II ve IV (9×, 1 yıl); IL-2 (5×, 1 yıl); Class I MHC molekülleriyle sunulan peptitlere sadece CD8+ T hücreleri cevap verir. (4×, 1 yıl); Plazma hücreleri (4×, 1 yıl)

### Tiroid ve Paratiroid Patolojileri — 61 soru, yıllar [2018, 2020, 2021, 2022], güven orta
- **Neden:** tanim_kavram (%38) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.361, 'yanlis_bul': 0.213, 'olumsuz': 0.164, 'en_tipik': 0.148, 'dogru_ifade': 0.049, 'vaka': 0.033, 'eslestirme': 0.016, 'onculu': 0.016} · düzey {'L2_anlama_iliski': 0.525, 'L1_hatirlama': 0.443, 'L3_uygulama': 0.033} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %26
- **Tekrar eden çekirdek kavramlar:** Kapsül invazyonu ve/veya damar invazyonu varlığı (6×, 2 yıl); Stromada değişikliğe uğramış kalsitonin moleküllerinden kaynaklanan amiloid birikimlerinin (4×, 2 yıl); Radyoaktif iyod tutan nodüllerin malign olma olasılığı daha yüksektir (3×, 1 yıl); Cushing sendromu (2×, 2 yıl)

### Özofagus Hastalıkları ve Tümörleri — 38 soru, yıllar [2018, 2020, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%34) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'en_tipik': 0.263, 'olumsuz': 0.263, 'dogrudan': 0.237, 'vaka': 0.079, 'yanlis_bul': 0.079, 'sayi': 0.053, 'dogru_ifade': 0.026} · düzey {'L1_hatirlama': 0.684, 'L2_anlama_iliski': 0.237, 'L3_uygulama': 0.079} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %26
- **Tekrar eden çekirdek kavramlar:** Çoğu sublingual yerleşimlidir (%60-70). (3×, 2 yıl); Odontom (3×, 1 yıl); Özofagus adenokarsinomu (2×, 1 yıl); Seroza invazyonu (2×, 1 yıl)

### Erkek Genital Sistem ve Prostat Hastalıkları — 37 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tani_ayirici (%24) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.324, 'dogru_ifade': 0.324, 'en_tipik': 0.108, 'yanlis_bul': 0.108, 'olumsuz': 0.081, 'onculu': 0.054} · düzey {'L2_anlama_iliski': 0.568, 'L1_hatirlama': 0.432} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %54
- **Tekrar eden çekirdek kavramlar:** Peyronie hastalığı (5×, 2 yıl); Kemik metastazları, tipik olarak osteoblastik lezyonlar şeklinde radyonüklid kemik taramal (4×, 1 yıl); Alfa adrenerjik blokörlerle semptomlar şiddetlenir. (3×, 3 yıl); α1-adrenerjik reseptörler aracılığı ile tıkanıklığa bağlı şikâyetler artabilir. (3×, 2 yıl)

### Adrenal Bez Patolojileri — 37 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%27) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.297, 'olumsuz': 0.189, 'en_tipik': 0.162, 'yanlis_bul': 0.162, 'dogru_ifade': 0.135, 'sayi': 0.054} · düzey {'L1_hatirlama': 0.649, 'L2_anlama_iliski': 0.351} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %19
- **Tekrar eden çekirdek kavramlar:** Kemik metastazları sıktır (2×, 1 yıl); Otoimmün adrenalit (2×, 1 yıl); %10'u biyolojik olarak benigndir. (2×, 1 yıl); Hastaların çoğunda ön hipofizde ACTH üreten kortikotrof hücre hiperplazisi bulunur. (2×, 1 yıl)

### Endometrial Hiperplazi ve Kanserleri — 32 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024], güven dusuk
- **Neden:** tanim_kavram (%53) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.375, 'olumsuz': 0.312, 'yanlis_bul': 0.094, 'en_tipik': 0.094, 'onculu': 0.062, 'sayi': 0.031, 'dogru_ifade': 0.031} · düzey {'L1_hatirlama': 0.688, 'L2_anlama_iliski': 0.312} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %28
- **Tekrar eden çekirdek kavramlar:** Adenomyozis (4×, 2 yıl); Seröz karsinomların prognozu endometrioid karsinomlara göre daha iyidir. (4×, 2 yıl); Adenomyozis (4×, 2 yıl); Endometriyozis (4×, 1 yıl)

### Karaciğer Sirozu ve Portal Hipertansiyon — 29 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** etiyoloji_risk (%34) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.345, 'yanlis_bul': 0.207, 'en_tipik': 0.172, 'olumsuz': 0.138, 'onculu': 0.138} · düzey {'L2_anlama_iliski': 0.621, 'L1_hatirlama': 0.379} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Yıldızsı hücreler aktive olduklarında Kupffer hücrelerine dönüşür (3×, 1 yıl); Şistozoma (şistozomiyazis etkeni) (3×, 1 yıl); Rodanin (2×, 1 yıl); I, II, III ve IV (2×, 1 yıl)

### Glomeruler Hastalıklar: Nefrotik Sendrom — 29 soru, yıllar [2019, 2020, 2021, 2023], güven dusuk
- **Neden:** tanimlayici_bulgu (%52) — Patolojik/klinik imza bulgusu tanıyı koydurur; hastalığa özgü tek bulgu ödüllendirilir.
- **Nasıl:** {'dogrudan': 0.414, 'vaka': 0.207, 'en_tipik': 0.138, 'yanlis_bul': 0.103, 'olumsuz': 0.103, 'onculu': 0.034} · düzey {'L1_hatirlama': 0.621, 'L3_uygulama': 0.207, 'L2_anlama_iliski': 0.172} · Bulgudan hastalığa ya da hastalıktan bulguya (ters yön); çeldirici komşu hastalığın bulgusudur.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %34
- **Tekrar eden çekirdek kavramlar:** Minimal değişiklik hastalığı (8×, 1 yıl); Çift kontür y tren rayı gör (7×, 1 yıl); Minimal değişiklik hastalığı (3×, 2 yıl); Henoch-Schönlein purpurası (3×, 1 yıl)

### Vulva, Vajen ve Serviks Hastalıkları — 28 soru, yıllar [2019, 2020, 2021, 2023, 2024, 2026], güven dusuk
- **Neden:** tanim_kavram (%39) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.571, 'olumsuz': 0.214, 'yanlis_bul': 0.107, 'en_tipik': 0.071, 'tanim': 0.036} · düzey {'L1_hatirlama': 0.75, 'L2_anlama_iliski': 0.25} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %32
- **Tekrar eden çekirdek kavramlar:** Epidermiste incelme (6×, 1 yıl); Botrioid sarkom (4×, 1 yıl); Koilositoz (3×, 2 yıl); Herpes Simpleks (3×, 1 yıl)

### Vasküler ve Kistik Böbrek Hastalıkları — 27 soru, yıllar [2019, 2020, 2021, 2022, 2023, 2024], güven dusuk
- **Neden:** tanim_kavram (%41) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.593, 'en_tipik': 0.148, 'yanlis_bul': 0.111, 'dogru_ifade': 0.074, 'onculu': 0.037, 'olumsuz': 0.037} · düzey {'L1_hatirlama': 0.741, 'L2_anlama_iliski': 0.259} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %30
- **Tekrar eden çekirdek kavramlar:** Malign hipertansiyon (Malign nefroskleroz) (7×, 1 yıl); Malign hipertansiyon (malign nefroskleroz) (5×, 2 yıl); Nefronofitizis-medüller kistik hastalık kompleksi (4×, 3 yıl); Nefrosistin (4×, 1 yıl)

### Akut ve Kronik Viral Hepatitler — 27 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** etiyoloji_risk (%30) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.444, 'olumsuz': 0.259, 'yanlis_bul': 0.185, 'en_tipik': 0.074, 'vaka': 0.037} · düzey {'L1_hatirlama': 0.593, 'L2_anlama_iliski': 0.37, 'L3_uygulama': 0.037} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %4
- **Tekrar eden çekirdek kavramlar:** Portal alanlarda köprüleşme fibrozisi (3×, 1 yıl); Köprüleşme nekrozu (3×, 1 yıl); Hepatosit sitoplazmasında buzlu cam görünümü (2×, 1 yıl); Siroza dönüşmez (2×, 1 yıl)

### Memenin Benign Hastalıkları — 26 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], güven dusuk
- **Neden:** tanim_kavram (%77) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.269, 'en_tipik': 0.231, 'dogrudan': 0.231, 'eslestirme': 0.077, 'yanlis_bul': 0.077, 'onculu': 0.038, 'dogru_ifade': 0.038, 'vaka': 0.038} · düzey {'L1_hatirlama': 0.731, 'L2_anlama_iliski': 0.231, 'L3_uygulama': 0.038} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %35
- **Tekrar eden çekirdek kavramlar:** Fibroadenom (6×, 2 yıl); Terminal duktal lobüler ünite – Duktal ektazi (4×, 1 yıl); Filloides tümör (3×, 1 yıl); Apokrin metaplazi (3×, 1 yıl)

### Üst Solunum Yolu Hastalıkları — 26 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** mekanizma (%38) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.5, 'yanlis_bul': 0.192, 'en_tipik': 0.154, 'tanim': 0.038, 'vaka': 0.038, 'dogru_ifade': 0.038, 'olumsuz': 0.038} · düzey {'L2_anlama_iliski': 0.654, 'L1_hatirlama': 0.308, 'L3_uygulama': 0.038} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %4
- **Tekrar eden çekirdek kavramlar:** Rinitis sicca (4×, 2 yıl); Septum anterior bölgesi (3×, 2 yıl); Genellikle kanserözdür. (2×, 1 yıl); Hasta eve gönderilmeyi hospitalize edilir (2×, 1 yıl)

### Akciğer Tümörleri — 25 soru, yıllar [2019, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%40) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.56, 'en_tipik': 0.16, 'yanlis_bul': 0.12, 'vaka': 0.08, 'sayi': 0.04, 'eslestirme': 0.04} · düzey {'L1_hatirlama': 0.56, 'L2_anlama_iliski': 0.36, 'L3_uygulama': 0.08} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %4
- **Tekrar eden çekirdek kavramlar:** Küçük hücreli karsinom (4×, 2 yıl); Adenokarsinom (3×, 1 yıl); Skuamöz hücreli karsinom (2×, 1 yıl)

### Pankreas ve Nöroendokrin Tümörler ve MEN Sendromu — 25 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** siniflama_ad (%48) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.24, 'olumsuz': 0.2, 'yanlis_bul': 0.16, 'en_tipik': 0.16, 'vaka': 0.08, 'onculu': 0.08, 'sayi': 0.04, 'eslestirme': 0.04} · düzey {'L1_hatirlama': 0.56, 'L2_anlama_iliski': 0.36, 'L3_uygulama': 0.08} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %20
- **Tekrar eden çekirdek kavramlar:** Somatotropin (3×, 1 yıl); Tripsin (3×, 1 yıl); Duodenum (2×, 1 yıl); Primer hiperparatiroidi (2×, 1 yıl)

### Yumuşak Doku Tümörleri — 24 soru, yıllar [2018, 2020, 2021, 2022, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%46) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'en_tipik': 0.375, 'dogrudan': 0.125, 'olumsuz': 0.125, 'yanlis_bul': 0.125, 'vaka': 0.083, 'dogru_ifade': 0.083, 'onculu': 0.042, 'sayi': 0.042} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.25, 'L3_uygulama': 0.083} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %8
- **Tekrar eden çekirdek kavramlar:** Myozitis ossiÕkans (4×, 1 yıl); El (2×, 1 yıl); Lipom (2×, 1 yıl); Verocay cisimcikleri içeren Antoni A ve Antoni B alanları (2×, 1 yıl)

### Over Tümörleri — 24 soru, yıllar [2019, 2020, 2021, 2023, 2024, 2025], güven dusuk
- **Neden:** tanim_kavram (%38) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.417, 'olumsuz': 0.208, 'yanlis_bul': 0.167, 'dogru_ifade': 0.083, 'eslestirme': 0.083, 'sayi': 0.042} · düzey {'L1_hatirlama': 0.583, 'L2_anlama_iliski': 0.417} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Hastalarda insülin rezistansı izlenmez. (6×, 1 yıl); Over (4×, 2 yıl); Düşük LDH seviyeleri (3×, 2 yıl); Fibrotekom (3×, 1 yıl)

### Meme Kanseri ve Moleküler Tipleri — 24 soru, yıllar [2018, 2020, 2021, 2022, 2023, 2024, 2025], güven dusuk
- **Neden:** siniflama_ad (%33) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.458, 'yanlis_bul': 0.25, 'en_tipik': 0.125, 'onculu': 0.083, 'olumsuz': 0.042, 'vaka': 0.042} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.458, 'L3_uygulama': 0.042} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Meme başının Paget hastalığı (3×, 1 yıl); Komedo tip (3×, 1 yıl); İnvaziv duktal karsinom (2×, 2 yıl); Özel tipleri içinde en kötü prognoza sahip tip tübüler karsinomdur. (2×, 1 yıl)

### Kolestatik Karaciğer Hastalıkları — 23 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%26) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.348, 'yanlis_bul': 0.261, 'sayi': 0.174, 'tanim': 0.087, 'en_tipik': 0.043, 'onculu': 0.043, 'dogru_ifade': 0.043} · düzey {'L2_anlama_iliski': 0.522, 'L1_hatirlama': 0.478} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %39
- **Tekrar eden çekirdek kavramlar:** Otoimmün mekanizmalar (3×, 1 yıl); ALT/AST oranının 2 kat artmış olması (2×, 1 yıl); Süpüratif kolanjit ve ekstrahepatik safra kanallarının harabiyeti vardır (2×, 1 yıl); Radyolojik bulguların normal olması (2×, 1 yıl)

### Genetik, Pediatrik ve Çevresel Patoloji — 23 soru, yıllar [2018, 2020, 2021, 2022, 2023, 2026], güven dusuk
- **Neden:** tanim_kavram (%39) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.435, 'dogrudan': 0.261, 'onculu': 0.13, 'en_tipik': 0.13, 'olumsuz': 0.043} · düzey {'L2_anlama_iliski': 0.696, 'L1_hatirlama': 0.304} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %4
- **Tekrar eden çekirdek kavramlar:** Terde düşük sodyum klorür düzeyi KF için sabit ve karakteristik biyokimyasal anormalliktir (3×, 2 yıl); Retinoblastom (2×, 2 yıl); Heksozaminidaz A enziminin beta alt biriminin eksikliği ile karakterizedir. (2×, 1 yıl)

### Makrositer ve Hemolitik Anemiler — 21 soru, yıllar [2018, 2020, 2022, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%38) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.714, 'olumsuz': 0.095, 'yanlis_bul': 0.095, 'onculu': 0.048, 'vaka': 0.048} · düzey {'L1_hatirlama': 0.571, 'L2_anlama_iliski': 0.381, 'L3_uygulama': 0.048} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %24
- **Tekrar eden çekirdek kavramlar:** Vazo-oklüzyon, geri dönüşümsüz olarak oraklaşmış eritrositlerin miktarı ile orantılıdır (4×, 1 yıl); Herediter sferositoz (2×, 1 yıl); İmmün hemolitik anemi (2×, 1 yıl)

### Uterus Düz Kas ve Trofoblastik Tümörleri — 21 soru, yıllar [2019, 2020, 2021, 2022, 2023, 2024, 2025], güven dusuk
- **Neden:** tanim_kavram (%43) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'en_tipik': 0.286, 'dogrudan': 0.238, 'olumsuz': 0.19, 'yanlis_bul': 0.143, 'onculu': 0.095, 'tanim': 0.048} · düzey {'L1_hatirlama': 0.524, 'L2_anlama_iliski': 0.476} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %14
- **Tekrar eden çekirdek kavramlar:** Geçirilmiş ektopik gebelik öyküsü (4×, 1 yıl); Fetusa ait parçalar, komplet mollerde yaygın olarak görülürken, parsiyel mollerde çok nadi (3×, 1 yıl); Leiomyom (2×, 2 yıl); Akut koryoamniyonit (2×, 1 yıl)

### Nörodejeneratif Hastalıklar — 21 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** siniflama_ad (%38) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.571, 'olumsuz': 0.095, 'yanlis_bul': 0.095, 'en_tipik': 0.095, 'vaka': 0.048, 'dogru_ifade': 0.048, 'tanim': 0.048} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.286, 'L3_uygulama': 0.048} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %43
- **Tekrar eden çekirdek kavramlar:** Myastenia Gravis (2×, 2 yıl); Lewy cisimcikli demans (2×, 2 yıl); Wernicke ensefalopatisi (2×, 1 yıl); Aβ amiloid (2×, 1 yıl)

### İnvaziv Serviks Kanseri ve Endometriyozis — 20 soru, yıllar [2020, 2021, 2024], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.45, 'onculu': 0.2, 'olumsuz': 0.15, 'yanlis_bul': 0.15, 'en_tipik': 0.05} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %15
- **Tekrar eden çekirdek kavramlar:** I ve III (7×, 2 yıl); Uterin serviks (3×, 1 yıl); p53 tümör baskılayıcı geni (3×, 1 yıl); Yalnız I (3×, 1 yıl)

### Hücre Hasarı ve Nekroz - I — 20 soru, yıllar [2020, 2021, 2022, 2023, 2025, 2026], güven dusuk
- **Neden:** mekanizma (%40) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.45, 'en_tipik': 0.15, 'yanlis_bul': 0.1, 'olumsuz': 0.1, 'dogru_ifade': 0.05, 'tanim': 0.05, 'sayi': 0.05, 'eslestirme': 0.05} · düzey {'L2_anlama_iliski': 0.6, 'L1_hatirlama': 0.4} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %15
- **Tekrar eden çekirdek kavramlar:** Likefaksiyon nekrozu (4×, 1 yıl); Koagülasyon nekrozu (4×, 1 yıl); Hücre dışına sodyum (Na⁺) çıkışı (3×, 1 yıl); Sitozolik kalsiyum artışı (2×, 1 yıl)
