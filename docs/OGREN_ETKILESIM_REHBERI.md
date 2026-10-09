# Öğren Ders Ekranı · Etkileşim ve İçerik Rehberi

> **Kimin için:** Öğren destesi üreten ya da düzenleyen her ajan (Claude, Gemini, Codex, yerel modeller) ve geliştirici.
> **Ne zaman okunur:** Yeni deste, yeni slayt, yeni etkileşim (mini soru, gizli tablo, zincir…) eklemeden ya da Öğren ekranının kodunu değiştirmeden **önce**.
> **Zorunlu kapı:** Gönderimden önce `python3 scripts/validate_learning_decks.py` **0 HATA** vermeli.

---

## 1. Veri nereye yazılır, ekrana nasıl gelir

```
meds_temp / meds_database (boru hattı çıktısı)
        │  deste üretici (ör. scripts/build_batch*_deck.py, ajanlar)
        ▼
src/data/interactive_learning_decks.json      ← TEK DOĞRU KAYNAK (git'te izlenir)
        │  vite eklentisi scripts/vite/splitLearningDecks.ts (dev/derleme başında, kaynak değişince)
        ▼
src/data/decks/catalog.json + src/data/decks/items/<id>.json   ← ÜRETİLİR, .gitignore'da, ELLE YAZILMAZ
        │  python3 scripts/build_kazanim_deck_index.py
        ▼
src/data/kazanimlar/byDeck.json                ← deste → kazanım dizini (bilgi bölmesindeki "Kazanımlar")
```

Kurallar:

1. **Desteyi yalnız `src/data/interactive_learning_decks.json` içine yaz.** `decks/items/` klasörüne doğrudan yazılan her şey, kaynak bir sonraki değiştiğinde bölme eklentisi tarafından **silinir** ve git'te hiç yoktur. (2026-10-09'da 100 slaytlık Dismorfoloji dersi yalnız `items/` içinde bulundu ve kaynağa geri taşındı.)
2. Mevcut desteyi güncellerken aynı `id` ile **yerinde değiştir**; yeni deste listenin sonuna eklenir. Dosyayı biçimiyle yaz: `json.dump(data, f, ensure_ascii=False, indent=1)`, önce `.tmp` dosyasına, sonra `os.replace`.
3. **Boş sonuçla asla üzerine yazma.** Slaytı olmayan deste yazılmaz; toplu işten sonra deste sayısı azalmamalı.
4. Sıra:
   ```bash
   python3 scripts/validate_learning_decks.py yeni_deste.json   # önce taslağı denetle
   # …kaynağa ekle…
   python3 scripts/validate_learning_decks.py                    # 0 HATA olmalı
   npx vite build   # ya da dev sunucusu: items/ yeniden bölünür
   python3 scripts/build_kazanim_deck_index.py                   # kazanım dizini
   npm run lint                                                  # tsc 0 hata
   ```
5. Kazanım verisi (`src/data/kazanimlar/k*.json`) değiştiğinde `build_kazanim_deck_index.py` yeniden çalıştırılır.

---

## 2. Deste şeması

```jsonc
{
  "id": "k1p-k1-05-ornek-ders",          // zorunlu; yalnız harf, rakam, - ve _
  "deckId": "k1p-k1-05-ornek-ders",      // id ile aynı
  "title": "Örnek Ders: Tam Başlık",     // zorunlu
  "shortTitle": "Örnek Ders",            // üst çubukta görünür
  "discipline": "Tıbbi Patoloji",        // zorunlu (yeni içerik); üst bilgide görünür
  "committee": "Kurul 1 (…)",
  "instructor": "Prof. Dr. …",
  "overview": "Dersin 2-3 cümlelik özeti",              // Araçlar → Ders notları
  "highYieldPearls": ["📌 [SINAV SPOTU] …"],             // Araçlar → Ders notları
  "matchedPastQuestionsCount": 12,                       // bilgi bölmesi → Sorular
  "kazanimlar": ["… kazanım metni …"],                   // varsa doğrudan kullanılır
  "slides": [ /* §3 */ ]
}
```

