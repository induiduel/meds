# Sağlık Bakanlığı sekmesi — plan (2026-10-14)

Kullanıcı isteği: siteye "Sağlık Bakanlığı" sekmesi; altında Sağlık Bakanlığı'na ve Karabük'e ait halk sağlığı
sayfaları (Karabük, Aşı, Yenidoğan, Kadın/Anne Sağlığı, Halk Sağlığı …). Resmî veriler ve istatistikler ders
PDF'leri, Öğren desteleri, kazanımlar ve çıkmış sorularla desteklenir. Veri kaynakları yalnız devlete ait olur.
Tüm aşamalar onaylı; aşamalar arası onay beklenmez (dağıtım/commit hariç — ayrıca sorulur).

## İlkeler

- **Kaynak zorunlu:** her sayı/olgu bir kaynak kimliğine bağlıdır (`kaynaklar.json`: kurum, belge, yıl, URL, erişim
  tarihi). Kaynaklar: Sağlık Bakanlığı (saglik.gov.tr, hsgm, asi, ketem, il sağlık müdürlüğü), TÜİK, Resmî Gazete,
  Çevre Şehircilik ve İklim Değişikliği Bakanlığı, Karabük Valiliği, devlet üniversitesi (TNSA — Hacettepe NEE, SB
  adına). Teyit edilemeyen sayı yazılmaz (PROJE_TANITIMI "Uydurma yok").
- **Ders bağı:** her bölüm müfredattaki konulara bağlanır: Öğren desteleri (slayt numarasıyla), kazanımlar, sınav
  spotları, çıkmış sorular (sayı + örnek + "Kendini sına"), ders PDF'i. Bağlar betikle üretilir, elle değil.
- **Sınav odağı:** her bölümde "Sınavda ne soruldu" kutusu — gerçek çıkmış sorulardan.
- Kaynak dışı bilgi soru/etkileşim olarak yazılmaz; etkileşimler yalnız resmî veri + ders notu temelli.

## Bilgi mimarisi (`/saglik`, rota `health_ministry`)

| Alt sayfa | Yol | İçerik |
|---|---|---|
| Genel bakış | `/saglik` | Türkiye kilit göstergeleri, bölüm kartları, Karabük özeti, en çok soru çıkan konular |
| Karabük | `/saglik/karabuk` | il nüfusu, sağlık kurumları (hastane, ASM, aile hekimi birimi, ilçe SM, KETEM, SHM, 112, ADSM), ilçe tablosu, il göstergeleri, çevre/hava (demir-çelik), kaynaklar |
| Aşı | `/saglik/asi` | etkileşimli aşı takvimi (yaş kaydırıcısı → o yaşta yapılacaklar), aşı kartları, gebe/erişkin aşıları, aşılama oranları, aşı ile önlenebilir hastalıklar |
| Yenidoğan | `/saglik/yenidogan` | Ulusal Yenidoğan Tarama Programı (topuk kanı, işitme, kalça, KKKH, göz), bebek izlem takvimi, demir/D vitamini destekleri, bebek ölüm göstergeleri |
| Kadın / Anne Sağlığı | `/saglik/anne-kadin` | doğum öncesi bakım izlem zaman çizelgesi, lohusa izlemi, anne ölüm oranı eğilimi, doğurganlık, üreme sağlığı/aile planlaması, evlilik öncesi tarama |
| Erken teşhis | `/saglik/tarama` | KETEM kanser taramaları (meme, serviks, kolorektal) yaş/aralık tablosu, diğer ulusal taramalar |
| Salgın hastalıklar | `/saglik/salgin` | bildirimi zorunlu hastalıklar (A–D grupları, süreler), sürveyans, salgın inceleme basamakları, güncel Türkiye verileri |
| Çevre ve sağlık | `/saglik/cevre` | içme suyu, hava kalitesi sınır değerleri, Karabük hava kalitesi, meslek sağlığı |
| Sağlık kurumları | `/saglik/kurumlar` | basamaklar, kurum türleri ve sayıları (Türkiye), sevk zinciri, kişi başına göstergeler |
| İstatistikler | `/saglik/istatistik` | gösterge sözlüğü (tanım + formül + son değer), eğilim grafikleri |

Telefon: üstte yatay bölüm şeridi; masaüstü: solda bölüm rayı, ortada içerik, sağda "Derste/Sınavda" yan paneli.

## Veri katmanı

