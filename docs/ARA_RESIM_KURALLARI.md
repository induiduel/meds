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
   "svg": "r01.svg", "lottie": "r01.json", "paragraf": 12, "bitis": 13, "kaynak": [14, 15]}]}
```
- `paragraf` / `bitis`: sesli ders v2 paragraf dizini (CdDetay `bolumler[].paragraflar[].i`); `bitis` yoksa = `paragraf`.
  İki resmin aralığı çakışamaz.
- `kaynak`: resmin dayandığı PDF sayfaları (1..sayfa sayısı). `adimlar` isteğe bağlı, en çok 6.
- SVG: `meds/public/ara_resim/<key>/<id>.svg` — statik, kendi içinde renkli, **açık zemin**, `viewBox`'lı; `<script>`,
  `foreignObject`, olay öznitelikleri, harici `href`/`url()` YOK; yazılar Türkçe `<text>` ögeleri (yol/çizgiye çevrilmez).

## Ne zaman resim yapılır
- **Slaytta resim olup olmamasına bakılmaz** (kullanıcı kararı 2026-11-06): mekanizma, sıralı aşamalar, süreç, yolak,
  neden-sonuç zinciri, karşılaştırma ya da görselleştirmeye uygun her konu resimlenir; bilgi **slayt/ders kaynaklı** olur.
- Slaytta zaten bulunan resmi yeniden çizmek YASAK (değer katmaz; lazer + canlı çizim o resmi zaten gösterir). Slayt
  resmi varsa ara resim onun göstermediği mekanizmayı/aşamayı tamamlar.
  Uydurma, kaynak dışı ayrıntı, slaytta olmayan değer YASAK (kural 4/21).
- Ders başına resim sayısı konuya göre belirlenir (tavan yok; uygun her mekanizma resimlenir). Tanım, liste ya da tek cümlelik bilgi için resim yapılmaz.
- Resim ≠ slayt kopyası: slaytı yeniden çizmek değil, anlatılan mekanizmayı sadeleştirip adım adım göstermek.
- Okunabilirlik: SVG yazıları **≥14 px eşdeğeri** (viewBox 1000–1200 genişlikte font-size 15–30). Renk yalnız anlam taşır
  (aynı yapı her resimde aynı renk).

## Ayrıntı ve akademik çizim standardı (ZORUNLU, kullanıcı kararı 2026-11-06, H506)
Kısa kelime öbekli "kutu + ok" resmi YASAK; öğrenci resme bakınca mekanizmayı slayta dönmeden anlamalı.
- **Gerçek yapıyı çiz:** hücre zarı (fosfolipid çift katman), reseptör/kanal, nöron, sinaps, organ kesiti, damar, beyin
  bölgesi, yolak düğümleri vektörel illüstrasyon olarak çizilir (eğrili `<path>`, degrade, `<use>` tekrar ögeleri, `marker` okları).
  Kutular yalnız sonuç/özet şeridi için kullanılır.
- **Paneller:** tipik 2–3 panel (A · yapı/yerleşim, B · işleyiş/zaman grafiği ya da karşılaştırma, C · klinik sonuç zinciri),
  her panel başlıklı; karşılaştırmada iki taraf aynı ölçek ve aynı çizim diliyle yan yana.
- **Etiketleme:** her yapı kılavuz çizgili etiketle adlandırılır; iyon, ilaç, bağlanma bölgesi, yön ve sonuç yazılır.
  Resim içi metin **en az 45 kelime, üst sınır yok** — öğretilmek istenen ne gerekiyorsa yazılır; tam cümleli açıklamalar kullanılabilir. Alt bilgi satırında kaynak slaytlar.
- **Akademik doğruluk:** her etiket ve ilişki slayt/ders anlatımında geçer; slaytta olmayan alt birim adı, değer, yolak
  basamağı eklenmez. Şematik sadeleştirme serbest, yanlış anatomi/yön yasak.
- **Lottie (isteğe bağlı):** süreç zamanla anlatılıyorsa (iyon akışı, ileti, kanal açılıp kapanması) aynı resmin
  `public/ara_resim/<key>/<id>.json` Lottie sürümü `lottie` alanına yazılır; harici varlık yok, hareketi azalt açıkken son
  kare. `svg` her zaman zorunlu durağan sürümdür (dışa aktarım, çevrimdışı, yükleme hatası).
- Örnek ölçü: `public/ara_resim/k2-07-genel-anestezik-ilaclarin-farmakolojisi/r01.svg` (zar kesiti + tek kanal kayıtları + sonuç zinciri).
- Başlık, alt yazı, adımlar ve SVG içi metinler Türkçe üslup standardına uyar (`TURKCE_USLUP_STANDARDI.md`).
- Resim konuşulan aralıkta görünür; ileride anlatılacak bilgiyi erken göstermez (kural 7 ruhu).

## Kapı
```
python3 meds/scripts/ara_resim/dogrula.py <key> [--kok <meds dizini>]
```
Şema, id tekilliği, SVG varlığı + XML + viewBox + güvenlik + metin ögesi, paragraf aralığı (v2 paragraf sayısı),
kaynak sayfa (hizalama `dosyalar[0].pages`), çakışma, Türkçe üslup, **ayrıntı** (≥45 kelime, ≥12 etiket, ≥15 çizim ögesi,
≥2 eğrili yol; ok yoksa UYARI), Lottie şeması. "N HATA, M UYARI"; HATA varsa çıkış 1. 0 HATA olmadan yayın yok.

## Gösterim ve dışa aktarım
- Ekran: `src/components/canliDers/CdAraResim.tsx` (+ `styles/v15/ara_resim.css`), veri `araResimVeri.ts`.
  Araç çubuğundaki resim düğmesi galeriyi açar; dokunulan resim dersi o paragrafa götürür. "Slayta dön" resmi o aralık
  bitene dek gizler; tam ekran büyütme vardır. Resmi olmayan derste hiçbir şey görünmez.
- Dışa aktarım: `cdAktarBelgesi` resmi `bitis` paragrafından sonra `![başlık](yol "alt yazı")` satırı olarak yazar;
  `metinDisaAktar` PDF'e 2× PNG (başlık + resim + alt yazı aynı sayfada), DOCX'e gömülü PNG, MD'ye mutlak bağlantı +
  alt yazı, TXT'ye `[Resim: başlık — alt yazı]` olarak koyar. Resim yüklenemezse metin satırı yazılır. Toplu sesli ders
  PDF'i ve Son Prova aynı yolu kullanır.
- Çevrimdışı: ders indirilirken SVG'ler sesli ders çevrimdışı önbelleğine yazılır, ders silinince silinir.
