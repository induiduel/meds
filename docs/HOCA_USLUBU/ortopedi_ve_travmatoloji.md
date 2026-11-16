# Ortopedi ve Travmatoloji — hoca üslubu ve kazanım haritası (otomatik; `scripts/hoca_profili/uslup_analiz.py`)

> 73 tekil çıkmış soru · güven: **orta** · yıllar: {2020: 44, 2021: 4, 2022: 3, 2023: 2, 2025: 3}

## 1. Üslup özeti

### Kök kalıbı
- **yanlis_bul**: %30 (genel ortalama %13)
- **dogrudan**: %23 (genel ortalama %40)
- **olumsuz**: %23 (genel ortalama %15)
- **dogru_ifade**: %11 (genel ortalama %6)
- **en_tipik**: %8 (genel ortalama %8)
- **vaka**: %3 (genel ortalama %5)
- **eslestirme**: %1 (genel ortalama %1)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %37 (genel ortalama %32)
- **siniflama_ad**: %18 (genel ortalama %9)
- **mekanizma**: %11 (genel ortalama %14)
- **etiyoloji_risk**: %8 (genel ortalama %11)
- **epidemiyoloji_sayi**: %7 (genel ortalama %2)
- **ilac_endikasyon**: %7 (genel ortalama %7)
- **tani_ayirici**: %7 (genel ortalama %12)

### Bilişsel düzey
- **L1_hatirlama**: %55 (genel ortalama %51)
- **L2_anlama_iliski**: %42 (genel ortalama %44)
- **L3_uygulama**: %3 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 11.5 kelime (p25 7 · medyan 9 · p75 13).
- Şık: ort. 5.7 kelime; bileşik şık %28; sayısal şık %1; mutlak ifadeli çeldirici %7.
- Doğru şık tek başına en uzun: %20 (genel %19). Doğru şık konumu: {'A': 0.288, 'C': 0.233, 'E': 0.178, 'D': 0.151, 'B': 0.151}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.726, 'bilesik_yer_degistirmeli': 0.178, 'mutlak_ifade_tuzagi': 0.068, 'ayni_ailede_komsu_kavram': 0.041, 'sayisal_yakin_deger': 0.014}
- Aynı bilginin yeniden sorulması: soruların %11'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: yanlis_bul %30, dogrudan %23, olumsuz %23.
- Kök 7–13 kelime; şık ort. 5.7 kelime, uzunluklar birbirine yakın (CV≈0.29).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L1_hatirlama %55, L2_anlama_iliski %42, L3_uygulama %3.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Kemik, eklem ve implant enfeksiyonları — 16 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** etiyoloji_risk (%25) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'olumsuz': 0.5, 'yanlis_bul': 0.25, 'dogrudan': 0.125, 'vaka': 0.125} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.375, 'L3_uygulama': 0.125} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %6
- **Tekrar eden çekirdek kavramlar:** Çoğu zaman tek başına intravenöz antibiyotik yeterlidir, debridmana gerek yoktur. (3×, 1 yıl); Diş ve çevresinin enfeksiyonları (2×, 1 yıl); Parçalı osteomiyelit (2×, 1 yıl)

### Yetişkin ve çocuk kırıklarına yaklaşım — 11 soru, yıllar [2020, 2025], güven dusuk
- **Neden:** ilac_endikasyon (%36) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.273, 'yanlis_bul': 0.273, 'dogru_ifade': 0.182, 'olumsuz': 0.091, 'en_tipik': 0.091, 'eslestirme': 0.091} · düzey {'L2_anlama_iliski': 0.545, 'L1_hatirlama': 0.455} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Pubis kolu kırığı (2×, 1 yıl); Cerrahi sonrası atel, alçı veya eksternal fiksatör gibi ek stabilizasyona gerek kalmaz. (2×, 1 yıl)

### Spondilodiskitler ve pot hastalığı — 11 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** epidemiyoloji_sayi (%36) — Pre-test olasılık: sıklık ve yaş/cinsiyet dağılımı klinik şüpheyi belirler.
- **Nasıl:** {'dogrudan': 0.364, 'yanlis_bul': 0.364, 'olumsuz': 0.182, 'dogru_ifade': 0.091} · düzey {'L1_hatirlama': 0.636, 'L2_anlama_iliski': 0.364} · Tek sayı ya da oran sorulur; çeldirici yakın değerlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %27
- **Tekrar eden çekirdek kavramlar:** Çocukluk yaş grubunda daha agresif seyreder. (3×, 1 yıl); Enfekte lenf nodundan direkt yayılım yolu ile vertebra korpusuna bulaşır. (2×, 2 yıl); Mycobacterium tuberculosis (2×, 1 yıl)

### Kemik ve kıkırdağın konjenital hastalıkları — 9 soru, yıllar [2020, 2023], güven dusuk
- **Neden:** tanim_kavram (%44) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.333, 'en_tipik': 0.333, 'yanlis_bul': 0.222, 'olumsuz': 0.111} · düzey {'L1_hatirlama': 0.556, 'L2_anlama_iliski': 0.444} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %44
- **Tekrar eden çekirdek kavramlar:** Fibular hemimeli (deficiency) (2×, 1 yıl)

### Eklem hastalıkları patolojisi ve artritler — 8 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%100) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.375, 'yanlis_bul': 0.25, 'dogru_ifade': 0.25, 'en_tipik': 0.125} · düzey {'L1_hatirlama': 0.75, 'L2_anlama_iliski': 0.25} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %12
- **Tekrar eden çekirdek kavramlar:** Dirsek (3×, 1 yıl); 20-50 yaş aralığında sık görülür. (2×, 1 yıl)

### Kemiklerin tümörlerine genel yaklaşım — 7 soru, yıllar [2020, 2022, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%86) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.571, 'yanlis_bul': 0.429} · düzey {'L1_hatirlama': 0.571, 'L2_anlama_iliski': 0.429} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Aspirinle geçen ağrı (2×, 2 yıl); Ewing sarkomu (2×, 1 yıl)

### Kemiğin edinsel hastalıkları — 7 soru, yıllar [2020], güven dusuk
- **Neden:** siniflama_ad (%57) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogru_ifade': 0.429, 'yanlis_bul': 0.286, 'en_tipik': 0.143, 'dogrudan': 0.143} · düzey {'L1_hatirlama': 0.571, 'L2_anlama_iliski': 0.429} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Hastalığın proliferatif döneminde kafatası tutulumunda görsel ve işitsel bozukluklar gibi  (2×, 1 yıl)

### Kırık komplikasyonlarına yaklaşım — 4 soru, yıllar [2020, 2025], güven dusuk
- **Neden:** siniflama_ad (%50) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'yanlis_bul': 0.5, 'olumsuz': 0.5} · düzey {'L2_anlama_iliski': 0.75, 'L1_hatirlama': 0.25} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Kaynama gecikmesi tanısı konduğunda, kırığın üzerinden geçen süreye bakılmaksızın cerrahi  (2×, 1 yıl); Olguların yarısı mortal seyreder (2×, 1 yıl); Yağ embolisi (2×, 1 yıl)
