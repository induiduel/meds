# İçerik Motoru v3 — Kroki (L0/L1/L2), maliyet katmanlı model yönlendirme, canlı çizim ve tekil ders paketi

> Kayıt: 2026-10-23 (Kurul 2 açılışına 3 gün). Kaynak: kullanıcının ilettiği "Kurul 1–6 uçtan uca mimari" önerisi,
> bu projenin **gerçek altyapısına** oturtularak uyarlandı. Önerideki her başlık ya mevcut bir parçanın üstüne kurulur ya da
> neden değiştirildiği yazılıdır. Bu belge `GELECEK_PLANLAMASI.md`'nin **P5** bölümüdür; işletim talimatı her aşama devreye
> girdikçe `KURUL_OTOMASYON_EL_KITABI.md`'ye taşınır. Makine okunur aşamalar: `otomasyon/hat.json`.
>
> **Kullanıcı kararı (2026-10-23):** Claude ile sürekli ders üretmek kullanım sınırını hızla tüketiyor. Hat; **önce
> betik (LLM'siz), sonra ücretsiz bulut LLM, en son Claude** sırasıyla çalışacak; her koşula (kota bitti, servis düştü,
> GPU meşgul, ağ yok) hazır yedek yolu olacak. 2026-10-20'deki "LLM yalnız Claude" kararı bu belgedeki yönlendirici
> devreye girdikçe **görev görev** gevşer; yönlendirici kurulana dek mevcut Claude hattı olduğu gibi çalışır.

---

## 0. Kısa özet

