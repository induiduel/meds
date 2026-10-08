# Revize v2 — Faz 14 Sorularının Yeniden Revizyonu (Talimatlar, Yol Adımı, AI Promptu)

> **REVİZE V2.** Bu aşama, Faz 14 tarafından incelenen/düzeltilmeye çalışılan soruları yeniden
> revize eder; her değişikliği kaydeder, soruları müfredat/kazanıma bağlar, RAG (chunk) ile zeminler
> ve vektörleştirir. GPU yok, ücretsiz (CPU + ücretsiz bulut AI). Eski veritabanına **dokunulmaz**.

Konum: `meds/scripts/v2/revize/`. Çıktı (v2'den erişilebilir): `meds_database_core/revize_v2/`.

---

## 0. Bu aşama neyi, nereden alır? (yol adımı)

**Model seçimi (bu aşama için):**
- **Birincil:** `deepseek/deepseek-v4.1-flash` (Command Code Provider, `/chat/completions`) — yüksek kalite,
  düşük maliyet, çok yüksek limit.
- **İkincil:** `claude-sonnet-5-5` (Command Code Provider, `/messages` — Anthropic uçlu).
- Anahtar: `.env` → `CMD_API_KEY` / `CMD_API_BASE_URL`. Zincir `MEDS_CMD_MODELS` ve `MEDS_CMD_MSG_MODELS`
  ile değiştirilebilir. GPU yok.

**Girdi (salt okunur):**
1. `meds_database_v2/phase14_past_question_editor/reviews.jsonl` — Faz 14 inceleme kayıtları
   (`source` = orijinal soru, `proposal` = önerilen düzeltme, `status`, `support_ratio`, model).
2. **RAG bilgi tabanı:** `meds_database_core/chunks/` + `vectors/` (e5). Ders notu parçaları.
3. **Müfredat/kazanım:** `semantic` çekirdeği (Ders → Kurul → Konu → Kazanım ağacı).
4. **Tıbbi sözlük/ICD:** `semantic` (ICD-10, UMLS, QID).

**İşleme (yol adımı):**
```
reviews.jsonl (Faz 14)
   → mevcut soru sürümü seçilir (proposal; yoksa source)
   → normalize + OCR/temizlik (v2 textnorm)
   → kazanım & konu eşleme (semantic taxonomy)
   → RAG kanıt getirme (semantic Engine.retrieve → ders notu parçası + sayfa)
   → AI revizyonu (aşağıdaki prompt) → yapılandırılmış JSON
   → kural doğrulama (bu dosyanın kuralları) → düzelt veya karantinaya al
   → değişiklik kaydı (changes.jsonl)
   → çıktı (questions.jsonl) + vektörleştirme (vectors/)
```

**Çıktı (v2 deposunda):**
```
meds_database_core/revize_v2/
├── questions.jsonl     # revize edilmiş, doğrulanmış sorular
├── changes.jsonl       # her değişikliğin kaydı (alan, eski→yeni, neden, model, zaman)
├── quarantine.jsonl    # kurtarılamayan / karantinaya alınan sorular + neden
├── report.json         # özet + ölçümler
├── _state/             # checkpoint (kaldığı yerden devam)
└── vectors/            # e5 vektörleri (npy + ids) — RAG için
```

---

## 1. Zorunlu kurallar (her subagent bunlara uyar)

### 1.1 Soru kökü
- Soru kökü **var mı?** Yoksa: şıklardan/metinden yararlanılarak **oluşturulur** (veri modelleme).
- Varsa: **düzgün ve tıbbi anlamda doğru** bir soru mu?
- Doğru ise: **şıklar soruya uygun** mu?
- Yanlış/hatalı/eksik/yarım ise: **sorunun ve şıkların ortak paydası + kazanımlar** kullanılarak düzeltilir.
- Soruda bulunmaması gereken: soru no, öğrenci adı, slayt/ders başlığı, anlamsız ifadeler → **format bozmadan silinir**.

### 1.2 Şıklar
- **Doğru şık tekrar sorgulanır**, cevap **işaretlenir/teyit edilir** (kanıt zorunlu).
- Her şık **soru ile ilişkili mi?** İlişkisiz şıklar düzeltilir.
- İlişkisiz/hatalı şıklar **benzer çıkmış sorular ve kazanım** dikkate alınarak düzeltilir.
- **Yazım/dilbilgisi** hataları düzeltilir.
- Şıklar **gereksiz uzun olmamalı**, uygun formatta, **eksiksiz ve hatasız** olmalı.
- **Tüm şıklar doğru veya tüm şıklar yanlış olamaz.**

### 1.3 Öncüllü sorular
- Öncüllü ise **öncüller bulunmalı** (I, II, III …).
- Öncüller şıklara yazılmışsa → **format düzenlenip soruya eklenir**.
- Şıklar öncülleri **harf/sayı ile temsil eder** (ör. A) Yalnız I  B) I ve II …).

