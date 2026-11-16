# Enfeksiyon Hastalıkları — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 409 tekil çıkmış soru · güven: **yuksek** · yıllar: {2016: 2, 2018: 21, 2019: 30, 2020: 160, 2021: 81, 2022: 17, 2023: 31, 2024: 32, 2025: 22, 2026: 19}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %26 (genel ortalama %40)
- **olumsuz**: %22 (genel ortalama %15)
- **yanlis_bul**: %19 (genel ortalama %13)
- **dogru_ifade**: %11 (genel ortalama %6)
- **en_tipik**: %7 (genel ortalama %8)
- **vaka**: %7 (genel ortalama %5)
- **onculu**: %5 (genel ortalama %8)

### Sorulan bilgi türü (neden sorulur)
- **etiyoloji_risk**: %33 (genel ortalama %11)
- **tanim_kavram**: %23 (genel ortalama %32)
- **tani_ayirici**: %16 (genel ortalama %12)
- **mekanizma**: %7 (genel ortalama %14)
- **onleme_halk_sagligi**: %7 (genel ortalama %5)
- **ilac_endikasyon**: %6 (genel ortalama %7)
- **siniflama_ad**: %4 (genel ortalama %9)

### Bilişsel düzey
- **L1_hatirlama**: %47 (genel ortalama %51)
- **L2_anlama_iliski**: %46 (genel ortalama %44)
- **L3_uygulama**: %7 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 13.7 kelime (p25 8 · medyan 10 · p75 16).
- Şık: ort. 4.7 kelime; bileşik şık %20; sayısal şık %2; mutlak ifadeli çeldirici %5.
- Doğru şık tek başına en uzun: %17 (genel %19). Doğru şık konumu: {'E': 0.249, 'C': 0.21, 'B': 0.198, 'A': 0.174, 'D': 0.169}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.77, 'bilesik_yer_degistirmeli': 0.149, 'ayni_ailede_komsu_kavram': 0.081, 'mutlak_ifade_tuzagi': 0.049, 'sayisal_yakin_deger': 0.015}
- Aynı bilginin yeniden sorulması: soruların %18'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %26, olumsuz %22, yanlis_bul %19.
- Kök 8–16 kelime; şık ort. 4.7 kelime, uzunluklar birbirine yakın (CV≈0.31).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %47, L2_anlama_iliski %46, L3_uygulama %7.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler — 53 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven orta
- **Neden:** etiyoloji_risk (%45) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.34, 'olumsuz': 0.302, 'yanlis_bul': 0.113, 'dogru_ifade': 0.075, 'onculu': 0.057, 'vaka': 0.038, 'sayi': 0.038, 'en_tipik': 0.019, 'tanim': 0.019} · düzey {'L1_hatirlama': 0.604, 'L2_anlama_iliski': 0.358, 'L3_uygulama': 0.038} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %13
- **Tekrar eden çekirdek kavramlar:** Üreter (8×, 3 yıl); Neisseria gonorrhoeae (5×, 1 yıl); İnsandan insana bulaşırlar (2×, 2 yıl); Kan dolaşımı (2×, 2 yıl)

### Bağışıklığı Baskılı Hastalarda Enfeksiyon — 48 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven orta
- **Neden:** tanim_kavram (%40) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.312, 'dogrudan': 0.229, 'yanlis_bul': 0.188, 'en_tipik': 0.167, 'dogru_ifade': 0.083, 'onculu': 0.021} · düzey {'L2_anlama_iliski': 0.521, 'L1_hatirlama': 0.479} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %15
- **Tekrar eden çekirdek kavramlar:** Febril nötropenide izole hümoral immün yetmezlik vardır. (8×, 2 yıl); Kadın cinsiyet (8×, 2 yıl); Persistan jeneralize lenfadenopati (7×, 2 yıl); Kaposi sarkomu (4×, 1 yıl)

### Cinsel yolla bulaşan hastalıklarda profilaksi ve korunma — 36 soru, yıllar [2018, 2019, 2020, 2021, 2023, 2024, 2026], güven dusuk
- **Neden:** onleme_halk_sagligi (%47) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.306, 'yanlis_bul': 0.194, 'dogru_ifade': 0.167, 'olumsuz': 0.139, 'en_tipik': 0.111, 'vaka': 0.056, 'onculu': 0.028} · düzey {'L1_hatirlama': 0.528, 'L2_anlama_iliski': 0.417, 'L3_uygulama': 0.056} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %3
- **Tekrar eden çekirdek kavramlar:** CYBE saptanan bireye izolasyon uygulanması (8×, 2 yıl); Doğrulama testi istenir (7×, 2 yıl); Bivalan aşının en önemli etkisi genital siğillerin önlenmesidir (6×, 1 yıl); Enjektör paylaşımı (5×, 2 yıl)

