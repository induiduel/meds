# Çocuk Sağlığı ve Hastalıkları — hoca üslubu ve kazanım haritası (otomatik; `scripts/hoca_profili/uslup_analiz.py`)

> 143 tekil çıkmış soru · güven: **yuksek** · yıllar: {2018: 15, 2020: 57, 2021: 11, 2022: 17, 2023: 2, 2024: 2, 2025: 1}

## 1. Üslup özeti

### Kök kalıbı
- **dogrudan**: %34 (genel ortalama %40)
- **yanlis_bul**: %22 (genel ortalama %13)
- **olumsuz**: %18 (genel ortalama %15)
- **en_tipik**: %11 (genel ortalama %8)
- **vaka**: %8 (genel ortalama %5)
- **dogru_ifade**: %2 (genel ortalama %6)
- **onculu**: %2 (genel ortalama %8)

### Sorulan bilgi türü (neden sorulur)
- **tanim_kavram**: %29 (genel ortalama %32)
- **tani_ayirici**: %23 (genel ortalama %12)
- **etiyoloji_risk**: %13 (genel ortalama %11)
- **mekanizma**: %11 (genel ortalama %14)
- **siniflama_ad**: %10 (genel ortalama %9)
- **ilac_endikasyon**: %6 (genel ortalama %7)
- **onleme_halk_sagligi**: %5 (genel ortalama %5)

### Bilişsel düzey
- **L2_anlama_iliski**: %50 (genel ortalama %44)
- **L1_hatirlama**: %43 (genel ortalama %51)
- **L3_uygulama**: %8 (genel ortalama %5)

### Biçim
- Kök uzunluğu: ort. 15.5 kelime (p25 8 · medyan 10 · p75 17).
- Şık: ort. 5.4 kelime; bileşik şık %22; sayısal şık %6; mutlak ifadeli çeldirici %1.
- Doğru şık tek başına en uzun: %20 (genel %19). Doğru şık konumu: {'A': 0.273, 'D': 0.217, 'E': 0.196, 'C': 0.196, 'B': 0.119}.
- Çeldirici stratejisi: {'ayni_turden_ayri_kavram': 0.671, 'bilesik_yer_degistirmeli': 0.21, 'ayni_ailede_komsu_kavram': 0.154, 'sayisal_yakin_deger': 0.063, 'mutlak_ifade_tuzagi': 0.014}
- Aynı bilginin yeniden sorulması: soruların %10'i birden çok kez çıkmış.

## 2. Yazım kuralları (bu dersin soruları için)

- Kök kalıbı payları çıkmışa ±10 puan: dogrudan %34, yanlis_bul %22, olumsuz %18.
- Kök 8–17 kelime; şık ort. 5.4 kelime, uzunluklar birbirine yakın (CV≈0.28).
- Doğru şık tek başına en uzun/en ayrıntılı olmaz; yer değiştirmeli bileşik şık ve komşu-kavram çeldiriciler tercih edilir.
- Bilişsel düzey hedefi: L2_anlama_iliski %50, L1_hatirlama %43, L3_uygulama %8.

## 3. Konu bazlı kazanım haritası (en çok sorulan 25 konu)

### Çocukluk Dönemi Su Metabolizması Bozuklukları — 23 soru, yıllar [2018, 2020, 2021, 2024], güven dusuk
- **Neden:** tani_ayirici (%30) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'dogrudan': 0.478, 'vaka': 0.174, 'dogru_ifade': 0.087, 'olumsuz': 0.087, 'tanim': 0.043, 'en_tipik': 0.043, 'yanlis_bul': 0.043, 'sayi': 0.043} · düzey {'L1_hatirlama': 0.522, 'L2_anlama_iliski': 0.304, 'L3_uygulama': 0.174} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %13
- **Tekrar eden çekirdek kavramlar:** Plazma sodyumunun 135 mEq/L'yi geçmesi (3×, 1 yıl); Sodyum (2×, 1 yıl); Üst solunum yolu enfeksiyonları (2×, 1 yıl); Hipermagnezemi (2×, 1 yıl)

