# Site haritası ve adres kuralları (2026-10-21, kullanıcı kararı)

Öğrenciler hangi aracı ne zaman kullanacaklarını bilemiyordu. Site artık **"ne yapmak istiyorum"** sorusuyla açılan dört
kategoriye ayrılır; adres çubuğu bu hiyerarşiyi gösterir. Yeni her sayfa, araç, kamp ya da check-up bu şemaya uyar.

Tek kaynak: `src/siteHaritasi.ts` (adres çevirisi + kategoriler) ve `src/components/merkez/merkezModel.ts`
(kategori → araçlar, "ne zaman kullanılır" cümleleri, check-up listesi, öğrenciye kapalı sayfalar).

## 1. Adres şeması

```
/<kategori>/<araç>/kurul<N>/<branş>/<öğe>                       dersler, sorular
/kamplar/kurul<N>/<araç>/<branş|konu>/<sürüm>/<bölüm>             kamplar (kurul önce gelir)
```

| Kategori | Merkez | Araçlar (görünen adres) |
|---|---|---|
| Ders çalış | `/dersler` | `/dersler/canliders[/kurul1[/tbg]]`, `/dersler/canliders/kurul1/<dersKey>`, `/dersler/interaktif[/<desteId>]`, `/dersler/ozetler`, `/dersler/kartlar` |
| Soru çöz | `/sorular` | `/sorular/soru-cozucu[/kurul1/<branş>]?ders=…`, `/sorular/cikmis[/<id>]`, `/sorular/deneme`, `/sorular/havuz[/<id>]`, `/sorular/ornek`, `/sorular/olasi` |
| Sınava hazırlan | `/kamplar[/kurulN]` | `/kamplar/kurul1/son-prova/…`, `/kamplar/kurul1/cikmis-cozucu[/<branş>]?ders=cp1-<branş>-<n>&coz=1`, `/kamplar/kurul1/kamp[/<branş>]`, `/kamplar/kurul1/en-onemliler/<branş>`, `/kamplar/spotlar` |
| Check Up (ayrı sekme) | `/kamplar/kurul1/checkup` | `/kamplar/kurul1/checkup/patoloji`, `/kamplar/kurul1/checkup/tbg/v1/{sesli-ders,soru-coz,kaliplar,deneme}` |
| Başvuru | `/kaynaklar` | sözlük, hastalıklar, Sağlık Bakanlığı, kazanımlar, geçmiş kurullar, güncellemeler (düz adreslerinde kalır) |

- **Branş adres adları:** patoloji, enfeksiyon, uroloji, **tbg** (genetik), halk-sagligi, kadin-dogum, farmakoloji.
  Kurul 2+: `k2noroloji` ↔ `kurul2/noroloji` (`bransAdresi` / `bransKimligi`).
- **Kamp / check-up sürümü:** içerik baştan yeniden kurulursa yeni sürüm (`v2`) açılır, eski sürüm adresi kalır.
- **Sayfa içi bölüm şeridi yok:** bölüm adı kabuğun üst çubuğunda görünür; kardeş araçlara merkez sayfasından geçilir (kullanıcı: şerit tasarımı bozuyordu).
- **Her bölüm ayrı sayfa:** bir kampın bölümleri sekme değil ayrı adrestir ve kendi başlığı/rengiyle ayrı görünür
  (TBG v1 örneği: iz yolu + sayfaya özgü baş + sonda "kampın diğer sayfaları" kartları).

## 2. Çeviri katmanı (nasıl çalışır)

Ekranlar hâlâ **iç adres** konuşur (`/canliders/<key>`, `/soru-cozucu?brans=…`, `/son-prova/…`, `/kamp/<N>/<b>`,
`/genetik-check-up?b=…`). `siteHaritasi.ts`:

- `disYol(iç)` → görünen adres; `icYol(görünen)` → iç adres; `kanonik(x)` iki biçimden tek görünen adres.
- `adresKatmaniniKur()` (main.tsx) `history.pushState/replaceState`'i sarar: kim ne yazarsa yazsın adres çubuğu görünen
  adres olur; açılışta eski biçimli adres (bildirim, paylaşım, yer imi) görünen adrese döner.
- `router.ts`: `parseLocation` önce `icYol` uygular; `pathFor` görünen adres verir (`icPathFor` iç adres);
  `navigateTo` `kanonik` uygular. `ROUTE_PATHS` iç adreslerdir (havuz `/havuz`, merkezler `/…-merkezi`).
- **Adresi kendisi okuyan ekran** `window.location` yerine `icKonum()` / `icUrl()` kullanır (yoldan gelen `kurul`,
  `brans`, `b`, `sekme` yalnız iç adreste sorgu olarak görünür).

## 3. Yeni sayfa eklerken (zorunlu sıra)

1. `router.ts`: `AppRoute` + iç adres (`ROUTE_PATHS`) + başlık.
2. `siteHaritasi.ts`: `disYol` ve `icYol`'a iki yönlü kural; kurul/branş yoldaysa iç adreste sorguya taşı.
3. `merkezModel.ts`: kategorisine "ne zaman kullanılır" cümlesiyle ekle (önerilen ilk adımsa `oner`); check-up ise
   `CHECKUPLAR`'a sürümüyle.
4. `shell/navModel.ts`: `NAV_TREE` grubuna aynı sırayla (gerekirse `V12_RAIL_IDS`).
5. Sınama: `npx tsx` ile gidiş-dönüş (`kanonik(disYol(x)) === disYol(x)`), tarayıcıda eski ve yeni adresle aç.
6. Çevrimdışı: `services/cevrimdisi/sayfaPaketleri.ts` iç adresle çalışır (`icYol` uygulanır); yeni iç adres kalıbını ekle.

## 4. Öğrenciye kapalı sayfalar

`merkezModel.KAPALI_SAYFALAR`: **Sınav çalışması** (`/sinav-calisma`), **Alternatif çözücü** (`/alternatif-cozucu`),
**Ders notları** (`/notlar`) — hatalı oldukları için (2026-10-21). Menüde yok, bağlantıları kaldırıldı (çıkmış → ders
notu, olası soru → ders notu, çözücü → alternatif anlatım); adresle açan öğrenci "kullanımdan kaldırıldı" ekranı ve
dört kategori kartını görür. Yönetici adresle açabilir. Geri açmak kullanıcı kararıdır.

## 5. Yasaklar

- Yeni sayfayı kategorisiz düz adresle (`/yeni-sey`) yayınlamak (Başvuru ve Kişisel/Topluluk araçları hariç).
- Bir kampın bölümlerini tek sayfada sekmeyle (`?b=`) göstermek; her bölüm kendi adresi ve görünümüyle olur.
- Eski adresi kırmak: eski biçim her zaman `disYol` ile yeni adrese yönlenmelidir (bildirim/paylaşım bağlantıları).
- Ekranda `window.location.pathname`'i yeni adrese göre ayrıştırmak; iç adres (`icKonum`) okunur.
