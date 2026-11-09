# Tahta Oyunları — Go, Çizgi Yarışı, XOX (altyapı + kural + arayüz planı)

Durum (2026-11-10): **motorlar, arayüz ve sınamalar hazır; `TURLER`'de açık (lobide "Tahta oyunları").** Ekranlar `src/components/masa/{go,cizgi,xox}/`, ortak parçalar `tahta/ortak.tsx`, kurallar `kurallar/TahtaKurallar.tsx`, stil `styles/masa/tahta.css`. Oyunlar Taş Masası altyapısını kullanır
(`src/services/masa/`): oda, bağlantı, bot, el/maç puanı, istatistik hazır gelir. Arayüz Fable ile yapılacak.

| Dosya | İçerik |
|---|---|
| `src/services/masa/tipler.ts` | `OyunTur` += `go`/`cizgi`/`xox`; `GoHamle/GoGorunum`, `CizgiHamle/CizgiGorunum/CizgiAdim`, `XoxHamle/XoxGorunum`, `XOX_HEDEF`, `OdaAyar.goBoyut/komi/cizgiKare/xoxBoyut`, `TAHTA_TURLER` |
| `src/services/masa/motor/go.ts` | Go motoru + basit bot (`goBotSec`), `say()` alan sayımı |
| `src/services/masa/motor/cizgi.ts` | Çizgi Yarışı motoru + bot |
| `src/services/masa/motor/xox.ts` | XOX motoru + bot (3×3 minimax) |
| `src/services/masa/motor/tahta.sinama.ts` | `npx tsx src/services/masa/motor/tahta.sinama.ts` → 49 sınama |
| `src/services/masa/sunucu.ts` | `ayarDuzelt` yeni ayarları süzer. **`TURLER`'e henüz eklenmedi** → oda kurulamaz |

**Açma sırası (arayüz bitince):** `sunucu.ts` `TURLER`'e türü ekle → `MasaMerkez.tsx` `OYUNLAR` + `KATEGORILER`'e
(ör. "Tahta oyunları") ekle → `MasaView` oyun ekranı yönlendirmesi → `kabukOrtak.tsx` `tasMi/birim/OyunResmi` →
`MasaLobi` ayar seçicileri → `MasaKurallar` sekmesi → `npm run lint` + `npx vite build` + bu sınama.
Not: `MasaUstCubuk`, `MasaLobi` `okey = tur !== 'uno'` varsayıyor; tahta oyunlarında bu ayrımlar düzeltilmeli.

Puan: üç oyunda da el kazanana **1**, kaybedene/berabere **0** (maç skoru = kazanılan el). `ElSatir.aciklama`
skor dökümünü taşır (Go: "Siyah 45 – Beyaz 40.5"). Oyuncu sayısı 2; bot seçeneği 1.

---

## 1. Go

Kurallar (Çin usulü alan sayımı, internetteki standart kurallar):
- Tahta 9×9 (varsayılan), 13×13, 19×19. Komi 6,5 (lobi ayarı 0–15, yarım adım). Siyah başlar; her elde renkler değişir.
- Taş boş kesişime konur. Özgürlüğü kalmayan rakip grup alınır (esir sayacı).
- **İntihar yasak**, **ko** (basit ko) + **konumsal süperko** (`gecmis`: tahta özetleri, FNV+djb2 karması, düz JSON).
- **Handikap** `goHandikap` 0–9: ≥2 iken siyah taşlar yıldız noktalarına (`handikapNoktalari`), beyaz başlar; ≥1 iken komi 0,5.
- **Süre** `goSure` (`GO_SURELER`: yok / 5 dk+3×30 sn / 10 dk+5×30 sn / 20 dk+5×60 sn): ana süre + Japon byo-yomi. Sunucu her hamleye `z` (sunucu saati) basar; `Motor.sureSonu` anında `surePlanla` zamanlayıcısı `{t:'sureBitti'}` uygular (motor saati doğrular), süresi biten kaybeder. Sayımda ve oda durdurulunca saat işlemez (`saatKaydir`).
- Pas serbest; art arda iki pas → **sayım aşaması**: iki oyuncu ölü grupları işaretler (`olu`, grup bazında aç/kapa;
  her değişiklik onayları sıfırlar), ikisi de `onayla` derse el biter. Anlaşamayan `devam` der → oyun sürer.
- Puan: diri taş + yalnız kendi taşlarınca çevrili boş noktalar (+ beyaza komi). Teslim her an.
- Bot: alır, atarideki grubunu kurtarır, gözünü doldurmaz, kendini atariye sokmaz; geç oyunda iyi hamle yoksa pas.
  Sayımda bot kendi **diri** grubu (`diriMi`: ≥2 göz ya da ≥5 özgürlük) ölü işaretlendiyse önce işareti geri alır, sonra onaylar.

Görünüm (`GoGorunum`): `tahta` (i = y·boyut + x), `renkler`, `esir`, `son` (halka), `ko`, `yasal` (gölge taş /
asistan), `yildiz` (hoshi), `asama`, `olu`, `onay`, sayımda `alan` + `puan` önizlemesi.

**Arayüz planı (resimdeki mantıkla, daha güzeli):**
- Masa: koyu ahşap zemin; tahta açık sarı ağaç damarlı (kaya/kaya rengi), ince siyah çizgiler, hoshi noktaları.
  Taşlar: siyah parlak (yumuşak yansıma), beyaz istiridye/porselen; gölge düşürür. Konunca hafif "tık" + küçük sıçrama.
