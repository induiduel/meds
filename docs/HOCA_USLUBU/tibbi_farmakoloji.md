# Tıbbi Farmakoloji — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 679 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 106, 2019: 7, 2020: 237, 2021: 75, 2022: 40, 2023: 28, 2024: 4, 2025: 14, 2026: 4}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %51 (genel ortalama %40)
- **onculu**: %23 (genel ortalama %8)
- **olumsuz**: %6 (genel ortalama %15)
- **yanlis_bul**: %5 (genel ortalama %13)
- **dogru_ifade**: %4 (genel ortalama %6)
- **sayi**: %4 (genel ortalama %3)
- **en_tipik**: %4 (genel ortalama %8)

### Sorulan bilgi türü (neden sorulur)
- **mekanizma**: %32 (genel ortalama %14)
- **tanim_kavram**: %26 (genel ortalama %32)
- **ilac_endikasyon**: %21 (genel ortalama %7)
- **ilac_yan_etki**: %7 (genel ortalama %2)
- **etiyoloji_risk**: %5 (genel ortalama %11)
- **siniflama_ad**: %3 (genel ortalama %9)
- **tani_ayirici**: %2 (genel ortalama %12)

### Bilişsel düzey
- **L2_anlama_iliski**: %53 (genel ortalama %44)
- **L1_hatirlama**: %45 (genel ortalama %51)
- **L3_uygulama**: %2 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 25.1 kelime (p25 10 · medyan 17 · p75 30).
- Şık: ort. 3.2 kelime; bileşik şık %27; sayısal şık %2; mutlak ifadeli çeldirici %2.
- Doğru şık tek başına en uzun: %18 (genel %19). Doğru şık konumu: {'A': 0.349, 'C': 0.186, 'B': 0.181, 'D': 0.144, 'E': 0.14}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.657, 'bilesik_yer_degistirmeli': 0.303, 'ayni_ailede_komsu_kavram': 0.169, 'mutlak_ifade_tuzagi': 0.022, 'sayisal_yakin_deger': 0.021}
- Aynı bilginin yeniden sorulması: soruların %13'i birden çok kez çıkmış.

### Dönem kayması (2023 sonrası − öncesi, puan farkı)
- {'kalip': {'onculu': -0.111, 'dogrudan': 0.153}}

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %51, onculu %23, olumsuz %6.
- Kök 10–30 kelime; şık ort. 3.2 kelime, uzunluklar birbirine yakın (CV≈0.22).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L2_anlama_iliski %53, L1_hatirlama %45, L3_uygulama %2.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Pankreatik Hormonlar ve Antidiyabetik İlaçlar — 36 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** ilac_endikasyon (%36) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.611, 'olumsuz': 0.111, 'en_tipik': 0.083, 'onculu': 0.083, 'sayi': 0.056, 'yanlis_bul': 0.028, 'vaka': 0.028} · düzey {'L1_hatirlama': 0.583, 'L2_anlama_iliski': 0.389, 'L3_uygulama': 0.028} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %47
- **Tekrar eden çekirdek kavramlar:** Gliburid (4×, 2 yıl); Glukagon (3×, 1 yıl); Repaglinid (3×, 1 yıl); Diyet ve egzersizle kan glukoz kontrolü sağlanamayan Tip 2 Diyabetes Mellitus hastaları (2×, 1 yıl)

### Diüretikler — 33 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%48) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.515, 'onculu': 0.242, 'en_tipik': 0.121, 'olumsuz': 0.061, 'yanlis_bul': 0.03, 'vaka': 0.03} · düzey {'L2_anlama_iliski': 0.545, 'L1_hatirlama': 0.424, 'L3_uygulama': 0.03} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %18
- **Tekrar eden çekirdek kavramlar:** Metabolik asidoz (6×, 1 yıl); Eplerenon (6×, 1 yıl); I, II, III ve IV (6×, 1 yıl); Mannitol (4×, 2 yıl)

### Tiroit ve Antitiroid İlaçlar — 24 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** mekanizma (%46) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'onculu': 0.5, 'dogru_ifade': 0.25, 'dogrudan': 0.25} · düzey {'L2_anlama_iliski': 0.708, 'L1_hatirlama': 0.292} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %12
- **Tekrar eden çekirdek kavramlar:** İlaçlara direnç çapraz olduğundan biri bırakıldığında diğerine başlanmaz (4×, 1 yıl); Yalnız IV (3×, 1 yıl); Metimazol (2×, 2 yıl)

