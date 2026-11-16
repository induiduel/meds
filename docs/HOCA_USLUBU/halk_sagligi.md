# Halk Sağlığı — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 362 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 28, 2019: 13, 2020: 174, 2021: 62, 2022: 11, 2023: 15, 2024: 15, 2025: 16, 2026: 6}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %45 (genel ortalama %40)
- **sayi**: %13 (genel ortalama %3)
- **olumsuz**: %10 (genel ortalama %15)
- **yanlis_bul**: %9 (genel ortalama %13)
- **onculu**: %8 (genel ortalama %8)
- **dogru_ifade**: %6 (genel ortalama %6)
- **en_tipik**: %3 (genel ortalama %8)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %33 (genel ortalama %32)
- **onleme_halk_sagligi**: %21 (genel ortalama %5)
- **tani_ayirici**: %12 (genel ortalama %12)
- **mekanizma**: %9 (genel ortalama %14)
- **epidemiyoloji_sayi**: %6 (genel ortalama %2)
- **etiyoloji_risk**: %6 (genel ortalama %11)
- **siniflama_ad**: %6 (genel ortalama %9)

### Bilişsel düzey
- **L1_hatirlama**: %58 (genel ortalama %51)
- **L2_anlama_iliski**: %40 (genel ortalama %44)
- **L3_uygulama**: %2 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 15.3 kelime (p25 8 · medyan 11 · p75 18).
- Şık: ort. 4.0 kelime; bileşik şık %22; sayısal şık %16; mutlak ifadeli çeldirici %4.
- Doğru şık tek başına en uzun: %12 (genel %19). Doğru şık konumu: {'A': 0.273, 'D': 0.24, 'C': 0.18, 'E': 0.157, 'B': 0.149}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.558, 'bilesik_yer_degistirmeli': 0.21, 'ayni_ailede_komsu_kavram': 0.196, 'sayisal_yakin_deger': 0.163, 'mutlak_ifade_tuzagi': 0.039}
- Aynı bilginin yeniden sorulması: soruların %14'i birden çok kez çıkmış.

### Dönem kayması (2023 sonrası − öncesi, puan farkı)
- {'kalip': {'sayi': 0.08, 'yanlis_bul': -0.086, 'dogrudan': -0.091}, 'duzey': {'L2_anlama_iliski': -0.115}, 'tur': {'onleme_halk_sagligi': 0.166, 'tani_ayirici': -0.112}}

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %45, sayi %13, olumsuz %10.
- Kök 8–18 kelime; şık ort. 4.0 kelime, uzunluklar birbirine yakın (CV≈0.23).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %58, L2_anlama_iliski %40, L3_uygulama %2.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Ana-Çocuk Sağlığı Düzeyinin İzlenmesi — 44 soru, yıllar [2019, 2020, 2021, 2023, 2024, 2025, 2026], güven orta
- **Neden:** onleme_halk_sagligi (%32) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.568, 'sayi': 0.159, 'olumsuz': 0.091, 'dogru_ifade': 0.068, 'vaka': 0.068, 'en_tipik': 0.045} · düzey {'L1_hatirlama': 0.636, 'L2_anlama_iliski': 0.295, 'L3_uygulama': 0.068} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %20
- **Tekrar eden çekirdek kavramlar:** Tetanoz (13×, 4 yıl); İzlemin gebeliğin 5. ayında başlamış olması (8×, 2 yıl); Doğurganlığı özendirmek, doğal nüfus artış hızına katkıda bulunmak (5×, 2 yıl); İnfertilite tedavisi (5×, 2 yıl)

### Bağışıklama ve önemi — 30 soru, yıllar [2019, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** onleme_halk_sagligi (%77) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.667, 'olumsuz': 0.233, 'vaka': 0.067, 'eslestirme': 0.033} · düzey {'L1_hatirlama': 0.9, 'L3_uygulama': 0.067, 'L2_anlama_iliski': 0.033} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Rotavirüs (5×, 1 yıl); Meningokok aşısı (4×, 2 yıl); BCG (4×, 1 yıl); BCG (2×, 2 yıl)

