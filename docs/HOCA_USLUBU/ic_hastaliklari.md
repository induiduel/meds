# İç Hastalıkları — hoca üslubu ve kazanım haritası (otomatik; `scripts/uretim/hoca_profili/uslup_analiz.py`)

> 462 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 79, 2019: 1, 2020: 228, 2021: 28, 2022: 19, 2023: 16, 2025: 1}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %25 (genel ortalama %40)
- **olumsuz**: %21 (genel ortalama %15)
- **yanlis_bul**: %18 (genel ortalama %13)
- **onculu**: %12 (genel ortalama %8)
- **vaka**: %10 (genel ortalama %5)
- **en_tipik**: %6 (genel ortalama %8)
- **dogru_ifade**: %5 (genel ortalama %6)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %27 (genel ortalama %32)
- **tani_ayirici**: %21 (genel ortalama %12)
- **etiyoloji_risk**: %14 (genel ortalama %11)
- **mekanizma**: %13 (genel ortalama %14)
- **siniflama_ad**: %9 (genel ortalama %9)
- **ilac_endikasyon**: %7 (genel ortalama %7)
- **onleme_halk_sagligi**: %4 (genel ortalama %5)

### Bilişsel düzey
- **L2_anlama_iliski**: %52 (genel ortalama %44)
- **L1_hatirlama**: %39 (genel ortalama %51)
- **L3_uygulama**: %10 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 23.5 kelime (p25 8 · medyan 11 · p75 24).
- Şık: ort. 4.9 kelime; bileşik şık %28; sayısal şık %8; mutlak ifadeli çeldirici %2.
- Doğru şık tek başına en uzun: %23 (genel %19). Doğru şık konumu: {'A': 0.247, 'D': 0.221, 'E': 0.197, 'C': 0.175, 'B': 0.16}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.61, 'bilesik_yer_degistirmeli': 0.26, 'ayni_ailede_komsu_kavram': 0.173, 'sayisal_yakin_deger': 0.078, 'mutlak_ifade_tuzagi': 0.019}
- Aynı bilginin yeniden sorulması: soruların %8'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %25, olumsuz %21, yanlis_bul %18.
- Kök 8–24 kelime; şık ort. 4.9 kelime, uzunluklar birbirine yakın (CV≈0.31).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L2_anlama_iliski %52, L1_hatirlama %39, L3_uygulama %10.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Diabetes Mellitus Sınıflandırılması, Tanısı ve Komplikasyonları — 58 soru, yıllar [2018, 2019, 2020, 2021, 2022, 2023], güven orta
- **Neden:** tani_ayirici (%33) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.276, 'yanlis_bul': 0.224, 'olumsuz': 0.207, 'dogru_ifade': 0.121, 'vaka': 0.121, 'en_tipik': 0.017, 'sayi': 0.017, 'onculu': 0.017} · düzey {'L2_anlama_iliski': 0.586, 'L1_hatirlama': 0.293, 'L3_uygulama': 0.121} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %7
- **Tekrar eden çekirdek kavramlar:** Tokluk kan şekerinin ≥150 mg/dl olması (4×, 1 yıl); Semptom olmasa dahi, 5. dekattan itibaren üç yılda bir açlık-tokluk kan şekeri ölçerek. (4×, 1 yıl); Hücresel glukoz uptake artışı (2×, 2 yıl); Bikarbonat replasmanı (2×, 2 yıl)

### Paratiroid bezi hastalıkları — 28 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%25) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.321, 'vaka': 0.25, 'dogru_ifade': 0.179, 'dogrudan': 0.107, 'sayi': 0.036, 'en_tipik': 0.036, 'olumsuz': 0.036, 'onculu': 0.036} · düzey {'L2_anlama_iliski': 0.536, 'L3_uygulama': 0.25, 'L1_hatirlama': 0.214} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %21
- **Tekrar eden çekirdek kavramlar:** Erişkinde kalsiyum alımının alt sınırı 200-300 mg/gündür (3×, 1 yıl); Hiperkalsemide QT mesafesi kısalır (2×, 2 yıl); Tiazid diüretikleri tedavide kullanılabilir (2×, 1 yıl); Primer hiperparatiroidi (2×, 1 yıl)

### Yaşlanmada Metabolik Sorunlar — 23 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** mekanizma (%48) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'olumsuz': 0.652, 'yanlis_bul': 0.13, 'onculu': 0.087, 'dogru_ifade': 0.043, 'vaka': 0.043, 'dogrudan': 0.043} · düzey {'L2_anlama_iliski': 0.522, 'L1_hatirlama': 0.435, 'L3_uygulama': 0.043} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %4
- **Tekrar eden çekirdek kavramlar:** Serum kreatinin düzeyi artar (2×, 2 yıl); Kas kitlesi yaşla azaldığından dolayı serum kreatinin düzeyi azalır (2×, 1 yıl)

