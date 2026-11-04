# Sesli ders ara resimleri (mekanizma resimleri)

Kullanıcı kararı 2026-11-04: tam içerik işçisi sesli derslerde mekanizma anlatan **ara resimler** üretir. Resim, bağlı
olduğu paragraf aralığı konuşulurken PDF alanının üstünde "ara sayfa" olarak görünür (ders sesi DURMAZ), aralık bitince
kendiliğinden kalkar; dışa aktarımda (PDF/DOCX/MD/TXT) aralığın sonuna yerleşir.

## Veri sözleşmesi (değiştirme; gerekirse alan ekle)

`meds/src/data/ara_resim/<ders key>.json`
```json
{"key": "k2-07-genel-anestezik-ilaclarin-farmakolojisi",
 "resimler": [{"id": "r01", "baslik": "GABA-A reseptörü: anestezik kapıyı daha uzun açık tutar",
   "aciklama": "1–2 cümlelik alt yazı", "adimlar": ["1. ...", "2. ..."],
   "svg": "r01.svg", "paragraf": 12, "bitis": 13, "kaynak": [14, 15]}]}
```
- `paragraf` / `bitis`: sesli ders v2 paragraf dizini (CdDetay `bolumler[].paragraflar[].i`); `bitis` yoksa = `paragraf`.
  İki resmin aralığı çakışamaz.
- `kaynak`: resmin dayandığı PDF sayfaları (1..sayfa sayısı). `adimlar` isteğe bağlı, en çok 6.
- SVG: `meds/public/ara_resim/<key>/<id>.svg` — statik, kendi içinde renkli, **açık zemin**, `viewBox`'lı; `<script>`,
  `foreignObject`, olay öznitelikleri, harici `href`/`url()` YOK; yazılar Türkçe `<text>` ögeleri (yol/çizgiye çevrilmez).

## Ne zaman resim yapılır
- Yalnız **mekanizma, süreç, yol (pathway), neden-sonuç zinciri ya da karşılaştırma** anlatan ve **slayt kaynaklı** bilgi.
  Uydurma, kaynak dışı ayrıntı, slaytta olmayan değer YASAK (kural 4/21).
- Ders başına tipik **4–10** resim. Tanım, liste ya da tek cümlelik bilgi için resim yapılmaz.
- Resim ≠ slayt kopyası: slaytı yeniden çizmek değil, anlatılan mekanizmayı sadeleştirip adım adım göstermek.
- Okunabilirlik: SVG yazıları **≥14 px eşdeğeri** (viewBox 1000 genişlikte font-size ≥14; tercihen 22–30), resim içi metin
  **en çok ~40 kelime**; ayrıntı alt yazıya/adımlara gider. Renk yalnız anlam taşır (aynı yapı her resimde aynı renk).
- Başlık, alt yazı, adımlar ve SVG içi metinler Türkçe üslup standardına uyar (`TURKCE_USLUP_STANDARDI.md`).
- Resim konuşulan aralıkta görünür; ileride anlatılacak bilgiyi erken göstermez (kural 7 ruhu).

## Kapı
```
python3 meds/scripts/ara_resim/dogrula.py <key> [--kok <meds dizini>]
```
Şema, id tekilliği, SVG varlığı + XML + viewBox + güvenlik + metin ögesi, paragraf aralığı (v2 paragraf sayısı),
kaynak sayfa (hizalama `dosyalar[0].pages`), çakışma, Türkçe üslup. "N HATA, M UYARI"; HATA varsa çıkış 1. 0 HATA olmadan yayın yok.

## Gösterim ve dışa aktarım
- Ekran: `src/components/canliDers/CdAraResim.tsx` (+ `styles/v15/ara_resim.css`), veri `araResimVeri.ts`.
  Araç çubuğundaki resim düğmesi galeriyi açar; dokunulan resim dersi o paragrafa götürür. "Slayta dön" resmi o aralık
  bitene dek gizler; tam ekran büyütme vardır. Resmi olmayan derste hiçbir şey görünmez.
- Dışa aktarım: `cdAktarBelgesi` resmi `bitis` paragrafından sonra `![başlık](yol "alt yazı")` satırı olarak yazar;
  `metinDisaAktar` PDF'e 2× PNG (başlık + resim + alt yazı aynı sayfada), DOCX'e gömülü PNG, MD'ye mutlak bağlantı +
  alt yazı, TXT'ye `[Resim: başlık — alt yazı]` olarak koyar. Resim yüklenemezse metin satırı yazılır. Toplu sesli ders
  PDF'i ve Son Prova aynı yolu kullanır.
- Çevrimdışı: ders indirilirken SVG'ler sesli ders çevrimdışı önbelleğine yazılır, ders silinince silinir.