### İmmünofarmakoloji — 23 soru, yıllar [2020, 2021, 2023, 2024, 2025, 2026], güven dusuk
- **Neden:** mekanizma (%30) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.739, 'en_tipik': 0.13, 'olumsuz': 0.043, 'tanim': 0.043, 'sayi': 0.043} · düzey {'L1_hatirlama': 0.652, 'L2_anlama_iliski': 0.348} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %48
- **Tekrar eden çekirdek kavramlar:** Hidroksiklorokin (8×, 3 yıl); Sirolimus (4×, 3 yıl); IgE (3×, 2 yıl); Kapromab pendetid (3×, 1 yıl)

### Gonadal Hormonlar, inhibitör ve replasman ilaçları — 20 soru, yıllar [2018, 2019, 2020], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.45, 'olumsuz': 0.3, 'yanlis_bul': 0.1, 'onculu': 0.1, 'sayi': 0.05} · düzey {'L1_hatirlama': 0.65, 'L2_anlama_iliski': 0.35} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** Levonorgestrel (6×, 2 yıl); Etonogestrel (5×, 1 yıl); Uterus içinde inflamasyon yapmaları (4×, 1 yıl); Siproteron (2×, 1 yıl)

### Antikoagülanlar ve antitrombotikler — 20 soru, yıllar [2018, 2020, 2021, 2022, 2023, 2025], güven dusuk
- **Neden:** ilac_endikasyon (%50) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.35, 'olumsuz': 0.2, 'onculu': 0.2, 'sayi': 0.1, 'yanlis_bul': 0.1, 'en_tipik': 0.05} · düzey {'L2_anlama_iliski': 0.5, 'L1_hatirlama': 0.5} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %25
- **Tekrar eden çekirdek kavramlar:** Enoksaparin (3×, 1 yıl); Aspirin (3×, 1 yıl); Antitrombin III (3×, 1 yıl)

### Sülfonamidler, Trimetoprim ve Kinolonlar — 19 soru, yıllar [2020, 2021, 2023, 2025], güven dusuk
- **Neden:** mekanizma (%26) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.421, 'dogru_ifade': 0.158, 'yanlis_bul': 0.158, 'onculu': 0.105, 'olumsuz': 0.053, 'sayi': 0.053, 'en_tipik': 0.053} · düzey {'L1_hatirlama': 0.579, 'L2_anlama_iliski': 0.421} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** Sülfonamidler gebeliğin geç döneminde uygulandığında bazal ganglionlarda işlev bozukluğu o (2×, 1 yıl); Kinolonlar (2×, 1 yıl); Toplum kökenli pnömoni tedavisi için uygundur. (2×, 1 yıl); II ve IV (2×, 1 yıl)

### Hipotalamohipofizer Sistem İlaçları — 19 soru, yıllar [2018, 2020, 2023], güven dusuk
- **Neden:** tanim_kavram (%37) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.579, 'onculu': 0.211, 'dogru_ifade': 0.105, 'yanlis_bul': 0.053, 'vaka': 0.053} · düzey {'L1_hatirlama': 0.526, 'L2_anlama_iliski': 0.421, 'L3_uygulama': 0.053} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %37
- **Tekrar eden çekirdek kavramlar:** Furosemid (2×, 1 yıl); Uterus ve memede oksitosin için reseptör bulunmaktadır. (2×, 1 yıl); 1-desamino-8-D-arginin vazopressin (DDAVP) (2×, 1 yıl)

### GİS Hastalıklarının Tedavisinde Kullanılan İlaçlar -1 — 19 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** mekanizma (%47) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.368, 'onculu': 0.211, 'yanlis_bul': 0.158, 'vaka': 0.105, 'olumsuz': 0.105, 'dogru_ifade': 0.053} · düzey {'L2_anlama_iliski': 0.579, 'L1_hatirlama': 0.316, 'L3_uygulama': 0.105} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** Pantoprazol (3×, 1 yıl); Prodrug'dur ve enterik kapsülleri aside dayanıklıdır (2×, 1 yıl); Proton pompasını reverzibl olarak inhibe ederler (2×, 1 yıl); Klaritromisin + Tinidazol + PPİ + akşam yatarken (2×, 1 yıl)

### Dermatolojik Farmakoloji — 19 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** ilac_endikasyon (%32) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.684, 'olumsuz': 0.158, 'vaka': 0.053, 'sayi': 0.053, 'yanlis_bul': 0.053} · düzey {'L1_hatirlama': 0.684, 'L2_anlama_iliski': 0.263, 'L3_uygulama': 0.053} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %37
- **Tekrar eden çekirdek kavramlar:** Ketokonazol (3×, 1 yıl); Pitiriyazis versikolor (3×, 1 yıl); Tinea versicolor (2×, 1 yıl); Leishmaniasis (2×, 1 yıl)