---

## 3. Slayt (adım) şeması

```jsonc
{
  "slideNumber": 1,                       // 1'den başlar, kesintisiz artar
  "title": "Konu: Alt başlık",            // ":" öncesi bölüm listesinde KONU, sonrası ALT BAŞLIK olur
  "subtitle": "Tek cümlelik özet",        // ASLA "…" ile kesme
  "badge": "Temel Kavram",                // ardışık aynı badge'ler bölüm listesinde tek bölüm olur
  "synthesisNarrative": "Markdown anlatım (§4)",
  "coreContent": {
    "keyBullets": [{ "title": "…", "desc": "…", "isKey": true }],
    "table": { "title": "…", "headers": ["A", "B", "C"], "rows": [["…", "…", "…"]] },
    "infographic": { "type": "metrics|process|comparison", "items": [{ "label": "…", "value": "%15", "detail": "…", "color": "red|amber|green|blue" }] },
    "formulaBox": { "title": "…", "formula": "…", "explanation": "…" }
  },
  "spotPearls": ["📌 [SINAV SPOTU] …", "🚨 [KRİTİK UYARI] …"],
  "medicalTerms": [{ "term": "Fenotip", "explanation": "…" }],
  "flashcards": [{ "id": "fc-1", "front": "Soru", "back": "Cevap", "hint": "…", "category": "…" }],
  "relatedQuestions": [ /* §6 */ ],
  "interactiveElements": [ /* §5 */ ],
  "professorAudioHighlight": { "quote": "…", "note": "…", "emphasisType": "pearl|direct_exam_warning|clinical_tip" },
  "importantPoint": "…", "examTip": "…",
  "sourcePdf": { "fileName": "…pdf", "startPage": 2, "endPage": 3, "primaryPage": 2, "citation": "Slayt 5 · Kurul 1 …" },
  "isCheckpoint": false, "checkpointNumber": 0
}
```

### Bölümler (sol liste)
- **Tekrar sayfası varsa** (`isCheckpoint: true`, başlık `"[TEKRAR SAYFASI - CHECKPOINT n] Bölüm adı"`), her tekrar sayfası bir bölümü kapatır ve bölümün adı olur. Önerilen yol budur: her 6–12 adımda bir tekrar sayfası.
- Yoksa ardışık aynı `badge` değerleri bir bölüm olur. Badge'ler her slaytta farklıysa 8–10 adımlık gruplar oluşur ve grubun ilk konusu bölüm adı olur.