### 1.4 Açık uçlu sorular
- Format düzgün kurulmamışsa → **düzeltilir**.
- Şıklar yoksa → **bağlama ve kazanımlara uygun şıklar eklenir**.
- Soru kökü yoksa → **şıklardan/metinden** veri modellemesiyle **oluşturulur**.
- Ders notuyla karışmışsa → **soru ibaresi taşımayan metin elenir**.
- Şıklarla karışmışsa → **kurtarılabiliyorsa ayrılır**, değilse **elenir** (kendi şıkları bulunamıyorsa).
- Kök+cevap özet şeklindeyse → **uygun dil ve formatla** geliştirilir; **aşırıya kaçmadan** detaylandırılır,
  **şıklar eklenir**, kök zenginleştirilir; benzer/çıkmış sorularla desteklenir.

### 1.5 Ders kazanımı
- Her soru **bir dersin bir konusuna** aittir; her konunun **birden çok kazanımı** olabilir.
- Müfredat **ders → kurul → konu → kazanım** ilişkisini verir.
- Her soru için **kazanım ve bilgi paketi (ders notu parçası)** eşleşmesi **yapılır/doğrulanır/düzeltilir**.
- Sorular **uygun ders/kurul/konu/kazanıma dağıtılır**.
- Soru yapısı (kök, şıklar, öncüller, açıklama, cevap) **kazanımlara uygun** hazırlanır.

### 1.6 OCR / gürültü
- Kesik/bozuk (OCR) metin düzeltilebiliyorsa **incelemeye gönderilir**, düzeltilemiyorsa **karantina**.
- Soru no, kategori, öğrenci/slayt/ders ismi, anlamsız ifadeler **silinir** (soru formatı bozulmadan).

### 1.7 Ek dikkat
- **Anlamsal/mantıksal bütünlük:** tüm şıklar doğru/yanlış olmamalı.
- **Soru kökünün yönü korunur** (olumlu ↔ olumsuz değiştirilmez; "yanlıştır/değildir/hariç" korunur).
- **Her değişiklik kaydedilir** (ekleme, düzeltme, silme; eski→yeni + neden).

---

## 2. Kalite hedefleri

| Ölçüt | Hedef |
|---|---|
| Doğru cevabın seçilmesi | **≥ %96** |
| Soru kökünün doğruluğu | **≥ %90** |
| Şıklar | Tam, eksiksiz, gereksiz uzun değil, doğru format |
| Değişiklik kaydı | Her alan için zorunlu |

> Ölçüm: `report.json` — yapısal geçerlilik, kanıt desteği (`support_ratio`), yön koruma, şık bütünlüğü
> ve (varsa) Faz 14 cevap anahtarı ile uyum üzerinden hesaplanır.

---

## 3. AI Promptu (birebir kullanılır)

