# Kardiyoloji — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 160 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 9, 2020: 61, 2021: 9, 2022: 24, 2023: 5, 2025: 2}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %34 (genel ortalama %40)
- **olumsuz**: %16 (genel ortalama %15)
- **yanlis_bul**: %12 (genel ortalama %13)
- **dogru_ifade**: %11 (genel ortalama %6)
- **vaka**: %11 (genel ortalama %5)
- **en_tipik**: %8 (genel ortalama %8)
- **sayi**: %4 (genel ortalama %3)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %40 (genel ortalama %32)
- **tani_ayirici**: %15 (genel ortalama %12)
- **mekanizma**: %15 (genel ortalama %14)
- **etiyoloji_risk**: %11 (genel ortalama %11)
- **siniflama_ad**: %8 (genel ortalama %9)
- **ilac_endikasyon**: %4 (genel ortalama %7)
- **epidemiyoloji_sayi**: %2 (genel ortalama %2)

### Bilişsel düzey
- **L1_hatirlama**: %51 (genel ortalama %51)
- **L2_anlama_iliski**: %39 (genel ortalama %44)
- **L3_uygulama**: %11 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 16.2 kelime (p25 8 · medyan 11 · p75 23).
- Şık: ort. 4.9 kelime; bileşik şık %18; sayısal şık %6; mutlak ifadeli çeldirici %4.
- Doğru şık tek başına en uzun: %26 (genel %19). Doğru şık konumu: {'B': 0.287, 'A': 0.269, 'C': 0.163, 'D': 0.15, 'E': 0.131}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.688, 'bilesik_yer_degistirmeli': 0.156, 'ayni_ailede_komsu_kavram': 0.144, 'sayisal_yakin_deger': 0.062, 'mutlak_ifade_tuzagi': 0.037}
- Aynı bilginin yeniden sorulması: soruların %7'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %34, olumsuz %16, yanlis_bul %12.
- Kök 8–23 kelime; şık ort. 4.9 kelime, uzunluklar birbirine yakın (CV≈0.29).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %51, L2_anlama_iliski %39, L3_uygulama %11.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Enfektif Endokardit — 32 soru, yıllar [2020, 2021, 2022, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%31) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.531, 'olumsuz': 0.156, 'vaka': 0.094, 'dogru_ifade': 0.062, 'en_tipik': 0.062, 'yanlis_bul': 0.062, 'onculu': 0.031} · düzey {'L1_hatirlama': 0.531, 'L2_anlama_iliski': 0.375, 'L3_uygulama': 0.094} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %34
- **Tekrar eden çekirdek kavramlar:** İki ayrı kan kültüründe infektif endokardit ile uyumlu tipik mikroorganizmanın üremesi (4×, 1 yıl); İlk basamak non-bakteriyel trombotik endokardit oluşmasıdır. (3×, 2 yıl); Gelişmiş ülkelerde en sık enfektif endokardit etkeni streptokoklardır. (3×, 1 yıl); Kadın cinsiyet (2×, 2 yıl)

### Koroner Kalp Hastalıkları — 19 soru, yıllar [2018, 2020, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%32) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.368, 'olumsuz': 0.158, 'onculu': 0.105, 'yanlis_bul': 0.105, 'tanim': 0.053, 'dogru_ifade': 0.053, 'en_tipik': 0.053, 'sayi': 0.053, 'vaka': 0.053} · düzey {'L1_hatirlama': 0.526, 'L2_anlama_iliski': 0.421, 'L3_uygulama': 0.053} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %16
- **Tekrar eden çekirdek kavramlar:** Dil altı nitratlarla genellikle ağrının şiddeti azalmaz (2×, 1 yıl)

### Ritim Bozukluklarına Giriş — 19 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%32) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.263, 'olumsuz': 0.211, 'vaka': 0.158, 'yanlis_bul': 0.158, 'dogru_ifade': 0.105, 'en_tipik': 0.053, 'sayi': 0.053} · düzey {'L1_hatirlama': 0.526, 'L2_anlama_iliski': 0.316, 'L3_uygulama': 0.158} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %11
- **Tekrar eden çekirdek kavramlar:** Ek hastalığı olmayan 40 yaşında erkek hasta (3×, 1 yıl)

