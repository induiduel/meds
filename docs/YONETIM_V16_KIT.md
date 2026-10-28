# Yönetim v16 — kabuk, kit ve sunucu yardımcıları

> Plan: `docs/YONETIM_V16_PLAN.md`. Bu belge sayfa ajanları içindir: **yeni sayfayı bu temelin üstüne kurun, kabuğa ve kite dokunmadan.**
> Kit ya da kabukta değişiklik gerekiyorsa küçük, geriye uyumlu tutun ve bu belgeyi güncelleyin.

## 0. Dosyalar

| Ne | Yol |
|---|---|
| Kabuk | `src/components/manage16/ManageV16.tsx` |
| Menü + rota + eski adres tablosu (TEK KAYNAK) | `src/components/manage16/menu.ts` |
| Kit (tek giriş) | `src/components/manage16/kit/index.ts` (+ `kit.css`) |
| Sayfalar | `src/components/manage16/sayfalar/<Ad>.tsx` (ör. `GenelBakis.tsx`, örnek liste sayfası `Denetim.tsx`) |
| Sunucu | `src/services/yonetim16/{denetim,sayfalama,atomikJson,siteAyar,ozet}.ts` |
| Şema | `deploy/pg/sql/yonetim16.sql` (açılışta kendiliğinden uygulanır) |
| İstemci site ayarı | `src/services/siteAyar.ts` |

Giriş (2026-10-28, H131): `/manage*` ayrı Vite girişi `manage.html` → `src/manage-main.tsx` (öğrenci App.tsx/index.css YÜKLENMEZ;
ilk yük ≤ 200 KB gzip). Sayfalar öğrenci uygulamasının ağır modüllerini (index.css sınıfları, Toast, api.ts) statik içe aktarmaz;
yalnız kit + `services/*` hafif yardımcılar. Temel CSS: `src/styles/yonetim-temel.css` (Tailwind yardımcı sınıfı yok).
App.tsx: uygulama içinden `/manage`'e geçiş tam sayfa gezinmesidir. Moderatörde ya da `?kabuk=v14` ile manage-main tam uygulamayı yükler ve eski konsol açılır (oturum boyunca hatırlanır; `?kabuk=v16` geri döndürür).
Moderatör ve `/yonetim` girişi hâlâ eski `ManageConsole`'dadır.

## 1. Adres şeması

`/manage/<grup>/<sayfa>[/<id>...]`. Çözüm `menu.ts::adresCoz` ile en uzun yol eşleşmesidir; kalan parçalar sayfaya `altYol`, ilki `id` olarak gelir.
Örnek: `/manage/kisi/abc123` → sayfa `kisi`, `id = 'abc123'`. `/manage/sistem` → grubun ilk sayfasına yönlenir.
Eski v14 adresleri (`ESKI_ADRES`) `replaceState` ile yeni adrese geçer (`kisiler/<k>` → `kisi/<k>`).
Bilinmeyen adres → "Sayfa bulunamadı".

## 2. Sayfa ekleme (3 adım)

1. `src/components/manage16/sayfalar/KisiListe.tsx` yazın; **varsayılan dışa aktarım** ve `SayfaProps` alır:
   ```tsx
   import type { SayfaProps } from '../menu';
   import { SayfaBasligi, VeriTablosu } from '../kit';
   export default function KisiListe({ id, altYol, git }: SayfaProps) { … }
   ```
2. `menu.ts`'de ilgili sayfa satırına `yukle: () => import('./sayfalar/KisiListe')` ekleyin. (Satır zaten var; yalnız `yukle` eklenir.
   Yeni sayfa gerekiyorsa plandaki adresle yeni satır.) `yukle` olmayan sayfa menüde "yakında" görünür.
3. `nice timeout 1500 npx tsc --noEmit` temiz + `npx vite build`. Sunucu kodu değiştiyse `systemctl --user restart meds-web` (kural 12).