### Hemoglobinopatiler — 22 soru, yıllar [2020, 2021, 2024, 2025], güven dusuk
- **Neden:** tanim_kavram (%32) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.409, 'olumsuz': 0.318, 'yanlis_bul': 0.182, 'dogru_ifade': 0.045, 'vaka': 0.045} · düzey {'L2_anlama_iliski': 0.545, 'L1_hatirlama': 0.409, 'L3_uygulama': 0.045} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %5
- **Tekrar eden çekirdek kavramlar:** Hidrops fetalis (4×, 1 yıl); Enfeksiyonlara artmış eğilim göstermeleri (3×, 1 yıl); Gastrointestinal sistemden demir atılımını engellemek (2×, 1 yıl); Demir desteği (2×, 1 yıl)

### Konjenital GİS Malformasyonları — 21 soru, yıllar [2018, 2020, 2022, 2023], güven dusuk
- **Neden:** tani_ayirici (%43) — Doğru tanı/tetkik seçimi hekimin ilk kararıdır; benzer tabloları ayırt eden TEK bulgu sorulur.
- **Nasıl:** {'yanlis_bul': 0.381, 'dogrudan': 0.286, 'en_tipik': 0.238, 'olumsuz': 0.095} · düzey {'L2_anlama_iliski': 0.81, 'L1_hatirlama': 0.19} · Kısa vaka ya da 'en tipik/ayırt edici' kökü; çeldirici benzer tablonun öteki hastalığıdır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %24
- **Tekrar eden çekirdek kavramlar:** İleum (2×, 1 yıl); İnfantil hipertrofik pilor stenozu, yenidoğan döneminde longitudinal kasların hipertrofisi (2×, 1 yıl); Normal sinir uyarılarını alan proksimal kolon kontraktedir (2×, 1 yıl); Mezenteroaksiyel volvulus çocuklarda nadir görülür (2×, 1 yıl)

### Çocukluk çağı anemilerine yaklaşım — 15 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%33) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'yanlis_bul': 0.333, 'dogrudan': 0.2, 'olumsuz': 0.133, 'vaka': 0.133, 'onculu': 0.133, 'en_tipik': 0.067} · düzey {'L2_anlama_iliski': 0.533, 'L1_hatirlama': 0.333, 'L3_uygulama': 0.133} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Fizyolojik anemi term bebeklerde 6-8. haftada, preterm bebeklerde 8-12. haftada gelişir (4×, 1 yıl); Azalmış total demir bağlama kapasitesi (3×, 1 yıl); B12 ve folik asit eksikliği, kemik iliği hipoplazisi yapıp eritroid seri baskısı ile anemi (2×, 1 yıl); 6 yaşın altındaki hafif trombositoz vakaları riskli olabileceği için ileri tetkik ve araşt (2×, 1 yıl)

### Biliyer Atrezi ve Diğer Safra Yolu Anomalileri — 12 soru, yıllar [2018, 2020], güven dusuk
- **Neden:** etiyoloji_risk (%33) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'yanlis_bul': 0.583, 'en_tipik': 0.333, 'dogrudan': 0.083} · düzey {'L2_anlama_iliski': 0.75, 'L1_hatirlama': 0.25} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Polispleni ve situs inversus perinatal/akkiz tipte sıkça rastlanır. (2×, 1 yıl); Çocuklarda karaciğer nakillerinin en sık nedenidir. (2×, 1 yıl)

### Siyanotik doğumsal kalp hastalıkları — 12 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%42) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.417, 'olumsuz': 0.333, 'vaka': 0.083, 'en_tipik': 0.083, 'onculu': 0.083} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.25, 'L3_uygulama': 0.083} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %17
- **Tekrar eden çekirdek kavramlar:** Mitral yetmezlik (3×, 1 yıl)

### Asiyanotik doğumsal kalp hastalıkları — 7 soru, yıllar [2020], güven dusuk
- **Neden:** tanim_kavram (%57) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.429, 'dogrudan': 0.429, 'en_tipik': 0.143} · düzey {'L1_hatirlama': 0.714, 'L2_anlama_iliski': 0.286} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %43
- **Tekrar eden çekirdek kavramlar:** Bradikardi (3×, 1 yıl); Aort koarktasyonu (3×, 1 yıl)