### Kanser kemoterapisi — 18 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** mekanizma (%28) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.889, 'yanlis_bul': 0.056, 'en_tipik': 0.056} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.333} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %28
- **Tekrar eden çekirdek kavramlar:** Streptozosin (6×, 4 yıl); Metotreksat (2×, 2 yıl)

### Antihipertansif İlaçlar — 18 soru, yıllar [2018, 2020, 2022], güven dusuk
- **Neden:** ilac_endikasyon (%33) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.444, 'onculu': 0.278, 'dogru_ifade': 0.111, 'en_tipik': 0.056, 'vaka': 0.056, 'yanlis_bul': 0.056} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.444, 'L3_uygulama': 0.056} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Kaptopril (2×, 1 yıl); Kaptopril (2×, 1 yıl)

### Astım ve diğer akciğer hastalıklarının tedavisinde kullanılan ilaçlar — 17 soru, yıllar [2019, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** mekanizma (%53) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'onculu': 0.353, 'dogrudan': 0.294, 'vaka': 0.118, 'en_tipik': 0.059, 'sayi': 0.059, 'olumsuz': 0.059, 'yanlis_bul': 0.059} · düzey {'L2_anlama_iliski': 0.647, 'L1_hatirlama': 0.235, 'L3_uygulama': 0.118} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %18
- **Tekrar eden çekirdek kavramlar:** Kromolin (3×, 1 yıl); II ve IV (3×, 1 yıl); α-agonistler adenilat siklaz ve IP3 üzerinden etkilidirler; tanımlanmış ve kanıtlanmış etk (2×, 2 yıl)

### Genel Anestezik İlaçlar — 17 soru, yıllar [2020, 2021, 2022, 2023, 2025], güven dusuk
- **Neden:** tanim_kavram (%53) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'onculu': 0.294, 'sayi': 0.176, 'dogrudan': 0.176, 'yanlis_bul': 0.118, 'dogru_ifade': 0.118, 'tanim': 0.059, 'vaka': 0.059} · düzey {'L2_anlama_iliski': 0.529, 'L1_hatirlama': 0.412, 'L3_uygulama': 0.059} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %6
- **Tekrar eden çekirdek kavramlar:** Sevofluran (3×, 1 yıl); II ve IV (2×, 2 yıl)

### Aminoglikozidler — 16 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** ilac_yan_etki (%44) — Hasta güvenliği: yan etki/kontrendikasyon bilmemek zarar demektir.
- **Nasıl:** {'dogrudan': 0.438, 'onculu': 0.312, 'yanlis_bul': 0.125, 'dogru_ifade': 0.125} · düzey {'L2_anlama_iliski': 0.75, 'L1_hatirlama': 0.25} · İlaçtan yan etkiye ve yan etkiden ilaca; çeldirici aynı sınıfın başka üyesidir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %12
- **Tekrar eden çekirdek kavramlar:** Amikasin (3×, 1 yıl); Yalnız IV (3×, 1 yıl); Yalnız IV (3×, 1 yıl); Amikasin (2×, 1 yıl)

### Tetrasiklin, Makrolit, Kloramfenikol ve Streptograminler — 16 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** mekanizma (%50) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.625, 'onculu': 0.312, 'yanlis_bul': 0.062} · düzey {'L2_anlama_iliski': 0.688, 'L1_hatirlama': 0.312} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %31
- **Tekrar eden çekirdek kavramlar:** Kloramfenikol (4×, 2 yıl); I, II, III ve IV (3×, 1 yıl); Oksitetrasiklin (2×, 1 yıl); I ve III (2×, 1 yıl)

### Histamin, serotonin, melatonin ve Ergot Alkaloidleri — 16 soru, yıllar [2018, 2020, 2023, 2025], güven dusuk
- **Neden:** mekanizma (%56) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.562, 'onculu': 0.375, 'dogru_ifade': 0.062} · düzey {'L2_anlama_iliski': 0.75, 'L1_hatirlama': 0.25} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %31
- **Tekrar eden çekirdek kavramlar:** Taşikardi (4×, 1 yıl); Serotonin (4×, 1 yıl); H1 reseptörü (3×, 1 yıl); I, II, III ve IV (2×, 1 yıl)

