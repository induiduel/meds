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

## Talimatlar

`docs/OGREN_ETKILESIM_REHBERI.md` (yeni) ve özetleri: kök `GEMINI.md`, `PROJE_TANITIMI.md`, `AGENTS.md`; `meds/AGENTS.md` §11, `meds/CLAUDE.md`, `meds/PROJECT_INSTRUCTIONS.md`.
