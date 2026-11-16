# Tıbbi Biyokimya — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 28 tekil çıkmış soru · güven: **dusuk** · yıllar: {2018: 1, 2020: 8, 2021: 3, 2022: 2}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %64 (genel ortalama %40)
- **sayi**: %7 (genel ortalama %3)
- **eslestirme**: %7 (genel ortalama %1)
- **olumsuz**: %7 (genel ortalama %15)
- **vaka**: %4 (genel ortalama %5)
- **en_tipik**: %4 (genel ortalama %8)
- **onculu**: %4 (genel ortalama %8)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %46 (genel ortalama %32)
- **tani_ayirici**: %14 (genel ortalama %12)
- **mekanizma**: %11 (genel ortalama %14)
- **ilac_yan_etki**: %7 (genel ortalama %2)
- **onleme_halk_sagligi**: %7 (genel ortalama %5)
- **siniflama_ad**: %7 (genel ortalama %9)
- **etiyoloji_risk**: %4 (genel ortalama %11)

### Bilişsel düzey
- **L1_hatirlama**: %64 (genel ortalama %51)
- **L2_anlama_iliski**: %32 (genel ortalama %44)
- **L3_uygulama**: %4 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 20.4 kelime (p25 9 · medyan 22 · p75 31).
- Şık: ort. 3.6 kelime; bileşik şık %14; sayısal şık %11; mutlak ifadeli çeldirici %4.
- Doğru şık tek başına en uzun: %36 (genel %19). Doğru şık konumu: {'A': 0.607, 'B': 0.214, 'C': 0.107, 'D': 0.071}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.714, 'bilesik_yer_degistirmeli': 0.143, 'sayisal_yakin_deger': 0.107, 'ayni_ailede_komsu_kavram': 0.036, 'mutlak_ifade_tuzagi': 0.036}
- Aynı bilginin yeniden sorulması: soruların %0'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %64, sayi %7, eslestirme %7.
- Kök 9–31 kelime; şık ort. 3.6 kelime, uzunluklar birbirine yakın (CV≈0.33).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %64, L2_anlama_iliski %32, L3_uygulama %4.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### K. Biyo.da Analiz Edilen Biy. Mat., Alınma, Taşınma, Analiz Edilmesinde Dik. Ed. Hususlar — 10 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%80) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.8, 'eslestirme': 0.2} · düzey {'L1_hatirlama': 0.8, 'L2_anlama_iliski': 0.2} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %40
- **Tekrar eden çekirdek kavramlar:** Hepatitler (2×, 1 yıl)

### Biyokimya Lab. Gelen Numunelerde Analiz Edilen Paket Testler — 9 soru, yıllar [2018, 2022], güven dusuk
- **Neden:** tani_ayirici (%33) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.667, 'vaka': 0.111, 'en_tipik': 0.111, 'onculu': 0.111} · düzey {'L1_hatirlama': 0.444, 'L2_anlama_iliski': 0.444, 'L3_uygulama': 0.111} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %11

### Biyokimyasal Analizlerde Hata Kaynakları — 7 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%43) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.571, 'olumsuz': 0.286, 'sayi': 0.143} · düzey {'L1_hatirlama': 0.571, 'L2_anlama_iliski': 0.429} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %43