### Antifungal İlaçlar — 15 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** mekanizma (%40) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.6, 'onculu': 0.133, 'en_tipik': 0.133, 'vaka': 0.067, 'sayi': 0.067} · düzey {'L1_hatirlama': 0.467, 'L2_anlama_iliski': 0.467, 'L3_uygulama': 0.067} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %47
- **Tekrar eden çekirdek kavramlar:** Dapson (5×, 2 yıl); Nistatin (2×, 1 yıl); I, II ve III (2×, 1 yıl); Griseofulvin (2×, 1 yıl)

### Beta Laktam ve Diğer Hücre Duvarı ile Membran Aktif Antibiyotikler — 15 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.533, 'onculu': 0.267, 'sayi': 0.133, 'olumsuz': 0.067} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %60
- **Tekrar eden çekirdek kavramlar:** İmipenem (4×, 3 yıl); Seftazidim (3×, 1 yıl); Glikopeptid (2×, 1 yıl); I ve III (2×, 1 yıl)

### Antimikobakteriyel İlaçlar — 15 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** mekanizma (%27) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'onculu': 0.4, 'dogrudan': 0.333, 'olumsuz': 0.133, 'dogru_ifade': 0.067, 'en_tipik': 0.067} · düzey {'L2_anlama_iliski': 0.6, 'L1_hatirlama': 0.4} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %7
- **Tekrar eden çekirdek kavramlar:** Yalnız IV (2×, 1 yıl); İzoniazid (2×, 1 yıl); Yalnız IV (2×, 1 yıl); Misoprostol (2×, 1 yıl)

### Antihelmintik İlaçlar — 15 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** ilac_endikasyon (%33) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.4, 'onculu': 0.267, 'tanim': 0.133, 'yanlis_bul': 0.133, 'olumsuz': 0.067} · düzey {'L2_anlama_iliski': 0.533, 'L1_hatirlama': 0.467} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %27
- **Tekrar eden çekirdek kavramlar:** Emilimi çok iyidir (>%90). Besinlerden etkilenmez (2×, 1 yıl); İvermektin (2×, 1 yıl); I ve III (2×, 1 yıl); İntravenöz ardışık üç doz ile kitlesel tedavi programları mümkündür. (2×, 1 yıl)

### Antiviral İlaçlar — 15 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** ilac_endikasyon (%47) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'onculu': 0.533, 'dogrudan': 0.267, 'yanlis_bul': 0.133, 'en_tipik': 0.067} · düzey {'L2_anlama_iliski': 0.8, 'L1_hatirlama': 0.2} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %13
- **Tekrar eden çekirdek kavramlar:** I, II, III ve IV (3×, 1 yıl); II ve IV (2×, 1 yıl); Yalnız IV (2×, 1 yıl)

### Kemik mineralizasyonu ve homeostaza etki eden ilaçlar — 15 soru, yıllar [2020, 2022, 2023], güven dusuk
- **Neden:** mekanizma (%33) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.467, 'yanlis_bul': 0.133, 'olumsuz': 0.133, 'onculu': 0.133, 'dogru_ifade': 0.067, 'sayi': 0.067} · düzey {'L1_hatirlama': 0.533, 'L2_anlama_iliski': 0.467} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Denosumab (2×, 2 yıl); Kalsiyum ve fosfat üzerine net etkileri: Serum kalsiyumu azalırken hiperfosfatemi şekillen (2×, 1 yıl); Serum Ca++ ve fosfat seviyeleri artar (2×, 1 yıl); Kemik mineral dansitesini dramatik düzeyde azalttıklarından gebelik sonu hipokalsemilerin  (2×, 1 yıl)

### Sedatif ve Hipnotik İlaçlar — 15 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%40) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'onculu': 0.533, 'dogrudan': 0.267, 'sayi': 0.067, 'yanlis_bul': 0.067, 'olumsuz': 0.067} · düzey {'L2_anlama_iliski': 0.667, 'L1_hatirlama': 0.333} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %13
- **Tekrar eden çekirdek kavramlar:** Flumazenil (3×, 1 yıl)

### Antimikrobik İlaçların Klinik Kullanımı, Önemi ve Önlemleri — 14 soru, yıllar [2018, 2019, 2020], güven dusuk
- **Neden:** ilac_endikasyon (%21) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.429, 'onculu': 0.429, 'sayi': 0.071, 'vaka': 0.071} · düzey {'L2_anlama_iliski': 0.643, 'L1_hatirlama': 0.286, 'L3_uygulama': 0.071} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %7
- **Tekrar eden çekirdek kavramlar:** I, II ve III (3×, 1 yıl); Yalnız IV (3×, 1 yıl); Trimetoprim-sülfametoksazol (2×, 1 yıl); Sefoksitin tek başına (2×, 1 yıl)