### Neonatal Kolestaz — 7 soru, yıllar [2018, 2022], güven dusuk
- **Neden:** ilac_endikasyon (%29) — Doğru ilacı doğru hastaya vermek: endikasyon/ilk seçenek.
- **Nasıl:** {'olumsuz': 0.429, 'en_tipik': 0.286, 'vaka': 0.143, 'yanlis_bul': 0.143} · düzey {'L2_anlama_iliski': 0.714, 'L3_uygulama': 0.143, 'L1_hatirlama': 0.143} · Durumdan ilaca; çeldirici aynı endikasyonda ikinci sıradaki ya da başka sınıf ilaçtır.
- **Zorluk:** orta-zor, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Down sendromu (3×, 1 yıl); İdiyopatik neonatal hepatit (2×, 1 yıl)

### Solunum Sist. Hastalık. Fizik Muayene — 6 soru, yıllar [2020, 2021, 2022], güven dusuk
- **Neden:** tanim_kavram (%50) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'dogrudan': 0.667, 'vaka': 0.333} · düzey {'L1_hatirlama': 0.333, 'L2_anlama_iliski': 0.333, 'L3_uygulama': 0.333} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Auditory fremitus (işitsel fremitus) (5×, 2 yıl)

### Fetal Dolaşım ve Neonatal adaptasyon — 5 soru, yıllar [2020, 2022, 2023], güven dusuk
- **Neden:** onleme_halk_sagligi (%60) — Korunma düzeyi ve tarama ilkeleri halk sağlığı mantığının çekirdeğidir.
- **Nasıl:** {'dogrudan': 0.4, 'yanlis_bul': 0.4, 'olumsuz': 0.2} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · Senaryoda uygun önleme düzeyi/yöntem seçilir; çeldirici bir üst/alt düzeydir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %0

### Solunum sistemi Semptomatolojisi — 5 soru, yıllar [2020], güven dusuk
- **Neden:** etiyoloji_risk (%40) — Neden ve risk faktörü önleme/tanıyı yönlendirir.
- **Nasıl:** {'tanim': 0.2, 'sayi': 0.2, 'en_tipik': 0.2, 'yanlis_bul': 0.2, 'olumsuz': 0.2} · düzey {'L1_hatirlama': 0.6, 'L2_anlama_iliski': 0.4} · En sık neden/en önemli risk kökü; çeldirici daha seyrek nedenlerdir.
- **Zorluk:** kolay-orta · **kaynağa bağımlılık:** özet kanıtlı %0

### Solunum sıkıntısı olan yeni doğana yaklaşım — 5 soru, yıllar [2020], güven dusuk
- **Neden:** siniflama_ad (%40) — Ortak dil: sınıflama, evre ve ad/eponim iletişim ve prognoz için gerekir.
- **Nasıl:** {'dogrudan': 0.8, 'yanlis_bul': 0.2} · düzey {'L1_hatirlama': 0.8, 'L2_anlama_iliski': 0.2} · Tanım ya da ölçütten ada, adtan özelliğe; çeldirici komşu tip/evredir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %0
- **Tekrar eden çekirdek kavramlar:** Oksijen vermek (2×, 1 yıl)

### Siyanoz — 3 soru, yıllar [2020, 2022], güven dusuk
- **Neden:** tanim_kavram (%67) — Temel kavram/tanım sonraki bilgilerin dayanağıdır; terimin sınırı ölçülür.
- **Nasıl:** {'olumsuz': 0.333, 'dogrudan': 0.333, 'yanlis_bul': 0.333} · düzey {'L1_hatirlama': 0.667, 'L2_anlama_iliski': 0.333} · Tanım → terim ya da terim → özellik; çeldirici komşu terimlerdir.
- **Zorluk:** kolay-orta, tekrar eden · **kaynağa bağımlılık:** özet kanıtlı %33
- **Tekrar eden çekirdek kavramlar:** Hipotermi (2×, 1 yıl)