### Hipotalamus-Hipofiz hastalıklarına giriş — 23 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%39) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.391, 'yanlis_bul': 0.217, 'vaka': 0.13, 'en_tipik': 0.087, 'olumsuz': 0.087, 'sayi': 0.043, 'onculu': 0.043} · düzey {'L2_anlama_iliski': 0.565, 'L1_hatirlama': 0.304, 'L3_uygulama': 0.13} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Hipermagnezemi (2×, 2 yıl); ADH (2×, 1 yıl)

### Demir metabolizması ve anormallikleri, Demir eksikliği ve birikimi — 21 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.333, 'olumsuz': 0.286, 'yanlis_bul': 0.19, 'onculu': 0.19} · düzey {'L1_hatirlama': 0.524, 'L2_anlama_iliski': 0.476} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %10
- **Tekrar eden çekirdek kavramlar:** Demir, ihtiyacı olan hücrelerin yüzeyinde bulunan divalent metal transporter 1 (DMT1) arac (3×, 1 yıl); Herediter hiperferritinemi-katarakt sendromu (2×, 1 yıl); Laboratuvarda total demir bağlama kapasitesi düşük ve transferrin satürasyonu yüksek olara (2×, 1 yıl); C vitamini intoksikasyonu (2×, 1 yıl)

### Obezite-Metabolizma-Endokrin İlişkisi — 21 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** ilac_endikasyon (%38) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'dogrudan': 0.333, 'yanlis_bul': 0.238, 'olumsuz': 0.19, 'onculu': 0.19, 'dogru_ifade': 0.048} · düzey {'L2_anlama_iliski': 0.619, 'L1_hatirlama': 0.381} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %10
- **Tekrar eden çekirdek kavramlar:** Hipertiroidi (3×, 1 yıl); Hastada suçluluk hissi uyandırmak (2×, 1 yıl); Leptin (2×, 1 yıl); Çok su içmek hatalı beslenme davranışlarından biridir. (2×, 1 yıl)

### Gastroenteritler — 20 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** etiyoloji_risk (%70) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'onculu': 0.4, 'olumsuz': 0.2, 'yanlis_bul': 0.15, 'tanim': 0.05, 'vaka': 0.05, 'dogru_ifade': 0.05, 'en_tipik': 0.05, 'dogrudan': 0.05} · düzey {'L2_anlama_iliski': 0.65, 'L1_hatirlama': 0.3, 'L3_uygulama': 0.05} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** I, II, III ve IV (2×, 2 yıl); Vibrio cholerae kalın bağırsak tipi ishale neden olur. (2×, 1 yıl); Vibrio cholerae (2×, 1 yıl)

### Elektrolitler ve Endokrin Sistem Arasındaki ilişki — 20 soru, yıllar [2018, 2020, 2021, 2025], güven dusuk
- **Neden:** tanim_kavram (%55) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.5, 'dogru_ifade': 0.1, 'yanlis_bul': 0.1, 'olumsuz': 0.1, 'en_tipik': 0.05, 'eslestirme': 0.05, 'vaka': 0.05, 'sayi': 0.05} · düzey {'L1_hatirlama': 0.7, 'L2_anlama_iliski': 0.25, 'L3_uygulama': 0.05} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %25
- **Tekrar eden çekirdek kavramlar:** Hiponatremi (2×, 1 yıl)

### GİS Motilite Bozuklukları — 19 soru, yıllar [2018, 2020, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%37) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.211, 'vaka': 0.158, 'onculu': 0.158, 'en_tipik': 0.105, 'sayi': 0.105, 'olumsuz': 0.105, 'dogru_ifade': 0.105, 'yanlis_bul': 0.053} · düzey {'L1_hatirlama': 0.474, 'L2_anlama_iliski': 0.368, 'L3_uygulama': 0.158} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** I ve III (3×, 1 yıl); Diabetes mellitus (2×, 1 yıl); Amiyotrofik lateral skleroz (2×, 1 yıl); Rektal fissür varlığı (2×, 1 yıl)

### Anemi Tanı, Patofizyoloji ve Sınıflaması — 15 soru, yıllar [2020, 2023], güven dusuk
- **Neden:** tanim_kavram (%40) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.333, 'onculu': 0.267, 'dogrudan': 0.2, 'yanlis_bul': 0.133, 'dogru_ifade': 0.067} · düzey {'L2_anlama_iliski': 0.6, 'L1_hatirlama': 0.4} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %13
- **Tekrar eden çekirdek kavramlar:** Eritropoietin; primer olarak karaciğer tarafından üretilen ve kemik iliğinde eritropoezi u (2×, 1 yıl); Vücuttaki bir kanama veya artmış eritrosit yıkımı neticesinde retikülositopeni meydana gel (2×, 1 yıl)

