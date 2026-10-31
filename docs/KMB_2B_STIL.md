# KMB 2B Düz Çizgi Film Stili (sahne kitaplığı sözleşmesi)

Kullanıcı kararı 2026-11-01: 3B deneme arşive alındı; KMB görsel asistanın tüm SVG sahneleri ve Lottie videoları
**düz vektör çizgi film** stilinde yeniden çizilir. Referans: "Bladder catheterization – Foley catheter" tipi
illüstrasyon (sırtüstü hasta, kesit penceresi, yeşil örtü, mavi böbrek küvet, sarı kateter). Örnek uygulama:
`src/components/kmb/sahneler.tsx` → `Erkek` sahnesi (onaylı).

## 1. Görünüm dili

- **Pürüzsüz dolgular**: iki duraklı yumuşak degrade (`url(#kmb-2b-…)`, `sahneOrtak.tsx` içinde) ya da düz renk.
  Parıltı, `filter` (gölge/bulanıklık), doku deseni, pırıltı çizgileri YOK (tek beyaz vurgu çizgisi serbest).
- **Kontur**: her nesnede 2–3 px sıcak/koyu kontur (`strokeLinejoin="round"`), palet yorumundaki renk.
- **Palet** (dolgu → kontur): deri `kmb-2b-deri` → `#b9805a`; mesane `kmb-2b-mesane` → `#7a2e26`; idrar `kmb-2b-idrar`;
  kateter lateks `kmb-2b-kateter` → `#b47a1a` (gövde 9 px koyu + 6,5 px açık iki çizgi = silindir); silikon `kmb-2b-silikon` → `#8a96a6`;
  balon `kmb-2b-balon` → doğru `#2e9e5b`, yanlış `#8d1f1f`; örtü `kmb-2b-ortu` → `#2f6f5f`; yatak `kmb-2b-yatak` → `#4f9aa0`;
  eldiven mavi `kmb-2b-eldiven` → `#3f6f9c`, steril krem `kmb-2b-eldiven-steril` → `#b59c72`; mukoza `kmb-2b-mukoza` → `#a85f5a`;
  prostat `kmb-2b-prostat` → `#9a5a44`; kemik `kmb-2b-kemik` → `#b9a479`; kas `kmb-2b-kas` → `#8d2f28`; metal `kmb-2b-metal` → `#5b6676`;
  plastik `kmb-2b-plastik` → `#6b7a90`; küvet `kmb-2b-kuvet` → `#1f4e79`; jel `kmb-2b-jel` (yarı saydam film); önlük `kmb-2b-onluk`.
- **Zemin**: beyaz `#ffffff` (ya da açık tek renk); 800×500 görünüm kutusu, 8:5.
- **Sıvılar** (idrar, jel, antiseptik, izotonik): yarı saydam film / ince çizgi, ASLA katı top ya da sakız. İdrar yalnız
  kateter mesaneye yerleştikten sonra akar (lümende ince sarı çizgi → damla → kapta film).
- **Yazı**: sahne içinde en az yazı; ölçek/birim gerekiyorsa küçük (≤ 11 px) ve tek font rengi `#3e4a58`.

## 2. H462 doğruluk kuralları (ZORUNLU, kullanıcı: "hata istemiyorum")

1. **İç içe geçme yok**: hiçbir nesne başka bir katı nesnenin içinden geçmez; kateter yalnız lümen içinde; balon lümen
   duvarına taşmaz; el, parmak, alet birbirine ve dokuya gömülmez. Katmanlama sırası gerçek öne/arkaya göre.
2. **Anatomik ölçek** 1 cm ≈ 12 px (tam gövde sahneleri): üretra 1 cm ≈ 12 px, 16 Fr kateter 5,3 mm ≈ 6,5 px, balon 10 mL ≈ r 17,
   mesane 8–10 cm, prostat 3–4 cm, penis 3,5 × 10 cm, testis 4,5 × 3 cm, el ≈ 18 cm. Yakın plan sahneler kendi ölçeğini
   tutarlı uygular (kateter/üretra oranı ≈ 1/2, balon/üretra oranı gerçekçi).
3. **Doğru yön ve dizilim**: sırtüstü hastada iç organlar gövdeyle aynı yönde (inferior = ayak yönü, anterior = yukarı);
   simfiz derinin hemen altında, mesane simfizin arka-üstünde, prostat arkasında; kadın meatus klitoris ile vajina arasında
   üstte; üretra skrotumun altından DOLANMAZ (bulbar üretra perinede, simfizin arka-altında öne kıvrılır).
4. **Kadraj kesmez**: anlatılan öge tam görünür; kameranın odaklandığı kutu (etiket koordinatı ± 120 px) sahne içinde.
5. **Her öge adıyla ayırt edilir**: el "el" gibi (avuç + 4 parmak + başparmak, parmak boğumları), kateter silindir gibi,
   probe/enjektör/küvet tanınır; aynı renkte iki şey yan yana gelirse kontur ya da ton ayırır.
6. **Fizik**: dik duran şey tutulur (penis eldivenli elle dik), yerçekimi (idrar aşağı/arkaya birikir, damla düşer),
   kapta sıvı yatay yüzey; ışık tek yönden.
7. **Kare denetimi**: her sahne `node scripts/kmb/sahne3b_onizle.mjs <sahne> --goster --etiket` (tüm ögeler + etiketler) ve
   `--film` (gerçek vuruş durumları) ile çizilir, PNG göz ile okunur; etiketler üst üste BİNMEZ (koordinatlar buna göre
   seçilir; etiket pili ≈ metin.length × 9,2 px genişlik, 28 px yükseklik), çizim kenarı kesilmez.

## 3. Kod sözleşmesi (değişmez)

- `Sahne = { ad, gizli, etiket: {id: [x, y, metin]}, Ciz: ({o}) => JSX }` (`sahneOrtak.tsx`). Her öge `<g {...o('id')}>`;
  öge kimlikleri ve sayısı `SAHNE_OGELERI` ile BİREBİR aynı kalır (asistan eylemleri, film vuruşları, sınav "sahnede bul" bunlara bağlı).
- `gizli`: başlangıçta görünmeyen ögeler (eylem `goster` açar). Semantik eski sahneyle aynı (ör. `e-balon-dogru` ile
  `e-balon-yanlis` birlikte görünmez; `f-balon-sonuk` ↔ `f-balon`).
- Renk eylemi `.boya` (dolgu) ve `.boya-cizgi` (çizgi) sınıflarını boyar → her ögede en az bir `.boya`/`.boya-cizgi` parçası.
- Çizilebilir yollar (`ciz` eylemi): `className="cz …"` + `pathLength={1}`; akış animasyonu `cz kmb-akis`.
- Ok işareti `markerEnd="url(#kmb-ok)"`; yardımcı `Boru` (`sahneOrtak.tsx`) kullanılabilir ama 2B'de iki çizgili kateter yeğlenir.
- Etiket koordinatları öge yakınında, birbirine ≥ 44 px dikey ya da pil genişliği kadar yatay uzaklıkta.
- Önizleme: sunucu 3000 `dist/`'i sunar → her değişiklikte `flock /tmp/kmb_build.lock npx vite build` (≈15 sn), sonra
  `node scripts/kmb/sahne3b_onizle.mjs <sahne> [--goster --etiket] [--eylem='[{"t":"goster","id":"…"}]'] --w=1280 --out=<klasör>`.
  Film vuruşları: `--film --hedef=N` (02.json `hedefCalisma[].film`). Tip denetimi `npx tsc --noEmit -p .`.
- Kapı: `python3 scripts/kmb/dogrula.py` 0 HATA.