### Bebek Beslenmesi — 22 soru, yıllar [2019, 2020, 2021, 2022, 2024, 2025, 2026], güven dusuk
- **Neden:** tanim_kavram (%45) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'sayi': 0.455, 'dogrudan': 0.227, 'yanlis_bul': 0.136, 'onculu': 0.091, 'dogru_ifade': 0.045, 'olumsuz': 0.045} · düzey {'L1_hatirlama': 0.727, 'L2_anlama_iliski': 0.273} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %41
- **Tekrar eden çekirdek kavramlar:** 3 saat (7×, 3 yıl); 3 saat (3×, 2 yıl); %60 (3×, 1 yıl); Bebekler 1 yaşında doğum ağırlıklarının 4 katına ulaşırlar (2×, 2 yıl)

### Epidemiyolojiye Giriş — 20 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** tani_ayirici (%40) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.45, 'tanim': 0.15, 'sayi': 0.15, 'yanlis_bul': 0.1, 'olumsuz': 0.05, 'en_tipik': 0.05, 'onculu': 0.05} · düzey {'L2_anlama_iliski': 0.65, 'L1_hatirlama': 0.35} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %40
- **Tekrar eden çekirdek kavramlar:** Sporadi (5×, 2 yıl); İnsidans (2×, 1 yıl); %22 (2×, 1 yıl)

### Yeterli ve Dengeli Beslenme — 19 soru, yıllar [2018, 2020, 2021, 2022, 2023, 2025], güven dusuk
- **Neden:** mekanizma (%32) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.316, 'dogru_ifade': 0.211, 'yanlis_bul': 0.158, 'olumsuz': 0.105, 'sayi': 0.105, 'onculu': 0.105} · düzey {'L2_anlama_iliski': 0.632, 'L1_hatirlama': 0.368} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %53
- **Tekrar eden çekirdek kavramlar:** Ağır şişman (morbid obez) (5×, 1 yıl); % 60-70 (4×, 1 yıl); Yaş ile azalır (2×, 2 yıl); Bağırsak kanseri riskinde artışa neden olma (2×, 1 yıl)

### Sağlık Yönetimi — 18 soru, yıllar [2018, 2020, 2022], güven dusuk
- **Neden:** tanim_kavram (%83) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.667, 'olumsuz': 0.222, 'dogru_ifade': 0.111} · düzey {'L1_hatirlama': 0.944, 'L2_anlama_iliski': 0.056} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %56
- **Tekrar eden çekirdek kavramlar:** Vizyon (3×, 2 yıl); Kararlar; birimler, kurullar ve komisyonlar kanalı ile alınır (3×, 1 yıl); Hastalar (3×, 1 yıl); Yönlendirme (3×, 1 yıl)

### Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri — 15 soru, yıllar [2019, 2020, 2021, 2023], güven dusuk
- **Neden:** tani_ayirici (%47) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.533, 'sayi': 0.267, 'yanlis_bul': 0.133, 'onculu': 0.067} · düzey {'L2_anlama_iliski': 0.667, 'L1_hatirlama': 0.333} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Tecrit (8×, 2 yıl); Eradikasyon (5×, 2 yıl); Filyasyon (4×, 3 yıl); Eliminasyon (4×, 2 yıl)

### Kanser Hastalıkları Epidemiyolojisi — 15 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024], güven dusuk
- **Neden:** tanim_kavram (%47) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'en_tipik': 0.4, 'onculu': 0.267, 'sayi': 0.133, 'yanlis_bul': 0.133, 'eslestirme': 0.067} · düzey {'L2_anlama_iliski': 0.6, 'L1_hatirlama': 0.4} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Tiroid (3×, 2 yıl); Lösemi (3×, 1 yıl); Akciğer (2×, 2 yıl); 0.4 (2×, 1 yıl)