### İntrauterin Enfeksiyonlar — 32 soru, yıllar [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** etiyoloji_risk (%38) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.312, 'olumsuz': 0.281, 'onculu': 0.125, 'dogru_ifade': 0.125, 'en_tipik': 0.094, 'yanlis_bul': 0.062} · düzey {'L1_hatirlama': 0.594, 'L2_anlama_iliski': 0.406} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %19
- **Tekrar eden çekirdek kavramlar:** IgG avidite testi (11×, 3 yıl); I, II ve III (7×, 2 yıl); Anti-streptolizin O (5×, 1 yıl); Veziküler döküntü (3×, 1 yıl)

### Genital Enfeksiyonlar — 28 soru, yıllar [2016, 2019, 2020, 2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** etiyoloji_risk (%39) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'olumsuz': 0.393, 'dogrudan': 0.143, 'en_tipik': 0.107, 'vaka': 0.107, 'dogru_ifade': 0.107, 'yanlis_bul': 0.107, 'onculu': 0.036} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.393, 'L3_uygulama': 0.107} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %7
- **Tekrar eden çekirdek kavramlar:** Karın muayenesinde defans-rebound (7×, 2 yıl); Molluscum contagiosum (5×, 2 yıl); Sifiliz (4×, 1 yıl); Direkt mikroskopide 10 lökosit görülmesi (3×, 3 yıl)

### Sifilis — 27 soru, yıllar [2018, 2019, 2020, 2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tani_ayirici (%30) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'yanlis_bul': 0.333, 'vaka': 0.259, 'dogrudan': 0.222, 'dogru_ifade': 0.074, 'olumsuz': 0.074, 'onculu': 0.037} · düzey {'L2_anlama_iliski': 0.444, 'L1_hatirlama': 0.296, 'L3_uygulama': 0.259} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %22
- **Tekrar eden çekirdek kavramlar:** Şankr bulaştırıcı değildir (7×, 2 yıl); Sekonder sifiliz ön tanısıyla kardiyovasküler komplikasyonlar açısından araştırılması (5×, 1 yıl); Tabes dorsalis (2×, 2 yıl); Primer sifiliz (2×, 2 yıl)

### İzolasyon Yöntemleri — 27 soru, yıllar [2019, 2020, 2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** tanim_kavram (%48) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.37, 'olumsuz': 0.333, 'yanlis_bul': 0.185, 'sayi': 0.037, 'dogru_ifade': 0.037, 'onculu': 0.037} · düzey {'L1_hatirlama': 0.741, 'L2_anlama_iliski': 0.259} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Kan transfüzyonu (6×, 2 yıl); Standart izolasyon sadece HIV pozitif hastalara uygulanır (6×, 2 yıl); Neisseria meningitidis (5×, 2 yıl); Odaya girmeden önce N95 maske takılması (4×, 2 yıl)

### Üriner Sistem Enfeksiyonları — 25 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** etiyoloji_risk (%56) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.24, 'vaka': 0.2, 'en_tipik': 0.16, 'olumsuz': 0.12, 'tanim': 0.12, 'yanlis_bul': 0.12, 'dogru_ifade': 0.04} · düzey {'L1_hatirlama': 0.44, 'L2_anlama_iliski': 0.36, 'L3_uygulama': 0.2} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %28
- **Tekrar eden çekirdek kavramlar:** Escherichia coli (8×, 4 yıl); Kontrolsüz diyabet (6×, 3 yıl); Gebelik (6×, 2 yıl); Staphylococcus aureus (2×, 2 yıl)

### Zoonotik Enfeksiyonlar — 25 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%20) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.32, 'dogrudan': 0.24, 'en_tipik': 0.16, 'onculu': 0.08, 'sayi': 0.08, 'dogru_ifade': 0.08, 'vaka': 0.04} · düzey {'L2_anlama_iliski': 0.72, 'L1_hatirlama': 0.24, 'L3_uygulama': 0.04} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %24
- **Tekrar eden çekirdek kavramlar:** Hayvanın 10 gün takibi yapılır; izlem sürecinde hastalık belirtisi göstermesi, kaçması vey (3×, 1 yıl); En sık komplikasyonu %20-60 oranıyla kardiyak tutulumdur. (3×, 1 yıl); Standart tüp aglütinasyon testi tedavinin takibinde kullanılmaz (2×, 1 yıl)