### Kalp Yetersizliği — 18 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** mekanizma (%61) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogru_ifade': 0.389, 'olumsuz': 0.278, 'dogrudan': 0.167, 'vaka': 0.111, 'sayi': 0.056} · düzey {'L2_anlama_iliski': 0.667, 'L1_hatirlama': 0.222, 'L3_uygulama': 0.111} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %11
- **Tekrar eden çekirdek kavramlar:** Renin-anjiyotensin-aldosteron sisteminin aktivasyonu, sol ventrikülün progresif yeniden şe (4×, 1 yıl); Venöz dönüş arttığında kalp debisinde görülen artışı açıklar (3×, 1 yıl); Aortik kompliansta artışı (3×, 1 yıl)

### Kalp Kapak Hastalıkları — 15 soru, yıllar [2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'vaka': 0.4, 'dogrudan': 0.333, 'dogru_ifade': 0.067, 'en_tipik': 0.067, 'eslestirme': 0.067, 'onculu': 0.067} · düzey {'L1_hatirlama': 0.4, 'L3_uygulama': 0.4, 'L2_anlama_iliski': 0.2} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %27
- **Tekrar eden çekirdek kavramlar:** Nabız pulsus parvus et tardus olarak palpe edilir (3×, 2 yıl); Atriyal fibrilasyon (2×, 1 yıl)

### Elektrokardiyografiye Giriş — 12 soru, yıllar [2018, 2020, 2022], güven dusuk
- **Neden:** tanim_kavram (%83) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.417, 'yanlis_bul': 0.167, 'sayi': 0.167, 'olumsuz': 0.167, 'dogru_ifade': 0.083} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.333} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %25

### Kalp Sesleri — 12 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%75) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.25, 'yanlis_bul': 0.25, 'dogru_ifade': 0.25, 'sayi': 0.083, 'olumsuz': 0.083, 'onculu': 0.083} · düzey {'L1_hatirlama': 0.583, 'L2_anlama_iliski': 0.417} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %8
- **Tekrar eden çekirdek kavramlar:** Mitral darlığında apikal odakta pansistolik üfürüm duyulur. (3×, 1 yıl)

### Konjenital Kalp Hastalıkları — 10 soru, yıllar [2018, 2020, 2022], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.5, 'en_tipik': 0.3, 'yanlis_bul': 0.1, 'onculu': 0.1} · düzey {'L1_hatirlama': 0.7, 'L2_anlama_iliski': 0.3} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %20
- **Tekrar eden çekirdek kavramlar:** Hepatit B enfeksiyonu (2×, 1 yıl); Patent duktus arteriozus (2×, 1 yıl)

### Perikarditler — 9 soru, yıllar [2018, 2020, 2022], güven dusuk
- **Neden:** tanim_kavram (%56) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.444, 'yanlis_bul': 0.333, 'vaka': 0.111, 'dogrudan': 0.111} · düzey {'L1_hatirlama': 0.444, 'L2_anlama_iliski': 0.444, 'L3_uygulama': 0.111} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %22

### Miyokarditler, Miyokardiyopatiler ve Kalp Tümörleri — 8 soru, yıllar [2018, 2020], güven dusuk
- **Neden:** tanim_kavram (%62) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'en_tipik': 0.5, 'yanlis_bul': 0.25, 'dogrudan': 0.25} · düzey {'L1_hatirlama': 0.75, 'L2_anlama_iliski': 0.25} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Papiller fibroelastom (2×, 0 yıl)

### Hipertansiyon — 6 soru, yıllar [2020, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.333, 'olumsuz': 0.333, 'vaka': 0.167, 'yanlis_bul': 0.167} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.333, 'L3_uygulama': 0.167} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %33
