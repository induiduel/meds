# Sesli soru çözücü — 2. adım: soru denetimi + açıklama + ses metni (yazar ajan talimatı)

Çalışma klasörü: `/home/indu/medsor/meds_temp/spot_cozucu/<brans>/`. 1. adımın çıktısı `onem/<kod>.json` hazır (maddeler, maddelerdeki
`ornek` soruları, maddelerin `cikmis` listeleri, `elenen_cikmis`). Çıkmış soruların tam metni `cikmis/<kod>.json`'da (temsilciler).
Ders PDF metni `pdf_metin/<kod>.md` — **tek kaynak**, baştan sona oku.

Öğrenci tam ekran bir "soru çözücü" ile dersin sorularını çözer (örnek + çıkmış karışık, 20–40 soruluk setler). Anlatım YOK, yalnız soru.
Asistan (EMA, Türkçe kadın sesi; metin harfi harfine okunur) soruyu ve şıkları okur. Öğrenci şık seçer ya da yardım düğmelerine basar:
- **İpucu** → `ipucu` okunur (cevabı söylemeden düşündürür).
- **Bir yanlışı ele** → rastgele bir yanlış şık vurgulanır, `siklar[harf]` okunur, şık elenir.
- **Çözümü dinle** → şıklar A'dan E'ye tek tek vurgulanıp `siklar[harf]` okunur, sonra "Doğru cevap X, <şık>." + `cozum` okunur.
- Yanlış şık seçerse "Yanlış." + o şıkkın `siklar` açıklaması; doğruyu seçerse "Doğru!" + `cozum`.
Bu yüzden her `siklar` açıklaması **tek başına** anlaşılır olmalı (önce/sonra ne çalınacağını varsaymaz).

