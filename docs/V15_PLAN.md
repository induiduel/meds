# v15 "Yalın" — koda geçiş planı

Kaynak: **MeDSor Tasarım Sistemi v15** (artifact https://claude.ai/artifact/D8pMJwGTeeGG5y9jwtpurR) — 258 ekran,
8 tema, `tokens.json`. Kural: **her sayfa ayrı aşamadır; kullanıcı onayı gelmeden sonraki sayfaya geçilmez.**

## İlkeler (tasarım sisteminden)
- Gezinme dört iş + Bugün: Ders çalış · Soru çöz · Sınava hazırlan · Başvuru. Adres şeması değişmez (`siteHaritasi.ts`).
- Bir ekranda tek iş, tek vurgu rengi (`--color-accent`); durum renkleri yalnız anlam taşırken. Gradyan/emoji kart yok.
- Ekran kaydırmadan tek bakışta: ikincil işler (ayar, süzgeç, paylaşım) ayrı ekran ya da çekmece.
- Kesme noktaları: <600 telefon (alt sekme) · 600–1023 tablet (76 px ray) · ≥1024 PC (236 px menü). Sayfa içi düzen kap
  sorgusuyla (`container`), bölünmüş ekranda da doğru düzen.
- Yazıyı opaklıkla soluklaştırma yok: `--color-ink-2/3`.

## Altyapı (yapıldı, aşama 1)
- Seçim: `utils/appearance.ts` → `DesignChoice 'v15'`, `Appearance.v15`; v12 bileşenleri üstünde çalışır (design='v12'),
  kök `data-v15="on"`. Ayarlar › Tasarım'da "Yalın (v15)". v13 ile birlikte açık olmaz. `index.html` erken betiği yazar.
- Renk: **yalnız palet kaydı** (`utils/palettes.ts`, `--color-*`). v15'in 8 teması kayıtta zaten var: Klinik mavi
  (light/a), Kâğıt (sepia/a), Gece/OLED (dark), Ameliyathane≈Nane/Zümrüt, Histoloji≈Erik, Laboratuvar≈Kehribar,
  Gece nöbeti≈Gece mavisi (kontrast kapısı kopya sayar, yeniden eklenmez). Tema/palet/vurgu değişimi her v15 bileşenine
  kendiliğinden yansır.
- Ölçüler: `styles/v15/tokens.css` (`--v15-s*`, `--v15-r-*`, `--v15-t-*`, gölge, kabuk değişkenleri, yazı tipleri).
- Kabuk: `components/v15/ShellV15.tsx` (SideNavV15, TopBarV15, TabBarV15), `navV15.ts` (bölümler merkezModel'den),
  `styles/v15/shell.css`. Yazı tipleri (Plus Jakarta Sans, Newsreader) yalnız v15'te yüklenir.

## Bileşenler (ortak, `styles/v15/tokens.css`)
| Sınıf | Ne |
| --- | --- |
| `.v15-card` | Kart yüzeyi (surface + line-soft, radius-lg) |
| `.v15-btn` / `.is-soft` | Birincil / yumuşak düğme (≥44 px) |
| `.v15-tag.is-{a,ok,w,b,ai,c}` | Durum etiketi |
| `.v15-tile.is-{…}` | Simge karosu |
| `.v15-bar` | İnce ilerleme çubuğu |
| `.v15-label`, `.v15-h2`, `.v15-cap` | Üst etiket, bölüm başlığı, yardımcı satır |
| `.v15-skel` | İskelet |
| `.v15-seg` | Bölüm seçici (bağlantı ya da `aria-current`) |
| `.v15-hscroll` | Kenarı solan yatay kaydırma satırı (çipler) |
| `<Halka>` (`components/v15/Halka.tsx`) | İlerleme halkası |
| `useV15Baslik` (`components/v15/baslik.ts`) | Sayfanın üst bar başlığı, alt satırı ve geri adresi |
| `.cd15-sat`, `.cd15-sw` (`styles/v15/sesli.css`) | Çekmece satırı ve anahtarı (Görünüm, menüler) |
Yeni bileşen önce buraya eklenir; sayfa CSS'i yalnız yerleşim yazar.

## Aşamalar
| # | Sayfa / grup | v15 ekranları | Durum |
|---|---|---|---|
| 1 | Kabuk + Bugün | A02 ana, Kabuk | Onaylandı (2026-10-27) |
| 2 | Ders çalış merkezi + branş + ders | B01–B03, Z02 | Onaylandı (2026-10-27) |
| 3 | Sesli ders oynatıcı | S01–S18 + S2 grubu (S19–S30, v15.3) | Onaylandı (2026-10-27) |
| 4 | Öğren listesi/slayt/etkileşim | B05–B07 | Onaylandı (2026-10-27) — kitaplık `OgrenKutuphaneV15`, slayt ekranı v15 katmanı (`styles/v15/ogren.css`) |
| 5 | Soru çöz merkezi + soru + yanlış çekmecesi + sonuç | C01–C10, Y01–Y06 süzgeç | Onaylandı (2026-10-27) — merkez `SorularMerkezV15` (+ Test oluştur → `/sorular/deneme?kurul=&ders=&n=&basla=1`), soru/yanlış çekmecesi/sonuç `PracticeV15` |
| 6 | Sınava hazırlan: kamplar, Check Up, Son Prova, 60 planı, takvim, olası | D01–D07 | Onaylandı (2026-10-27) — merkez `KamplarMerkezV15`; kamp/Son Prova/60 planı iç sayfaları açık iş |
| 7 | Başvuru: kaynaklar, Sağlık Bakanlığı, sözlük, spotlar, önem | G01–G02, B08–B10 | **Onay bekliyor** — merkez `KaynaklarMerkezV15`; iç sayfalar açık iş |
| 8 | Profil, ayarlar, görünüm (tema/palet/yazı), başarımlar | G04–G06, V01–V04, W01–W02, AB01–AB08 | Kuruldu (2026-10-27): ProfileV12 v15 dalı — profil kartı + gruplu satırlar (Ben/Ayarlar/Diğer), her bölüm #hash ekranı, Geri listeye; paneller v12'den, `styles/v15/profil.css` |
| 9 | Diyaloglar, çekmeceler, tostlar, durumlar | H01–H11, A06–A08, AB12–AB18 | |
| 10 | Açılış + kayıt akışı | I01–I11 | |

### Yeni sayfalar (tasarım sohbetinde istenenler; sitede yok, sıfırdan kurulacak)
| Sayfa | v15 ekranları | Not |
|---|---|---|
| Oyunlar merkezi (boşluk, eşleştir, kartlar, sırala, blitz, ızgara, düello, sınıf yarışması) | F01–F11, N01–N08 | ✅ Canlı yarışma kuruldu (Soru çöz › Oyunlar); diğer oyun türleri (boşluk, eşleştir, sırala, blitz) yok |
| Hücrem (DNA, glukoz, mitokondri, 28 evrim basamağı) | M01–M17 | ✅ /hucrem: 28 basamak = tanim.json kilitleri `tur: hucre` (onceki şartı sunucuda), ATP ile açılır, SVG hücre katman katman büyür; 3B yok |
| Yüzen kronometre + çalışma kapsülü | T01–T15, U01–U12 | Sistem süresinden ayrı tutulur |
| Ders programı (liste/hafta/gün/ay, içe aktar) | AA01–AA07 | ✅ gün/hafta/liste kuruldu (ay ve içe aktarma yok) |
| İstatistik ve grafikler (14 grafik) | J01–J02, X01–X10 | |
| Zihin haritası biçimleri, şemalar | J03–J06, W05–W10, V05–V08 | ✖ Kullanıcı reddetti (2026-10-27, "çok kötü"): menüden ve ders sayfasından kaldırıldı; kod duruyor, adres açık ama bağlantısız. Yeniden yapılacaksa önce tasarım onayı |
| Not / kalem / renklendirme, paylaşılan notlar | K01–K08 | ✅ Notlarım (yaz/kalem/fosforlu/silgi, renk etiketi, hesaba eşitleme); paylaşılan not (ortak) yok, paylaş = metni gönder |
| Topluluk: sohbet, yorumlar | L01–L06 | ✅ /topluluk: Genel + Kurul 1–6 kanalları, ders yorumları (ders ayrıntısı › Yorumlar), yanıt, sil, şikâyet |
| PDF oluştur sihirbazı + geçmiş | Y07–Y13 | ✅ /pdf-olustur (sesli · etkileşimli · arşiv → kurul → ortak TopluPdf penceresi), geçmiş cihazda |
| Arka plan işleri, hesap, güvenlik, verilerim, erişilebilirlik, komut paleti | AB01–AB18 | ✅ Erişilebilirlik sekmesi (hareket, yüksek kontrast, geniş aralık, alt çizgi, belirgin odak); hesap/veriler zaten vardı; komut paleti = ⌘K arama |

## Aşama 2 notları
- Merkez `components/v15/DerslerMerkezV15.tsx` (MerkezView v15'te buna döner): kurul seçici + branş çipleri, 4 araç kartı
  (sayılar: kuruldaki sesli ders, kuruldaki Öğren destesi), "Devam et" (kaldığın yer kayıtları; yoksa sıradaki ders),
  "Diğer araçlar" çekmecesi (Z02 ayrı sayfa yerine çekmece: ikincil iş).
- Branş: `BransV15.tsx`, adres değişmedi (`/dersler/canliders/kurulN/<branş>`; CanliDersView v15'te buna döner).
  Seçici: Dersler · Önem listesi (`/kamplar/kurulN/en-onemliler/<branş>`) · Çıkmışlar (`/sorular/soru-cozucu/kurulN/<branş>`).
- **Yeni sayfa** ders ayrıntısı: `DersDetayV15.tsx`, rota `ders_detay`, iç `/ders/<key>` ↔ görünen `/dersler/ders/kurulN/<key>`
  (siteHaritasi iki yön, gidiş-dönüş sınandı). Bölüm saatleri seçili sesin `zamanlama`sından; bölüme dokunmak sesli dersi
  `?p=<paragraf>` ile açar. v15 dışında sesli derse yönlenir.
- Ortak veri `dersVeri.ts` (liste, ilerleme = bitti işareti ya da kayıtlı konum / süre, branş/ders adresleri).
- Sesli ders listesinin branşsız hâli (B04) aşama 3'te.

## Aşama 3 notları (sesli ders)
- Önce tasarım: artifact v15.3 "S2 · Sesli ders v2" (12 ekran): ana ekran v2, terim kartı, çıkmış belirdi, kompakt çıkmış
  kartı, cevaplandı, Görünüm › PDF katmanları / Düzen, gruplu ders menüsü, kalem kutusu, oynatıcı seçenekleri, 8 panel türü,
  PDF üstü işaretler. README'de "Sesli ders v2" bölümü (denetimlerin yeri tablosu, çizim kuralları, panel amaçları).
- Kod: `components/canliDers/CdV15.tsx` (CdV15Bas, CdV15Gorunum, CdV15Menu, CdV15KalemDugme/Kutusu) +
  `styles/v15/sesli.css`; CanliDersDers v15'te bunları kullanır, davranış aynı. Geri düğmesi ders ayrıntısına döner.
- Odak ekranı: sesli ders açıkken kabuğun üst barı ve alt sekmesi çizilmez (ShellV15).
- PDF katmanlarına "Çıkmış soru işaretleri" (`cd-pdf-cikmis`) eklendi (tüm tasarımlarda görünür; çip bu anahtara bağlı).
- Çıkmış: v15'te `CikmisKart` (telefonda oynatıcının üstünde alt kart, ≤%64 yükseklik; PC'de sağda yüzen 440 px kart,
  perdesiz). Eski tasarımlarda `CikmisPencere` aynen.
- Yapılmadı (sonraki tur): "Çıkmış belirdi" oynatıcı şeridi, değer kartı panel türü (yalnız tasarımda), oynatıcı ⋯
  sheet'inin v15 biçimi (eski açılır menü duruyor), sesli ders listesi (B04).

## İç sayfalar (yapılan)
- Sesli ders listesi (B04): `v15/SesliListeV15.tsx` (`/dersler/canliders/kurulN`, branşsız).
- Ders özetleri (b2ozet): `v15/OzetlerV15.tsx` + `styles/v15/ozet.css`; LectureSummariesView v15 dalı, okuyucu aynı.
- Sınav spotları (B08): `v15/SpotsV15.tsx` + `styles/v15/spot.css` (önem rozetli kart ızgarası, ders/durum çipleri, Kendini sına, kartta ayrıntı, Öğrendim, Karta ekle, `?id=` derin bağlantı). ExamSpotsView v15 dalı.
- Başlangıç ekranı (En önemliler + Soru çözücü ortak `ui/Baslangic.tsx`): v15 dalı (devam kartı + halkalı branş kartları, başlık üst barda).
- En önemliler (B09): OnemListesi'ne `styles/v15/onem.css` katmanı (düz yüzey, tek vurgu) + üst bar başlığı; yapı zaten gezgin + madde tablosu.
- Sözlük (B10): GlossaryV12 (liste + bilgi kartı) üstüne `styles/v15/sozluk.css` (başlık üst barda, Newsreader okuma yazısı).
- Ezber kartları: FlashcardsV12 üstüne `styles/v15/kartlar.css` (hap düğmeler, büyük kart, Newsreader ön yüz) + üst bar başlığı.
- Notlarım (Çalışma masam › Notlar): NotesView'e `styles/v15/notlar.css` (sabit yükseklik; liste ve düzenleyici kendi alanında kayar). `/notlar` (Ders notları) öğrenciye kapalı, geçirilmedi.
- Bitirdiklerim: v15'te tanıtım başlığı, "nasıl kullanılır" adımları ve numaralı başlıklar yok; başlık üst barda, Sınav planı kartı, modüller hap şeridi (`styles/v15/bitir.css`).
- Çıkmış sorular (C07): CikmisV12 çerçevesine `styles/v15/cikmis.css` (başlık + sayı üst barda, hap denetimler).
- Soru çözücü (C06): başlangıç ortak Baslangic v15; branş sayfasına `styles/v15/cozucu.css` (başlık üst barda, satır ek düğmeleri tek satır kaydırılan şerit).
- Soru ekle / havuz (C10): PoolV12'ye `styles/v15/havuz.css` + üst bar başlığı; 4 adımlı Soru ekle çekmecesi değişmedi.
- Sınava hazırlan iç sayfaları (Kurul kampı + kamp ayrıntısı, Son Prova + ders, Patoloji Check Up, Sınav planı): ortak `styles/v15/kamp.css`
  (simge/h1 gizli, açıklama tek satır, düz yüzey) + `v15/V15BaslikYaz.tsx` (JSX'ten üst bar başlığı; iç sayfada ders/kamp adı).
- Başvuru iç sayfaları: Hastalıklar (DiseasesV12, sözlük katmanı `styles/v15/sozluk.css`), Kazanımlar (ortak PageToolbar kuralı
  `styles/v15/shell.css`: v15'te `.pt-h` başlığı üst barda, sayaç kalır — PageToolbar kullanan tüm eski sayfalara yayılır),
  Sağlık Bakanlığı (`styles/v15/saglik.css`, giriş bloğu simge/etiket/başlık gizli).
- Kişisel: Başarımlar ve İstatistiklerim başlığı üst barda (`styles/v15/shell.css`); Profil ve ayarlar yapısı (kullanıcı başlığı + sekmeler) tasarıma uygun, değişmedi.
- Dağıtım: 2026-10-27 commit bdaeb994, onem 385 (v15 isteğe bağlı).
- Öğren etkileşimleri (B07): `styles/v15/ogren.css` etkileşim katmanı (ls-ix kart, hap düğme, Newsreader soru kökü); katman artık LessonPlayer'da da yüklenir (derin bağlantıyla açılan destede eksikti). Açık deste odak ekranı (ShellV15 `odakEkrani`: üst bar + sekmeler gizli, dersin kendi çubukları).
- Olası sorular, KMB, Güncelleme günlüğü: başlık/simge üst barda (`styles/v15/shell.css`). Takvim sayfası sitede yok (`/takvim` → soru ekle); tasarımdaki D06 yeni sayfa olarak bekliyor.

## Gezinme (2026-10-27, kullanıcı isteği: geri dönüş kolay, alt çubuk standart uygulama gibi)
- `components/v15/gezinme.ts`: oturum içi geçmiş yığını + sekme başına son adres (sessionStorage).
- Üst bar: kök olmayan (Bugün/merkez dışı) her sayfada Geri; önce uygulama içi geçmiş, yoksa bölüm merkezi.
- Alt çubuk: Bugün · Ders · Soru · Sınav · Menü. Sekme kaldığın sayfayı açar, etkin sekmeye dokunmak merkeze döner;
  gizli "yeniden dokun / uzun bas" kalktı. Menü: Başvuru · Ben (masam, Bitirdiklerim, istatistik, başarımlar, ayarlar) · Araçlar.
- Kenar menüsü alt kısmı: Çalışma masam, Bitirdiklerim, İstatistiklerim, Başarımlar + ayarlar.

## Yeni sayfalar (kuruldu)
- Sınav takvimi (D06 + J zaman çizelgesi): `v15/SinavTakvimiV15.tsx` + `styles/v15/takvim.css`; rota `sinav_takvimi`, iç `/takvim` ↔
  görünen `/kamplar/takvim`; merkezModel kamplar + navModel (Sınava hazırlan). Sıradaki sınav (kalan gün, kurul ilerlemesi),
  T‑5/T‑3/T‑1 hazırlık günleri (Son Prova / Çıkmış çözücü / En önemliler'e götürür), yılın sınavları.
- Soru haritası (b2harita): `v15/SoruHaritasiV15.tsx` + `styles/v15/harita.css`; rota `soru_haritasi` (/soru-haritasi ↔ /sorular/soru-haritasi).
  Dizin `src/data/soru_haritasi.json` ← `scripts/v15/soru_haritasi.py` (pastQuestions.json sayımı; çıkmış verisi değişince yeniden çalıştır).
  Hücre → `/sorular/cikmis?kurul=&ders=&yil=` (PastExamsView `?ders=`/`?yil=` ile süzgeç başlatır).
- Yüzen kronometre (T): `v15/KronometreV15.tsx` + `styles/v15/kronometre.css`; Menü › Araçlar ve kenar menüsünden (`kronometreAc`).
  Başlat/duraklat, tur, bitir (geçmiş 50 oturum, localStorage), sistem süresinden ayrı. Odak ekranında (sesli ders) gizli.
  Yapılmadı: çalışma kapsülü (U, ses oynatıcıyla birleşme), Profil › Kronometre geçmişi ekranı.

## Kalan iç sayfalar (kullanıcı kararı 2026-10-27: eski görünümün hepsi v15'e geçecek)
Tasarımı olan: sesli ders listesi (B04), Öğren etkileşimleri (B07), spotlar (B08), önem (B09), sözlük (B10), notlar (B11),
Bitirdiklerim (B12), çıkmışlar (C07), soru çözücü (C06), soru ekle (C10), kamp aşamaları (D02), Check Up (D03), Son Prova (D04),
60 planı (D05), takvim (D06), olası (D07), KMB (E01–E05), Sağlık Bakanlığı (G02), profil/ayarlar/başarım/çevrimdışı (G04–G07),
istatistik (X), sıralama (M07), güncellemeler (AB15).
Tasarımı v15.4'te eklenen (B2, artifact sürüm 18): Ders özetleri + okuyucu, Hastalıklar (anatomiden gez) + ayrıntı, Kazanımlar,
Örnek sorular, Öncelikli dersler, Soru haritası, Çalışma masam, Çalışma müziği.

## Her aşamanın kapısı
`npx tsc --noEmit` 0 · 390/820/1366 genişlikte taşma 0, konsol hatası 0 · açık + koyu tema ekran görüntüsü ·
kullanıcı onayı. Dağıtım yalnız `deploy/oracle/dagit.sh` (onem +1), kullanıcı isterse.

- **Ders programı** `DersProgramiV15.tsx` + `styles/v15/program.css`, rota `ders_programi` (`/program` ↔ `/dersler/program`). Veri `src/data/dersler/kN.json`; sesli dersi olan satır ders ayrıntısına gider. Kurul 1 kaydında saat yok (—).
- **Çalışma grafikleri** `CalismaGrafikleriV15.tsx` + `styles/v15/grafik.css`: İstatistiklerim tepesinde (yalnız v15), sayfanın 7/30 gün seçimine bağlı; özet kutuları, günlük süre çubukları (dokun/üzerine gel → gün ayrıntısı), modül dağılımı. Veri calismaTakip.
- **Oyunlar** `OyunlarV15.tsx` + `styles/v15/oyun.css`, rota `oyunlar` (`/oyunlar` ↔ `/sorular/oyunlar?oda=KOD`). Sunucu `services/quiz/quizRealtimeServer` (/api/quiz/ws) + soru kaynağı `services/quiz/oyunSoruKaynagi.ts` (sesli çözücü setleri, kök ≤220 karakter, LLM yok), `GET /api/oyun/kaynaklar`. Oda RAM'de; kopan oyuncu oyun sürerken puanıyla kalır.
- **Notlarım** `NotlarimV15.tsx` + `styles/v15/notlarim.css`, rota `notlarim` (`/notlarim?not=<id>`), Menü › Ben. Anahtarlar `medsoru_notlarim_v1` + `medsoru_notlarim_cizim:<id>` userKvSync'te. Tuval yüksekliği `clientHeight` (scrollHeight tuvali sonsuz büyütür).
- **PDF oluştur** `PdfSihirbaziV15.tsx` + `styles/v15/pdfsihirbaz.css`, rota `pdf_olustur` (`/pdf-olustur`), Menü › Araçlar (eski "PDF" düğmesi "Soru kitapçığı" oldu). TopluPdf'e `dugmeYazi`/`onBitti`, pencere body'ye portal.
- **Topluluk** `ToplulukV15.tsx` + `styles/v15/topluluk.css`, rota `topluluk` (`/topluluk?kanal=genel|kurul-N|ders:<key>`). Sunucu `services/topluluk.ts` + `deploy/pg/sql/topluluk.sql` (açılışta uygulanır); yazma doğrulanmış Firebase uid ile, STUDENT_WRITE_ROUTES'ta; GET'ler jeton taşır (adminFetchAuth ogrenciJetonu). Dışarı uid/e-posta çıkmaz.
- **Hücrem** `HucremV15.tsx` + `styles/v15/hucrem.css`, rota `hucrem`. Basamaklar `src/data/basarim/tanim.json` (fiyat 50+15·i, toplam 7.070 mol); motor `satinAl` önceki basamağı ister. Mağaza ekranı hucre türünü listelemez.
- **Zihin haritası** `ZihinHaritasiV15.tsx` + `styles/v15/zihin.css`, rota `zihin_haritasi` (`/zihin-haritasi?ders=<key>` ↔ `/dersler/zihin-haritasi`). Ders ayrıntısında "Zihin haritası" satırı.