### Çevre Sağlığına Giriş ve Genel Bilgiler — 14 soru, yıllar [2018, 2020, 2023], güven dusuk
- **Neden:** tanim_kavram (%57) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.357, 'yanlis_bul': 0.286, 'olumsuz': 0.071, 'sayi': 0.071, 'eslestirme': 0.071, 'en_tipik': 0.071, 'onculu': 0.071} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.5} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %21
- **Tekrar eden çekirdek kavramlar:** Tavsiye edilen atık depolama metodlarından biridir (2×, 1 yıl); 500 mikrogram/m3/10 dakika (2×, 1 yıl); Biyolojik savaşta temel hedef, sivillerde panik ve kargaşa yaratmaktır. (2×, 0 yıl)

### Akılcı İlaç Kullanımı — 13 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%69) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.308, 'olumsuz': 0.308, 'dogrudan': 0.231, 'tanim': 0.077, 'onculu': 0.077} · düzey {'L2_anlama_iliski': 0.538, 'L1_hatirlama': 0.462} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** İlaç-ilaç etkileşimleri ve besin-ilaç etkileşimlerinin dikkate alınması (3×, 1 yıl); Hastalık ve ölümlerde artış olabilmesi (3×, 1 yıl)

### İş kazaları — 12 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** mekanizma (%75) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.583, 'dogru_ifade': 0.167, 'sayi': 0.083, 'onculu': 0.083, 'yanlis_bul': 0.083} · düzey {'L2_anlama_iliski': 0.75, 'L1_hatirlama': 0.25} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %67
- **Tekrar eden çekirdek kavramlar:** İş kazalarının %2'si kaçınılmazdır. (2×, 1 yıl); Koruyucusuz ekipmanlar, uygun olmayan koruyucular (2×, 1 yıl)

### Sağlığın geliştirilmesi — 11 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%55) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.727, 'onculu': 0.182, 'dogru_ifade': 0.091} · düzey {'L1_hatirlama': 0.545, 'L2_anlama_iliski': 0.455} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %55
- **Tekrar eden çekirdek kavramlar:** Sağlıkla ilgili risk faktörlerinin azalması (4×, 2 yıl); 1986 (3×, 1 yıl); Milano Bildirgesi (2×, 1 yıl)

### Meslek hastalıkları — 11 soru, yıllar [2020], güven dusuk
- **Neden:** siniflama_ad (%45) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.636, 'sayi': 0.182, 'dogru_ifade': 0.091, 'olumsuz': 0.091} · düzey {'L1_hatirlama': 0.909, 'L2_anlama_iliski': 0.091} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %45

### Vaka-Kontrol çalışmaları — 11 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** etiyoloji_risk (%36) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'yanlis_bul': 0.273, 'dogru_ifade': 0.273, 'dogrudan': 0.182, 'sayi': 0.182, 'onculu': 0.091} · düzey {'L2_anlama_iliski': 0.545, 'L1_hatirlama': 0.455} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Etken sonuç ilişkisini çok iyi gösterir (2×, 2 yıl); Vaka-kontrol tipi araştırmalarda tespit edilir. (2×, 1 yıl)

### Halk Sağlığı Tarihçesi — 11 soru, yıllar [2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** onleme_halk_sagligi (%55) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.364, 'olumsuz': 0.273, 'onculu': 0.182, 'yanlis_bul': 0.091, 'eslestirme': 0.091} · düzey {'L1_hatirlama': 0.545, 'L2_anlama_iliski': 0.455} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Kan basıncı (tansiyon) ölçümü (2×, 2 yıl)

### Önemli Beslenme Sorunları — 11 soru, yıllar [2018, 2020, 2021, 2025], güven dusuk
- **Neden:** tanim_kavram (%45) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.636, 'onculu': 0.182, 'dogru_ifade': 0.091, 'yanlis_bul': 0.091} · düzey {'L1_hatirlama': 0.545, 'L2_anlama_iliski': 0.455} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %27