- **Koy → Onayla** iki adımı (resimdeki SUBMIT): dokunulan noktada yarı saydam taş + kesişimden geçen yatay/dikey
  vurgu çizgisi (resimdeki beyaz çizgi); `Onayla` ile gönderilir. Asistan kapalıysa (Zorlu) gölge taş yine var.
- Son hamle halkası; ko noktası küçük kare; alınan taşlar animasyonla kenardaki kâseye uçar, kâsede esir sayısı (`x 74`).
- Üst bilgi: iki oyuncu (avatar, renk, esir, komi "6.5"), "Sıra sende" hapı; alt çubuk: `Pas`, kâse, `Onayla`, `⋯` (teslim).
- Sayım ekranı: ölü taşlar yarı saydam + çarpı; alan noktaları küçük renkli kareler; canlı puan; iki onay rozeti.
- Telefon: tahta ekran genişliği; yakınlaştırma 13/19'da (çimdik), dokunma noktası büyüteci.

## 2. Çizgi Yarışı

Kurallar (kullanıcı tarifi + motor kararları — **değişiklik kullanıcıya sorulur**):
- Modlar: **32 / 64 / 96 / 128 kare** = yol uzunluğu (satır). Sütun sayısı az tutulur: 32→3, 64→5, 96→5, 128→7.
  Yan geçiş hakkı (el boyunca): 32→2, 64→3, 96→4, 128→5.
- 1. oyuncu alttan (r=0) yukarı, 2. oyuncu üstten aşağı, ikisi de orta sütundan başlar. **Rakibin kale satırına ilk
  ulaşan kazanır.**
- Tur: `zar` (1–6, sunucu atar) → her adım tek tek `ilerle` (`duz`). Yandaki sütuna (`sol`/`sag`, 1 adım, yan hakkı
  düşer) yalnız **önü rakip çizgisiyle kapalıyken** geçilir — sütunlar gereksiz kullanılmasın. Yolu olmayan kalanı
  yakar (`bekle`; motor yol yoksa kendisi bekletir).
- **Kapışma:** iki baş aynı sütunda yüz yüze ve en az biri kendi yarısını geçmişse (yani biri rakip sahada karşılaştı).
  Kapışma turunda sıradaki zar atar, iki zar birden atılır; büyük atan **fark kadar ilerler**, küçük atan **fark kadar
  geriler** (çizgi baştan kısalır). Eşitlikte bir şey olmaz. Mağlubun yalnız kale hücresi kaldıysa ve yine kaybederse
  galip kaleyi alır → kazanır. Mağlup geri çekilirken yan geçiş köşesini geçerse galibin önü açılır, kapışma biter;
  galip normal ilerler (gerekirse kendisi yana geçer).
- Tam orta çizgide yüz yüze gelme (ikisi de kendi yarısında) kapışma değildir: önü kapanan yana geçmek zorundadır.
- Bot: zar atar, düz gider, kapalıysa ortaya yakın yana geçer.

Görünüm (`CizgiGorunum`): `cizgiler` (oyuncu → hücre dizisi, baş sonda), `yanHak`, `zar`, `kalan`, `kapisma`,
`yonler` (geçerli düğmeler), **`gecmis` son 4 tur** (`CizgiAdim`: `zar`, `fark` ±, `eklenen`, `silinen`, `kapisma`).

**Arayüz planı:**
- Dikey kareli kâğıt/ahşap şerit; benim sahâm altta. Orta çizgi belirgin; iki kale satırı renkli.
- Çizgi: yuvarlak uçlu kalın kalem çizgisi, oyuncu rengi. Son 4 tur kademeli: en yeni parlak, eskiler soluklaşır;
  **gerileyen kısım** (`silinen`) mağlubun ikinci renginde kesik çizgi olarak 1–2 tur görünür ve söner.
- Zar: 3B zar yuvarlanır; kapışmada iki zar yan yana, kazanan parlar, "+3 / −3" etiketi.
- Adımlar: zar sonrası baş hücresinde ok düğmeleri (`yonler`); "Hepsini ilerle" kısayolu (düz giderken).
- Mod kartları: 32 hızlı · 64 klasik · 96 uzun · 128 maraton; sahne uzunsa otomatik kaydırma başı takip eder.

## 3. XOX

- Tahta 3×3, 4×4, 5×5, 6×6. Hedef (yan yana): 3→3, 4→4, 5→4, 6→5 (`XOX_HEDEF`; büyük tahtada beraberliği azaltır).
- X başlar; her elde başlayan değişir (X hep başlayanındır). Yatay/dikey/çapraz hedef kadar dizen kazanır; tahta dolarsa berabere.
- Bot: 3×3 kusursuz (minimax); büyüklerde kazan → engelle → açık dizi puanı.

Görünüm: `tahta`, `isaretler`, `son`, `cizgi` (kazanan dizi), `hedef`.

**Arayüz planı:** ahşap ya da kâğıt tahta, el çizimi X/O (çizilme animasyonu), kazanan diziye çekilen çizgi, berabere
sarsıntısı; boyut kartlarında hedef yazılı ("5×5 · 4'lü").

---

## Açık sorular (kullanıcıya)
1. ~~Çizgi kural kararları~~ — kullanıcı onayladı (2026-11-10).
2. ~~Go: süperko, handikap, süre~~ — eklendi (2026-11-10).
3. XOX: büyük tahtalarda hedef (4×4→4, 5×5→4, 6×6→5) uygun mu?