- `src/data/saglik/` (tembel `import()`): `kaynaklar.json`, `turkiye.json`, `karabuk.json`, `asi.json`,
  `yenidogan.json`, `anne_kadin.json`, `tarama.json`, `salgin.json`, `cevre.json`, `kurumlar.json`,
  `baglantilar.json` (üretilir).
- `scripts/saglik/baglantilari_kur.py`: her bölümün konu/anahtar kelime tanımından çıkmış soruları
  (`src/data/pastQuestions.json`, disiplin+konu+kök eşleşmesi), kazanımları (`kazanimlar/lite`), desteleri
  (`interactive_learning_decks.json` + kazanım slayt bağları), spotları (`exam_spots_k1.json`) bulur →
  `baglantilar.json`. Ders başına yalnız Dönem 3 verisi.
- `scripts/saglik/dogrula.py`: her veri öğesinin `kaynak` alanı kaynaklar.json'da var mı, URL devlet alan adı mı
  (`.gov.tr`, `tuik`, `resmigazete`, `.edu.tr`), boş sayı/metin yok mu.

## Aşamalar

1. **Plan + iskelet** — rota, gezinme (Başvuru grubu + v12 Kaynaklar rayı), sayfa kabuğu, CSS (`sbk-` öneki).
2. **Resmî veri araştırması** (paralel 4 ajan): aşı · anne/kadın/yenidoğan/tarama · Karabük · Türkiye
   istatistik/salgın/çevre/kurumlar. Çıktı: kaynaklı JSON.
3. **Ders bağları** — `baglantilari_kur.py` → `baglantilar.json`.
4. **Arayüz** — bölüm sayfaları, etkileşimli aşı takvimi, gebe/bebek izlem zaman çizelgesi, gösterge grafikleri,
   Karabük panosu, "Derste/Sınavda" paneli, Kendini sına (çıkmış sorulardan).
5. **Doğrulama** — `dogrula.py`, ikinci ajanla rakam/kaynak denetimi, `npm run lint`, `npx vite build`,
   tarayıcıda 375/820/1440 + koyu tema.
6. **Kayıt** — DEGISIKLIK_KAYDI, hafıza. Commit/Oracle dağıtımı kullanıcıya sorulur.

## Durum

- [x] 1 Plan + iskelet — rota `health_ministry` (`/saglik`, `/saglik/<bölüm>`), gezinme (Başvuru + v12 Kaynaklar), ön yükleme, arama paleti alt sayfaları
- [x] 2 Araştırma — aşı (24 kaynak), anne/kadın/yenidoğan/tarama (48), Karabük (40), Türkiye istatistik/salgın/çevre/kurumlar (103); birleşik 192 kaynak
- [x] 3 Bağlar — `scripts/saglik/baglantilari_kur.py` (9 bölüm, ~840 çıkmış soru, kazanım, deste, slayt çapası, spot, müfredat haritası)
- [x] 4 Arayüz — `components/saglik/` (SaglikView, SaglikBolumler, SaglikAraclar, SaglikOrtak, saglikVeri) + `styles/saglik.css`
- [x] 5 Doğrulama — bağımsız denetim 156 kalem: 154 doğru, 0 yanlış, 1 yuvarlama (TDH 2025 → 1,42 düzeltildi), 1 kaynak eksik (topuk kanı zamanlaması → BCE 2026 eklendi); 5 göstergeye SİY 2025 bülteni değerleri eklendi. tsc 0, vite build; tarayıcı 375/800/1440 taşma taraması temiz
- [x] 6 Kayıt — DEGISIKLIK_KAYDI, hafıza. Commit/Oracle dağıtımı YAPILMADI (kullanıcıya soruldu)

## Veri güncelleme yolu

1. Araştırma çıktısını (asi.json, anne_yenidogan.json, karabuk.json, turkiye.json; her biri `kaynaklar` listesiyle) bir klasöre koy.
2. `python3 scripts/saglik/birlestir.py --kaynak <klasör>` — devlet alan adı denetimi, kimlik birleştirme, kaynaksız öge eleme →
   `src/data/saglik/{kaynaklar,asi,anne_yenidogan,karabuk,turkiye}.json`.
3. `python3 scripts/saglik/baglantilari_kur.py` — çıkmış soru / kazanım / deste bağları → `baglantilar.json` + `sorular/<bölüm>.json`.
   Çıkmış sorular ya da desteler değişince yeniden çalıştır.
4. `npx vite build` (sunucu yeniden başlatılmaz; veri ön yüzle derlenir).
