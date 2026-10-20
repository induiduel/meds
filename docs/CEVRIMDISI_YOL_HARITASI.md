# Çevrimdışı çalışma — analiz ve yol haritası (2026-10-20)

Amaç: kullanıcı bir içeriği indirdiğinde o içerik **internetsiz, eksiksiz ve hatasız** çalışsın; indirmesi gereken her şey
(kod, veri, ses, PDF, sistem dosyaları, yazı tipleri, simgeler, bağımlı içerik) kendiliğinden insin.

Altyapı: katalog `src/services/cevrimdisiKatalog.ts` (sunucu) → motor `src/services/cevrimdisi/paketMotoru.ts`
(+ `uyarlayicilar.ts`: sesli ders, soru veritabanı) → önbellek `medsor-paket-v1` → `public/sw.js` sunar.
Sınama: `scripts/cevrimdisi_sinama/` (aşağıda).

## 1. Özellik × indirilmesi gerekenler

| Özellik (rota) | Paket | İçerik | Not |
|---|---|---|---|
| Uygulama kabuğu (her sayfa) | `uygulama` (zorunlu) | tüm kod parçaları, CSS, index.html, **branş/ders dizinleri** (spot/çözücü/asistan/önem `index.json`, `cozucu_ogren`, sınav çalışması/örnek soru dizinleri), simgeler + manifest, sessiz klip, **Google yazı tipleri** (CSS + latin/latin-ext woff2) | dizinler ve yazı tipleri 2026-10-20'de eklendi |
| Etkileşimli ders `/ogren/<id>` | `ogren:<id>` | deste JSON, EMA sesleri (isteğe bağlı), ders PDF'leri + eşleme + PDF.js yardımcıları (isteğe bağlı) | |
| Soru çözücü `/soru-cozucu` | `cozucu:<branş>:<kod>` | ders JSON, dizin, Öğren eşlemesi, klipler + ortak klipler | |
| En önemliler + sesli asistan `/en-onemliler` | `onem:<branş>:<kod>` | önem listesi, asistan JSON + klipler | |
| Alternatif çözücü | `alt:<kod>` | ders JSON + klipler | |
| Sesli ders `/canliders/<key>` | `sesli:<key>` | ses (tercih edilen varyant), konuşma metni, PDF | ayrı sistem: `canliDersCevrimdisi.ts` |
| TBG sınav kampı `/genetik-check-up` | `sayfa:tbg-kampi` → **bağımlı** `sesli:k1-70-tbg-sinav-kampi` | g07 asistan klipleri + sesli ders | bağımlılık alanı (`bagimli`) 2026-10-20 |
| Kurul kampı `/kamp` | `kamp:<kurul>:<branş>` | kamp JSON + EMA klipleri | kamp verisi üretilince kendiliğinden listelenir |
| Olası sorular | `veri:olasi` | özet + yayımlanmış kurul setleri | set yayımlanınca listelenir |
| Çıkmış / Test / Soru havuzu | `db:sorular` | IndexedDB (offlineDatabaseService) | |
| Sözlük, hastalıklar, kartlar | `veri:sozluk`, `veri:spot` | | |
| Ders özetleri / notları / kazanımlar / sınav çalışması / örnek sorular / Sağlık Bakanlığı | `veri:ozet`, `veri:notlar`, `veri:kazanim`, `veri:sinav`, `veri:ornek`, `veri:saglik` | | |
| Kullanıcı verisi (notlar, ilerleme, istatistik) | — | cihazda (localStorage/IndexedDB); bağlantı gelince eşitlenir | sunucu yedeği internetsizken sessizce bekler |

İnternet gerektiren (çevrimdışında bilerek kapalı): yapay zekâ sohbeti/yazım yardımcısı modeli, sıralama, müzik akışı, canlı
olaylar (SSE), yönetim paneli, soru ekleme gönderimi (kuyruğa alınır, bağlantı gelince gider).

## 2. Bulunan ve düzeltilen hatalar (2026-10-20)