### Ekranda nerede görünür
| Alan | Ana içerik | Bilgi bölmesi (altta) | Pekiştir |
|---|---|---|---|
| title / subtitle / synthesisNarrative / keyBullets / table / infographic / formulaBox | ✓ | | |
| spotPearls | | Sınav spotu | |
| medicalTerms (+ metinde geçen sözlük terimleri) | altı noktalı terim | Terimler | |
| professorAudioHighlight / importantPoint / examTip | | Hoca notu | |
| kazanımlar (byDeck.json, sıkı eşleşme) | | Kazanımlar | |
| relatedQuestions / practiceQuestion | | Sorular (her soruda "Çöz") | ✓ |
| interactiveElements / flashcards | | | ✓ |
| sourcePdf | | Kaynak (PDF'te aç) | |

Ana içerikte yalnız ders anlatılır; kaynak, terim listesi, kazanım ve sayılar bilgi bölmesine aittir. Anlatıma "PDF'te aç", "Panelde oku", "Kapsamlı ders notu" gibi başlığa ait olmayan satırlar **yazılmaz**.

## 4. Metin Biçimi, Sayfa Düzeni ve Tekrarı Önleme Kuralları

- **Bitişik Blok Metin Yasağı & Madde İmleri:** Asla 80-130 kelimelik tek bir bitişik blok paragraf yazılmamalıdır. İçerik gözü dinlendiren, nefes alan bir sayfa mimarisine sahip olmalıdır:
  * **1-2 Cümlelik Giriş:** Konunun ana eksenini belirten net başlangıç.
  * **Maddeler Halinde Aşamalar:** Biyokimyasal veya fizyopatolojik aşamalar `- **Aşama / Kavram:** Açıklama` biçiminde maddeli yazılmalıdır.
  * **Paragraf Boşlukları:** Bloklar arasında çift satır kırılımı (`\n\n`) olmalı, metin parçalı ve tane tane okunmalıdır.
  * **Vurgu Kutusu:** Önemli sınav spotu veya klinik kural `> [!NOTE]` veya `> [!IMPORTANT]` içinde ayrı bir kutu olarak verilmelidir.
- **Adımlar Arası Tekrarı Önleme (Sıfır Tekrar):** Her slayt zincirde yeni ve özgün bir bilgi sunmalıdır. Önceki veya sonraki adımlarda anlatılan genel tanımlar (örneğin "Anöploidi nedir...", "En sık anne yaşından kaynaklanır...") her slaytın başında kopyala-yapıştır yapılarak tekrarlanamaz. Her slayt sadece kendi spesifik alt başlığına odaklanmalıdır.
- **Asgari Kelime Yoğunluğu (Orta Yoğunluk):** Her slaytın anlatım metni (`synthesisNarrative` veya `content`) **EN AZ 60 KELİME** (ideal orta yoğunluk: **70 - 150 kelime**) içermelidir. Sayfalar asla boş, tek cümlelik veya 20-30 kelimelik yüzeysel özetlerle geçiştirilemez. Tıbbi mekanizmalar, hücresel/organ düzeyindeki süreçler ve klinik bağlantılar tam cümlelerle anlatılmalıdır.
- **Müfredat ve Ders Özeti Sadakati (Örnek Sorular):** Örnek sorular (`ornek_sorular/` ve destelerdeki soru havuzu) oluşturulurken **YALNIZCA müfredat ve ilgili amfi ders özetinde (`meds_database_v2/ders_notlari_k*/`) yer alan bilgiler** kullanılmalıdır. Müfredat dışı, kaynakta geçmeyen afaki/spekülatif bilgilerle soru yazılamaz; sorular doğrudan dersin öğrenim hedefleriyle örtüşmelidir.
- Markdown: `**kalın**`, `==vurgu==` (sarı işaret; paragraf başına en fazla 2), `- madde` ve iki boşlukla alt madde, `### Ara başlık`, `> Temel ilke…` (mavi kutu; içinde UYARI/DİKKAT/TUZAK/KRİTİK geçerse turuncu).
- Tablolar `| a | b |` biçiminde yazılabilir; ekrana sığan tabloya çevrilir (dar ekranda kartlara dönüşür). Sütun sayısı 2–4 arası tutulmalı.
- Etiketler: `[SINAV SPOTU]`, `[KRİTİK UYARI]`, `[KLİNİK İPUCU]`, `[YÜKSEK VERİM]` (4+ büyük harf, köşeli parantez) renkli etikete dönüşür. Başka amaçla köşeli parantez içinde **büyük harfli 4+ karakter** kullanma.
- Satır başındaki emoji (📌🚨🔴🔵) ekranda gizlenir; anlam etiketle verilmeli.
- **Kesme yasak:** hiçbir alan `...` ya da `…` ile bitmez. Üretici bir metni kısaltması gerekiyorsa tam cümle kurar.
- Tıbbi içerik `GEMINI.md` kurallarına uyar: mekanizma önce, kaynaklı, sınav dilinde, spekülasyonsuz.

---

## 5. Etkileşim türleri (`interactiveElements[]`)

Her slaytta 1–4 etkileşim önerilir. Ekranda **Pekiştir** bölümünde sekmeler halinde (Akış) ya da sağ panelde (Stüdyo) görünür. Her kartta öğrencilerin hata bildirebildiği bir bayrak vardır (§7).

### 5.1 `micro_quiz` — Mini soru
```json
{ "type": "micro_quiz", "question": "…?",
  "microQuizOptions": [
    { "key": "A", "text": "…", "isCorrect": false, "explanation": "Yanlış. … neden" },
    { "key": "B", "text": "…", "isCorrect": true,  "explanation": "Doğru! … mekanizma" } ] }
```
- 4–5 şık, **tam olarak bir** `isCorrect: true`.
- **Her şıkta `explanation` zorunlu:** ilk seçim cevabı belirler; sonra her şıkka dokununca açıklaması o şıkkın kartının içinde "Neden doğru / Neden yanlış" başlığıyla açılır, aynı şıkka tekrar dokununca kapanır. Açıklama "Doğru!/Yanlış." ile başlayabilir (ekranda temizlenir), ardından gerekçe gelir.

### 5.2 `branching_logic` — Klinik karar
```json
{ "type": "branching_logic", "scenario": "Vaka…; ilk yaklaşımınız?",
  "options": [ { "text": "…", "isCorrect": true, "feedback": "…" }, { "text": "…", "isCorrect": false, "feedback": "…" } ] }
```
- 3–4 seçenek, tek doğru, her seçenekte `feedback`. Harfler ekranda otomatik verilir.

### 5.3 `cloze_masking` — Boşluk doldur
```json
{ "type": "cloze_masking", "sentence": "… FMR1 geninin 5' UTR bölgesindeki CGG trinükleotid tekrar artışıdır.",
  "maskedTerm": "CGG", "hint": "Sitozin-Guanin-Guanin nükleotid tripleti" }
```
- `maskedTerm` cümlede **birebir** geçer. Köşeli parantezle işaretlenebilir (`[CGG]`); ekran parantezleri de boşluğa dahil eder, ama yeni içerikte **parantezsiz** yazmak tercih edilir.
- `hint` cevabın hiçbir kelimesini/parçasını içermez (§5.9).

### 5.4 `interactive_table` — Gizli tablo
```json
{ "type": "interactive_table", "tableTitle": "…", "tableHeaders": ["Parametre", "Değer", "Not"],
  "tableRows": [ { "cells": [
    { "text": "Haploid baz çifti", "isMasked": false },
    { "text": "3.2 milyar bp", "isMasked": true, "hint": "Gb cinsinden" },
    { "text": "23 kromozom", "isMasked": false } ] } ] }
```
- Her satırda başlık sayısı kadar hücre; satır başına 1 gizli hücre; ilk sütun gizlenmez.
- Gizli hücre ipucu cevabı ele vermez: `"~20.000 gen"` için `"Yaklaşık gen adedi"` **yasak** ("gen"), `"45,X Monozomisi"` için `"45,X"` **yasak**. İpucu yoksa düğmede "Göster" yazar.

### 5.5 `causal_chain` — Mekanizma zinciri
```json
{ "type": "causal_chain", "chainTitle": "Mekanizma Basamakları",
  "steps": [ "1. Tetikleyici: …tam cümle…", "2. Patofizyolojik ilerleme: …", "3. Klinik sonuç: …" ] }
```
- 3–6 basamak; biçim `"N. Etiket: açıklama"` (etiket 48 karakteri geçmez, ekranda küçük başlık olur).
- **Uzunluk sınırı yok, kesme yasak.** Metin ekranda tamamen ve satır kırılarak gösterilir. (24 basamak "…" ile kesilmişti; `--duzelt` ile slayttaki tam metinden tamamlandı.)

### 5.6 `before_after_slider` — Karşılaştır
```json
{ "type": "before_after_slider", "leftTitle": "Sitogenetik", "rightTitle": "Moleküler genetik",
  "leftPoints": ["…", "…", "…"], "rightPoints": ["…", "…", "…"] }
```
- Sol ve sağ madde sayısı **eşit**; aynı sıradaki maddeler aynı ölçütü karşılaştırır (ekranda aynı satırda durur).

### 5.7 `active_recall` — Aktif hatırlama
```json
{ "type": "active_recall", "question": "… en kritik sınav ayrımı nedir?", "answer": "…" }
```
- Soru kendi başına anlaşılır; slayt başlığını kesip kopyalama.

### 5.8 Kartlar (`flashcards`)
- `front` ≤ 140 karakter tek soru; `back` 1–2 cümle; `category` kısa etiket. Eski `question/answer` alanları da okunur ama yeni içerikte `front/back` kullanılır.

### 5.9 Ortak kurallar
- **İpucu sızıntısı yasak:** ipucu, cevabın 3+ harfli herhangi bir kelimesini (ya da 5+ harfli kelimenin ilk 5 harfini) veya bir sayısını içeremez. Doğrulayıcı `ipucu-sizinti` olarak yakalar; ekran da böyle ipuçlarını göstermez.
- Hiçbir metin `…` ile bitmez (`kesik-metin`).
- Türkçe tıp dili, sınav üslubu; kaynak atfı ("slaytta", "notta") yazılmaz.

---

## 6. Sorular (`relatedQuestions[]`, `practiceQuestion`)

```json
{ "id": "k1-01-…-q05", "examYear": "2026-2027 Kurul 1", "stem": "…?",
  "options": [ { "key": "A", "text": "…", "explanation": "…" }, … ],
  "correctAnswer": "D", "explanation": "Genel açıklama", "isPracticeQuestion": true }
```
- `correctAnswer` **yalnız tek harf (A–E)**. Eski veride sıra numarası (`0`, `1`) ya da tam şık metni (`"E) …"`) var; ekran bunları okur ama yeni içerikte kullanılmaz (`soru-cevap-eski` uyarısı).
- Şık başına `explanation` önerilir (öğrenci şıkları tek tek açabiliyor). Şık açıklaması yoksa genel `explanation` metnindeki şu satırlar ilgili şıkka dağıtılır: `Doğru cevap B'dir: …`, `A seçeneği yanlıştır: …`, `C şıkkı doğrudur: …`, `D) yanlış - …`. Bu kalıplara uymayan satırlar şıkların altındaki **Açıklama** panelinde gösterilir. Yeni içerikte her şık gerekçesini ayrı satıra bu kalıpla ya da doğrudan `options[].explanation` alanına yaz.
- Çıkmış sınav sorusuysa `examYear` gerçek sınavı, çalışma sorusuysa `isPracticeQuestion: true` taşır.

---

## 7. Öğrenci hata bildirimi (geri bildirim)

Her Pekiştir kartında, tabloda, adım başlığında ve bilgi bölmesindeki her öğede (spot, terim, hoca notu, önemli nokta, sınav ipucu) bayrak düğmesi vardır. Bildirim yapılmış öğede bayrak turuncu ve sayılıdır; tıklanınca bildirimler (kim, ne zaman, **hangi bilgi yanlış**, **neden yanlış**) ve 👍/👎 oyları açılır.

**Uç noktalar** (`server.ts`, mantık `src/services/learnFeedbackService.ts`, kayıt `data/learn_feedback.json`):

| Yöntem | Yol | Gövde / sorgu | Yanıt |
|---|---|---|---|
| GET | `/api/learn/feedback` | `?deckId=…&voterId=…` | `{ items: [{ id, targetKey, targetLabel, field, reason, author:{id,name}, createdAt, up, down, myVote, mine }] }` |
| POST | `/api/learn/feedback` | `{ deckId, deckTitle, slideNumber, targetKey, targetLabel, location, field, reason, author:{id,name} }` | `{ success, item }` (sunucu `link` üretir) · 400: `field` < 3 ya da `reason` < 5 karakter |
| POST | `/api/learn/feedback/:id/vote` | `{ voterId, vote: 1 \| -1 \| 0 }` | `{ success, item }` · kendi bildirimine oy verilemez |
| POST | `/api/admin/learn-feedback/:id/resolve` | (yönetici) | bildirimi kapatır, listeden düşer |

- `targetKey` biçimi: `"<slideNumber>:<tür>:<sıra|kimlik>"` — ör. `5:ix-micro_quiz:1`, `5:q:k1-01-…-q05`, `5:table:0`, `5:term:Fenotip`, `5:spot:0`, `5:text:0`. İçerik değişip öğe sırası kayarsa eski bildirim yanlış öğede görünebilir; etkileşim **eklerken sona ekle**, var olanların sırasını değiştirme.
- **Konum:** her bildirim öğenin ekrandaki yerini taşır (`location`): `Ana içerik › Başlık ve anlatım`, `Ana içerik › Tablo: <başlık>`, `Pekiştir › Mini soru (2. etkinlik)`, `Bilgi bölmesi › Sınav spotu › 1. öğe`, `Bilgi bölmesi › Terimler › 3. öğe (Terim: Fenotip)`, `Bilgi bölmesi › Hoca notu (Önemli nokta)`.
- **Derin bağlantı:** sunucu her bildirime `link = /ogren/<deckId>?adim=<slideNumber>&hedef=<targetKey>` yazar. Bu bağlantı açılınca ders o adımda açılır; hedef bilgi bölmesindeyse ilgili sekme (Akış) ya da kutucuk (Stüdyo), Pekiştir'deyse ilgili etkinlik sekmesi açılır; öğe ekrana kaydırılır ve mavi çerçeveyle vurgulanır. Öğe artık yoksa "Bildirilen öğe bulunamadı" uyarısıyla adım açılır. Adres çubuğundaki `adim/hedef` okunduktan sonra temizlenir.
- Her ekran öğesi hedef anahtarını `data-fb-key` niteliğinde taşır; yeni bir bildirilebilir öğe eklerken bu niteliği ve bayrağın `target.key` değerini aynı tut.
- Her yeni bildirim yöneticiye e-posta + telefon bildirimi olarak gider (`triggerAdminNotification`, `link` parametresiyle). E-postadaki/bildirimdeki bağlantı doğrudan öğeye gider; konu satırı `[MedSoru Öğren Hata Bildirimi] <Ders> · Adım n`.
- Sunucuya ulaşılamazsa bildirim tarayıcıda (`medsoru_learn_feedback_local_v1`) "yalnızca bu cihazda" olarak saklanır; oylanamaz.
- İstemci: `src/components/learn/lesson/lessonFeedback.ts` (API + kimlik), arayüz: `LessonFeedbackUI.tsx`.

---

## 8. Yeni bir etkileşim TÜRÜ eklemek (kod)

Dosyalar: `src/components/learn/lesson/`
1. **Şema:** bu rehberde §5'e yeni alt başlık ekle (alanlar, kurallar, örnek JSON).
2. **Doğrulayıcı:** `scripts/validate_learning_decks.py` → `TYPES` kümesine ekle, `check_deck` içinde zorunlu alanları denetle.
3. **Veri katmanı:** `lessonModel.ts` → gerekiyorsa `repairInteractive` içinde eski/bozuk biçimleri normalleştir.
4. **Görünüm:** `LessonBlocks.tsx` → `IX_META` (ikon + kısa Türkçe ad, ≤ 18 karakter), yeni bileşen, `IxBody` içindeki `switch`. Bileşen tamamlanınca `onDone()` çağırır (adım ilerlemesi ve "Tamam" etiketi buna bağlı).
5. **Stil:** `src/index.css` sonundaki `ls-*` bloklarına; renkler yalnız `--color-*` token'larıyla (açık/koyu tema), dar ekran için `@container ls-col` / `@media (max-width: 767px)`.
6. **Hata bildirimi:** `PracticeCard` hedefi otomatik `"<adım>:ix-<tür>:<sıra>"` olur; ek iş gerekmez.
7. **Doğrulama:** `npm run lint` 0 hata; tarayıcıda 1440 px ve 375 px genişlikte Akış + Stüdyo, koyu tema, etiketlerin taşmaması, `onDone` sonrası adımın ✓ olması.

### Ekran kuralları (değiştirirken korunmalı)
- Telefonda (≤ 767 px) yalnız **Akış (A)** düzeni; Stüdyo (B) masaüstü/tablette Araçlar → Düzen'den seçilir.
- İkincil özellikler **Araçlar** menüsündedir: Düzen, Görünüm (Ders / Yan yana / PDF), Okuma (Sayfa sayfa / Kaydırarak), Hatırlama modu, Fosforlu kalem + Kalem modu, Ders notları, Asistana sor, Tıbbi sözlük, Tam ekran, Bu adımı PDF yap, Klasik görünüm.
- Tam ekran belge kökünü tam ekrana alır; API yoksa/yanıtsızsa (iPhone) odak moduna düşer.
- Kalem/çizim katmanı (`SlideDrawingCanvas`) CSS pikseliyle çizer; DPR ile ikinci kez çarpma (telefonda çizgiler kayıyordu).
- **Kalem algılama** (`src/components/ui/penInput.ts`): bir kez `pointerType: "pen"` görülünce cihaz kalemli sayılır (oturum boyunca). Kalemli cihazda marker ve çizim yalnız kalemle yazar; parmak sayfayı kaydırır (`startFingerPan`). Kalem hiç görülmezse parmak yazar. Yüzen çubuktaki "Parmakla yaz" algılamayı sıfırlar.
- **Araçlar menüsü** her seçimden sonra kapanır. Marker ve Kalem seçilince ekranın tepesinde yüzen çubuk açılır: marker için 4 renk + silgi; kalem için Kalem/Marker/Silgi, 6 renk, 3 kalınlık; kalem/parmak durumu ve kapatma. İşaretlerken bilgi çekmecesi gizlenir.
- Kalıcı tercih anahtarları: `medsoru_learn_layout`, `medsoru_learn_mode`, `medsoru_learn_toc`, `medsoru_learn_done_v1`, `medsoru_learn_progress_v1`, `medsoru_learn_voter_id`.

---

## 9. Gönderim öncesi kontrol listesi

- [ ] Deste yalnız `src/data/interactive_learning_decks.json` içinde; `items/` elle değiştirilmedi.
- [ ] `python3 scripts/validate_learning_decks.py` → **0 HATA** (yeni destede uyarı da olmamalı).
- [ ] Hiçbir metin `…` ile bitmiyor; ipuçları cevabı ele vermiyor.
- [ ] Mini soru/klinik karar: tek doğru, her şıkta açıklama.
- [ ] Zincir basamakları "N. Etiket: tam cümle"; karşılaştırmada sol/sağ eşit.
- [ ] `correctAnswer` tek harf; şıklarda `key` A–E.
- [ ] Her 6–12 adımda bir tekrar sayfası ya da tutarlı `badge` ile bölümleme.
- [ ] `python3 scripts/build_kazanim_deck_index.py` çalıştırıldı.
- [ ] `npm run lint` 0 hata; ekranda Akış ve Stüdyo'da göz kontrolü.

## Not kutuları (anlatım içinde `>`)

Ardışık `>` satırları tek not kutusu (`ls-note`) olur. İlk satır `[!NOTE]`/`[!IMPORTANT]`/`[!WARNING]`/`[!TIP]` ya da `[TEMEL İLKE]`, `[SINAV SPOTU]`, `[KRİTİK UYARI]` gibi büyük harfli bir etiketse etiket notun başlığına taşınır. Ton etiketten seçilir (kritik/uyarı → kırmızı, sınav/spot → turuncu, klinik/önemli/ipucu → mavi, özet/yüksek verim → yeşil, diğerleri nötr). `> [!NOTE]` satırını tek başına bırakıp metni sonraki `>` satırına yazmak doğrudur.