### Akut romatizmal ateş — 23 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%43) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.304, 'yanlis_bul': 0.261, 'dogrudan': 0.217, 'dogru_ifade': 0.174, 'en_tipik': 0.043} · düzey {'L2_anlama_iliski': 0.522, 'L1_hatirlama': 0.478} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %9
- **Tekrar eden çekirdek kavramlar:** Kalpteki lezyonlarda streptokoklar mevcuttur. (4×, 2 yıl); Ateş (≥38,5 °C) (3×, 2 yıl); Gansiklovir (3×, 1 yıl); Hepsi (2×, 1 yıl)

### İnfluenza — 21 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** etiyoloji_risk (%52) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.333, 'yanlis_bul': 0.333, 'dogru_ifade': 0.19, 'olumsuz': 0.095, 'onculu': 0.048} · düzey {'L2_anlama_iliski': 0.571, 'L1_hatirlama': 0.429} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** hepsi doğru (3×, 1 yıl); Majör değişiklikler yapar (3×, 1 yıl); Hastaneye yatarsa hava yolu izolasyonu gerekir (2×, 2 yıl); Hepsi doğrudur (2×, 1 yıl)

### Üretral Akıntı — 18 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** etiyoloji_risk (%39) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'vaka': 0.333, 'dogrudan': 0.222, 'dogru_ifade': 0.167, 'en_tipik': 0.111, 'eslestirme': 0.056, 'onculu': 0.056, 'yanlis_bul': 0.056} · düzey {'L2_anlama_iliski': 0.389, 'L3_uygulama': 0.333, 'L1_hatirlama': 0.278} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Hepsi (3×, 2 yıl); Sağlıklı bireylerin genital florasında da bulunabildiğinden, kültürde üremesi tek başına a (2×, 2 yıl); Doksisiklin (2×, 1 yıl); Genital (üretral/vajinal) akıntı (2×, 1 yıl)

### Kırım-Kongo kanamalı ateşi — 16 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** tani_ayirici (%38) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogru_ifade': 0.25, 'dogrudan': 0.25, 'olumsuz': 0.25, 'onculu': 0.125, 'yanlis_bul': 0.125} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %6
- **Tekrar eden çekirdek kavramlar:** Trombosit sayısının normal olması (4×, 2 yıl); Bilinç bulanıklığı (4×, 1 yıl); I, II ve III (2×, 2 yıl); Fibrinojen yüksekliği hastalığın ciddiyet kriterlerinden biridir. (2×, 2 yıl)

### Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi — 13 soru, yıllar [2016, 2019, 2020, 2021, 2023, 2024, 2025], güven dusuk
- **Neden:** etiyoloji_risk (%46) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'olumsuz': 0.308, 'yanlis_bul': 0.308, 'dogru_ifade': 0.154, 'dogrudan': 0.154, 'vaka': 0.077} · düzey {'L2_anlama_iliski': 0.538, 'L1_hatirlama': 0.385, 'L3_uygulama': 0.077} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %15
- **Tekrar eden çekirdek kavramlar:** Hepsi (4×, 2 yıl); Oral herpes enfeksiyonları (4×, 1 yıl); Hastanın cinsel partnerinin tedavi edilmesine gerek yoktur. (2×, 2 yıl); Kandida vajiniti (2×, 2 yıl)

### Mikroorganizmalarda Direnç Sorunu ve Antimikrobiyal Yönetim — 13 soru, yıllar [2019, 2020, 2021, 2024, 2025], güven dusuk
- **Neden:** tanim_kavram (%46) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.308, 'eslestirme': 0.231, 'olumsuz': 0.154, 'dogrudan': 0.154, 'dogru_ifade': 0.077, 'onculu': 0.077} · düzey {'L2_anlama_iliski': 0.692, 'L1_hatirlama': 0.308} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Ateşi olan her hastaya antibiyotik başlanmalı. (6×, 3 yıl); Escherichia coli - Vankomisin (4×, 2 yıl); Genişlemiş spektrumlu beta-laktamaz (GSBL) üreten bakteriler 3. kuşak sefalosporinlerle te (2×, 1 yıl)

### Kolera — 4 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** etiyoloji_risk (%50) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'onculu': 0.5, 'yanlis_bul': 0.5} · düzey {'L2_anlama_iliski': 1.0} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Birkaç dışkılamadan sonra tipik ağrılı, kokulu, yeşil ishal başlar. (3×, 1 yıl)