```
Sen bir tıp fakültesi sınav sorusu editörüsün. Aşağıdaki soruyu, SADECE verilen ders notu
kanıtlarına ve müfredat kazanımına dayanarak düzelt ve tamamla. Dışarıdan bilgi uydurma.

KURALLAR:
1) Soru kökü yoksa şıklardan/metinden uygun bir kök oluştur. Kök tıbbi olarak doğru ve net olsun.
2) Soru kökünün YÖNÜNÜ koru (olumlu/olumsuz; "yanlıştır/değildir/hariç" aynen kalsın). Değiştirme.
3) 4 veya 5 şık üret (A..E). Her şık soruyla ilişkili, kısa ve net olsun. Gereksiz uzun şık yazma.
4) Tüm şıklar doğru veya tüm şıklar yanlış olmasın.
5) Doğru şıkkı kanıta dayanarak seç ve gerekçesini yaz. Kanıt yoksa "dogru_secenek": null ve
   "belirsiz": true bırak.
6) Öncüllü soruysa öncülleri ayrı listele; şıklar öncülleri harf/sayı ile temsil etsin (ör. "Yalnız I").
7) OCR hatalarını, soru no/öğrenci/slayt/ders adı gibi gürültüleri temizle. Soru formatını bozma.
8) Açıklama kısa, tıbbi olarak doğru ve KANITA DAYALI olsun; ama kaynağa/ders notuna ATIF YAPMA.
11) YASAK: açıklamada veya kökte "kaynakta", "slaytta", "ders notunda", "kanıtta", "kanıt", "alıntı",
    "[Kaynak: ...]", "metinde" gibi ATIF/META ifadeler KULLANMA (kaynaklar ayrı alanda tutulur).
12) YASAK: "yanlış ifade olarak", "soru ... demektedir", "belirtilmektedir ki" gibi DOLAYLI/ANLATICI üslup.
    Açıklama, sınav çözümü gibi DOĞRUDAN klinik gerekçe yazsın.
13) Soru kökü SINAV FORMATINI korusun ("... hangisidir?", "... değildir?"). Kök anlatı cümlesine dönüşmesin.
14) aciklama_maddeleri: 3-6 madde; her madde tek klinik gerekçe. Doğru şıkkın nedenini ve gerektiğinde
    çeldiricilerin neden yanlış olduğunu belirt. Kaynağa atıf yok; sınav çözümü üslubu; tıbbi literatüre uygun.

**ÖRNEK AÇIKLAMA ÜSLUBU (hedef):**
> • Norplant, yavaş salınımlı levonorgestrel salgılayan klasik bir subdermal implant sistemidir.
> • Levonorgestrel endometriyumu gebeliğe elverişsiz hale getirir, servikal mukusu kalınlaştırır ve ovulasyonu baskılar.
> • A seçeneği aort stenozuna aittir; B seçeneği mitral darlık bulgusudur.
9) Soru gerçekten soru değilse (ders notu/başlık/şık yığını) ve kurtarılamıyorsa soru_degil=true ver.
10) Kanıt yetersizse zorla düzeltme; karantina=true ve neden yaz.

SORU (mevcut sürüm):
{kök}
ŞIKLAR: {secenekler}
İŞARETLİ CEVAP: {dogru_secenek}

MÜFREDAT: Ders={ders} | Konu={konu} | Kazanım={kazanim}

DERS NOTU KANITLARI (yalnız bunlara dayan):
{kanit_metinleri}  # her parça [kaynak: chunk_id, sayfa]

YALNIZCA şu JSON'u döndür:
{
 "soru_degil": false,
 "karantina": false,
 "neden": "",
 "soru_koku": "...",
 "oncul": ["I ...", "II ..."],
 "secenekler": {"A":"...","B":"...","C":"...","D":"...","E":"..."},
 "dogru_secenek": "A",
 "belirsiz": false,
 "aciklama": "...",
 "aciklama_maddeleri": ["..."],
 "kullanilan_kaynaklar": ["chunk_id", ...],
 "ders_adi": "...", "kurul_adi": "...", "konu_adi": "...", "kazanim": "...",
 "degisiklikler": [{"alan":"soru_koku","eski":"...","yeni":"...","neden":"..."}]
}
```

---

## 4. Çıktı kaydı şeması (questions.jsonl)

```
id                 : kaynak soru kimliği
durum              : revize | karantina
kategori           : kapali | oncul | acik
ders_adi, kurul_adi, konu_adi, kazanim
soru_koku, oncul[], secenekler{A..E}, dogru_secenek, aciklama, aciklama_maddeleri[]
kaynak_baglari[]   : {chunk_id, source_id, sayfa, alinti}
support_ratio      : kanıt desteği
dogrulama          : {soru_koku_ok, siklar_ok, yon_ok, cevap_ok, karantina}
degisiklikler[]    : her değişiklik (alan, eski, yeni, neden)
model, zaman        : üretici model + ISO zaman
revize              : "v2"
```

---

## 5. Çalıştırma

```bash
cd /home/indu/medsor/meds/scripts
PY=/home/indu/medsor/meds/.venv-ocr/bin/python

$PY -m v2.revize run --limit 50      # revize (kaldığı yerden devam eder)
$PY -m v2.revize report              # özet + ölçümler
$PY -m v2.revize vectorize           # revize soruları e5 ile vektörle (RAG)
```

Servis: `meds-revize` (systemd) — düşük hızda, ücretsiz kota dostu, kesintisiz sürer.
Erişim: dosyalar `meds_database_core/revize_v2/` altında (v2 deposu) + `/api/v2/...` üzerinden salt okunur.