1. **İndirilen uygulama kabuğu siliniyordu (kritik).** `index.html` içindeki "taze yükleme" betiği, Wi-Fi bağlı ama internet
   yokken (`navigator.onLine` true) herhangi bir `Failed to fetch` hatasında `/index.html`'i **tüm** önbelleklerden (çevrimdışı
   paketi dahil) siliyordu → sonraki her sayfa "MeDSor Çevrimdışı Mod" yedek ekranına düşüyordu. Artık yalnız sunucu gerçekten
   yanıt verirse (`/api/surum`, SW'den geçmez) ve kullanıcı önbelleklerine dokunmadan çalışır; genel "Failed to fetch" tetiklemez.
2. **Gerçek bağlantı denetimi** (`services/cevrimdisi/baglanti.ts`): parça yüklenemediğinde yenileme kararı (App.wrapLazy,
   kök hata sınırı, vite:preloadError) sunucuya ulaşılıyorsa verilir; yoksa "cihazında yok" ekranı. O ekran 'online' olayı
   gelmese de sunucu dönünce kendini açar.
3. **Liste ekranları tek branş inmişken açılmıyordu** (spotlar, en önemliler, soru çözücü, alternatif çözücü, sınav çalışması,
   istatistik, bitirdiklerim): tüm branşların dizin parçaları istenir. Dizinler uygulama paketine alındı.
4. **Yanlış "Bağlantı geri geldi"**: SW'nin cihazdaki kopyaları başarılı yanıt sayılıyordu. SW internetsiz 503'e
   `X-Cevrimdisi`, paket kopyasına `X-From-Cache` ekler; `net.ts` bunlarla "çevrimdışı" gösterir.
5. Internetsiz yedekleme denemesi konsola hata yazıyordu (uyarıya indirildi).
6. Google yazı tipi CSS'i hiç önbelleğe alınmıyordu (internetsiz açılışta sistem yazı tipi). SW + uygulama paketi.

## 3. Sınama düzeneği (`scripts/cevrimdisi_sinama/`)

- `vekil.mjs` — `:3100 → :3000` vekil; denetim `:3101/kapat|ac`. Kapalıyken bağlantılar anında kesilir: tarayıcı ve SW gerçek ağ
  hatası görür, `navigator.onLine` true kalır (en zor durum: Wi-Fi var, internet yok). Ayrı köken → SW/önbellekler bağımsız.
- `envanter.mjs` — çevrimiçi: her rotanın istediği adresler, kataloğun kapsamadıkları.
- `sinama.mjs` — temiz profil → paketler uygulamanın kendi motoruyla iner (`window.__medsorCevrimdisi`) → ağ kesilir → 34 rota:
  konsol hatası, düşen istek, hata metni, "cihazında yok", boş ekran, kabuk varlığı; ekran görüntüleri.
- `etkilesim.mjs` — internetsiz eylemler: Öğren ilerleme/ses/PDF, çözücü/asistan/alternatif ses, sesli ders oynatma, çıkmış
  cevap, arama, test.

Çalıştırma: `node scripts/cevrimdisi_sinama/vekil.mjs &` sonra `node scripts/cevrimdisi_sinama/sinama.mjs && node scripts/cevrimdisi_sinama/etkilesim.mjs`.

## 4. Yol haritası (kalanlar)

- [ ] Sınama sonuçlarındaki kalan eksikler (etkileşim senaryoları) — `DEGISIKLIK_KAYDI.md`'de güncel durum.
- [ ] Oracle'da (gerçek SW, HTTPS, telefon) uçak modu sınaması: sesli ders + çözücü + Öğren PDF.
- [ ] "Bu sayfayı çevrimdışı kullan" kısayolu: liste ekranlarında sayfanın gerektirdiği paket kümesini tek dokunuşla indir.
- [ ] Bağımlılık alanının genişletilmesi (ör. Öğren dersi → aynı dersin çözücü/asistan paketleri isteğe bağlı öneri).
- [ ] Gece hattı yeni bir içerik türü eklediğinde katalog kapsam denetimi: `envanter.mjs` çıktısında "eksik" API'ler 0 olmalı
      (bilerek çevrimiçi olanlar hariç listesiyle).