## Hangi sorular
- `onem/<kod>.json` → her maddenin her `ornek` sorusu: `ref` = `"o:<madde_id>:<sıra>"` (sıra 1'den; ör. `o:e07-03:1`), `tur: "ornek"`,
  `onem_id`, `zorluk` örnekteki gibi.
- Maddelerin `cikmis` listelerindeki her çıkmış temsilci (bir kez): `ref` = `"c:<id>"`, `tur: "cikmis"`, `onem_id` = bağlandığı ilk madde,
  `sinav` = temsilcinin `sinav` alanı. `soru` = temsilcinin `kok`u; `soru`, `secenekler`, `dogru` **BİREBİR** kopyalanır (yazım hatası bile
  düzeltilmez; yalnız baş/son boşluk).
- `elenen_cikmis`teki sorular ALINMAZ.

## Kesin kurallar
1. **Tek kaynak ders PDF'i.** Açıklamalardaki her tıbbi bilgi PDF metninde geçmeli (aynı ya da açıkça eşdeğer ifade). Kitap/genel bilgi
   ekleme, sayı uydurma. Bir çeldirici kavram PDF'te hiç yoksa onun hakkında bilgi UYDURMA: "X bu sorunun cevabı değil; …" diyerek PDF'teki
   doğru bilgiyi öğret (sorunun sorduğu özelliğin gerçekte neye ait olduğunu söyle).
2. **Önce soruyu denetle (hatasızlık).** PDF'e göre doğru cevap tartışmasız tek doğru mu? Başka şık da doğru sayılabilir mi? Kök belirsiz mi?
   - Örnek soruda sorun varsa en küçük düzeltmeyi yap ve AYNI düzeltmeyi `onem/<kod>.json`'daki örneğe de yaz (iki dosya aynı kalmalı);
     `kontrol: {"durum": "duzeltildi", "not": "neyi neden değiştirdin, PDF s. n"}`. Sorun yoksa `kontrol: {"durum": "tamam"}`.
   - Çıkmış soruyu DEĞİŞTİRME. Anahtar PDF'le çelişiyorsa ya da PDF kapsamı dışındaysa soruyu alma: `onem/<kod>.json`'da maddelerin
     `cikmis` listesinden çıkar, `elenen_cikmis`e `{id, neden, not}` ekle; örnek sayısı alt sınırın altına düşerse yeni örnek soru ekle
     (TALIMAT_ONEM.md kurallarıyla) ve `onem_dogrula.py`'yi yeniden geçir.
3. **Öğrenciye dönük dil:** "PDF", "kaynak", "slayt", "ders notu", "talimat", "ipucu", "çeldirici", "şık" (hiç kullanma; asistan harfleri
   kendisi söyler), "A şıkkı" gibi harf anma YASAK. Soru numarası okunmaz. "Hoca", "sınavda şu yıl" yok. Kısa, net, öğretici; dolgu sözcüğü yok.
4. **Kısa:** açıklamalar 1–2 cümle; her cümle tek bilgi; akılda kalıcı hap cümle.

## Alanlar (soru başına)
- `ref`, `tur`, `onem_id`, (`zorluk` | `sinav`), `kontrol`, `soru`, `secenekler` {A..E}, `dogru`.
- `kok_ses`: kökün ses biçimi (anlam birebir aynı; şıkları içermez). Öncüllü sorularda öncüller de köke dahildir ("Bir, … İki, …").
- `secenek_ses`: {A..E} her şıkkın ses biçimi (yalnız şık metni; harf yok). "I ve III" → "bir ve üç"; "Yalnız II" → "yalnız iki".
- `ipucu`: {metin, ses} — TEK cümle, 6–24 kelime. Cevabı söylemez; doğru şık metnindeki 4+ harfli hiçbir sözcüğün ilk 5 harfi ipucunda
  geçmez; cevabın sayısı geçmez; eşanlamlı ya da tanımla da sızdırmaz. Hangi mekanizmayı/ayırt edici özelliği hatırlamalı, hangi kavram
  çiftini ayırmalı — onu söyler.
- `siklar`: {A..E} her şık için {metin, ses} — 1–2 cümle, 6–36 kelime:
  - Yanlış şık: şıktaki kavramla başla, PDF'teki gerçek özelliğini söyle, neden bu sorunun cevabı olmadığını göster.
  - Doğru şık: şıktaki kavramla başla, "doğru" sözcüğünü içersin, neden doğru olduğunu söylesin.
  - "Hangisi yanlıştır/değildir" sorularında doğru şıkkın açıklaması: ifadenin neden yanlış olduğu + "bu yüzden doğru cevaptır"; diğer
    şıklarda ifadenin neden doğru olduğu (yani cevap olmadığı).
  - Öncüllü sorularda şık açıklaması hangi öncülün doğru/yanlış olduğunu söyler.
  - Her açıklama o şıkka özgü; beş açıklama birbirini tekrar etmez. Sayılar PDF'teki gibi.
- `cozum`: {metin, ses} — 1–2 cümle, 10–42 kelime: sorunun öğrettiği ana bilgi + ayırt edici nokta. "Doğru cevap …" diye BAŞLAMA.
- `sayfa`: sorunun bilgilerinin geçtiği PDF sayfaları (`[26, 33]`), en az 1.

## Çift biçim: `metin` (ekranda) ve `ses` (EMA okur)
İkisi aynı içerik, yalnız yazım farklı.
- `metin`: normal Türkçe yazım; kısaltma, sayı, simge serbest (`ÜSE`, `%30`, `≥10⁵`). `**kalın**` ile en kritik 1 terim. Parantez kullanma.
- `ses` (ve `kok_ses`, `secenek_ses`):
  - **Sayılar ve simgeler yazıyla:** "%10" → "yüzde on", "1–2" → "bir ile iki", "≥10⁵ CFU/ml" → "mililitrede on üzeri beş ya da daha fazla
    koloni", "2 g" → "iki gram", "x2" → "günde iki kez" (PDF'te öyleyse), "~700" → "yaklaşık yedi yüz", "≥" → "eşit ya da büyük".
    Rakam (0–9), %, /, →, ±, ≈, ~, <, >, =, +, ⁺, parantez, köşeli parantez, `*`, `#`, `:`, `;`, tırnak, `|` (durak hariç) YASAK.
    `:` ve `;` yerine virgül ya da nokta. Roma rakamı sayıyla ("tip iki", "öncül üç").
  - **Kısaltmalar harf harf, Türkçe harf adlarıyla, boşlukla ayrık:** A a, B be, C ce, Ç çe, D de, E e, F fe, G ge, H ha, I ı, İ i, J je,
    K ka, L le, M me, N ne, O o, Ö ö, P pe, R re, S se, Ş şe, T te, U u, Ü ü, V ve, Y ye, Z ze, Q ku, W çift ve, X iks.
    Örnekler: HIV → "ha i ve", HPV → "ha pe ve", HSV → "ha se ve", CMV → "ce me ve", ÜSE → "ü se e", CYBE → "ce ye be e", PID → "pe i de",
    VUR → "ve u re", PCR → "pe ce re", ELISA → "e le i se a" (yerleşik okunuş "elayza" de olur), MRSA → "me re se a", VRE → "ve re e",
    ESBL → "e se be le", CRP → "ce re pe", BT → "be te", USG → "u se ge", IVP → "i ve pe", ESWL → "e se çift ve le", PNL → "pe ne le",
    DMSA → "de me se a", ADH → "a de ha", DDAVP → "de de a ve pe", IM → "i me", IV → "i ve", PO → "pe o".
  - Yalnız şu yerleşik okunuşlar kelime gibi kalır: AIDS → "eyds", TORCH → "torç", COVID-19 → "kovid on dokuz", SARS-CoV-2 → "sars ko ve
    iki"; VDRL → "ve de re le", RPR → "re pe re" harf harf.
    Bunların dışında kısaltmayı birleştirme, kelime gibi okutma ("hıv", "üse", "denea" YASAK).
  - Türkçe açılımı yerleşik ve kısaysa açılımı kullanabilirsin (ÜSE → "üriner sistem enfeksiyonu", CYBE → "cinsel yolla bulaşan
    enfeksiyon"), ama cevabı ele verecekse kullanma.
  - **Latince/İngilizce adlar Türkçe okunuşla:** "Treponema pallidum" → "Treponema pallidum", "Chlamydia trachomatis" → "Klamidya
    trakomatis", "Neisseria gonorrhoeae" → "Nayseriya gonore", "Escherichia coli" → "Eşerişya koli", "Proteus mirabilis" → "Proteus
    mirabilis", "Klebsiella" → "Klebsiella", "Staphylococcus saprophyticus" → "Stafilokokus saprofitikus", "Trichomonas vaginalis" →
    "Trikomonas vajinalis", "Candida" → "Kandida", "Gardnerella" → "Gardnerella", "Mycoplasma" → "Mikoplazma", "Ureaplasma" →
    "Üreaplazma", "Pseudomonas" → "Psödomonas", "Enterococcus" → "Enterokok", "ceftriaxone" → "seftriakson", "Jarisch-Herxheimer" →
    "Yariş Herksaymır". Yerleşik Türkçe tıp yazımı ("siprofloksasin", "nitrofurantoin", "fosfomisin").
  - **Yunan harfleri:** α alfa, β beta, γ gama. "β-laktam" → "beta laktam".
  - **Duraklar:** cümle sonu nokta. Vurgudan önce kısa durak ` | ` — cümle başına en çok bir; çoğu cümlede hiç gerekmez.
  - 25 kelimeden uzun ses cümlesini ikiye böl. Büyük harfli kısaltma, `**` ya da karışık harf (IgG, mRNA) seste YASAK.

## Çıktı — `cozucu/<kod>.json`
```json
{"kod": "e07", "sorular": [
 {"ref": "o:e07-03:1", "tur": "ornek", "onem_id": "e07-03", "zorluk": "orta", "kontrol": {"durum": "tamam"},
  "soru": "…", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C",
  "kok_ses": "…", "secenek_ses": {"A": "…", …}, "ipucu": {"metin": "…", "ses": "…"},
  "siklar": {"A": {"metin": "…", "ses": "…"}, …}, "cozum": {"metin": "…", "ses": "…"}, "sayfa": [3]},
 {"ref": "c:c1b740ecd59e", "tur": "cikmis", "onem_id": "e07-01", "sinav": "2020-2021 Kurul 1", "kontrol": {"durum": "tamam"}, …}
]}
```
Sıra serbest (birleştirici ders akışına göre dizer).

## Bitiş
`python3 /home/indu/medsor/meds/scripts/spot_cozucu/cozucu_dogrula.py cozucu/<kod>.json` → **0 HATA** (ve 1. adım değiştiyse
`onem_dogrula.py onem/<kod>.json` → 0 HATA). UYARI'ları tek tek kontrol et (PDF'te olmayan sayı = büyük olasılıkla hata). Kısaltma okunuşu
denetimi: `python3 /home/indu/medsor/meds/scripts/patoloji_cozucu/okunus_denet.py cozucu/<kod>.json` (Türkçe açılımla okunanlar burada da
görünür; onlar doğru). JSON'u Python ile yaz (`ensure_ascii=False`, `indent=1`). Yerel GPU/LLM yok. Yalnız kendi derslerinin dosyalarını
yaz; geçici dosyalar `/tmp/claude-1000/spot_<kod>/`.