Kurallar:
- Her sayfa kendi yığınıdır (`React.lazy`). **Sayfadan başka sayfayı statik import etmeyin**; ortak parça kite gider.
- Panel içi gezinme yalnız `git('kisi/abc')` / `git('sistem/denetim?hedef=x')` ile (tam sayfa yenilemesi yok). Bağlantılarda `href={manageAdres(yol)}` + `onClick` ile `git`.
- Sayfa durumu adreste: `VeriTablosu` `?q=&sayfa=&sirala=&yon=&s.<süzgeç>=` tutar. Ayrıntı için `/<id>` alt yolunu kullanın (paylaşılabilir bağlantı).
- Global durum yok: veri `useAdminSorgu` ile sayfada. `questions` gibi büyük dizileri istemcide tutmayın; uç sayfalasın.
- Türkçe metin; renk yalnız `--color-*` tokenları (kit sınıfları zaten öyle). Sınıf öneki `m16-`.
- Adlandırma: dosya/bileşen Türkçe PascalCase (`SohbetOdalari.tsx`), uç `/api/admin/<grup>/<kaynak>`, SSE olayı `<konu>_changed`.

## 3. Veri katmanı (`kit/api.ts`)

- `adminIstek<T>(yol, { yontem, govde, sorgu, sinyal })` → JSON; 2xx dışı ya da HTML (uç hedefte yok) → `AdminHata` (`.durum`).
  Ön eksiz `fetch('/api/...')` kullanır: yerel panelde Canlı seçiliyse istek Oracle vekiline gider, yönetici jetonu kendiliğinden eklenir.
  **`safeJsonFetch` kullanmayın** (vekil başlığını atlar).
- `useAdminSorgu<T>(yol | null, { sorgu, canliOlay: ['olay_changed'], aralikMs })` → `{ veri, yukleniyor, hata, yenile, setVeri }`.
  Bellek önbelleği (SWR); `canliOlay` SSE gelince ve `resync`'te yeniden çeker.
- Liste yanıtı tipi: `ListeYaniti<T> = { ogeler, toplam, sayfa, boyut, yuzler? }`.

**Canlı/Yerel:** localhost'ta varsayılan Canlı (Oracle). Yeni uçlarınız Oracle'a dağıtılmadan "Canlı"da HTML döner → kit "Uç bulunamadı"
gösterir. Geliştirirken üst bardan **Yerel**'e alın; işiniz bitince `localStorage.medsoru_panel_hedef='oracle'` olarak bırakın.
Cihaza özel uçlar `config/deployment.ts::PANEL_DEVICE_ONLY` listesindedir.

## 4. Kit bileşenleri (`import { … } from '../kit'`)