### Sağlık Göstergeleri — 10 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** prognoz_komplikasyon (%40) — Seyir ve komplikasyon izlem ve tedavi kararını belirler.
- **Nasıl:** {'sayi': 0.7, 'dogru_ifade': 0.1, 'tanim': 0.1, 'dogrudan': 0.1} · düzey {'L2_anlama_iliski': 0.8, 'L1_hatirlama': 0.2} · Komplikasyon ya da prognoz belirleyicisi sorulur; çeldirici başka hastalığın komplikasyonudur.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %10
- **Tekrar eden çekirdek kavramlar:** 0,4 (8×, 2 yıl)

### Sağlık Eğitimi — 10 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** onleme_halk_sagligi (%80) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'olumsuz': 0.3, 'onculu': 0.2, 'dogru_ifade': 0.2, 'dogrudan': 0.2, 'eslestirme': 0.1} · düzey {'L1_hatirlama': 0.7, 'L2_anlama_iliski': 0.3} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %20
- **Tekrar eden çekirdek kavramlar:** Sadece hekim olmalı (2×, 1 yıl); Sağlık eğitiminde sadece doktorlar görev almalıdır. (2×, 1 yıl)

### Yaşlı Sağlığı Sorunları ve Sağlık Hizmetleri — 10 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** tanim_kavram (%40) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.4, 'olumsuz': 0.2, 'yanlis_bul': 0.1, 'onculu': 0.1, 'dogru_ifade': 0.1, 'sayi': 0.1} · düzey {'L1_hatirlama': 0.7, 'L2_anlama_iliski': 0.3} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Yaşlılığa bağlı senil purpura (3×, 1 yıl); I, II, III ve IV (2×, 2 yıl)

### Gebelik ve Emzirme Döneminde Beslenme — 9 soru, yıllar [2021, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%44) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.556, 'sayi': 0.222, 'olumsuz': 0.111, 'onculu': 0.111} · düzey {'L1_hatirlama': 0.778, 'L2_anlama_iliski': 0.222} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %44
- **Tekrar eden çekirdek kavramlar:** Sağlık eğitimi (3×, 1 yıl)

### Kohort Çalışmaları — 8 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%38) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.5, 'yanlis_bul': 0.25, 'dogru_ifade': 0.125, 'sayi': 0.125} · düzey {'L1_hatirlama': 0.625, 'L2_anlama_iliski': 0.375} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Kohort çalışmalarının sonuçları evrene genellenebilir. (2×, 2 yıl); Toplumda az görülen hastalıklar için uygun olan yöntemdir (2×, 2 yıl)

### Türkiye’de Sağlık Hizmetleri — 8 soru, yıllar [2018, 2020, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%88) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.75, 'onculu': 0.125, 'olumsuz': 0.125} · düzey {'L1_hatirlama': 0.875, 'L2_anlama_iliski': 0.125} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %0

### Enfeksiyon Hastalıklarının Epidemiyolojisi — 6 soru, yıllar [2020, 2021, 2025], güven dusuk
- **Neden:** tani_ayirici (%100) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.333, 'tanim': 0.333, 'eslestirme': 0.333} · düzey {'L2_anlama_iliski': 1.0} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %67
- **Tekrar eden çekirdek kavramlar:** Bir hastalığın bir toplulukta alışılmış seyrinden daha fazla görülmesi (5×, 2 yıl); Epidemi (2×, 2 yıl)

### Koruyucu Sağlık Hizmetleri — 5 soru, yıllar [2018, 2019, 2022, 2024], güven dusuk
- **Neden:** onleme_halk_sagligi (%40) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.6, 'yanlis_bul': 0.2, 'onculu': 0.2} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %0

### Mobbing — 4 soru, yıllar [2020], güven dusuk
- **Neden:** tanim_kavram (%100) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'vaka': 0.25, 'dogrudan': 0.25, 'olumsuz': 0.25, 'sayi': 0.25} · düzey {'L1_hatirlama': 0.75, 'L3_uygulama': 0.25} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %50