| Önerideki fikir | Bu projedeki karşılığı | Karar |
|---|---|---|
| Kurul 1–6 modüler arşiv, aktif kurul derleme modu | takvim (`kurulTakvimi.ts`, `aktif_kurul.py`), `/gecmis-kurullar`, `?kurul=N`, ders kayıt defteri `kN.json` | **Var** → arşiv kipine "hızlı tekrar" görünümü eklenecek (§9) |
| Drive webhook ile anında tetik | Oracle `izle.py` 50 dk tarama, sha256 farkı | **Uyarla:** Drive `changes.watch` (Oracle HTTPS ucu) + tarama yedek olarak kalır (§8) |
| Slayt kayması: SimHash + pHash, tekrar OCR yok | PDF düzeyinde sha256; sayfa düzeyinde iz **yok** | **Yeni (R1):** sayfa izi + eski→yeni sayfa eşlemesi, yalnız yeni sayfa okunur (§2.2) |
| L0 Ham kroki (bbox, tablo, ROI) | `cikar.py` (`kaynak.md`, `sayfalar.json`, sayfa PNG), `pdf_isaret.py` (kelime/tablo/resim kutuları) | **Kısmen var** → tek `l0/` klasöründe birleşir, ROI eklenir (§2) |
| L1 Bağlam ve otorite yaması | önem haritası, çıkmış bağları, kazanımlar, `ogrenci_not_isaret.py`, hoca kaydı Whisper dökümü (elle) | **Kısmen var** → sayfa başına yama dosyası, hoca sesi hatta (§2) |
| L2 Anlatı, çizim, soru | `konusma_v2.json` (ses/ekran iki yüz, kimlik), çapa + imleç yolu, Öğren destesi, spot/çözücü/asistan | **Var** → çizim komutları + parça başı 1–6 soru eklenir (§3, §6) |
| 4 çizim kipi (kontur, yolak, EKG fazı, görselsiz şema) | `PdfDocView` halka/imleç (`yol`), `SlideDrawingCanvas`, kelime zamanı | **Yeni (R4–R5)**, kelime kimliğine bağlı (ms'ye değil) (§4) |
| 3+1 renk sistemi, uyarlanır kontrast | `palettes.ts` + kontrast kapısı, öğrenci notu kırmızı marker (`.pdv-not`), cümle/kelime vurgusu | **Kısmen var** → sayfa parlaklığı L0'da ölçülür, renkler palet jetonu (§5) |
| LiteLLM ile model bağımsızlık; Ollama/vLLM | `scripts/agents/cloud_llm.py` (Gemini Free 1–7, Groq, Zen, OpenRouter zinciri, kota defteri, görsel OCR) | **Uyarla:** LiteLLM eklenmez, mevcut istemci **görev yönlendiricisi** ile genişler; **yerel model YOK** (AGENTS.md 10) (§1) |
| EMA GPU → CPU düşüşü | `meds-ema` drop-in: koruyucu etkinse GPU, değilse CPU; CUDA hatasında oturum CPU | **Var** → OOM'da iş yeniden kuyruğa + CPU sağlaması belgelenir (§7) |
| `display_text` / `tts_text` + fonetik | `konusma_v2` `ekran`/`ses`, `okunus.py` (kısaltma, `SAYI_TTS`), `ekranYazim.ts`, `yazim_sozlugu.py` | **Var** → tek okunuş sözlüğü + noktalama temizliği + duraklama (§7) |
| WhisperX kelime hizalama | `kelime_zaman.py` (faster-whisper, CPU/GPU istisnası), `cumle_zaman.py` | **Var** (WhisperX gerekmez) |
| Tekil `.meds` SQLite dosyası | çevrimdışı paket motoru (`paketMotoru.ts`, Cache Storage), JSON uçları | **Uyarla:** paket **türetilmiş dışa aktarımdır**, doğruluk kaynağı değildir (§6) |
| Kendi okuyucu: sesli ders + mini quiz + çözücü + "Anlatıldığı yere git" | canlı ders, soru çözücü, `/k/<kimlik>` deeplink | **Var** → "Çıkmışı göster" rozeti, parça sonu soruları, çözücüden cümleye ışınlanma (§9) |
| OpenCV/SciPy ile sıfır-token görsel analiz, cümle ses önbelleği, VAD, DSP, kısa kimlikli iskelet | `ogrenci_not_isaret.py` (piksel farkı), çapa M#/R# | **Ek (§12)**: koordinatı hiçbir model üretmez |
| Kişisel zayıf nokta ısı haritası | çalışma takibi, userKvSync | **Yeni (§13)** |
| Her LLM'in yapabileceği betikleştirilmiş hat, derleyici/çözücü | TALIMAT dosyaları Claude'un dosya gezmesine dayalı | **Yeni (§14)**: görev paketi + derleyici + kapı |
| Her PDF neyi tarayacağını bilsin | `isle.py` tüm havuzda 30 sorgu, yalnız kurul süzgeci; ters yön yok | **Yeni (§15)**: çıkmış dizini + tarama planı + ters yön |
| Soru → bilgi yeri → tekrar | önem haritası sayfa düzeyi | **Yeni (§16)**: kanıt bölgeleri (doğru/çeldirici/kök) |
| SoM, makro→mikro, kapsam denetimi, çeldirici, ok açılımı | kısmen talimatlarda | **§17** |
| Akıllı hız, görsel atlas, karşılaştırma, etimoloji, kart; donanım optimizasyonları | — | **§18, §19** |

---

## 1. Maliyet katmanlı model yönlendirme (bu planın kalbi)

### 1.1 Üç katman

| Katman | Ne | Maliyet | Ne zaman |
|---|---|---|---|
| **B — Betik** | Deterministik Python/TS: PyMuPDF, Tesseract, bge-m3/e5 (CPU), faster-whisper, kurallı üreticiler, şablonlar | 0 | Her zaman önce. Çıktısı kapıdan geçerse LLM çağrılmaz. |
| **Ü — Ücretsiz bulut** | `cloud_llm.chat` / `vision_ocr` zinciri (Gemini Free anahtar havuzu, Groq gpt-oss/Qwen, Zen Muse Spark, OpenRouter ekleri) | 0 (kota) | Sınırlı, şemalı JSON işleri; görsel betimleme; yazar ya da denetçi rolü |
| **C — Claude** | `claude -p` (dar izin listesi, mevcut zincir) | kullanım sınırı | Ü iki farklı model ailesiyle kapıdan geçemezse; örneklem denetimi; yüksek riskli kararlar (§1.4) |

Yerel LLM (Ollama, llama-server, vLLM) **yok** — AGENTS.md 10 kesin. GPU istisnaları yalnız ses/vektör/zamanlama işleri içindir.

### 1.2 Görev yönlendiricisi (`otomasyon/llm/`)

- **`gorevler.json`** (defter, `hat.json` gibi): her görev için
  `{id, katmanlar: ["B","Ü","C"], sema, kapi, yazar_ailesi, denetci_ailesi, deneme: {Ü: 2, C: 1}, girdi_sinir_kelime,
  ornekleme_C: 0.0–1.0, risk: "dusuk|orta|yuksek"}`.
- **`yonlendir.py`** — tek giriş: `calistir(gorev, girdi) → {cikti, katman, model, deneme, kapi_raporu}`.
  1. B üreticisi varsa çalıştır → kapı 0 HATA ise bitir.
  2. Ü: yazar ailesiyle üret → **şema doğrulaması** (JSON Schema) → görevin kapısı → hata listesi aynı modele geri
     (en çok `deneme.Ü` tur) → hâlâ hata varsa **ikinci model ailesi** (Gemini ↔ Groq/gpt-oss) aynı turu dener.
  3. C: yalnız `katmanlar` içinde varsa ve günlük bütçe izin veriyorsa; yoksa iş **ertesi geceye ertelenir**
     (`bekliyor_butce`, panoda sarı) — sessiz başarısızlık değil, düşük kaliteli yayın hiç değil.
- **Yazar ≠ denetçi** kuralı (El kitabı §0.2) model ailesiyle sağlanır: Gemini yazdıysa denetçi Groq/gpt-oss (ya da
  tersi); risk "yüksek" görevlerde denetçi Claude. Denetçi raporu her durumda `denetim/<kod>.md`'ye yazılır.
- **Claude bütçesi** `otomasyon/llm/butce.json`: `{gunluk_cagri, gunluk_dakika, ders_basina_cagri, oncelik: [...]}`.
  Sayaç `meds_temp/state/claude_butce.json`. Panelde (Yönetim › Hat) kalan bütçe ve ertelenen işler görünür.
- **Önbellek:** istem + girdi karması → yanıt (`meds_temp/llm_onbellek/<gorev>/<sha>.json`). Aynı girdi ikinci kez
  hiçbir modele gitmez (yeniden koşu, prova, kapı düzeltmesi sonrası tekrar ücretsizdir).
- **Gizlilik:** ücretsiz katmana yalnız ders PDF metni / görseli, çıkmış soru ve üretilmiş taslak gider. Öğrenci adı,
  e-posta, kişisel not metni, hoca ses kaydının ham dosyası gitmez (döküm metni ders içeriği olduğu için gidebilir).
  Gemini ücretsiz katmanında istemler sağlayıcının geliştirmesinde kullanılabilir — bu yüzden kişisel veri yasağı kesin.

### 1.3 Görev × katman tablosu (ilk sürüm)

| Görev | B (betikle) | Ü | C | Not |
|---|---|---|---|---|
| Metin çıkarma, OCR, tablo, kelime kutusu | ✔ tamamı | — | — | `cikar.py`, `pdf_isaret.py` |
| ROI koordinatı, eğri, ok, kontur | ✔ OpenCV + iskelet + tepe bulma (§12.1) | — | — | koordinatı **hiçbir model üretmez** |
| Görsel betimleme, ROI adlandırma | etiket = ROI içindeki L0 kelimeleri | ✔ `vision_ocr` yalnız etiketsiz ROI'ye ad | — | yalnız slaytta görünen; kapı §4.3 |
| Önem haritası, çıkmış eşleme, tekrar ailesi | ✔ tamamı | — | — | `onem_haritasi.py`, bge-m3 |
| Okunuş (`ses` metni), yazım (`ekran`) | ✔ sözlük + kural | yeni kısaltma adayı önerisi | — | öneri sözlüğe insan/kapı onayıyla girer |
| Öğren etkileşimleri: tablo, venn, eşleme, boşluk doldurma, sıralama | ✔ `sayfalar.json` tablolarından ve vurgulu cümlelerden şablon | çeldirici + açıklama cilası | — | kronoloji/sızıntı kapısı (Kural 7–8) betikte |
| Mini soru, klinik karar, tuzak avı | — | ✔ yazar | örneklem | `validate_learning_decks.py --kurul2` |
| Sesli ders metni v2 (anlatım) | iskelet: sayfa sırası, madde listesi, vurgu | ✔ yazar (bölüm bölüm, ≤3 sayfa/istem) | denetçi (yüksek risk) | `konusma_v2.py --dogrula`, `metin_denetle.py` (H22) |
| Spot / önem listesi | aday listesi (`aday_hazirla.py`) | ✔ yazar | örneklem | `onem_dogrula.py` |
| Soru çözücü, asistan, parça başı 1–6 soru | çıkmış eşlemesi, şık havuzu | ✔ yazar | denetçi örneklemi | `cozucu_dogrula.py`, `sik_aciklama.py`, `turkce_uslup.py` |
| Bağımsız denetim | — | ✔ farklı aile | ✔ yüksek risk + %20 örneklem | rapor zorunlu |
| Çapa (cümle → madde/resim) | ✔ `pdf_isaret` LCS + bge-m3 | belirsiz cümleler | — | `capa_dogrula.py` ≥%70 |
| Görselsiz slayt şeması (DSL) | düğüm adayları (terimler) | ✔ yazar | — | §4.4 kapısı |
| Çıkmış anahtar çelişkisi (H10/H19), olası soru sentezi | aday bulma | ön eleme | ✔ karar | yüksek risk: yanlış anahtar öğrenciyi yanıltır |
| Hastalık şema 2, Check Up, kamp, Son Prova | depo özeti | ✔ yazar | denetçi | mevcut TALIMAT dosyaları istem olarak yeniden kullanılır |

Hedef ölçü: **Kurul 2 dersi başına Claude çağrısı ≈7'den ≤1'e** (yalnız denetim örneklemi ya da yüksek risk).

### 1.4 Ne zaman mutlaka Claude (risk "yüksek")

Çıkmış cevap anahtarı değiştirme; olası soru son sentezi; bir dersin **ilk** yayınından önceki son denetçi geçişi
(Kurul 2'nin ilk 5 dersi, kalite ölçülene dek); Ü'nün iki ailesinin de geçemediği işler. Bütçe biterse bu işler bekler.

### 1.5 Mevcut TALIMAT dosyaları

`TALIMAT*.md` dosyaları model bağımsız istem olarak kalır. Claude'a özgü kısımlar (Read/Write/Bash ile dosya gezme)
yönlendiricide **girdi paketi** (ilgili depo özeti + sayfalar + şema) ve **çıktı şeması** ile değiştirilir: Ü modelleri
dosya sistemi görmez, yalnız istem içindeki paketi görür. Böylece aynı talimat üç katmanda da çalışır.

---

## 2. Kroki: L0 / L1 / L2 katmanları

Yer: mevcut ders bilgi deposu genişler — `meds_database_v2/ders_bilgi/<ders kimliği>/` (El kitabı D3, "her PDF bir kez").

```
ders_bilgi/k2-07/
  manifest.json            (mevcut) + katman karmaları {l0_sha, l1_sha:{sayfa:sha}, l2_sha:{parca:sha}}
  l0/sayfalar.json         sayfa: kimlik k2-07-p12, iz {metin_simhash, gorsel_phash}, boyut, parlaklik, metin, kelimeler[bbox],
                           tablolar[hücre], resimler[bbox], roi[], vurgulu (hoca rengi/kalın)
  l0/goruntu/<p>.webp      sayfa görüntüsü (bir kez)
  l1/<p>.json              sayfa yaması: cikmis[], ogrenci_not[], hoca_ses[], kazanim[], onem {puan}
  l2/konusma_v2.json       (mevcut biçim) + cizim[] + parca_sorulari[]
  l2/capa.json             (mevcut çapa)
```

### 2.1 L0 — değişmez kroki (bir kez)

- Kelime kutuları zaten `pdf_isaret.py`'de okunuyor; R1'de bu okuma **L0'a bir kez yazılır**, `pdf_isaret` L0'dan okur.
- `parlaklik`: sayfa görüntüsünün ortalama göreli parlaklığı (WCAG bağıl ışıklılık) + koyu/açık/renkli zemin sınıfı → §5.
- `roi`: görsel alt bölgeleri `{id: k2-07-p12-g1-r3, tur: kontur|yolak|egri|tablo_hucre|etiket, bbox, nokta[]?, etiket}`.
  Koordinatlar yalnız betikle çıkar (§12.1); ad önce ROI içindeki L0 kelimelerinden, yoksa Ü görsel modelinden. Kapı geçmeyen ROI yazılmaz.
- Kimlik standardı (`GELECEK_PLANLAMASI §5`) korunur: sayfa `k2-07-p12`, görsel `-g1`, tablo `-t1`; ROI için `-r3` eklenir.

### 2.2 Slayt kayması (sayfa izi)

- Her sayfa için `metin_simhash` (64 bit, Türkçe katlanmış sözcük 3'lüleri) + `gorsel_phash` (64 bit, 32×32 DCT).
- Hoca PDF'i güncelleyince: yeni sayfalar eski sayfalarla eşlenir (Hamming ≤ 6 metin ve ≤ 10 görsel → aynı sayfa;
  yalnız biri tutarsa "değişmiş sayfa"). Sonuç `l0/sayfa_eslesme.json: {eski_p: yeni_p | null}`.
- Eşleşen sayfada OCR, ROI, görsel betimleme **yapılmaz**, L0 kaydı taşınır; yalnız yeni/değişmiş sayfa okunur.
- **Kimlik kararı:** `k2-07-p12` konum numarasıdır (ön yüz sayfa numarası ister). Eşleşen sayfanın L1/L2 içeriği yeni
  numarasına taşınır; eski kimlik `takma_ad` olarak kalır, `/k/<eski>` yeni sayfaya yönlenir (kimlikler kırılmaz).

### 2.3 L1 — bağlam ve otorite yaması (sayfa başına)

| Kaynak | Bugün | v3 |
|---|---|---|
| Çıkmış soru bağı | `onem_haritasi.py` sayfa düzeyi | cümle/kelime düzeyi: en iyi sayfada bge-m3 + `pdf_isaret` LCS ile kelime aralığı → yeşil (§5) |
| Öğrenci notu PDF'i | `ogrenci_not_isaret.py` (piksel farkı, elle DERSLER listesi) | Drive `Kurul N/Ogrenci_Notu/` → otomatik; **hizalama kapısı**: not sayfası ders sayfasıyla `gorsel_phash` ve kelime kutusu kaymasıyla eşleşmeli, kayıksa (k1-51 tuzağı) yazılmaz + bildirim |
| Hoca ses kaydı | elle 3–5 Whisper varyantı + uzlaşı (`~/.cache/medsor-kd-ses`) | Drive `Kurul N/Hoca_Ses/` → `hoca_dokum.py` (faster-whisper CPU, gece) → döküm ↔ sayfa hizalama (`pdf_hizala` yöntemi) → "önemli/dikkat/sınavda" cümleleri `hoca_ses[]` (zaman damgası + alıntı) |
| Kazanım / müfredat | `isle.py` eşleşmesi | sayfa başına kazanım kimliği |

- Kurallar: hoca ↔ PDF çelişkisinde **PDF esas** (k1-64 kararı), çelişki raporlanır. Kırmızı vurgu yalnız öğrenci notu
  ya da hoca kaydı dayanaklıdır (H22: asılsız "hoca vurguladı" yok). Öğrenci notunun yorumu H23'e uyar.
- Yeni L1 verisi gelince yalnız o sayfanın `l1/<p>.json`'ı değişir; karma değişen sayfaya dokunan L2 parçaları kirlenir (§2.5).

### 2.4 L2 — anlatı, çizim ve soru

`konusma_v2.json` (H12/H22 kapılı, cümle kimlikli) temel kalır. Eklenenler:
- `cizim[]`: cümle/kelime kimliğine bağlı çizim komutları (§4).
- `parca_sorulari[]`: her mantıksal parça (bölüm `-b03`) için 1–6 soru (§3.2).
- Her parça `girdi_sha` taşır = L0 sayfa karmaları + L1 yama karmaları + talimat sürümü.

### 2.5 Delta motoru (ne değişince ne yeniden üretilir)

| Değişen | Yeniden üretilen | Üretilmeyen |
|---|---|---|
| PDF yeni sürüm (3 sayfa eklendi) | yalnız yeni sayfaların L0'ı; o sayfalara düşen L2 parçaları; çapa yalnız etkilenen paragraflar | eşleşen sayfaların OCR/ROI/betimlemesi |
| Yeni öğrenci notu / hoca kaydı | ilgili sayfaların L1'i → vurgular; anlatım yalnız `--anlatim-guncelle` istenirse | L0, ses |
| Yeni çıkmış soru | L1 çıkmış bağı + önem puanı + yeşil vurgular + çözücüye ekleme | anlatım ve ses (sayfa önemi eşik aşmadıkça) |
| "Burayı daha kısa/detaylı anlat" (panel komutu, parça kimliğiyle) | o parçanın L2 metni → yalnız o parçanın EMA klipleri → kelime/cümle zamanı → çapa | diğer parçalar |
| Okunuş sözlüğü değişikliği | yalnız etkilenen sözcüğü içeren klipler (klip özetinde `okunus` karması — `sayi_imi` gibi) | metin |
| Talimat/şema sürümü | `surum` artışıyla işaretlenen ürünler, gece kotası içinde sırayla | — |

Uygulama: `otomasyon/delta.py` karmaları karşılaştırır, kirli parçaları `hat.json` aşamalarına iş olarak verir.
Ses tarafı zaten klip özetiyle artımlı (yalnız değişen klip); metin tarafı bu motorla parça düzeyine iner.

---

## 3. Soru katmanı

### 3.1 Kaynak kuralları (değişmez)

AGENTS.md Kural 4 (yalnız ders notu/PDF bilgisi), Kural 7 (geriye dönük bilgi, ileri sızıntı yok), Kural 6 (Öğren
destesinde soru gösterimi yok) ve şık açıklama standardı geçerlidir. Parça sorusu yalnız o parçaya kadar anlatılanı sorar.

### 3.2 Parça başı 1–6 soru (sesli ders)

- Sayı kuralı (betik): `min(6, max(1, round(parça_önem/20) + çıkmış_bağ_sayısı))`; çıkmışı olan parçada önce çıkmışlar.
- Öncelik: **çıkmış** (yeşil bağlı) → **mevcut çözücü / örnek soru** (zaten denetimli, kimlikli) → **yeni üretim** (Ü yazar,
  farklı aile denetçi). Yani soru çoğu parçada **hiç üretilmez, eşlenir**.
- Her soru `bagli_cumle: k2-07-c0142` taşır → "Anlatıldığı yere git" ve ses zamanı bundan türetilir (ms elle yazılmaz).
- Ekran: sesli derste parça sonu kartı (Öğren destesinden ayrı ürün — Kural 6 Öğren destesine özgüdür).

---

## 4. Canlı çizim ve simülasyon motoru

### 4.1 Zaman bağı: kelime kimliği, milisaniye değil

Önerideki `start_ms/end_ms` alanları ses varyantı değişince (yeni EMA, okunuş düzeltmesi) bozulur. Bu projede
çizim komutları **cümle kimliği + kelime sırasına** bağlanır; milisaniye istemcide `kelime_zaman` dosyasından o anki
varyant için hesaplanır (H12: türev veri metnin aynı sürümünden — `metinHash` kapısı zaten var).

```json
{"id": "k2-07-c0142-z1", "tur": "egri_faz", "hedef": "k2-07-p12-g1-r1",
 "bas": {"cumle": "k2-07-c0142", "kelime": 4}, "son": {"cumle": "k2-07-c0143", "kelime": 9},
 "fazlar": [{"nokta": [1, 2], "faz": "yukselis"}, {"nokta": [2, 3], "faz": "inis"}]}
```

### 4.2 Dört kip

| Kip | Girdi (L0) | Çizim (ön yüz) | Yedek |
|---|---|---|---|
| **kontur** (radyolojik/histolojik hat) | ROI `nokta[]` | Catmull-Rom eğrisi, `stroke-dashoffset` ile kalem darbesi | mevcut halka (elips) |
| **akis** (enzim/reseptör/yolak) | iki ROI (kaynak → hedef) | ok + parçacık akışı (SVG `offset-path`) | düz ok |
| **egri_faz** (EKG, aksiyon potansiyeli, spirometri) | `egri` ROI nokta dizisi | yükseliş sıcak renk, iniş soğuk renk iz sürme | eğri boyunca imleç (`yol`) |
| **sema** (görselsiz slayt) | — (L2 DSL) | yarı saydam katmanda adım adım düğüm/ok (`──►` aktivasyon, `──┤` inhibisyon) | madde listesi vurgusu |

- Ön yüz: `PdfDocView` üstünde tek SVG katmanı (mevcut `.pdv-not` ve imleç katmanlarıyla aynı koordinat sistemi).
  `prefers-reduced-motion`'da çizimler anında tam görünür. Telefonda tuval/GPU bellek kuralları (2026-10-22 simsiyah ekran
  düzeltmesi) korunur: SVG yalnız görünen sayfada, komut sayısı sayfa başına tavanlı.
- Ses yoksa (çevrimdışı metin kipi) çizim cümle tıklamasıyla oynar.

### 4.3 Kapılar (`cizim_dogrula.py`)

- ROI kutusu kendi resim kutusunun içinde; `nokta[]` ROI içinde ve sıralı; `egri` noktaları sayfa görüntüsünde koyu
  piksel üstünde (≥%70) — Ü görsel modelinin uydurduğu koordinat elenir.
- Komut aralığı geçerli cümle/kelime kimliğine düşer; aynı anda en çok 2 çizim; `sema` düğümlerinin her terimi o parçanın
  anlatımında geçer (ileri sızıntı yok, Kural 7).
- Geçmeyen komut **atılır, yedek kip kullanılır** — ders yayından kalmaz (çizim zenginleştirmedir, içerik değildir).

### 4.4 Şema DSL'i (görselsiz slayt)

`{"dugum": [{"id": "n1", "metin": "…", "cumle": "k2-07-c0150"}], "kenar": [{"a": "n1", "b": "n2", "tur": "aktive|inhibe|donusur"}]}`
— düzen istemcide (katmanlı yerleşim, elle koordinat yok), en çok 8 düğüm. Ü yazar; terim/sızıntı kapısı betikte.

---

## 5. Renk ve işaret sistemi

| Katman | Dayanak | Ön yüz jetonu | Bugün |
|---|---|---|---|
| **Yeşil** — çıkmış | L1 `cikmis[]` (kelime aralığı + soru kimlikleri) | `--isaret-cikmis` + "Çıkmışı göster" rozeti | vurgu `c` (sesli ders), "sınavda çıktı" rozetleri |
| **Kırmızı** — öğrenci notu / hoca | L1 `ogrenci_not[]`, `hoca_ses[]` | `--isaret-not` (+ ★, alıntı + zaman balonu) | `.pdv-not` kırmızı marker |
| **Mavi açık** — okunan paragraf/blok | çapa | `--isaret-odak` | var |
| **Mavi koyu** — okunan cümle/kelime | kelime zamanı | `--isaret-aktif` | var |
| **Mor kesikli** — kişisel zayıf nokta | öğrencinin yanlış/emin değilim cevapları (§13) | `--isaret-zayif` (kesikli çerçeve, dolgu yok) | yok |

- Renkler sabit RGBA değil, **palet jetonu** (`palettes.ts` tek kaynak, 3 tema × 4 palet; mevcut kontrast kapısı).
- Slayt zemini L0 `parlaklik` sınıfına göre jetonun "açık zemin / koyu zemin / renkli zemin" türevi seçilir; türevler
  derlemede kontrast kapısından (≥3:1 vurgu–zemin, metin okunurluğu bozulmadan) geçer — çalışma anında hesap yok.
- Renk tek başına anlam taşımaz: yeşilde rozet, kırmızıda ★ simgesi, morda kesikli çizgi (renk körlüğü).
- Parlaklık doğru hesaplanır: sRGB değerleri önce doğrusallaştırılır (WCAG bağıl ışıklılık), ortalama **işaretin düşeceği
  metin kutusunun** çevresinden alınır (tüm sayfadan değil — beyaz slaytta koyu röntgen kutusu ayrı sınıf alır). Eşik ve
  sınıf L0'a yazılır (`kutu.zemin: acik|koyu|renkli`); RGBA değerleri koda gömülmez, palet jetonu türevidir.

---

## 6. Tekil ders paketi (`.medspak`)

- **Rol:** türetilmiş, sürümlü **dışa aktarım ve çevrimdışı taşıma** biçimi. Doğruluk kaynağı değişmez: dosyalar +
  meds-pg (`interactive_learning_decks.json`, `konusma_v2`, …). Paket her yayından sonra betikle yeniden üretilir; elle yazılmaz
  (Kural 5'teki dışa aktarım paketleriyle aynı ilke).
- **Biçim:** SQLite (tek dosya, parça düzeyinde güncellenebilir, `sqlite3`/`sql.js` ile okunur).
  Tablolar: `meta(anahtar, deger)` (`surum`, `ders_id`, `kurul`, `kaynak_sha`, `uretildi`), `sayfa` (L0), `yama` (L1),
  `cumle` (L2: kimlik, ekran, ses, vurgu, çapa), `cizim`, `soru` (çıkmış + parça + çözücü; kimlik, `bagli_cumle`),
  `ses_parca` (varyant, paragraf, Opus blob, kelime zamanı), `ek` (isteğe bağlı: ham PDF, öğrenci PDF'i, hoca dökümü).
- **Ses biçimi:** paket içinde Opus (≈%40 küçük). Site bugünkü MP3'leri sunmayı sürdürür; Opus yalnız pakette, Safari
  uyumu sınandıktan sonra sitede de seçenek olur.
- **Üretim:** `scripts/paket/medspak_uret.py <ders_id> [--ekler]` → `meds_export/medspak/<ders_id>.medspak`; kapı
  `medspak_dogrula.py` (her kimlik çözülür, ses/kelime zamanı `metinHash` tutarlı, boyut tavanı).
- **Okuyucu:** önce web uygulamasının çevrimdışı motoruna uyarlayıcı (`paketMotoru.ts` yeni tür `medspak:<ders>`),
  sql.js tembel yüklenir. Bağımsız masaüstü/mobil okuyucu ancak web uyarlayıcısı oturduktan sonra değerlendirilir.
- **Gizlilik:** öğrenci PDF'i ve hoca kaydı paket eklerine yalnız yönetici dışa aktarımında girer; öğrenci indirmesinde yok.

---

## 7. Ses: EMA, okunuş, duraklama

- **Donanım:** `meds-ema` zaten "koruyucu etkinse GPU, değilse CPU". v3 eki: CUDA OOM / sürücü hatası → o iş parçası
  kuyruğa geri, süreç CPU kipinde yeniden başlar (XTTS işçisindeki davranışla aynı), panoda "CPU'ya düştü" sayacı.
  GPU kuralları (AGENTS.md 10, %60, ısı protokolü) değişmez.
- **Tek okunuş sözlüğü:** `okunus.py` (kısaltma bitişik okunuş, `SAYI_TTS`), `yazim_sozlugu.py` (ekran), `modul_okunus.py`
  dağınık listeleri `src/data/sesli_anlatim/okunus_sozlugu.json`'da birleşir: `{yazim, okunus, tur: kisaltma|latince|ingilizce|birim, kaynak}`
  (ör. `mmHg → milimetre cıva`, `Staphylococcus aureus → stafilokokus aureus`, `pacemaker → peysmeykır`).
  Kısaltma kuralı H3 kararına bağlı kalır (uzun harf okunuşu; kelime gibi okunan yerleşik kısaltmalar listede açıkça).
  Yeni aday: B çıkarır (büyük harfli, kaynakta sık) → Ü okunuş önerir → `okunus_denet.py` kapısı → sözlüğe.
- **Noktalama temizliği:** `ses` metninden `: ; ( ) [ ] / * > →` çıkarılır, anlamı virgül/nokta ile kurulur; EMA SSML
  bilmediği için duraklama **cümle bölmesi + işçide sessizlik ekleme** ile yapılır (`<dur:200>` işareti yalnız işçiye
  giden metinde, ekrana ve kelime sayımına girmez — kelime zamanı bölmesi `/\S+/g` ile birebir kalmalı).
- **Hizalama:** `kelime_zaman.py` + `cumle_zaman.py` (mevcut). Ek sağlama: `metinHash` tutmayan türev veri kullanılmaz (H12).

---

## 8. Drive ve kurul akışı

- **Klasör sözleşmesi** (Drive, her kurul): `Kurul N/` ders PDF'leri (mevcut), `Kurul N/Ogrenci_Notu/`, `Kurul N/Hoca_Ses/`
  (m4a/mp3; dosya adı ders adı ya da defter kodu `2f01`). `izle.py` üç türü ayrı kuyruğa yazar; ders eşleşmesi defterden.
- **Anında tetik:** Oracle'da Drive `changes.watch` bildirim ucu (HTTPS, kanal ~7 günde yenilenir, `meds-drive-kanal.timer`);
  bildirim gelince tarama hemen koşar. Bildirim düşerse 50 dk tarama yedek olarak sürer (sessiz kaçırma yok).
- **Kurul durumları:** `aktif` (derleme kipi: tüm hat), `arsiv` (yalnız düzeltme; otomatik toplu müdahale yok — El kitabı §0.4),
  `gelecek` (defter + takvim hazır, içerik yok). Durum takvimden türetilir; ayrı alan tutulmaz.
- **Arşiv "hızlı tekrar" görünümü** (`/gecmis-kurullar` içinde, site haritası kural 16'ya göre `/dersler/.../kurul1/...`):
  ders başına sesli ders + çözücü (çıkmış + örnek) + yeşil/kırmızı vurgulu slayt tarama + konu araması — yeni veri değil,
  mevcut ürünlerin tek ekranda toplanması.

---

## 9. Okuyucu (mevcut ekranlar üzerine)

1. **Sesli ders kipi** (canlı ders): yeşil vurguda "Çıkmışı göster" → ses durur, çıkmış soru penceresi (`/api/k/<soru>`),
   kapanınca aynı kelimeden sürer. Alt panelde katman düğmeleri: öğrenci notu, hoca alıntıları, çizimler.
2. **Parça sonu soruları** (§3.2): bölüm bitince 1–6 soru; yanlışta "Bu parçayı tekrar dinle".
3. **Soru çözücü:** "Sadece çıkmış / Sadece örnek / Karma" süzgeci; her soruda "Anlatıldığı yere git" → `/k/<bagli_cumle>`
   (sesli ders o cümleye kayar ve oradan çalar — altyapısı §11/§12 GELECEK_PLANLAMASI'nda kuruldu), "Teste dön" geri yığını.

---

## 10. Yol haritası (R0–R7)

Her adım `hat.json`'a aşama olarak girer, kapısı olmadan yayın yok, Kurul 1 verisine toplu müdahale yok. Sıra, kullanıcının
"önce betikleştir, her LLM yapabilsin" şartına göre: **önce sözleşme ve derleyiciler, sonra model değişimi**.

| Adım | İş | Bitti ölçütü |
|---|---|---|
| **R0 — Sözleşme** | `otomasyon/gorev.py` (hazirla/calistir/derle/dogrula/uygula), paket biçimi, ortak kural parçaları, `gorevler.json`, yönlendirici + bütçe + önbellek, `--katman elle` (§14, §1.2) | 3 görev türü (`parca_sorusu`, `okunus_oner`, `denetim`) K1 sınama verisiyle gidiş-dönüş sınamasından geçer; aynı paket Claude, Gemini ve Groq'ta derlenebilir cevap üretir |
| **R1 — L0 kroki** | birleşik L0, sayfa izi + eşleme, bölge düzeyi OCR, `pdf_isaret` L0'dan; §12.1 betikleri (öğrenci notu hizalı fark, eğri iskeleti, ok, kontur, SoM kopyası) | 3 sayfa eklenmiş PDF'te yalnız 3 sayfa okunur; K1 öğrenci notlarında hizalı fark elle sonuçla örtüşür (k1-51 kayık notu reddedilir) |
| **R2 — Hedefli çıkmış + kanıt bölgeleri** | çıkmış dizini, tarama planı, ters yön (§15); kanıt bağı + kapı + tekrar sunumu (§16) | 5 K2 dersinde hedefli tarama kaçan bağ 0; K1 çözücü sorularının ≥%90'ı `kesin` bölge alır, örneklem denetiminde yanlış bölge 0 |
| **R3 — Gölge kipi** | Claude hattı yayına devam eder; aynı dersler görev sözleşmesiyle Ü'de paralel üretilir, yalnız kapı sonucu ve denetçi bulgusu kaydedilir | 5 K2 dersinde Ü kapı geçme oranı ve bulgu türleri panoda |
| **R4 — Görev görev geçiş** | önce düşük risk (okunuş, parça sorusu, kanıt bağı, şablon etkileşimler, spot), sonra makro harita + bölüm anlatımı (§17.2) + kapsam denetimi (§17.3) + çeldirici (§17.4); Claude yalnız yüksek risk ve örneklem | ders başı Claude çağrısı ≤1; kapı hata oranı Claude dönemiyle aynı ya da düşük |
| **R5 — L1 akışları + delta** | Drive `Ogrenci_Notu/`, `Hoca_Ses/`, `changes.watch`; hoca dökümü + kalıp avı; delta motoru, panelde "bu parçayı kısalt/detaylandır" | yeni not/kayıt/çıkmış yalnız etkilenen sayfa ve parçaları yeniden üretir |
| **R6 — Ses + çizim + öğrenci özellikleri** | cümle ses önbelleği + VAD (DSP A/B), çizim motoru (eğri fazı, kontur, akış, şema), zayıf nokta katmanı, akıllı hız, görsel atlas, karşılaştırma paneli, etimoloji, tek tıkla kart (§12.4, §4, §13, §18) | 3 K2 dersinde çizim kapısı 0 HATA, telefonda kare süresi bozulmaz; her özellik çevrimdışında çalışır |
| **R7 — Paket** | `.medspak` üretici + doğrulayıcı + çevrimdışı uyarlayıcı; Opus sınaması (§6) | bir ders paketi internetsiz açılır, tüm kimlikler çözülür |

**R0 durumu (2026-10-23): kuruldu.** `otomasyon/gorev.py` + `otomasyon/llm/` (çekirdek, yönlendirici, bütçe, önbellek, kural
parçaları, `parca_sorusu` / `sik_aciklama` / `denetim`, öz-sınama `gorev_sinama` gece aşaması). Ölçüm (K1, sınama klasörüne,
canlıya yazılmadı): `parca_sorusu k1-03-b02` Gemini ilk turda 0 HATA, Groq bağımsız denetim `gecer`; `sik_aciklama
k1-03-…-q01` mevcut açıklama kapıdan geçemedi → Gemini 2. turda 0 HATA; elle kip ve Claude katmanı (araçsız `claude -p`) sınandı.
Yan bulgular düzeltildi: H25 (Claude CLI yolu), H26 (Gemini düşünme payı / sessiz boş yanıt). Açık: mevcut zincirlerin sözleşmeye
taşınması (R3), panel görünümü, gece hattında yönlendiricili üretim.

**R1 + R2 durumu (2026-10-23): kuruldu, K1'de ölçüldü** (işletim: El kitabı §16; gece aşaması `kroki`).
| Parça | Ölçüm (Kurul 1, canlıya yazılmadı) |
|---|---|
| L0 kroki | 64 dersin 62'si (2 eksik kaynak: k1-06 PDF Drive'da yok; k1-47 depo metni geçen yılın PDF'i — içerik doğrulaması eşlemeyi reddetti), 1.211 resim OCR'ı yalnız metinsiz resimde, ilk kurulum ~16 dk, artımlı koşu saniyeler, toplam 15 MB |
| Sayfa izi / kayma | 3 sayfa eklenmiş + 1 değişmiş + 1 silinmiş PDF: 36 aynı / 1 değişmiş / 3 yeni — hepsi doğru, OCR tekrarı 0, 32 takma ad |
| Öğrenci notu (hizalı fark) | mevcut 6 dersle sözcük uyumu 0,91–1,00; yapay 7 px + %1,5 kaymada hizasız 14 yanlış parça, hizalı 0; kayık derste 5 sayfa yazılmadı |
| Eğri | yapay EKG: ortalama hata 0,8 px, R tepeleri 2/2, QRS yükseliş/iniş doğru; yazı bloğu ve logo reddedildi (tekillik kapısı) |
| Ok | vektör çizimden; k1-12 araşidonik asit şeması: çizgi oklarında 11 bağın 10'u doğru (⊣ dahil); blok oklar düşük güven |
| SoM | 62 derste 8.802 bölge; numaralı kopyalar `meds_temp/kroki/<ders>/som/` (bitişik şekiller tek bölgeye birleşebiliyor) |
| Çıkmış dizini | 5.942 Dönem 3 sorusu, 4.969 aile, 2.896 varlık; ilk vektörleme 40 dk (vektör servisi 2 CPU kotalı), sonra yalnız yeni soru |
| Tarama planı | ders başına havuzun %5–15'i aday; **konu kilidi** (sorunun kayıtlı konusu = ders defteri konusu; K1 1.463/1.707, K2 571/571) + konusu tanınmayanlarda TEK DERS kuralı (yedek yol 26 sorunun 24'ünü doğru derse); elle atamayla duyarlılık %83,5 — "kaçan"ların incelemesi elle atamanın eksik/yanlış olduğunu gösterdi (k1-46 listesine cinsel yolla bulaşan enfeksiyon soruları karışmış) |
| Kanıt bölgeleri | 5.297 örnek soru (elle konan kanıt sayfası ölçüt): `kesin` %69 → kabul %96,0; **TEKRAR katmanı** (otomatik sunulan) %33 → kabul %98,8. Kurallar ablasyonla seçildi: başlık birimi kesin olamaz, olumsuz kök en çok olası, şekil/tablo atfı → şeklin sayfası, ikinci sinyal (bge-m3 en iyi 2 sayfa) |
Bilinçli sınırlar: birim düzeyinde sinir ağı vektörü yok (servis kotası; TF-IDF + sözcüksel şart); `pdf_isaret.py` henüz L0'dan okumuyor (canlı betik, ayrı adım); resim içi (raster) oklar yok; SoM'da bitişik şekiller birleşebilir.

**R3 + R4 durumu (2026-10-23): kuruldu** (işletim: El kitabı §17; gece aşamaları `golge`, `gorev_gece`).
| Parça | Ölçüm (Kurul 1; ücretsiz katman, Claude yok) |
|---|---|
| `kanit_bagla` (6'lık parti, kısmi kabul) | gölge 32 parti: kapı %97, ortalama 1,17 tur; elle kanıt sayfasıyla ham uyum %89 — uyumsuzlukların incelenmesinde yarısı modelin doğru seçimi (özet slaytı ↔ tanım maddesi); gerçek hata türü "hedefler/içerik" gündem sayfaları → bu sayfalar aday dışı bırakıldı. k1-12'de gece politikası: 2 parti → 10 karar uygulandı, tekrar kartı 49 → 52 |
| `som_sec` (Gemini görsel, numara seçimi) | 5 elle doğrulanmış sorgunun 4'ü doğru numara, 1'i "yok" (yanlış numara 0) |
| `sik_aciklama` / `parca_sorusu` | gölge: kapı %100; bağımsız denetim "kaynak dışı" buldu → parça sorusunda tüm şıklar ders kavramı olmalı (betik kapısı), şık açıklamasında kaynak dışı kimlik cümlesi engel değil (standart §3) — `denetim_engelleyen` |
| Betik kanıt (R2 iyileştirmesi) | uzun bloklar maddelere bölündü (bölge ≤ 8 satır): kesin %71 / kabul %96,4; TEKRAR katmanı %34 / kabul %99,0 |
Yan bulgular düzeltildi: H27 (cloud_llm bir 400 + geçersiz anahtarla gpt-oss-120b'yi bütün gün "kota dolu" işaretliyordu; tek anahtarın 401'i modeli atlatıyordu). Açık (kullanıcı): `.env` `GROQ_API_KEY_2` geçersiz.

**R4 — önem listesi + soru çözücü görev yolu (2026-10-23): kuruldu, `mod: golge`** (El kitabı §18). `onem_listesi` (sayfa grubu),
`cozucu_sorusu` (4'lük parti), `spot_birlestir.py` (ders düzeyi kurallar betikle), `spot_zinciri.py`; ders zinciri `mod` anahtarıyla
görev yolunu (aktif) ya da Claude + gölge kıyasını (golge) çalıştırır. K1 e07'de çözücü tamamen ücretsiz katmanla 0 HATA; önem
listesi yeni kapılarla Claude yedeğine 3 çağrı düştü (ders başına önceki ~2 uzun Claude oturumu yerine). Geçiş kararı için gölge
kayıtlarında ≥5 Kurul 2 dersi önerilir.

Açık R4 işleri (sıradaki): kalan Claude adımlarını (asistan, sesli metin v2, çapa, bağımsız denetim) görev paketlerine çevirmek —
her biri `gorevler.json` kaydı + modül + kapı + `sinama_ornekleri` + gölge örneklemi; eşik aşılınca kullanıcı onayıyla devir.
Kurul 2 PDF'leri gelmeden Claude zinciri çalışmadığı için şu an harcanan Claude kotası yok. R1 ve R2 R0'dan bağımsız
betik işleridir ve paralel yürüyebilir (aynı dosyalara dokunmazlar).

## 11. Bilinçli olarak yapılmayanlar / riskler

- Yerel LLM, CUDA'lı eğitim, LoRA: yok (AGENTS.md 10).
- Milisaniyelik eşzamanlama Whisper hizalamasının doğruluğuyla sınırlıdır (~50–150 ms); hedef "algılanmayan gecikme",
  ölçüm `kelime_zaman` sınama seti.
- Görsel modelin koordinatları güvenilmez → her ROI betik kapısından geçer; geçmeyen çizim yedek kipe düşer.
- Ücretsiz kotalar değişebilir: zincir sırası `.env` (`MEDS_CLOUD_CHAIN`) ile değişir, kod değişmez; kota bitince iş
  ertelenir, kalitesiz yayın yapılmaz.
- `.medspak` doğruluk kaynağı olmaz; iki kaynak tutarsızlığı riski bu yüzden yok.

---

## 12. Sıfır-token betik kataloğu (kullanıcı eki 2026-10-23)

En ağır işler LLM'e de GPU'ya da gitmez; klasik görüntü işleme, vektör çarpımı ve dizi hizalamayla çözülür. Ortam:
`meds/.venv-ocr` (OpenCV, SciPy, RapidFuzz, NetworkX, NumPy, PyMuPDF **kurulu**; scikit-image, librosa, webrtcvad
**eklenecek** — hepsi CPU, `CUDA_VISIBLE_DEVICES=""`). Her betik B katmanıdır: çıktısı kapıdan geçerse model çağrılmaz.

### 12.1 Görüntü işleme (L0 / L1)

| İş | Yöntem | Bugün | Uyarlama / kapı |
|---|---|---|---|
| **Öğrenci notu işaretleri** | ham sayfa ↔ not sayfası **önce hizalanır** (`cv2.findTransformECC` ya da ORB + homografi), sonra `absdiff` → HSV renk süzgeci → bağlı bileşen kutuları → L0 kelime kutularıyla **IoU** (≥0,3 fosforlu, alt çizgi için kutunun alt bandı) | `ogrenci_not_isaret.py` piksel farkı + kelime çakışması (hizalama yok) | k1-51 tuzağı (kayık not PDF'i yanlış satır üretti) hizalama adımıyla kapanır; hizalama hatası > 3 px ya da eşleşen kelime < %20 → yazılmaz + bildirim. Sonuç L1 `ogrenci_not[]` |
| **EKG / aksiyon potansiyeli / spirometri eğrisi** | ızgara rengi HSV ile silinir → eşik → `skeletonize` → soldan sağa (x, y) dizisi → yumuşatma → `scipy.signal.find_peaks` (tepe + çukur) → türev işaretine göre `yukselis` / `inis` dilimleri | yok | ROI `tur: egri`, `nokta[]` seyreltilmiş (≤200). Kapı: noktaların ≥%90'ı koyu piksel üstünde, x tekdüze artar. Hangi fazın anlatıldığını cümledeki terim belirler ("depolarizasyon" → yükseliş) — kural sözlüğü, gerekirse Ü |
| **Yolak okları** (`──►`, `──┤`) | `HoughLinesP` + `approxPolyDP` uç (üçgen = aktivasyon, dik çizgi = inhibisyon) → kuyruk ve uca en yakın L0 metin kutusu | yok | kenar `{a: terim, b: terim, tur}` L0 `ok[]`. Konuşmada iki terim aynı cümlede geçince `akis` çizimi kendiliğinden (B üretir, LLM yok) |
| **Kontur** (fissür, opasite, histolojik sınır) | ROI içinde Canny + en uzun kontur (`findContours`), Catmull-Rom için seyreltme | yok | yalnız ROI bilinen bir resim kutusunda ve konuşmada ROI etiketi geçiyorsa; yoksa mevcut halka |
| **Görsel kapatma** (resim içi etiketler) | ROI/resim kutusu içinde kalan L0 kelimeleri → maske listesi | yok | Yeni ürün "Görsel ezber" (sesli ders + slayt tarama ekranında, Öğren destesi değil). Öğren destesine girerse `OGREN_ETKILESIM_REHBERI.md` ve kronoloji kuralı geçerli |
| **Sayfa izi** | metin SimHash + görsel pHash (DCT, NumPy ile; `imagehash` gerekmez) | yok | §2.2 |
| **Zemin parlaklığı** | metin kutusu çevresi, doğrusal sRGB → bağıl ışıklılık | yok | §5 |

### 12.2 Eşleme ve hizalama (L1)

| İş | Yöntem | Bugün | Uyarlama |
|---|---|---|---|
| Çıkmış → slayt **cümlesi** (yeşil) | bge-m3 (CPU :8094) kosinüs + BM25, sayfa adayından cümleye iniş, kelime aralığı `pdf_isaret` LCS ile | sayfa düzeyi (`onem_haritasi.py`) | çıkmış vektörleri bir kez hesaplanır, `l1/vektor_onbellek` (karma anahtarlı); eşik altı → bağ yok (zorla yeşil yok) |
| Hoca kaydı → slayt zaman çizelgesi | faster-whisper (CPU) döküm → `pdf_hizala` sıra korumalı DP + RapidFuzz kayan pencere | elle (k1-64, k1-51) | §2.3 `hoca_dokum.py` |
| Hoca vurgusu (kırmızı) | dökümde kalıp avı ("sınavda çıkar", "önemli", "yıldız", "sorarım", "dikkat", "mutlaka") **zorunlu**; ses enerjisi / perde yükselişi (librosa RMS + f0) yalnız **aday puanı** | elle | H22: yalnız akustik iz kırmızı yapmaz (asılsız vurgu olur); kalıp + o anki slayt cümlesi şart, alıntı ve zaman damgası saklanır |
| Görselsiz slayt şeması | metindeki `→ ↑ ↓ ⊣` sembolleri ve "uyarır/baskılar/dönüştürür" kalıpları → NetworkX çizgesi; ön yüzde katmanlı yerleşim (dagre/elkjs, paket eklenmeden önce boyut ölçülür) | yok | LLM yalnız sembol yoksa ve yalnız `A -> B (uyarır)` satırları yazar (§4.4 DSL) |

### 12.3 Sıfır-token öğrenme malzemesi

- **Boşluk doldurma (yeşil/kırmızı cümlelerden):** sayı + birim, ilaç/enzim/gen (sözlük `t-<slug>`), kranial sinir numarası,
  artar/azalır yönü maskelenir. Kapılar: Kural 8 (ipucu cevabı sızdırmaz — `validate_learning_decks.py` aynı işlevi),
  Kural 7 (yalnız o parçaya kadar anlatılan). Sesli ders parça sonu kartı ve slayt taramasında; Öğren destesine
  girecekse rehberdeki öge sayısı (4–6) ve tür dengesi uygulanır.
- **Görsel kapatma** (§12.1), **eşleme kartları** (tablolardan satır ↔ sütun), **sıralama** (numaralı madde/ok zinciri) —
  hepsi L0'dan; çeldirici ve açıklama gerekiyorsa Ü cilalar (şık açıklama standardı).

### 12.4 Ses (EMA) için betikler

| İş | Yöntem | Uyarlama |
|---|---|---|
| **Cümle düzeyi içerik adresli ses önbelleği** | `sha256(normalize(ses) + ses_kimligi + okunus_surumu + motor_surumu)` → `ses_onbellek/<sha>.wav`; yalnız yeni cümle sentezlenir, paragraf `ffmpeg concat` ile kurulur | Bugün klip özetiyle **paragraf** düzeyi artımlı. Cümle cümle sentezin tonlamayı bozup bozmadığı önce 3 derste A/B dinlenir (cümle sınırında doğal düşüş). Kazanç: cümle zamanları **ölçülerek** gelir → `cumle_zaman.py` tahmini gerekmez |
| **VAD kırpma** | dBFS eşiğiyle baş/son ölü sessizlik kırpılır, cümleler arası sabit doğal boşluk (≈120–180 ms; noktalama türüne göre) eklenir | webrtcvad şart değil (NumPy dBFS yeter). Kırpma kelime zamanından **önce**; zamanlama her zaman son sesten ölçülür (H12) |
| **DSP vurgusu** (çıkmış/hoca cümlesi) | önce 300–350 ms es, `atempo≈0,92`, hafif presence EQ | **Ayar, varsayılan kapalı**: "kısa ve öz" kuralı (H22, sesli ders kısa ve öz kararı) süreyi uzatmamayı ister; ders başına vurgulu cümle tavanı (%15). Açılırsa kelime zamanı DSP'den sonra ölçülür. Karar A/B dinlemesinden sonra kullanıcının |

### 12.5 Kısa kimlikli iskelet derleyici (LLM çıktısını küçültme)

- LLM'e giden paket: cümleler `S1…Sn`, maddeler `M1…`, resim/ROI `R1…`, çıkmışlar `Q1…` (mevcut çapa talimatının M#/R#
  yaklaşımının genellemesi). LLM yalnız metin + kısa etiket yazar: `… [CIZ:R2:egri] [ISARET:M3] [SORU:Q4]`.
- `otomasyon/llm/derle.py` etiketleri L0 kimliklerine (`k2-07-p12-g1-r2`), kelime aralıklarına ve çizim komutlarına çevirir;
  bilinmeyen etiket = kapı HATASI (model uydurduysa iş geri döner). Koordinat, renk, uzun JSON anahtarı hiçbir zaman
  model çıktısında yer almaz → çıktı belirteci ve hata oranı düşer; aynı derleyici Ü ve C çıktısına aynı uygulanır.

---

## 13. Kişisel zayıf nokta katmanı (kullanıcı eki 2026-10-23)

- **Veri:** öğrencinin cevabı (çözücü, çıkmış, parça sonu soruları, olası sorular) zaten soru kimliği taşır; soru →
  `bagli_cumle` (§3.2) → çapa → slayt kutusu. Kayıt cihazda `medsoru_zayif_v1` = `{cumle_id: {yanlis, emin_degil, dogru_sonra, son}}`;
  **`userKvSync` `SYNC_PATTERNS`'e eklenir** (yeni kişisel anahtar kuralı) → cihazlar arası eşitlenir, sunucuda `user_data`.
- **Puan:** yanlış +2, emin değilim +1, sonradan doğru −1 (en az 0); 21 günde yarılanır (aralıklı tekrar). Eşik üstü cümle
  slaytta **mor kesikli çerçeve** (§5), resim bölgesine bağlıysa ROI çerçevesi.
- **"Sadece yanlış yaptığım yerleri anlat":** puanı eşik üstü cümlelerden çalma listesi (kimlik sırasıyla, ders → bölüm);
  her cümlenin sesi ve kelime zamanı zaten var (cümle önbelleği §12.4 bunu kesintisiz yapar), aradaki bağlam için
  önceki cümle de çalınır. Liste bitince o cümlelerin soruları yeniden sorulur; doğru → puan düşer.
- **Ekranlar:** sesli ders katman düğmesi "Zayıf noktalarım"; Bitirdiklerim / 60 planında ders başına zayıf nokta sayısı;
  çevrimdışında da çalışır (veri cihazda).
- **Gizlilik:** zayıf nokta verisi kişiseldir; ücretsiz LLM katmanına ve `.medspak` öğrenci indirmesi dışındaki paketlere girmez.
  Yönetim › Kişiler'de yalnız toplu sayı (ders başına) görünür. Toplu (anonim) "en çok yanlış yapılan cümleler" önem
  haritasına ek sinyal olabilir — ayrı karar.

---

## 14. Görev sözleşmesi: her LLM'in yapabileceği kadar betikleştirilmiş hat (kullanıcı şartı 2026-10-23)

**İlke:** zekâ gerektiren kısım küçük, kapalı ve tanımlı bir **görev**dir; geri kalan her şey (veri toplama, bağlam kurma,
kimlik, koordinat, biçim, birleştirme, doğrulama, yayın) betiktir. LLM dosya sistemi, araç ya da proje bilgisi
gerektirmeden yalnız **tek bir görev paketini** okuyup **tek bir cevap** yazar. Bu yüzden aynı görev Claude, Gemini,
Groq, OpenRouter modeli ya da bir insanın web sohbetine kopyala-yapıştırla yapılabilir.

### 14.1 Dört komutlu tek arayüz (`otomasyon/gorev.py`)

```
python3 meds/otomasyon/gorev.py hazirla  <gorev> <hedef>   → is/<is_id>/paket.md + paket.json + sema.json   (ÇÖZÜCÜ / decompiler)
python3 meds/otomasyon/gorev.py calistir <is_id> [--katman B|Ü|C|elle]  → is/<is_id>/cevap.txt        (yönlendirici §1.2)
python3 meds/otomasyon/gorev.py derle    <is_id>            → is/<is_id>/cikti.json + derleme_raporu  (DERLEYİCİ / compiler)
python3 meds/otomasyon/gorev.py dogrula  <is_id>            → kapı raporu; 0 HATA ise "uygula" hakkı
python3 meds/otomasyon/gorev.py uygula   <is_id>            → L2'ye yazar (yedekli, geri alınır), delta motoruna haber verir
```
- `hedef` her zaman kimliktir: `k2-07` (ders), `k2-07-b03` (bölüm), `k2-07-p12` (sayfa), `k2-07-q05` (soru).
- Durumlar `is/<is_id>/durum.json`: `hazir → cevap_var → derlendi → dogrulandi → uygulandi | reddedildi(neden)`.
  Her adım yeniden çalıştırılabilir ve **idempotent**tir; yarıda kalan iş kaldığı yerden sürer.
- `--katman elle`: `paket.md` ekrana/dosyaya basılır, insan herhangi bir LLM'e yapıştırır, cevabı `cevap.txt`'ye koyar.
  Kota/servis yokken bile hat durmaz (son çare kip; panoda "elle bekliyor" listesi).

### 14.2 Görev paketi (`paket.md`) — modelden bağımsız biçim

Sabit bölümler, sabit sırayla: `# GÖREV` (tek paragraf amaç) · `# KURALLAR` (numaralı, en çok ~15; ortak kurallar
`otomasyon/llm/kurallar/*.md` parçalarından **betikle** eklenir: kaynak sadakati, Türkçe üslup, şık açıklama, H22…) ·
`# GİRDİ` (kısa kimlikli: `S1…` cümle/madde, `M1…` madde, `R1…` görsel bölge, `T1…` tablo, `Q1…` çıkmış, `K1…` kazanım) ·
`# BAĞLAM` (salt okunur: önceki parçanın özeti, sonraki parçanın başlıkları — §17.2) · `# ÇIKTI BİÇİMİ` (şema + 1 dolu örnek) ·
`# DENETİM LİSTESİ` (derleyicinin bakacağı maddeler; model kendini buna göre sınar).
- Paket boyu tavanlıdır (`girdi_sinir_kelime`, ücretsiz modellerin bağlamına göre; varsayılan ≈6.000 kelime); aşarsa çözücü
  görevi **bölüm** hedeflerine böler. Hiçbir görev "tüm dersi yaz" değildir.
- Çıktı biçimi iki türdür: **kısa etiketli düz metin** (anlatım: `S4 … [CIZ:R2:egri] [ISARET:M3]`) ya da **küçük JSON**
  (soru, kart, eşleme). Uzun anahtar, koordinat, renk, kimlik üretimi modelden istenmez.

### 14.3 Derleyici ve çözücü kuralları

- **Çözücü** (L0/L1/L2 → paket): kimlikleri kısa etiketlere çevirir ve eşlemeyi `paket.json`'a yazar
  (`{"S4": "k2-07-c0142", "R2": "k2-07-p12-g1-r2"}`). Aynı girdi → bayt bayt aynı paket (karma = önbellek anahtarı).
- **Derleyici** (cevap → L2): etiketleri geri çevirir, kelime aralıklarını ve çizim komutlarını kurar, `ekran`/`ses` iki
  yüzünü üretir (okunuş sözlüğü §7), kimlik verir (kalıcı kimlik kuralı). Bilinmeyen etiket, eksik zorunlu alan, şemaya
  uymayan değer = **derleme HATASI** (modelin uydurması yayına sızamaz).
- **Gidiş-dönüş sınaması:** `cozucu(derleyici(x))` mevcut L2 için aynı paketi vermelidir; her görev türünde örnek derslerle
  (`otomasyon/llm/sinama/`) birim sınaması — `hat.py --dogrula` bu sınamaları da koşar. Kurul 1'in mevcut çıktıları
  (K1 verisine yazmadan) sınama verisidir.
- **Kademeli onarım:** kapı hatası → yalnız hatalı birimler için **yama görevi** (`<gorev>.yama`: hatalı satırlar + hata
  listesi; tüm paket yeniden gönderilmez). En çok 2 yama turu, sonra bir üst katman (§1.2).

### 14.4 Görev kataloğu (ilk sürüm; her biri `gorevler.json` kaydı + paket şablonu + şema + derleyici + kapı)

| Görev | Hedef | Çıktı | Kapı |
|---|---|---|---|
| `makro_harita` | ders | bölümler (sayfa grupları), konu akışı, bölümler arası bağ | her sayfa tam bir bölümde; sıra bozulmaz |
| `anlatim` | bölüm | kısa etiketli anlatım | `konusma_v2 --dogrula`, kapsam (§17.3), H22, üslup |
| `anlatim.yama` | cümle kümesi | yalnız düzeltilen cümleler | aynı |
| `parca_sorusu` | bölüm | 1–6 soru JSON | şık açıklama, kronoloji, kanıt bölgesi (§16) |
| `kanit_bagla` | soru | doğru şıkkı destekleyen S/M etiketleri + kısa gerekçe | §16.2 |
| `som_sec` | görsel | anlatılan yapının SoM numarası (§17.1) | numara geçerli, konuşmada etiket terimi var |
| `karsilastirma_onayla` | ikili aday | eşleşen satırlar | §18.3 |
| `okunus_oner` | kısaltma listesi | okunuş | `okunus_denet.py` |
| `denetim` | herhangi `is_id` | bulgu listesi (satır etiketiyle) | rapor biçimi |
| Mevcutlar (onem, cozucu, asistan, hastalık, kamp, Son Prova, olası soru) | — | TALIMAT dosyaları pakete dönüştürülür | mevcut kapılar |

Yeni ürün eklemek = yeni görev kaydı + şablon + şema + derleyici + kapı + sınama verisi. Hattın geri kalanı değişmez.

---

## 15. Hedefli çıkmış taraması (her PDF neyi tarayacağını bilir) (kullanıcı şartı)

**Bugün:** `isle.py::cikmis_adaylari` her PDF için tüm havuzda (yalnız kurul süzgeciyle) 30 benzer soru sorgusu yapar;
ders zinciri `aday_hazirla.py` ile yeniden süzer. Yeni çıkmış eklenince **hiçbir PDF'in bağı güncellenmez** (ters yön yok).

### 15.1 Çıkmış dizini (bir kez, artımlı) — `scripts/cikmis_dizin/dizin.py`

Her tekil çıkmış (kopya ailesi tek kayıt, `tekrar_analizi` grupları) için bir kez:
`{id, aile, donem, kurul, brans, ders_kodu?, konu_kimligi?, yil, varliklar: [t-…, h-…, ilaç, gen, sayı+birim], kok_vektor (bge-m3),
dogru_sik_vektor, karma}` → `meds_database_v2/cikmis_dizin/` (+ meds-pg tablosu). Yeni/değişen soru yalnız kendi satırını
yeniden hesaplar. Ters dizinler: `varlik → [soru]`, `brans/konu → [soru]`.

### 15.2 PDF tarama planı (`l1/tarama_plani.json`)

PDF işlenirken, havuzu taramadan önce aday kümesi daraltılır:
1. **Kapsam süzgeci (kesin):** dönem 3; ders kayıt defterinden branş + konu kimliği; kurul eşlemesi **soru yılının
   müfredatına** göre (konular yıllar arasında kurul değiştirebilir — `cikmis_kurul` kuralı, prova bulgusu). Dönem
   karışması yasağı (PROJE_TANITIMI §5): başka dönemin sorusu hiç aday olmaz.
2. **Varlık kesişimi:** PDF'in L0 varlıkları ∩ soru varlıkları ≥ 1 (ya da konu kimliği eşit).
3. **Vektör sırası yalnız adaylarda:** kök + doğru şık ↔ sayfa/cümle vektörleri; eşik ve komşu sayfa kuralı (`onem_haritasi`).
4. Plan dosyası: `{pdf_sha, dizin_surumu, suzgec, aday_sayisi, bagli: [...], bagsiz: [...], neden}` — hangi soruların neden
   alındığı/alınmadığı görünür; aynı plan ve dizin sürümüyle tarama **tekrarlanmaz**.

### 15.3 Ters yön: yeni çıkmış hangi PDF'leri etkiler

Yeni çıkmış dizine girince: varlık + konu ters dizininden **etkilenebilecek dersler** bulunur → yalnız o derslerin L1
çıkmış yaması (cümle düzeyi, §12.2) yeniden kurulur → delta motoru (§2.5) önem/yeşil/çözücü/tekrar kartı işlerini
yalnız o dersler için açar. Kurul 1 dersleri yalnız **öneri** üretir (otomatik toplu müdahale yok).

### 15.4 Ölçüt
Bir PDF başına vektör karşılaştırması "tüm havuz" yerine "aday kümesi" (hedef: ≤ %10'u); kalibrasyon için ilk 5 K2
dersinde tam tarama ile hedefli tarama karşılaştırılır — **kaçan bağ sayısı 0** olmalı, değilse süzgeç gevşetilir.

---

## 16. Kanıt bölgeleri ve otomatik tekrar sunumu (kullanıcı şartı)

**Amaç:** her çıkmış ve örnek sorunun işaret ettiği bilginin slayttaki yeri kesin bilinsin; öğrenciye tekrar için o bölge
sunulsun — betik işi gibi otomatik ama **mantıksal/anlamsal kusursuz**.

### 16.1 Kanıt bağı veri modeli (L1 `kanit[]`)
`{soru, rol: dogru|celdirici|kok, hedef: [k2-07-p12 kelime aralığı | M3 | R2], cumle: [k2-07-c0142…], guven: kesin|olasi, yontem, kanit_metni}`
- `dogru`: doğru şıkkı destekleyen yer (zorunlu). `celdirici`: yanlış şıkkın **derste anlatıldığı** yer (ayırt etme için).
  `kok`: sorunun klinik/bağlam bilgisinin yeri.

### 16.2 Belirleme (önce betik, belirsizse görev)
1. Aday bölgeler: §15 planındaki sayfa → cümle/madde (bge-m3) → kelime aralığı (`pdf_isaret` LCS).
2. **Sözcüksel şart:** doğru şıkkın ana teriminin (ya da sözlükteki eşanlamlısının, `t-<slug>` "tamlama ≠ kavram" kuralıyla)
   bölgede geçmesi; sayı/birim soruyorsa sayının birebir geçmesi.
3. **Anlamsal şart:** bölge ↔ "kök + doğru şık" benzerliği eşik üstü **ve** aynı bölge ↔ çeldiricilerin en iyisi arasında fark
   ≥ δ (bölge doğru cevabı ayırt etmeli, yalnız konuyu değil).
4. İki şart da tutarsa `kesin` (betik). Biri tutarsa `kanit_bagla` görevi (§14.4) — model yalnız S/M etiketi seçer;
   farklı aile denetler. Hiçbiri tutmazsa bağ **yok**: soru "derste karşılığı bulunamadı" listesine (müfredat dışı ya da
   eşleme hatası; panoda) — zorla bölge gösterilmez.
5. Kapı (`kanit_dogrula.py`): bölge sorunun dersinde, soru dönem/kurul uyumlu, bölge silinmiş/değişmiş sayfada değil
   (sayfa izi), aynı bölgeye bağlı sorular birbiriyle çelişmiyor (aynı bölge iki farklı doğru cevabı desteklemiyor).

### 16.3 Tekrar sunumu (yeni LLM gerektirmez)
- **Ders sonu "sınava dönük tekrar":** `kesin` bölgeler önem puanı + soruldu sayısı sırasıyla; her kart = bölge görüntüsü
  (sayfa kırpması) + bağlı cümlelerin sesi + soru. Çeldirici bölgesi varsa yan yana ("bunu şununla karıştırma").
- **Çözücüde "Anlatıldığı yere git":** `dogru` bölgenin ilk cümlesi (§9).
- **Zayıf nokta katmanı (§13)** ve **akıllı hız (§18.1)** aynı bölge verisini kullanır.
- Hoca PDF'i güncellenince bölgeler sayfa izi ile taşınır; taşınamayan bölge `olasi`ya düşer ve yeniden belirlenir.

---

## 17. PDF'in en doğru işlenmesi için kalite mühendisliği (kullanıcı eki 2026-10-23)

### 17.1 Set-of-Mark (SoM) etiketleme
Görsel modele ham görüntü değil, §12.1'deki betiğin bulduğu bölgelerin üstüne **numara basılmış kopya** gönderilir
(`l0/som/<g>.webp`, numara ↔ ROI kimliği eşlemesi pakette). Model koordinat yazmaz; yalnız numara seçer (`som_sec` görevi).
Derleyici numarayı gerçek poligona çevirir. Böylece §1.3'teki "görsel adlandırma" görevi de SoM ile yapılır.

### 17.2 Önce makro harita, sonra pencereli mikro anlatım
1. `makro_harita` (düşük girdi: yalnız sayfa başlıkları, ilk satırlar, tablo/görsel listesi; çoğu derste `kapsam.py`
   başlık bölgesi + benzerlik kümesiyle **betikle** çıkar, model yalnız belirsiz sınırda) → bölümler ve "birbirinin devamı" grupları.
2. `anlatim` görevi bölüm bölüm; pakette `# BAĞLAM`: önceki bölümün 3–5 cümlelik özeti (önceki görevin çıktısından, betikle)
   + sonraki bölümün **yalnız başlıkları**. Kural: sonraki bölüme ön atıf yapılabilir ("bir sonraki bölümde göreceğiz"),
   ama henüz anlatılmayan bilgi açıklanmaz ve **etkileşim/soru öğelerine girmez** (Kural 7 kronoloji).

### 17.3 Sıfır kayıp kapsam denetimi (`kapsam_denetle.py`, deterministik)
- Her bölümün L0 metninden çıkar: sayı + birim, eşik ifadeleri (`>120 ms`, `%…`), büyük harfli kısaltmalar, sözlük
  terimleri/hastalıklar/ilaçlar/genler, tablo hücreleri, parantez içi bilgiler. Başlık/altbilgi/hoca adı/kaynakça
  (sayfalar arası tekrarlanan satırlar, `kapsam.py` UNVAN kuralı) **sayılmaz**.
- Anlatımın **`ekran`** yüzünde (rakamlı yazım; `ses` yüzü okunuşludur) her birinin geçip geçmediği bakılır (Türkçe katlama,
  5 harf kök, eşanlamlı sözlüğü). Eksikler → `anlatim.yama` görevi yalnız eksik ögelerle: "S7–S9'da şunlar eksik: […]".
- Eşik ürün türüne göre: **tam ders** = önem/çıkmış/hoca vurgulu ögelerin %100'ü + diğerlerinin ≥ %95'i; **sınav odaklı
  özet (V2)** = çıkmış bağlı + hoca/öğrenci vurgulu ögelerin %100'ü (H24: önemli yer atlanamaz), diğerleri serbest.
- Ters yön de denetlenir: anlatımdaki sayı/terim L0'da ya da kanıtlı referansta yoksa **uydurma şüphesi** (H10 kapısıyla birlikte).

### 17.4 Çeldirici tersine mühendisliği
- Pakete bölümle eşleşen çıkmışların (Q1…) doğru şıkkı **ve çeldiricileri** girer; çeldiricinin ders içindeki yeri (§16 `celdirici`
  bölgesi) varsa ayırt edici bilgi de.
- "Öğrencilerin en çok düştüğü" çeldirici yalnız gerçek veriden: çözücü/çıkmış cevap istatistiği (anonim toplam, en az n=20
  cevap). Yoksa yalnız "bu soruda şıklarda X de vardı" denir.
- H22 kuralı: "sınavda mutlaka şunu koyarlar" gibi genelleme yasak; yalnız gerçek çıkmışa dayanan "2024 sınavında şıklarda
  Bradikinin de vardı; o geç fazda etkilidir" biçimi. Ayırt edici bilgi PDF'te değilse anlatıma girmez.

### 17.5 Ok ve sembol açılımı (paket kuralı)
- Slayttaki `A → B`, `X ↑` zincirleri düz okunmaz; ilişki cümleyle kurulur. **Ama mekanizma yalnız PDF'te (ya da aynı dersin
  bilgi deposunda) yazanla açıklanır**; PDF mekanizmayı vermiyorsa ilişki olduğu gibi ve açıkça söylenir. Standart kaynakla
  tamamlama yalnız `kanit.referans` ile ve raporda listelenerek (El kitabı §0.1). Model uydurmasın diye kural pakete ve
  kapsam denetiminin ters yönüne (§17.3) bağlıdır.
- Her mekanizma cümlesi mümkünse bir görsel/tablo bölgesine `[CIZ:Rn:kip]` ile bağlanır; bağlanamıyorsa zorlanmaz.
- `ses` yüzünde sembol yok, kısaltma okunuşu sözlükten — bu derleyicinin işidir, modelin değil (§7, §14.3).

### 17.6 Uçtan uca akış (Drive → yayın)
```
Drive (PDF / Ogrenci_Notu / Hoca_Ses)
 → L0: PyMuPDF metin+kelime kutusu (OCR yalnız metinsiz resim/bölge) · OpenCV ROI/eğri/ok · SoM kopyası · sayfa izi   [B]
 → L1: hedefli çıkmış planı (§15) · kanıt bölgeleri (§16) · öğrenci notu hizalı fark · hoca dökümü + kalıp avı · kazanım [B, belirsizde Ü]
 → makro harita [B, belirsizde Ü] → bölüm bölüm anlatım + parça soruları [Ü yazar] → derleyici → kapsam/üslup/H22/kronoloji kapıları
   → eksikse yama görevi (≤2) → denetim [farklı aile Ü; yüksek riskte C]
 → okunuş + EMA (cümle önbelleği, VAD) → kelime/cümle zamanı → çapa → yayın → .medspak (türetilmiş)
```
Her ok bir `gorev.py` ya da `hat.json` aşamasıdır; her aşama tek başına yeniden çalıştırılabilir.

---

## 18. Sıfır maliyetli öğrenci özellikleri (kullanıcı eki 2026-10-23)

| # | Özellik | Veri | Uyarlama |
|---|---|---|---|
| 18.1 | **Akıllı hız**: normal cümle seçilen hızda (ör. 1,75×), yeşil/kırmızı cümlede 1,0×'a iner, bitince geri çıkar | cümle vurgusu + kelime zamanı | Kullanıcı ayarı (aç/kapa, iki hız); hız geçişi ≈150 ms yumuşak; `playbackRate` + `preservesPitch`. Kişisel zayıf nokta cümleleri de yavaşlatılabilir (§13) |
| 18.2 | **Görsel atlas**: yalnız resim ve tablolar art arda; her biri o görseli anlatan cümlelerin sesiyle | L0 resim/tablo + çapa (R#) + kelime zamanı | Anlatımı olmayan görsel sessiz gösterilir; kaydırma listesi sanallaştırılır (telefonda tuval/GPU belleği kuralları) |
| 18.3 | **Karşılaştırma yan paneli** (Tip 1 ↔ Tip 2): bir kavram dinlenirken karşıtının ilgili satırı | betik adayları: tablo sütunları, paralel başlıklar ("Tip 1/Tip 2", "akut/kronik"), zıt kalıplar (artar/azalır, erken/geç, var/yok) | Yanlış eşleşme öğrenciyi yanıltır → aday `karsilastirma_onayla` görevinden + farklı aile denetimden geçer; **iki taraf da anlatılmış olmalı** (karşı taraf ileride ise panel o noktaya gelene dek kapalı — Kural 7 mantığı) |
| 18.4 | **Etimoloji çözümleyici** (Rabdo + miyo + liz) | statik önek-kök-sonek sözlüğü (`src/data/etimoloji.json`) | Yalnız sözcüğün **tamamı** sözlük parçalarıyla kapanıyorsa ve terim tıp sözlüğünde varsa gösterilir (yanlış bölme yok); sözlük elle/kaynaklı derlenir, Ü yalnız aday önerir; çevrimdışı pakete girer |
| 18.5 | **Tek tıkla kart** (aralıklı tekrar): o anki cümle + bölge kırpması + çizim + ses kesiti | cümle kimliği, çapa, kelime zamanı | Kart **kopya değil kimlik** saklar (`{cumle, bolge, aralik}`) → içerik güncellenince kart da güncel; mevcut kart/tekrar altyapısına ve `flashcards_anki.txt` dışa aktarımına bağlanır; kişisel anahtar `SYNC_PATTERNS`'e |

---

## 19. Donanım ve hat optimizasyonları (kullanıcı eki 2026-10-23)

| Öneri | Durum | Karar |
|---|---|---|
| Hibrit OCR atlatma (önce gömülü metin, OCR yalnız metinsiz bölge) | `cikar.py` sayfa düzeyinde yapıyor (boş sayfa → Tesseract) | **Bölge düzeyine in:** metni olan sayfadaki **metinsiz resim kutusu** (etiketli şema) kırpılıp OCR'lanır → L0 `resim_metni` (SoM ve görsel kapatma bunu kullanır) |
| WebP + vektör katman | Site slaytı PDF.js ile **zaten vektörel** çiziyor | Sayfa görüntüsü yalnız analiz (L0) ve kart kırpması için WebP; paket PDF'i taşır, görüntüyü değil |
| Borulu sentez (bölüm yazılır yazılmaz ses) | ses EMA kuyruğunda, ders bitince | Bölüm kapıdan geçince EMA işi o bölüm için kuyruğa; yayın yine **tüm ders kapıdan geçince** (yarım ders yayınlanmaz) |
| EMA toplu işleme / INT8 ONNX | EMA 8,6 M parametre, CPU'da ~20–25× gerçek zaman | Önce ölç: darboğaz değilse yapılmaz. Cümle önbelleği (§12.4) asıl kazançtır |
| SQLite sayfa bazlı akış | site ders başına JSON'u tembel yüklüyor | `.medspak` çevrimiçi açılacaksa HTTP Range VFS (sql.js-httpvfs türü) değerlendirilir; çevrimdışında dosya cihazda |
| Genel | — | Tüm yeni betikler `CUDA_VISIBLE_DEVICES=""`, birimlerde `MemoryMax/CPUQuota/OOMScoreAdjust` (AGENTS.md 10); ağır OpenCV işleri gece, sayfa başına süre tavanı |

## 20. Kurul 2 provası ve ücretsiz kapasite ölçümü (2026-10-23)
Sahte Kurul 2 dersi (2x99 "Gebelik Terminolojisi ve Kavramları", 60 sayfa; Kurul 1 çıkmışları yalnız okunarak; çıktılar
`meds_temp/spot_cozucu/provak2`, canlıya/K1'e yazım yok) `prova.py --gorev --sesli --ses-yok` ile, Claude'suz:

| Adım | Sonuç | Çağrı (yaklaşık) |
|---|---|---|
| hazırla | 27 çıkmış aday → 24 tekil (H30 düzeltmesinden sonra; önce 0) | 0 |
| önem | 6/6 parça, 44 madde, 23 örnek soru, 0 HATA | ~15 |
| çözücü | 34/34 soru, 0 HATA | ~20 |
| denetim | 4/16 iş denetlendi, sonra bütün ücretsiz kotalar doldu | ~16 gerekir |
| asistan, sesli metin | koşulmadı (kota) | ~40 gerekir |

- Bir ders ≈ 90 ücretsiz çağrı. 2026-10-23'te toplam 287 çağrı (222 Gemini) sonra Gemini anahtarlarının hepsi, Groq
  gpt-oss/qwen günlük sınırda. **Ücretsiz kapasite ≈ günde 2 ders**; kalanı Claude bütçesine (12/gün) ya da ertesi güne düşer
  (önbellek sayesinde yarım kalan ders kaldığı yerden sürer).
- Bulunan ve düzeltilen hatalar: H30 (konu eşlemesi), H31 (hesap sorusu, iç etiket sızıntısı), H32 (zorluk dağılımı),
  H33 (Türkçe harf kaybı kabul ediliyordu, kabul edilmiş iş yeni kapıdan geçmiyordu, ses kısaltma onarımı), H34 (zincir:
  Gemini tavanı, Zen kapandı, OpenRouter eklendi), "uygulandı" işaretli işin yeni klasöre yazılmaması, JSON ham yanıtın atılması.
- Sıradaki tasarruf adayları: (1) denetimi iş başına değil ders başına toplu yapmak (16 → ~3 çağrı); (2) düzeltme turunda
  bütün paketi değil yalnız hatalı ögeleri göndermek (Groq 413'ü de çözer); (3) `ses` alanlarını modele yazdırmayıp
  metinden betikle üretmek (sayı/yüzde/tarih/birim okunuşu; `modul_okunus` yalnız kısaltmayı çeviriyor).

## 21. Ajan katmanı: yalnız OpenCode, yetmezse yerel Claude (kullanıcı kararı 2026-10-24)
- Görevlerin varsayılan katmanı `A` (`gorevler.json`). Sıra `yazar_ajanlari`: `opencode` (OpenCode CLI, ücretsiz DeepSeek V4.1
  Flash) → `opencode_glm` (aynı CLI, GLM 5.3 Flash) → `claude` (bu makinede `claude -p`, C bütçesi 12/gün). Denetimde sıra
  `opencode_glm → opencode → claude` ve yazar ajanı `haric_aile` ile atlanır: yazar ≠ denetçi model ailesi.
- Ayarlar `otomasyon/llm/butce.json` `ajanlar` (komut, modeller, günlük tavan, zaman aşımı); sayaç
  `meds_temp/state/ajan_butce.json`. Ajan boş klasörde (`meds_temp/ajan_cwd`), salt okunur (`opencode run --agent plan`),
  istem stdin'den. Command Code ve Antigravity tanımlı ama `kapali` (Antigravity'de oturum açık, istem argümanla).
- Doğrudan API zinciri (`Ü`, scripts/agents/cloud_llm.py) görev hattında kullanılmaz; yalnız `--katman Ü` ile elle.
  `som_sec` (görsel) ajan görsel desteği olmadığından kapalı.
- Tasarruf: kısmi düzeltme (`yonlendir.kismi_duzeltme`: yalnız hatalı ögeler ve onların girdisi) + toplu denetim
  (`spot_zinciri.denetim`: aynı yazarın işleri ≤60 bin karakterlik paketlerde D1, D2 …). 2x99'da 19 iş → 5 paket.
- `MEDS_AJAN_CLAUDE=0`: Claude yedeği kapalı (gölge kıyası ve `prova.py --claudesuz`).

### 21.1 Ajan profilleri (kullanıcı isteği 2026-10-24)
Hat tek bir ajanla uçtan uca çalışabilir; limiti olmayan ajana geçmek tek ayar. `butce.json` `profiller`:
`karma` (varsayılan: OpenCode → yerel Claude), `opencode` (DeepSeek yazar / GLM denetçi), `antigravity` (Gemini 3.8 Flash /
GPT-OSS 120B), `claude` (Opus / Sonnet, günlük tavan `claude.profil_gunluk_cagri` 120), `commandcode` (varsayılan / Kimi K3).
Seçim: `MEDS_AJAN_PROFIL` > `--profil` (gorev.py, prova.py, spot_zinciri.py) > `etkin_profil` (`gorev.py profil <ad>` kalıcı
yapar; gece hattı bunu kullanır). `gorev.py profil` profilleri ve bugünkü kullanımı gösterir. Her profilde yazar ≠ denetçi
model ailesi; iki düzeltmeden sonra kalan engel profilin `son_care` ajanına gider. Hiçbir ajanın limiti yoksa `--katman elle`
(paket.md herhangi bir LLM'e elle verilir). Sınama 2026-10-24: sekiz ajan girişinin hepsi Türkçe JSON döndürdü.

### 21.2 Oturum kuyruğu — profil `oturum` (kullanıcı isteği 2026-10-24)
Hat model çağırmaz: her paket `meds_temp/gorev/<iş>/paket.md` olarak hazırlanır, `meds_temp/gorev/kuyruk.json`'a yazılır,
iş `elle_bekliyor` olur ve zincir kod 3 ile durur (komutu kuyruğa kaydedilir). Açılan bir Claude Code oturumu `/kuyruk`
becerisiyle (`/home/indu/medsor/.claude/skills/kuyruk/SKILL.md`) kuyruğu eritir: `gorev.py kuyruk --json` → her paket yeni
bağlamlı alt ajana → cevap `cevap.txt` → `gorev.py derle <iş>` 0 HATA (aile/model "oturum") → paket bitince
`gorev.py kuyruk --surdur` (zincirler kaldığı yerden; yeni paket çıkarsa döngü). Denetim bulgusu düzeltmesi:
`duzeltme_paket.md` → `duzeltme_cevap.txt` → `gorev.py duzeltme-derle <iş>`. Denetim paketleri MUTLAKA yeni bağlamlı alt
ajanla (yazar = denetçi modeli olduğundan bağımsızlık ayrı bağlamla sağlanır). Etkinleştirme: `gorev.py profil oturum`
(kalıcı) ya da `--profil oturum` (tek koşu). Oturum ile `claude -p` aynı Claude limitinden yer; fark: oturumda çalışır,
kullanıcı izler ve araya girebilir.

## 22. R5–R7 durumu ve k2-02 ölçümü (2026-10-24)
| Aşama | Yapılan | Kalan |
|---|---|---|
| Sesli metin kapsamı | `isle.sesli_kapsam`: her içerik/şekil sayfası anlatılır, sayfa başına bilgi maddesi kadar cümle (görselde +1, ≤4); TALIMAT_SESLI "Derinlik" | — |
| R5 delta | `scripts/ders_isci/delta.py` (iz eşleme → ekler / kısmi / tam), `isle.py` paralel üretimden önce; taslağa `sayfa_izleri.json` | kısmi kipte bilgi paketi güncellenmez; Drive `changes.watch` ve ayrı `Ogrenci_Notu/`, `Hoca_Ses/` klasörleri yok (onay kapısı yüklemesi bunun yerine) |
| R6 çizim | `scripts/cizim/` (cizim_uret + cizim_dogrula + TALIMAT_CIZIM), ders zinciri `cizim` adımı, `CizimLayer.tsx` (kontur, akış, eğri fazı, şema), sunucu işarete `z` ekler | eğri fazı derste örnek çıkmadı (k2-02'de grafik yok); kroki OpenCV adayları (ok/eğri) istemde henüz kullanılmıyor — Claude görüntüden okuyor, kapı pikselle doğruluyor |
| R7 paket | `scripts/paket/medspak_uret.py` + `medspak_dogrula.py` (SQLite; ses MP3) | okuyucu uyarlayıcısı (`paketMotoru.ts` `medspak:` türü), Opus dönüşümü (ffmpeg yok) |

k2-02 (62 sayfa): sesli metin 1.628 → **2.189 kelime (~20 dk), 106 cümle**, atlanan sayfa 0; işaret kapsamı **%96**;
çizim 80 aday → **68 komut** (38 akış, 23 şema, 7 kontur; 12 kapıda atıldı); paket 8,1 MB, 0 HATA. EMA sesi GPU'da ~1 dk.