### Hipoglisemiler — 14 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** mekanizma (%50) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'onculu': 0.429, 'olumsuz': 0.214, 'dogrudan': 0.214, 'yanlis_bul': 0.143} · düzey {'L2_anlama_iliski': 0.786, 'L1_hatirlama': 0.214} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %7
- **Tekrar eden çekirdek kavramlar:** İnsülin sekresyonu artar (3×, 2 yıl); Karaciğerde glikojenoliz azalır (2×, 1 yıl); I ve IV (2×, 1 yıl)

### Ailesel Akdeniz Ateşi — 14 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** tani_ayirici (%50) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'olumsuz': 0.5, 'onculu': 0.286, 'yanlis_bul': 0.214} · düzey {'L2_anlama_iliski': 0.929, 'L1_hatirlama': 0.071} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %21
- **Tekrar eden çekirdek kavramlar:** FMF'te genellikle poliartrit şeklinde eklem tutulumu olur (4×, 3 yıl); I, II ve III (3×, 1 yıl); Tutulan eklem sıvısı incelemesinde eozinofil baskınlığı ve yoğun karbonhidrat konsantrasyo (2×, 1 yıl); Albümin (2×, 1 yıl)

### Sarılıklar — 14 soru, yıllar [2018, 2020, 2021, 2022], güven dusuk
- **Neden:** siniflama_ad (%29) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.357, 'olumsuz': 0.286, 'vaka': 0.214, 'onculu': 0.071, 'yanlis_bul': 0.071} · düzey {'L1_hatirlama': 0.643, 'L3_uygulama': 0.214, 'L2_anlama_iliski': 0.143} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %7
- **Tekrar eden çekirdek kavramlar:** Dubin-Johnson sendromu (3×, 2 yıl); I ve III (2×, 1 yıl); Bilirubin oluşumu başta dalak ve tiroid olmak üzere RES (retikuloendotelyal sistem) hücrel (2×, 1 yıl); Dubin-Johnson sendromu (2×, 1 yıl)

### Megaloblastik anemiler — 14 soru, yıllar [2020, 2022, 2023], güven dusuk
- **Neden:** tanim_kavram (%57) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'vaka': 0.357, 'yanlis_bul': 0.214, 'dogrudan': 0.214, 'en_tipik': 0.071, 'eslestirme': 0.071, 'olumsuz': 0.071} · düzey {'L1_hatirlama': 0.357, 'L3_uygulama': 0.357, 'L2_anlama_iliski': 0.286} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %21
- **Tekrar eden çekirdek kavramlar:** B12 vitamini eksikliğinde makrositer ve nonmegaloblastik anemi meydana gelir. (2×, 1 yıl); Nörolojik şikâyetlerin olması (2×, 1 yıl); Önce B12 tedavisi başlanmalı; folat verilirse anemi düzelir fakat geri dönüşümsüz nöroloji (2×, 1 yıl); Oral B12 vitamini vermesi (2×, 0 yıl)

### Cushing Sendromu — 13 soru, yıllar [2018, 2020, 2022], güven dusuk
- **Neden:** tani_ayirici (%54) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'olumsuz': 0.462, 'en_tipik': 0.231, 'onculu': 0.231, 'dogrudan': 0.077} · düzey {'L2_anlama_iliski': 0.538, 'L1_hatirlama': 0.462} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %23
- **Tekrar eden çekirdek kavramlar:** Cushing hastalığı (2×, 2 yıl); II ve IV (2×, 1 yıl)

### Akut Pankreatitler — 12 soru, yıllar [2018, 2020, 2023], güven dusuk
- **Neden:** tani_ayirici (%33) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'olumsuz': 0.5, 'en_tipik': 0.167, 'vaka': 0.167, 'yanlis_bul': 0.083, 'dogrudan': 0.083} · düzey {'L2_anlama_iliski': 0.417, 'L1_hatirlama': 0.417, 'L3_uygulama': 0.167} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Safra taşları (3×, 2 yıl); Hiperkalsemi (3×, 1 yıl); Oral gıda alımına devam edilir (2×, 1 yıl); Hipokalsemi (2×, 0 yıl)