| Bileşen | Öz API |
|---|---|
| `SayfaBasligi` | `baslik`, `aciklama?`, `eylemler?` (sağdaki düğmeler), `children?` (sekme/süzgeç alanı) |
| `VeriTablosu<T>` | `kimlik` (sütun seçimi kaydı), `sutunlar: Sutun<T>[]`, `satirKimligi`, **`kaynak`** (sunucu kipi) **ya da** `ogeler` (yerel kip, küçük listeler), `ekSorgu?`, `suzgecler?: {anahtar, etiket, secenekler}[]` (çip; sunucuya `s.<anahtar>`), `secim?` + `topluEylemler?(seciliIdler, temizle)`, `satirTikla?`, `etkin?`, `canliOlay?`, `aramaYeri?`, `boyut?` (50), `aracEk?`, `adresteDurum?` (true). 120 satırı aşan sayfada sanal kaydırma. Klavye: satırda Enter aç, Boşluk seç, ↑/↓ gez. |
| `Sutun<T>` | `anahtar`, `baslik`, `hucre?(t)`, `sirala?: true \| 'sunucuAnahtari'`, `genislik?` ('120px', 'minmax(200px,2fr)'), `gizli?`, `hizala?: 'sag'\|'orta'`, `deger?(t)` (yerel kip sıralama/arama) |
| `AyrintiCekmecesi` | `acik`, `kapat`, `baslik`, `altBaslik?`, `children` (Alanlar sekmesi), `kayit?` (JSON sekmesi), `hedef?` (Geçmiş sekmesi = denetim kaydı), `ekSekmeler?`, `eylemler?` (alt çubuk), `kirli?` (kapatırken onay), `genis?`. Esc kapatır. |
| `Form` | `alanlar: AlanTanim[]`, `deger`, `kaydet(yeni, degisen)` (fırlatılan hata formda gösterilir), `iptal?`, `kaydetMetni?`, `kirliDegisti?` (çekmeceye `kirli` vermek için). Alan türleri: `metin uzun sayi secim anahtar etiketler tarih json`; `zorunlu enAz enFazla desen dogrula ipucu salt`. Kirliyken sekme kapatma uyarısı (`useKirliUyari`). |
| `onayIste(o)` | `Promise<boolean>`. Tehlikeli işlemde `{ baslik, aciklama, tehlikeli: true, yazilacak: 'SIFIRLA', onayMetni }` → kullanıcı sözcüğü yazmadan düğme açılmaz. Kabukta `OnayHost` takılı. |
| `TopluIslem` | `secili`, `temizle`, `children` (düğmeler). VeriTablosu `topluEylemler` ile kendisi kullanır. |
| `JsonGoruntuleyici` / `JsonDuzenleyici` | `veri`, `enYuksek?` / `deger`, `kaydet(yeni)`, `iptal?` (geçersiz JSON'da kaydet kapalı) |
| `DegisiklikGecmisi` | `hedef?` ya da `uc?` (önek), `boyut?` — denetim kaydından; fark varsa önce/sonra gösterir |
| `BosDurum`, `Yukleniyor` (`satir?` iskelet), `Hata` (`hata`, `yenile?`; 401/403 = "Yetki yok") | durum ekranları |
| `Rozet` (`ton`), `Durum` (noktalı), `durumTonu(httpKodu)` | ton: `notr iyi uyari kotu vurgu bilgi` |
| `IstatistikKart` (`etiket deger alt? ton? ikon? onClick? yukleniyor?`), `IstatistikIzgara` | sayı kartları |
| `bildir(metin, 'iyi'\|'kotu'\|'bilgi')` | kısa bildirim (kabukta `BildirimHost`) |
| `zamanMetni(iso)` | "3 dk önce" |

CSS yardımcıları: `.m16-kart` (kutu, içinde `h2`), `.m16-btn` (+ `birincil`, `tehlike`, `hayalet`, `ikon`), `.m16-girdi`, `.m16-izgara-2`,
`.m16-liste`, `.m16-satirlar` (dt/dd), `.m16-cip`.

## 5. Sunucu yardımcıları

### 5.1 Sayfalama (`yonetim16/sayfalama.ts`)
```ts
const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 500 }); // {sayfa, boyut, q, sirala, yon, suzgec}
// JSON dosyası / bellekteki dizi:
res.json(diziSayfala(liste, s, {
  araMetni: (x) => `${x.id} ${x.ad}`,
  siralayicilar: { ad: (x) => x.ad, at: (x) => x.at },
  suzgecler: { durum: (x, v) => x.durum === v },
  yuzler: { durum: (x) => x.durum },   // çip sayıları
  eslestir: (x) => ({ id: x.id, ad: x.ad }), // listeye hafif satır
}));
// meds-pg tablosu (sütun adları izin listesinden; değerler parametreli):
const q = pgSayfaSorgusu(s, { tablo: 'public.topluluk_mesajlar', araSutunlari: ['metin'], siralanabilir: ['at'], varsayilanSira: 'at', suzgecSutunlari: { oda: 'oda_id' } });
const [{ rows }, c] = await Promise.all([pgDb.query(q.veri, q.degerler), pgDb.query(q.sayim, q.degerler)]);
res.json({ ogeler: rows, toplam: c.rows[0].n, sayfa: s.sayfa, boyut: s.boyut });
```

### 5.2 Atomik JSON (`yonetim16/atomikJson.ts`)
- `await atomikJsonYaz(dosya, veri, { yedek: 2, yedekKlasoru?, girinti?, bosYazma? })` — dosya başına kilit, geçici dosya + fsync + rename.
- `await atomikJsonGuncelle<T>(dosya, (eski) => yeni)` — oku-değiştir-yaz kilit içinde (yarış yok).
- Boş dizi/nesne yazımı varsayılan **reddedilir** (CLAUDE.md "boş sonuçla ezme").
- `data/content/` altındaki dosyada `yedekKlasoru`'nu katman DIŞINA verin (`data/_yedek/<ad>`): eşitleme betiği katmandaki her `.json`'u yerele çeker.
- Mevcut büyük yazma yollarına (pastQuestions, desteler) bağlamak ayrı iştir; o yolu değiştiren sayfa ajanı `fs.writeFileSync`'i bununla değiştirebilir.

### 5.3 Denetim (`yonetim16/denetim.ts`)
- Ara katman **otomatik**: tüm `POST/PUT/PATCH/DELETE /api/admin/*` (+ `/api/notebooklm/manage`, `/api/sesli-anlatim/yerel` yönetici uçları,
  `/api/canli-ders/video-is`, `/api/system/services`) ve `KISISEL_OKUMA` desenlerine uyan GET'ler kaydedilir. Sizin bir şey yapmanız gerekmez.
- Kişisel veri okuyan **yeni** GET ucu yazıyorsanız (`/api/admin/user-data/…`, `/api/admin/topluluk/mesajlar…`, `/api/admin/people/:key` zaten listede)
  desen `KISISEL_OKUMA`'ya eklenmeli. Makine yoklaması yapan yazma uçlarını `ATLA`'ya ekleyin (gürültü).
- Uç içinde: `denetimHedef(res, 'ders:k2-07')`, `denetimFark(res, onceki, sonraki)` (değişen alanlar önce/sonra), `denetimNot(res, {silinen: 12})`.
  Elle satır: `denetimKaydet(req, { tur, uc, hedef, ozet })`. Gizli alan adları (`pass|token|secret|key…`) maskelenir, gövde ~4 KB'a kırpılır.
- Hedef adlandırma: `<tür>:<kimlik>` — `kisi:<uid>`, `soru:<id>`, `ders:<id>`, `oda:<id>`, `site-ayar`.
- Okuma: `GET /api/admin/denetim?sayfa&boyut&hedef&uc(önek)&kim&tur=yazma|okuma&durum=hata&yontem&q&sirala=at|uc|kim|durum|sure_ms&yon`.
- SSE (yalnız yönetici): `denetim_eklendi`. pg kapalıyken satırlar `data/yonetici_denetim.jsonl`'a düşer.
- Kayıt, isteği **alan** sunucuda tutulur: yerel panel Canlı'dayken kayıt Oracle'dadır (kim = `panel-anahtarı` görünebilir).

### 5.4 Site ayarı (`yonetim16/siteAyar.ts` + istemci `services/siteAyar.ts`)
Şema (`src/data/site_ayar.json` varsayılan; panel yazımı `data/content/site_ayar.json`):
```json
{ "surum": 3, "guncellendi": "…", "guncelleyen": "…",
  "sayfalar":   { "sinav_calisma": "acik|gizli|kapali" },
  "bayraklar":  { "quiz_cok_oyunculu": true },
  "gorunurluk": { "ders:k2-07": "acik|gizli|yalniz-yonetici", "kurul:3": "gizli" },
  "duyuru": { "acik": true, "metin": "…", "ton": "bilgi|uyari|hata", "baglanti": "/…", "bitis": "ISO" },
  "bakim": { "acik": false, "sure": "15 dk" } }
```
- `GET /api/site-ayar` (herkese, bellek önbelleği + ETag, SW baypas), `GET /api/admin/site-ayar`, `PUT /api/admin/site-ayar` (kısmi; haritada
  `null` = anahtarı sil → derleme varsayılanı). Geçersiz değer 400. Yazım denetime fark olarak düşer. SSE `site_ayar_changed` (herkese).
- Bakım: `PUT {bakim:{acik,sure}}` ya da eski `POST /api/admin/bakim` — ikisi de kalıcı; sunucu açılışta kalıcı durumu uygular.
- İstemci: `sayfaGizli(route)`, `sayfaKapali(route)`, `bayrak(ad, varsayilan)`, `gorunurluk('ders:k2-07')`, `useSiteAyar()` (yeniden çizim).
  Açılışta localStorage'dan senkron okunur; derleme sabitleri (`GIZLI_SAYFALAR`/`KAPALI_SAYFALAR`) varsayılandır. App.tsx rota koruması buna bağlı.
  **Menü çalışma anında süzülür (2026-10-28):** `menudeGorunur(route)` — navModel (NAV_TREE/MORE_TREE/V12_*), merkezModel
  (MERKEZ_ARACLARI/CHECKUPLAR) ve navV15 (V15_SECTIONS) dizileri `siteAyarAbone` ile YERİNDE yeniden hesaplanır; bileşen `useSiteAyar` ile çizilir.
  Yeni sabit sayfa listesi yazan bileşen `menudeGorunur` ile süzmelidir (DerslerMerkezV15 ANA gibi). Derleme varsayılanları `merkez/sayfaSabitleri.ts`.
  Sayfa durumları: `acik | gizli | kapali | yalniz-yonetici` (+ `menu[route]=false` yalnız menüden kaldırır). App.tsx: `sayfaYonlendir` → Bugün,
  kapalıda içerik `gorunenTab` ile hiç kurulmaz. Duyuru bandı `components/system/DuyuruBandi.tsx` (baslangic/bitis/kurul/kapatilabilir).
  **Bayraklar** (yoksa açık): sunucu kapısı `bayrakKapisi` (BAYRAKLAR + BAYRAK_UC: oyunlar, topluluk_sohbet, topluluk_mesaj, arkadaslik,
  siralama_herkese, kayit_acik, not_paylas), istemci `BAYRAK_SAYFA` (sayfa gizleme), oyun: `oyun_mod_<id>`, `oyun_kaynak_<brans>`.
  Uçlar: `GET /api/admin/site-ayar/bayraklar`, `GET /api/admin/site/surum`, `GET|DELETE /api/admin/quiz/odalar[/:id]`, `GET /api/admin/quiz/{kaynaklar,modlar}`.
- Dağıtım: `data/content/site_ayar.json` [0b] eşitlemesiyle (`deploy/oracle/content-overlay-sync.sh`, katmandaki her .json) yerel
  `src/data/site_ayar.json`'a çekilir → commit'leyin. Yeni panel-yazılır içerik dosyası da aynı yolu izler: `src/data`'da varsayılan dosya
  (yoksa eşitleme DURUR) + `resolveContent`/`writableContent`.

### 5.5 Genel bakış ucu
`GET /api/admin/ozet[?taze=1]` (30 sn önbellek): `saglik{pg,calismaSn,yiginMb,rssMb,yuk,sseIstemci,sunucu}`, `kullanici{simdi,bugun,hafta}`,
`bekleyen{sikayet,geriBildirim,tuyo,onarim,faz14}`, `hata{istemci24s}`, `site{bakim,duyuru,gizliSayfa}`, `surum{onem,baslik,commit,dagitim}`, `sonDenetim[]`.
Yeni sayaç: `registerOzetRoutes` bağımlılıklarına işlev ekleyin (server.ts "Yönetim v16 temeli" bloğu).

## 6. Yeni uç yazarken kontrol listesi
- `requireAdmin` (moderatöre açıksa `requireModeratorOrAdmin`), liste ucu `listeSorgusu` + `ListeYaniti` biçimi, varsayılan 50 satır.
- İçerik yazımı `data/content` katmanına + `atomikJsonGuncelle` + SSE olayı; JSON tam dosya dökümü istemciye gönderilmez.
- Tehlikeli işlem: istemcide `onayIste({ yazilacak })`; sunucuda da gövdede onay sözcüğü isteyin.
- LLM tetikleyen uç (kural 20): zamanlayıcı yok, yalnız elle; `llm_kilit` kurallarına uyun.
- Kişisel veri okuması → `KISISEL_OKUMA` deseni.
- Sunucu değişince `systemctl --user restart meds-web`; commit/dağıtım kullanıcıda.

## 7. İçerik grupları (Kurullar ve dersler, Öğrenme, Kaynaklar — 2026-10-28)
- Sunucu: `src/services/yonetim16/icerik.ts` (`registerIcerik16Routes`): `/api/admin/kurullar`, `/dersler[/:id]`, `/branslar`, `/sesli-dersler`,
  `/spot-cozucu`, `/ders-icerik`, `/sinav-dagilimi`, `/k16/katalog/:varlik[/meta|/:id]` (katalog varlıkları `dataCatalogService.katalogErisimi`
  üzerinden + `spot`, `kisaltma`, `terim`, `saglik` bağdaştırıcıları). Yazma yalnız tek kayıt; `data/content` + `atomikJsonGuncelle`, yedek `data/_yedek/<ad>`.
- Kit: `KatalogSayfasi` (katalog varlığı için hazır liste + çekmece + form), `GorunurlukRozeti`/`GorunurlukBaglantisi` (H320: seçici kaldırıldı, bkz. §8b; site-ayar `gorunurluk`
  anahtarları: `ders:<id>`, `kurul:<n>`, `deste:<id>`, `sesli:<key>`, `paket:<key>`, `onem|asistan|cozucu:<dizin>/<kod>`).
- **Öğrenci tarafında uygulanır (2026-10-28), bkz. §8.** Kurul takvimi, ders defteri
  ve sınav dağılımı ön yüzde derlemede okunur: panel düzenlemesi canlıya dağıtımdaki katman eşitlemesi + derlemeyle yansır.

## 8. İçerik görünürlüğü (öğrenci tarafı, 2026-10-28)
- Kural TEK yerde: `src/services/icerikGorunurlukKural.ts` (saf; istemci + sunucu). `icerikDurumu(g, tur, id)` en kısıtlayıcı durumu verir:
  doğrudan anahtar + **kalıtım** — kimlikten ders (`k2-07`; sesli anahtarı, `k2p-k2-07-…` deste, paket) ve kurul (`k<N>`; önem/asistan/çözücü
  dizini `k<N>…` değilse kurul 1). `gizli` ve `yalniz-yonetici` öğrenciye ikisi de kapalı.
- İstemci: `icerikGizli(tur, id)`, `kurulGizli(n)` (`services/siteAyar.ts`; yönetici her şeyi görür). Bileşen `useSiteAyar()` ile abone olmalı.
  Uygulanan yerler: `v15/dersVeri.ts::useDersListesi` (merkez, sesli liste, branş, ders detayı, video, program), `DersDetayV15`/`CanliDersView`
  (adresle açılınca kapalı ekranı), `v15/dersIcerik.ts` (paket sekmeleri), `InteractiveDeckView` (kitaplık + deste açılışı), `KurulSecV15` ve
  `kurul/KurulSecici` (gizli kurul seçilemez, `varsayilanKurul` atlar), `DerslerMerkezV15` (gizli kurul → kapalı ekranı),
  `spots/{onem/onemVeri,cozucu/cozucuVeri,asistan/asistanVeri}.ts` (dizin süzülür, ders dosyası açılmaz).
- Kapalı ekranı: `v15/IcerikKapaliV15.tsx` (`ne`, `geri`). Yeni öğrenci listesi yazan bileşen aynı yardımcıyla süzmelidir.
- Sunucu: `yonetim16/siteAyar.ts::icerikKapisi` (server.ts'de bayrakKapisi'nın ardından). `GET /api/canli-ders/:key[/…]`, `/api/canli-ders/ses/:key/…`,
  `/api/decks|ogren|interactive-decks/:id` → 403 `{ icerikKapali: true }`; `/api/canli-ders`, `/api/canli-ders/ara` (`sonuc[].k`) ve `/api/decks` listeleri süzülür (ETag/304 kapalı,
  `Cache-Control: private, no-cache`). Gerçek loopback / panel anahtarı / yönetici jetonu yönetici sayılır (süzme yok). Önem/asistan/çözücü ve
  ders içerik paketi ön yüz paketinde olduğundan yalnız istemcide süzülür. `cdDetayGetir` 403'te cihazdaki çevrimdışı kopyaya düşmez.

## 8b. Görünürlük tek yerde (H320, 2026-10-28)
- Görünürlük YALNIZ **Site › Görünürlük** sayfasında yazılır: "Sayfalar" sekmesi (`site_ayar.sayfalar` + `menu`), "İçerik" sekmesi
  (`site_ayar.gorunurluk`, liste `GET /api/admin/gorunurluk/icerik`, yazım `PUT /api/admin/site-ayar {gorunurluk}`; gizleme onaylı, 8 sn Geri al, toplu seçim).
- Başka sayfa görünürlük YAZMAZ: yalnız `GorunurlukBaglantisi` (rozet + "Değiştir" → `site/gorunurluk?sekme=icerik&q=<anahtar>`, `gorunurlukYolu()`).
- `site/menu` adresi Görünürlük › Sayfalar'a yönlenir. Yeni içerik türü eklenirse: anahtar öneki + `/gorunurluk/icerik` ucuna kaynak + `TUR_SECENEK`.

## 9. 2026-10-28 eklenen sayfalar ve temizlik
- Yeni sayfalar: Sorular › Serbest girdiler (`/api/admin/sorular/serbest[/:id]`, questionIntake.ts; "Yeniden ayrıştır" elle + onay),
  Sorular › Taslaklar (`/api/admin/sorular/taslak`, salt okunur; kümeleme aracı `?kabuk=v14`), Kullanıcılar › Gizlilik talepleri
  (`/api/admin/gizlilik`, `PUT …/:id`; öğrenci `POST /api/gizlilik/talep`, doğrulanmış oturum; `data/gizlilik_talepleri.json` gitignore,
  okuma KISISEL_OKUMA'da), Site › Kanallar (SMTP + yönetici push; mevcut uçlar), Oyunlar › Quiz havuzu (`/api/admin/quiz/havuz[/:id]`,
  `meds_database_v2/ders_isci/yayinlanan/*/quiz_havuzu.json`), Öğrenme › Ses kuyruğu (`/api/admin/sesli-kuyruk[/:id]`; yalnız
  yeniden dene/öne al/iptal — üretim BAŞLATMA yok, kural 20). Sunucu: `yonetim16/ekSayfalar.ts`.
- v14'ten kaldırılanlar: Tüm veriler (ManageDataSection), Veri Merkezi v2 (ManageDataCoreSection; `/api/v2/*` herkese açık API'de kaldığı için
  uçlar duruyor), Taslak stüdyosu (DraftStudio + draftStudioService + studioAiService + `/api/studio/ai-*`), Otomasyon › Zamanlama ve anahtarlar
  (ManageAutomationSection; Otomasyon yalnız Drive ve servisler). "Tüm veriler"e sıçrayan bağlantılar v16 havuz/çıkmış sayfasını açar.
  Ders işçisi bölümü salt okunur arşiv (yazma istekleri istemcide engellenir). FlatfileDataOnboarding KULLANILIYOR (AdminPastExamImporterModal,
  NotebookLM) — kaldı.

