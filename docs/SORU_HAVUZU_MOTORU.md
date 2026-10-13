# Soru havuzu motoru (`src/services/recall/`, hatirlama-v1 · 2026-10-13)

Öğrencilerin sınav çıkışı yazdığı hatırlamaları (Soru ekle kutusu, serbest girdi) **temizler**, **sınıflar**
(kurul → ders → konu), **tıbbi terimleri ayıklar**, aynı soruyu anlatanları **gruplar** ve kanıta dayalı bir
**taslak** kurar. LLM, GPU ve ağ yok; sunucu belleğinde ~80 MB, kurulum ~3 sn (dilimli, olay döngüsü ≤50 ms kilitlenir).
Yapay zekâ birleştirmesi (Gemini, ders notu kaynaklı) bunun üstünde, arka planda ve ayrı kalır (`poolClusterService.aiMerge`).

## Aşamalar

| Aşama | Dosya | Ne yapar |
|---|---|---|
| 1. Temizleme | `normalize.ts` | Katlama, kısaltma/argo açma, sohbet/üst söylem ayıklama, cevap iddiası (harf + metin), soru no, harfli/harfsiz şık, olumsuz kök, çok sorulu mesajı bölme (`splitRecall`), okunur cümle (`cleanSentence`) |
| 2. Sözlük + düzeltme | `lexicon.ts` | Çıkmış soru bankası + tıbbi sözlük + hastalıklardan 26 bin sözcük; simetrik silme ile 1–2 harf hatası, ünlüsüz yazım ("gstrt"→gastrit), Türkçe ek ayırma; gündelik sözcük koruması; 3,7 bin terimlik dizin |
| 3. Sınıflama | `engine.ts` | Kurul içinde ders: çıkmış soru merkezleri + k-en yakın komşu + ders özeti merkezleri + açık ders ipucu ("pato", "farmada"); konu = en yakın ders özetinin başlığı |
| 4. Gruplama | `cluster.ts` | Öğrenilmiş çift olasılığı (TF-IDF kosinüs, kapsama, 4'lü harf dizisi, terim, aynı çıkmış soruya yaslanma, şık, soru no, ders çelişkisi) + ortalama bağlantılı kümeleme; yuva numarası farklıysa kesin ayrı |
| 5. Taslak | `cluster.ts` `draftCluster` | Ortak ögeleri en çok kapsayan hatırlamanın temizlenmiş cümlesi, ders/konu oyu, cevap oyları, "önceki yıllarda çıkmış" eşleşmesi (küme merkezi + birinci/ikinci aday farkı) |

Bağlantılar: `poolClusterService.ts` (havuz kümeleri, `POST /api/recall/match`), `QuickAddHero.tsx` (yazarken eşleşme ve
ders tahmini sunucudan), `pool/PoolView.tsx` (öneri bandı, satırda "n benzer"), `admin/QuestionClusterAutomationModal.tsx`.

## Sınama seti (`scripts/eval/datasets/hatirlama/`)

5.700 doğrulanmış çıkmış sorudan 6 kurul × 24 soru (her konudan bilerek 3 farklı soru — en zor ayırma durumu) ve her
biri için 4–10 öğrenci tarzı mesaj: %40–75 aksansız, kısaltma/harf hatası, sohbet, yanlış cevap iddiası (~%25),
±1 yanlış soru no, çok sorulu ve soru içermeyen mesajlar. Toplam 1.023 mesaj. k1–k3 geliştirme (ağırlıklar burada
öğrenildi), k4–k6 test. Bankadan hedef sorular çıkarılarak ölçülür (yeni sınav); `--bank include` eski soru tekrarını ölçer.

## Sonuçlar (2026-10-13)

| Ölçüt | Eski | Yeni |
|---|---|---|
| Gruplama, test (k4–k6), çift F1 · ARI | %37,5 · 0,371 (kume-v2) | **%65,7 · 0,656** |
| Gruplama, tüm set, banka soruyu içeriyorsa | — | %74,8 · 0,749 |
| Soru ekle anlık eşleşme: ilk öneri doğru · yanlış alarm (963 mesaj akışı) | %54,5 · 326 (tarayıcı, 39 ms/mesaj) | **%83,0 · 78** (0,4 ms) |
| Ders tahmini | %36,4 (medicalPredictorService) | **%63,2**; güven ≥0,75'te %88,5 isabet |
| Gürültü (yalnız sohbet) ayıklama kesinlik/duyarlılık | yok | %94 / %94 |
| Cevap iddiası harfi | yok (yalnız LLM) | %73 |
| "Önceki yıllarda çıkmış" önerisi, soru bankadaysa | yok | %98,9 doğru (kümelerin %54'ünde) |
| Aynı, soru bankada yoksa | — | 33 öneri: 28'i aynı sorunun başka yıldaki hâli, 5 yanlış |
| Kitle kaynak veri setleri (küme sayısı verilmeden) P / R | %99,8–82 / %16–9 | %99,8–98 / %57–39 |

Sınırlar (dürüst): ders sınıflaması dersler arası gerçek örtüşmede (genetik/patoloji/pediatri aynı hastalığı işler)
tavana yakın; bu yüzden ders gruplamada yalnız güven ≥0,75 iken ceza olarak kullanılır. Duyarlılık (%58) kesinliğe
(%76) göre bilerek düşük tutuldu: yanlış birleşme, eksik birleşmeden pahalıdır. bge-m3/e5 anlam vektörleri denendi:
katkı yok (AP 0,580 → 0,589), Oracle'ın tek çekirdeğine yük olacağı için kullanılmadı.

## Komutlar

```bash
npm run eval:recall                       # test kümesi (k4–k6)
npx tsx scripts/eval/recall-engine.mts --split all --bank include
npx tsx scripts/eval/recall-engine.mts --fit --l2 0.5 --drop opt   # çift modelini yeniden öğren (dev), eşik seç
npm run eval:recall:realtime              # Soru ekle anlık eşleşme: eski ↔ yeni
npx tsx scripts/eval/pool-cluster-check.mts   # gerçek data/questions.json üzerinde kümeler
```

Motoru değiştirmeden önce ve sonra `eval:recall` ve `eval:recall:realtime` çalıştırılır; test F1 ve ilk öneri doğruluğu
düşmemeli. Ağırlıklar yalnız `--fit` ile (geliştirme kümesinde) değiştirilir, test kümesine bakılarak elle ayarlanmaz.
Eski "4 aşamalı saf NLP" kitle kaynak denemesi: `scripts/archive/kitle_kaynak/README.md` (neden arşivlendiği).