### Akut Hepatitler — 12 soru, yıllar [2018, 2020, 2021, 2022, 2023], güven dusuk
- **Neden:** etiyoloji_risk (%50) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'yanlis_bul': 0.417, 'dogrudan': 0.167, 'onculu': 0.167, 'olumsuz': 0.083, 'sayi': 0.083, 'dogru_ifade': 0.083} · düzey {'L2_anlama_iliski': 0.583, 'L1_hatirlama': 0.417} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %8
- **Tekrar eden çekirdek kavramlar:** Akut enfeksiyonda ilk yükselen antikor anti-HAV IgG'dir. (2×, 1 yıl)

### Cinsel Farklılaşma Bozuklukları — 12 soru, yıllar [2018, 2020, 2021, 2023], güven dusuk
- **Neden:** tani_ayirici (%58) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'en_tipik': 0.333, 'dogrudan': 0.333, 'olumsuz': 0.167, 'vaka': 0.167} · düzey {'L2_anlama_iliski': 0.417, 'L1_hatirlama': 0.417, 'L3_uygulama': 0.167} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** 17-alfa-hidroksilaz enzim eksikliği (2×, 1 yıl)

### Gastrointestinal Sistem Parazitozları — 12 soru, yıllar [2018, 2020, 2021], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.583, 'sayi': 0.167, 'vaka': 0.083, 'eslestirme': 0.083, 'onculu': 0.083} · düzey {'L1_hatirlama': 0.583, 'L2_anlama_iliski': 0.333, 'L3_uygulama': 0.083} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Taenia saginata (2×, 1 yıl)

### Bakteriyel İshaller — 11 soru, yıllar [2020], güven dusuk
- **Neden:** etiyoloji_risk (%64) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'yanlis_bul': 0.636, 'dogrudan': 0.182, 'onculu': 0.182} · düzey {'L2_anlama_iliski': 0.818, 'L1_hatirlama': 0.182} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Hafif bir klinik tablodur, antibiyotik tedavisine gerek yoktur (2×, 1 yıl); Sadece bağırsak ile sınırlı enfeksiyonlara neden olur, sistemik enfeksiyona neden olmaz (2×, 1 yıl)

### Yaşlılıkta Beslenme — 11 soru, yıllar [2018, 2020], güven dusuk
- **Neden:** tanim_kavram (%45) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.455, 'yanlis_bul': 0.182, 'onculu': 0.182, 'dogrudan': 0.091, 'dogru_ifade': 0.091} · düzey {'L1_hatirlama': 0.545, 'L2_anlama_iliski': 0.455} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Obezite (2×, 1 yıl)

### Siroz ve Komplikasyonları — 10 soru, yıllar [2020, 2023], güven dusuk
- **Neden:** etiyoloji_risk (%30) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'dogrudan': 0.6, 'olumsuz': 0.3, 'en_tipik': 0.1} · düzey {'L1_hatirlama': 0.8, 'L2_anlama_iliski': 0.2} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Parasentez (3×, 1 yıl); Asit (2×, 1 yıl); Hepsi (2×, 1 yıl)

### Hemostaz ve anormallikleri, Kanama Pıhtılaşma bozuklukları — 10 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%30) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.3, 'dogrudan': 0.2, 'dogru_ifade': 0.1, 'onculu': 0.1, 'olumsuz': 0.1, 'vaka': 0.1, 'en_tipik': 0.1} · düzey {'L1_hatirlama': 0.5, 'L2_anlama_iliski': 0.4, 'L3_uygulama': 0.1} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %20
- **Tekrar eden çekirdek kavramlar:** En sık görülen tip, Tip 1'dir. (2×, 1 yıl)

### D Vitamini Metabolizması — 10 soru, yıllar [2020, 2021], güven dusuk
- **Neden:** mekanizma (%40) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.5, 'yanlis_bul': 0.2, 'vaka': 0.2, 'dogru_ifade': 0.1} · düzey {'L2_anlama_iliski': 0.7, 'L3_uygulama': 0.2, 'L1_hatirlama': 0.1} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor · **kaynağa bağımlılık:** özet kanıtlı %20

### Endokrin Sistem Hastalıklarına Genel Yaklaşım — 7 soru, yıllar [2018, 2020, 2023], güven dusuk
- **Neden:** mekanizma (%43) — Neden-sonuç zinciri klinik muhakemenin temelidir; ezberlenen sonuç değil, zincirin bir halkası sorulur.
- **Nasıl:** {'dogrudan': 0.429, 'vaka': 0.286, 'yanlis_bul': 0.143, 'onculu': 0.143} · düzey {'L2_anlama_iliski': 0.571, 'L3_uygulama': 0.286, 'L1_hatirlama': 0.143} · Sonuçtan kök nedene ya da nedenden sonuca; çeldirici zincirin komşu halkasıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %29
- **Tekrar eden çekirdek kavramlar:** I, III, IV ve V (2×, 1 yıl)