## 10. Son "yakında" sayfalar (2026-10-28) — menüde yakında kalmadı
- Sunucu: `src/services/yonetim16/sistemEk.ts` (`registerYonetimSistemEk`, server.ts'de Topluluk+Sistem bloğunun önünde).
- **Gelen** (`gelen`, `GelenKutusu.tsx`): `GET /api/admin/gelen` — soru şikâyetleri (iç loopback isteğiyle `/api/admin/sorular/sikayet`),
  topluluk mesaj şikâyetleri (meds-pg), açık Öğren geri bildirimleri, son 24 sa istemci hataları (mesaja göre gruplu), bekleyen gizlilik
  talepleri, Faz 14 `bekliyor`, kamp tüyo önerileri. 15 sn önbellek (`?taze=1`), yanıtta `kaynaklar{<tür>:{toplam,hata?}}`; satır `hedef` sayfaya gider.
- **Topluluk › Geri bildirim** (`GeriBildirim.tsx`): `GET /api/admin/topluluk/geri-bildirim` (varsayılan `s.durum=acik`, `hepsi`),
  `PUT …/:id {durum: acik|cozuldu, yanit}`. Durum server.ts'deki `learnFeedback` deposundan yazılır (önbellek tutarlı); yanıt iç nottur
  (`data/learn_feedback_yanit.json`), öğrenciye gönderilmez. SSE `learn_feedback_changed`. `/topluluk/geri-bildirim/<id>` çekmeceyi açar.
- **Sistem › Hat** (`Hat.tsx`, sekmeler `/asamalar|dersler|eylemler|gunluk`): mevcut `/api/admin/hat`, `/hat/dersler`, `/hat/eylemler`, `/hat/gece`.
  hat.json salt okunur. Ders eylemleri ve gece hattı Claude kullanır → `onayIste({yazilacak:'BASLAT'})` + sunucu `onay:true` (kural 20).
- **Sistem › Drive** (`Drive.tsx`): `GET /api/admin/sistem/drive` (ayar, son tarama, öğrenci envanteri, okul kataloğu) ve `/drive/dosyalar`
  (`s.kaynak=okul|ogrenci|tarama`, `s.kurul`). "Elle tara" = mevcut `POST /api/admin/drive/check-updates` (yalnız karşılaştırma, onaylı).
- **Sistem › RAG indeksi** (`Rag.tsx`): `/api/rag/vectors/health` + `GET /api/admin/sistem/rag` (hat raporu, cron günlüğü, son elle iş).
  `POST /api/admin/sistem/rag/denetle {onay:'DENETLE', kuru}` yalnız cihazda, `nice`, `CUDA_VISIBLE_DEVICES=""`; varsayılan `--kuru`.
- **Sistem › Fazlar** (`Fazlar.tsx`, `/sistem/fazlar/<kategori>`): `GET /api/admin/sistem/fazlar/:kategori` (phaseDataExplorer → ListeYaniti;
  `q` = explore `deger`), ayrıntı `GET /api/admin/phases/question/:id`. Salt okunur; elle düzeltme eski konsolda.
- **Sistem › Bağlantılar** (`Baglantilar.tsx`): `GET /api/admin/sistem/baglanti` (ders başına çıkmış soru / slaytlı / Öğren bağlı / terimli)
  ve `/baglanti/:ders` (`s.var=slayt|-slayt|ogren|-ogren|terim`). Faz verisi + çıkmış `discipline`'dan; 5 dk önbellek. Soru → `sorular/cikmis/<id>`.
- İçerik kapısı: `/api/canli-ders/ara` sonuçları (`sonuc[].k`) öğrenciye kapalı sesli dersleri içermez (`icerikKapisi`, §8).


## Ek (2026-10-28, H290–H295)
- `VeriTablosu` `dusur?(t)`: sunucu kipinde işlenen satırı istemcide düşürür (toplam azalır, süzgeç/sayfa korunur).
- Gelen işlemleri satırda/çekmecede; işlem yapan uçlar `gelenOnbellekSil()` çağırır (yonetim16/sistemEk.ts).
- `POST /api/admin/gelen/hata/goruldu {kimlikler[]}`: istemci hatası gruplarını görüldü işaretler.
- Toplu yazımda kalıp: onay (sayı + `yazimHedefi()`), başarısız sayısını bildir, 8 sn `bildir(…, {etiket:'Geri al', yap})`.

## Ek (2026-10-28, H420–H424) — birleştirilen sayfalar
- **Birleştirme deseni:** sayfa bileşeni silinmez; `gomulu` prop'uyla (SayfaBasligi yerine h2) başka sayfanın sekmesi/bölümü olur.
  Eski tam yol `menu.ts` → `ESKI_YOL` (önek → yeni yol + sorgu; kalan alt parçalar korunur); `adresCoz` yönlendirir,
  `ManageV16` hedef sorguyu mevcut sorguyla birleştirir. `m16_sabit` / `m16_son` açılışta `yolGuncelle` ile çevrilir, tekrar süzülür.
- `?bolum=<id>` → `sayfalar/ortak/bolumKaydir.ts` veri yüklenince o `<section id>`'ye kaydırır.

| Eski yol | Yeni yer |
|---|---|
| `ogrenme/ses-kuyrugu[/<iş>]` | `ogrenme/sesli[/<iş>]?sekme=kuyruk` (Sesli ders › Ses kuyruğu sekmesi) |
| `sistem/dagitim` | `site/surum?bolum=dagitim` (Site › Sürüm ve dağıtım; kanonik Site grubunda, çünkü sayfanın asıl içeriği öğrenciye görünen sürüm notu, dağıtım bilgisi onu destekler) |
| `sorular/dondurma` | `site/bayraklar?bolum=dondurma` (Özellik bayrakları › Havuz dondurma bölümü; aynı uç `/api/admin/havuz-dondur`, aynı yazılacak-sözcük onayı) |
