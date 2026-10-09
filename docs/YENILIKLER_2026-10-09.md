# Yenilikler — 2026-10-09

Bu belge 8–9 Ekim 2026'da yapılan arayüz, Öğren ders ekranı ve veri değişikliklerini özetler.
Öğren içerik şeması ve kuralları: [OGREN_ETKILESIM_REHBERI.md](OGREN_ETKILESIM_REHBERI.md).

## Öğren · yeni ders ekranı (`src/components/learn/lesson/`)

| Özellik | Ayrıntı |
|---|---|
| İki düzen | **Akış (A):** tek sütun okuma + altta bilgi çekmecesi. **Stüdyo (B):** ekrana sığan üç bölme (içerik, Pekiştir paneli, bilgi kutucukları). Telefonda (≤ 767 px) yalnız Akış. Araçlar → Düzen'den seçilir, tercih hatırlanır. |
| Bölüm listesi | Bölüm → adım (konu + alt başlık), açılır-kapanır, ilerleme halkası, arama, "Tekrar" etiketi. Bölümler tekrar sayfalarından, yoksa `badge` değişimlerinden ya da 8–10 adımlık gruplardan çıkarılır. |
| Bilgi bölmesi | Sınav spotu, Hoca notu, Terimler, Kazanımlar, Sorular (her soruda **Çöz**), Kaynak. Ana içerikte yalnız ders anlatılır. |
| Etkinlikler (Pekiştir) | Mini soru, klinik karar, boşluk doldur, gizli tablo, mekanizma zinciri, karşılaştır, aktif hatırlama, çevir kartları, çıkmış/çalışma soruları. Etkinlikler bitince adım ✓ olur. |
| Şıklı sorular | İlk seçim cevabı belirler; sonra her şıkka dokununca açıklaması **kartın içinde** "Neden doğru / Neden yanlış" başlığıyla açılır, tekrar dokununca kapanır. Çalışma sorularında tek parça açıklamadaki "A seçeneği yanlıştır: …" satırları ilgili şıkka dağıtılır, kalanı "Açıklama" panelinde. |
| Araçlar menüsü | Düzen, Görünüm (Ders / Yan yana / PDF), Okuma (Sayfa sayfa / Kaydırarak), Hatırlama modu, Fosforlu kalem, Kalem modu (çizim), Ders notları, Asistana sor, Tıbbi sözlük, Tam ekran, Bu adımı PDF yap, Klasik görünüm. |
| Terimler | Adımın kendi terimleri + metinde geçen tıbbi sözlük terimleri (730 terim); ilk geçtiği yerde altı noktalı, dokununca tanım. Eski destelerde adım başına 0 → 2–13 terim. |
| Kazanımlar | `src/data/kazanimlar/byDeck.json` (`scripts/build_kazanim_deck_index.py`, 115 destenin 101'i); adıma yalnız ≥ 2 ayırt edici ortak kökle eşleşenler gösterilir. |
| Geçişler | Adım geçişinde bloklar sırayla belirir, başlığın altından vurgu şeridi çizilir; "hareketi azalt" açıksa kapalı. |
| Tam ekran | Belge kökü tam ekrana alınır (bilgisayar, Android); API yoksa/yanıtsızsa (iPhone) arayüzü gizleyen odak modu. |
| Kalem algılama | Telefon/tablette gerçek kalem algılanınca yalnız kalem yazar, parmak kaydırır; kalem yoksa parmak yazar. Marker/Kalem için ekranın tepesinde yüzen renk–araç–kapatma çubuğu; Araçlar menüsü her seçimden sonra kapanır. |
| Telefonda | Daha küçük yazı (anlatım 14 px, başlık 20 px), etkinlik sekmelerinde yalnız ikon. |

## Öğrenci hata bildirimi

- Her etkinlik kartında, tabloda, adım başlığında ve bilgi bölmesindeki her öğede bayrak. Bildirim: **hangi bilgi yanlış** + **neden yanlış**; kim, ne zaman, konum; 👍/👎 oy (kendi bildirimine oy yok).
- **Konum + derin bağlantı:** her bildirim öğenin yerini (`Pekiştir › Gizli tablo (2. etkinlik)`, `Ana içerik › Tablo: …`, `Bilgi bölmesi › Sınav spotu › 1. öğe`) ve `/ogren/<deste>?adim=n&hedef=<anahtar>` bağlantısını taşır. Yönetici e-posta/telefon bildirimindeki bağlantıya tıklayınca ders o adımda açılır, ilgili sekme açılır, öğe vurgulanır.
- Sunucu: `src/services/learnFeedbackService.ts`, kayıt `data/learn_feedback.json`; uç noktalar `GET/POST /api/learn/feedback`, `POST /api/learn/feedback/:id/vote`, `POST /api/admin/learn-feedback/:id/resolve`. Bildirim servisine (`serverNotificationService`) isteğe bağlı `link` parametresi eklendi.

## Hata düzeltmeleri

- **Kalem modu telefonda yanlış yere çiziyordu:** `SlideDrawingCanvas` koordinatları DPR ile iki kez çarpıyordu; çizgiler parmağın 2–3 kat uzağına düşüyordu (klasik ekranda da). Düzeltildi.
- Mekanizma zinciri basamakları "…" ile kesikti (24/126): slayttaki tam metinden tamamlandı (ekranda ve veride).
- Boşluk doldurmada `[CGG]` köşeli parantezi açıkta kalıyordu: parantez boşluğa dahil.
- Gizli tablo / boşluk ipuçları cevabı ele veriyordu (75): ekranda gizlenir, veriden silindi.
- Esc, açık PDF/sözlük penceresi varken arkadaki dersi de kapatıyordu.
- Öğren "+" menüsü masaüstünde ve ders üstünde görünüyordu (`ms-*` display, Tailwind `md:hidden`'ı eziyordu).
- Eski biçimli cevaplar (sıra numarası `0/1`, `"E) …"`) doğru okunur.

## Veri

- **Kaybolma riski giderildi:** 100 adımlık Dismorfoloji dersi ve 15 güncel deste yalnız gitignored `src/data/decks/items/` içindeydi (kaynakta 16 adımlık eski sürüm). Kaynak `src/data/interactive_learning_decks.json` güncellendi; `items/` yalnız üretilir.
- `scripts/validate_learning_decks.py`: deste kuralları denetleyicisi (0 HATA kapısı); `--duzelt` kesik zincir ve ipucu sızıntısını onarır. Mevcut veri: 0 HATA, 680 eski biçim uyarısı.

## Diğer sayfalar

- Genişlik: Örnek sorular, Öğren listesi, Veri merkezi, Test çöz, kartlar, tam ekran çözüm, kitapçık ekranı dolduruyor.
- Tasarım dili: yeni bileşenlerdeki ham Tailwind renkleri uygulama token'larına çevrildi (yönetici bildirim kartı dahil).
- Kazanımlar: ders ve konu düzeyinde açılır-kapanır, satır görünümü.
- Çıkmış sorular: sürüm seçici ikon olarak soru başlığında; karşılaştırma görünümü "değişiklik izleme" (kelime düzeyinde fark); "Hakkında" penceresi cevap özeti + şık şık analiz; terim vurgusu kelimeleri bölmüyor.

## İkinci tur (9 Ekim akşam)

- **Öğren açılış sayfası yeniden yazıldı** (`src/components/learn/LearnHub.tsx`): özet (ders, adım, soru, ilerleme), en son açılan üç yarım ders, arama (`/` kısayolu), durum süzgeci (Devam eden / Başlanmadı / Biten), ders dalı çipleri, sıra numaralı ders kartları (adım, soru, kart, ilerleme, PDF). Yönetici için turuncu kutu yerine küçük "Yayında / Arşiv / Tümü" seçici. Düzeltilen hatalar: "Tümü" sayısı 114 gösterip 7 ders listeliyordu; ders adlarındaki "(Yeni Mikro-Ders)" eki ekranda görünüyordu (`deckName`, `src/data/deckStore.ts`).
- **Ders notları:** mavi zeminli `ls-callout` yerine beyaz zeminli, sol kenarında ton çizgisi olan `ls-note`. Ardışık `>` satırları tek nota toplanır; `[!NOTE]`, `[TEMEL İLKE]`, `[SINAV SPOTU]` gibi etiketler notun başlığı olur (önceden `> [!NOTE]` satırı ayrı, boş bir mavi kutu oluyordu). Ton: kritik/uyarı kırmızı, sınav spotu turuncu, klinik/önemli mavi, özet yeşil, diğerleri nötr. Anahtar madde kutuları ve formül de mavi zeminden çıktı; başlıktaki mavi vurgu bloğu yerine başlığın altında çizilen kısa çizgi.
- **Telefonda tablolar:** kart görünümünde her satır "etiket | değer" iki sütun; dokunmatikte satır vurgusu takılı kalmıyor. Alt gezinmede 7'den çok adımlı bölümlerde noktalar yerine "2 / 9" (iki satıra kırılıyordu).
- **Ders katmanı kayması:** `scrollIntoView` arkadaki sayfayı da kaydırıyordu; ders içinde yalnız kendi kapsayıcısı kaydırılır, açıkken `html` kaydırması kilitli.
- **Yönetici bildirimleri:** telefon bildirimine tıklayınca Öğren bildirimi artık dersin ilgili adımına ve öğesine gider (`public/sw.js` önce bildirimdeki bağlantıyı kullanır). Yönetim panelindeki son bildirimler listesinde Öğren bildirimleri için "Derste gör"; çıkmış soru bildirimleri `/cikmis/<id>` açar. Öğren bildiriminin başlığı ayrı ("MedSoru Öğren: Hata Bildirimi").
- **Çıkmış sorular yeniden tasarlandı ("sınav kitapçığı")** — sınıflar `cx-*`, `src/index.css` sonu:
  - Başlık + canlı soru sayısı; arama ve Filtre tek kontrolde (etkin filtre sayısı rozetle). Kurul seçici altı çizili sekmeler (K1…K6, Final, Bütünleme); geniş ekranda sıralama ve "Kendini sına" anahtarı aynı satırda. Etkin filtreler ayrı satırda kaldırılabilir koyu çipler.
  - Soru: koyu numara rozeti, ders + "Kurul · yıl", en fazla birkaç küçük durum işareti, ⋯ menüsü. Şıklar optik form kabarcığı; doğru cevap dolu yeşil kabarcık, kendini sınada yanlış seçim kırmızı ve üstü çizili, altında sonuç satırı. Kısa şıklar geniş ekranda iki sütun. Anket satırları da aynı dilde (kabarcık + ince yüzde çizgisi).
  - Alt satır yalnız beğen/beğenme/yorum, Açıklama ve paylaş; Kopyala ⋯ menüsünde. Şık itirazı fareyle üstüne gelince şıkkın sağında; dokunmatikte ⋯ menüsünden ("Cevaba itiraz et").
  - Telefonda sorular kenardan kenara (çerçevesiz), sürüm seçici ⋯ menüsünde. Açıklamalı, Denetleyici, Faz 14, Yeni ve Cevapsız/Belirsiz süzgeçleri Filtre çekmecesinde.

## Faz 14 kullanıcı kuyruğu (9 Ekim gece)

- **Yapay zekâ incelemesine gönder** (Çıkmış › ⋯ menüsü, herkes): isteğe bağlı notla soru Faz 14 kuyruğuna girer. Kartta "Sırada N" / "Onayda" işareti görünür; aynı soruya gelen yeni istekler bekleyen incelemeye not olarak eklenir.
- **Hatalı soru bildirimi ve şık itirazı** da bildirim metniyle aynı kuyruğa girer (canlı sitede buluta düşen bildirimler bulut köprüsünden, son 24 saatteki aynı notla tekrar eklenmeden).
- **İşleme:** `scripts/advanced_ai/phase14_cloud_question_editor.py --kullanici-kuyrugu` (systemd işi `meds-faz14-kullanici`, günlük `meds_temp/logs/phase14_kullanici.log`). Yalnız ücretsiz anahtarlar; kota bitince istekler bekler, sunucu 10 dakikada bir yeniden dener. Daha önce incelenmiş sorular da yeniden incelenir; öğrenci notları modele "ipucu, doğru kabul etme" talimatıyla verilir.
- **Dosyalar:** kuyruğu yalnız sunucu yazar (`meds_database_v2/phase14_past_question_editor/kullanici_kuyrugu.json`), betik sonucu `kullanici_sonuclari.jsonl`'e ekler, inceleme `reviews.jsonl`'e `kaynak: "kullanici"` ve `istek_id` ile yazılır. Kod: `src/services/phase14UserQueue.ts`.
- **Otomatik yazma:** sunucu dakikada bir sonuçları okur. Cevap kesinse öneri `applyPhase14Review` ile (yönetici onayıyla aynı yol) veritabanına yazılır. Cevap belirsiz ya da şüpheliyse yönetici onayına (/test/cikmis) kalır; içerik aynıysa "değişiklik yok" olarak kapanır.
- **E-posta:** soru güncellenince hata bildirenlere eski ve yeni hal yan yana gider (`src/services/phase14Mail.ts`). Yönetici ve giriş yapmamış kullanıcılar e-posta almaz. E-posta adresi yalnız yerel kuyruk dosyasında tutulur, soru kaydına ve buluta yazılmaz. Yönetici onayına kalan soru onaylanınca da e-posta gider.
- **Anket:** ⋯ › "Ankete aç" ile cevabı olan soru da topluluk oylamasına açılır (`data/user_answer_polls.json`, kabul edilen cevapla karşılaştırılır). Oy verildikten sonra anketin başlığında "Oyun B · Değiştir": oy geri alınır, başka şık seçilir (`DELETE /api/past-question-reviews/:id/answer-votes`).
- Yeni uç noktalar: `POST /api/past-exams/:id/ai-review`, `GET /api/past-exams/ai-review-queue`, `POST /api/past-question-reviews/:id/open-poll`, `DELETE /api/past-question-reviews/:id/answer-votes`.

## Soru ekle ve küçük düzeltmeler (9 Ekim gece)

- **Ana sayfa (Soru ekle) kendi tasarımında kaldı**; yalnız: üstteki kurul seçimi kaldırıldı, kurul · ders · sene · no **soru kökü yazılınca** yazma alanının altındaki şeritte belirir (`src/components/ui/MetaPicker.tsx`, "token" görünümü). Telefonda yazma alanına dokununca alan **tam ekran** açılır (üstte kapat ve Ekle, altta künye şeridi; klavyeye göre yükseklik `--vvh`), kapatınca animasyonla yerine döner; telefonun geri tuşu da kapatır, gönderim başarılı olunca kendiliğinden kapanır.
- **Telefonda adım adım soru ekleme** (ana sayfa, tam ekran yazma): 1) Soru kökü → sağ üstte **Devam et**; 2) **Soru tipi**: Klasik ya da Öncüllü (büyük seçim kartları, seçince geçer); 3) Öncüllü ise **öncüller** (I–VI, Enter sonraki öncüle geçer, ekle/sil); 4) **Şıklar** A–E ve doğru cevap (öncüllüde "Yalnız I", "I ve II"… kalıpları dokununca sıradaki boş şıkka yazılır); 5) **Son dokunuş**: ipucu, kurul, ders, sene, soru no, özet ve **Havuza ekle**. Üstte adım sayacı ve ilerleme çizgisi; adımlar arası kayma animasyonu; geri düğmesi ve telefonun geri tuşu bir önceki adıma döner. Öncüller kayda kökün altına "I. …" satırları olarak eklenir (çıkmış soru gösterimi bunları madde olarak okur).
- **Soru katkısı yap penceresi** (`ContributeModal.tsx`): "Hangi soru?" bölümü Kurul · Ders · Sene · Soru no seçicileri (ızgara, kaydırılan pencerede kırpılmaz); kurul uyarısı, benzer taslak ve AI önerisi kutuları sade tasarımda; açılış ve kapanış animasyonlu. Telefonda başlığın pencereyi ekrandan taşırması düzeltildi.
- **Sene seçimi:** 2016–17'den bu öğretim yılına kadar (yeniden eskiye) ve "Bilmiyorum"; varsayılan bu öğretim yılı, seçim cihazda hatırlanır. Katkıyla `examYear` ("2025-2026") olarak kaydedilir; soruda yıl zaten varsa ezilmez.
- Kurul listesinde Final'in "Bütünleme" görünmesi düzeltildi (`committeeShortLabel` önce kimliğe bakar).
- **⋯ menüsü (tüm sayfalar):** masaüstünde belgenin üst katmanında açılır; altta yer yoksa yukarı açılır, ekrana sığacak kadar kayar. Önceden alttaki kartın arkasında kalıyordu.
- **Kapanış animasyonları:** ortak pencere (`ui/Dialog`: Esc, dış tıklama, kapat), ⋯ menüsü (masaüstü kutu ve telefon paneli), künye seçicileri, Çıkmış filtre çekmecesi ve katkı penceresi artık kapanırken de animasyonlu (hareketi azalt açıksa kapalı).
- **Çıkmış · karşılaştırma:** sürüm farkı (Denetleyici ↔ Eski) ve Ham ↔ Düzenlenmiş görünümü aynı "fark kâğıdı"nda: kitapçık kabarcıklı şıklar, eklenen kelimeler yeşil, çıkarılanlar kırmızı üstü çizili, değişen satırın altında soluk "önceki" hali; eski cevap kesik çizgili kabarcık. Eski sürüm kaydı yoksa "kaydı yok" yazar (önceden yanlış değişiklik sayısı gösteriyordu). Numarasız soruda rozet "?".

## Talimatlar

`docs/OGREN_ETKILESIM_REHBERI.md` (yeni) ve özetleri: kök `GEMINI.md`, `PROJE_TANITIMI.md`, `AGENTS.md`; `meds/AGENTS.md` §11, `meds/CLAUDE.md`, `meds/PROJECT_INSTRUCTIONS.md`.
