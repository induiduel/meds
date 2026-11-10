# Ek modül içerik yazım talimatı (yazar ajan)

Ek modüller, kurul müfredatı dışındaki geçici/seçmeli dersler içindir (`/dersler/ek-moduller`). Kazanım listesi yoktur;
içerik **basit, zevkli, kolay ezberlenir** olur. Ayrıntıya boğulmaz: her konu 4–5 kısa bölüm.

Öğrenci içeriği üç yoldan kullanır: **sesli ders** (EMA sesi `ses` cümlelerini okur, ekranda `ekran` notu durur),
**spot anlatıcı** (kısa tek cümlelik bilgiler), **sorular** (soru okunur, çözüm sesli anlatılır). Aynı içerik PDF'e de basılır.

## Hocanın çalışma soruları varsa: ESAS KAYNAK odur
Modülün çalışma klasöründe (`/home/indu/medsor/meds_temp/ek_modul/<modul>/hoca_calisma_sorulari.txt`) dersin hocasına ait
çalışma soruları (boşluk doldurma, doğru–yanlış, çoktan seçmeli; cevaplı) varsa:
- Konuna düşen **her hoca sorusunun bilgisi** anlatımda (ekran ya da ses) açıkça geçer. Hiçbiri atlanmaz. Önce hoca
  metnini baştan sona oku, konuna ait soruları işaretle, anlatımı onların üstüne kur; kalan yeri beceri bilgisiyle doldur.
- Hocanın ifadesi ve sayısı esastır. Bilgi çerçevesi ya da genel bilgi hocayla çelişirse **hocanınki** yazılır.
  Hocanın kendi içinde çeliştiği yerlerde görev metnindeki karar uygulanır ve ekranda kısa bir not düşülür
  ("Çalışma sorularında 90° de geçiyor; ikisini de bil").
- Hocanın sorduğu sözcükler anlatımda aynen geçer (tabanlık, dikiş mühürleyici, klinometre…): öğrenci boşluğu o sözcükle dolduracak.
- **Sorular hocanın üslubunda** yazılır: kısa, doğrudan kök; "Aşağıdakilerden hangisi … en …?", "… değildir?", "… neden …?",
  "… hangi amaçla kullanılır?", yanlış uygulama kombinasyonları ("Pamuklu içlik + ıslak çorap + …"). Uzun vaka kökü en çok 2.
  Hocanın sorusu KOPYALANMAZ; aynı bilgi başka biçimde sorulur: boşluk doldurma → çoktan seçmeli, doğru–yanlış → "hangisi
  doğrudur/yanlıştır", ters yön (cevabı köke, kökü seçeneğe taşı), aynı kalıpta komşu bilgi. Her konuda 8 sorunun **en az 6'sı**
  doğrudan hoca sorularındaki bilgilerden kurulur. Yanlış seçenekler hocanın kendi yanlış seçenekleri ve doğru–yanlış
  sorularındaki "Yanlış" ifadeler gibi kurulur.
- `dogru_yanlis` etkinliğinde hocanın ifadeleri yeniden yazılarak (anlamı korunarak) kullanılabilir.

## Altın kural: ekran metni ≠ okuma metni
- `ekran`: göze hitap eden **not**. Rakamlar rakamla (3 L, %20, 35 °C), kısa maddeler, kalın anahtar sözcükler.
- `ses`: kulağa hitap eden **anlatım**. Doğal konuşma cümleleri; ekranı aynen okumaz, aynı bilgiyi anlatır.
  - Sayılar ve birimler YAZIYLA: "otuz beş derece", "yüzde yirmi", "üç litre", "altmış metre", "yüz on iki".
  - Rakam, %, °, /, parantez, tırnak, madde imi, `**`, kısaltma (vb., dk, km, L) YOK. Yabancı sözcük Türkçe okunuşuyla
    ("polaris", "kriptosporidyum", "ciardiya").
  - Her cümle en çok 22 kelime. "Şimdi", "Evet arkadaşlar", "bu bölümde göreceğiz" gibi dolgu yok; doğrudan bilgi.
  - Sıcak, sade, biraz esprili bir doğa eğitmeni dili; öğrenciye "sen" diye hitap.

## Üslup yasakları (kapı HATA verir)
- Çeviri mecaz: "imzası", "motoru", "freni", "çapası", "altın standart". İç etiket: "Akılda tut:", "Kısa formül:", "Ayrım cümlesi:".
- "PDF", "slayt", "şık", "A şıkkı", "çeldirici", "hoca", "sınavda çıkar" sözcükleri.
- Şık açıklamasında geçiştirme: "bu sorunun cevabı değil", "yanlıştır." tek başına, "… olarak geçmez".
- Uydurma sayı. Verilen bilgi çerçevesindeki sayıları kullan; çerçevede olmayan kesin sayı yazma.
- Tehlikeli ya da yanlış tavsiye. Emin olmadığın bilgiyi yazma.

## Dosya şeması — `src/data/ek_moduller/<modul>/b<N>.json`
```json
{
  "no": 1, "baslik": "Hazırlık ve Planlama", "ozet": "tek cümle",
  "konular": [
    {
      "id": "1a", "baslik": "…", "ozet": "tek cümle (≤18 kelime)",
      "gorsel": "1a.svg", "gorsel_alt": "görselde ne var (tek cümle)",
      "ek_gorseller": [ { "dosya": "ikinci.svg", "alt": "…" } ],
      "bolumler": [
        { "baslik": "…",
          "ekran": "Bir giriş cümlesi.\n\n- **Anahtar:** kısa açıklama\n- **Anahtar:** kısa açıklama\n\n> [!IMPORTANT] Tek cümlelik en kritik bilgi.",
          "ses": ["cümle 1", "cümle 2", "…"] }
      ],
      "akilda": { "kod": "D-U-R", "acilim": "Dur · Uzaklara bak · Rota planla", "not": "tek cümle ne işe yarar" },
      "yap": ["Yapılması gereken kısa madde", "…"], "yapma": ["Yapılmaması gereken kısa madde", "…"],
      "spotlar": [ { "metin": "**Kalın anahtar** ile tek cümle ekran spotu.", "ses": "aynı bilginin konuşma hâli" } ],
      "etkinlikler": [
        { "tur": "dogru_yanlis", "baslik": "Efsane mi, gerçek mi?", "ifadeler": [ { "metin": "…", "dogru": false, "aciklama": "tek cümle" } ] },
        { "tur": "sirala", "baslik": "…", "soru": "Doğru sıraya diz", "adimlar": ["1. adım", "2. adım", "…"], "aciklama": "tek cümle" },
        { "tur": "esle", "baslik": "…", "ciftler": [ { "sol": "…", "sag": "…" } ] }
      ],
      "sorular": [
        { "no": 1, "zorluk": "kolay", "kok": "…?", "secenekler": { "A": "…", "B": "…", "C": "…", "D": "…", "E": "…" }, "dogru": "C",
          "cozum": "Ekranda görünen 1–2 cümlelik çözüm.",
          "siklar": { "A": "…", "B": "…", "C": "…", "D": "…", "E": "…" },
          "ses_cozum": "Sesli çözüm: 2–3 konuşma cümlesi; doğru cevabın gerekçesi ve en güçlü yanlışın neden yanlış olduğu." }
      ]
    }
  ]
}
```

## Sayısal sınırlar (doğrulayıcı denetler)
- Konu başına **4–6 bölüm** (`ek_gorseller` isteğe bağlı; yalnız görevde adı verilen dosyalar). `ekran`: 1 giriş cümlesi + **3–5 madde** (`- **X:** …`, madde ≤ 16 kelime) + isteğe bağlı tek
  `> [!IMPORTANT]` ya da `> [!NOTE]` satırı; toplam 35–90 kelime. `ses`: **5–8 cümle, 60–120 kelime**.
- Bölümler birbirini tekrar etmez; her bölüm yeni bilgi verir.
- `akilda`: gerçekten işe yarayan tek bir akılda tutma kodu/tekerleme (zorlama ise bilgi çerçevesindekini kullan).
- `yap` 3–5, `yapma` 3–5 madde (madde ≤ 12 kelime).
- `spotlar`: **7 adet**. `metin` ≤ 22 kelime, en az bir `**kalın**`; `ses` tek cümle ≤ 24 kelime, kurallara uygun.
- `etkinlikler`: **2 adet, farklı türde**. dogru_yanlis 4–5 ifade (en az biri doğru, en az ikisi yanlış); sirala 4–6 adım
  (doğru sırayla yazılır, ekranda karıştırılır); esle 4–5 çift (sol ve sağ ≤ 6 kelime, sağlar birbirinden açıkça farklı).
- `sorular`: **8 adet** — 3 kolay, 3 orta, 2 zor; 5 seçenek.
  - Yalnız **bu konunun ve aynı başlıktaki önceki konunun** anlatımında (ekran ya da ses) geçen bilgi sorulur.
  - Hoca soruları varsa üslup yukarıdaki "ESAS KAYNAK" bölümüne göre; "Orta/zor sorular kısa bir durum verir" maddesi yerine
    hocanın zor soru kalıpları ("en çok artıran", "en az tipik", "tek başına yeterli değildir", kombinasyon) kullanılır.
  - Doğru cevabın gerekçesi anlatımda açıkça bulunur. Tek doğru cevap tartışmasızdır. "Hepsi/hiçbiri" seçeneği yok.
  - Yanlış seçenekler anlatımda geçen komşu kavramlardan ya da yaygın yanlış inanışlardan kurulur, inandırıcıdır.
  - Doğru seçenek en uzun seçenek olmaz. 8 soruda doğru harfler dağıtılır (her harf en az 1, en çok 2 kez).
  - Orta/zor sorular kısa bir durum verir ("Yürüyüşün üçüncü saatinde…") ve karar ister; ezber sorusu en çok 3.
  - `kok` ≤ 45 kelime, seçenek ≤ 14 kelime. Rakam ekranda rakamla yazılır.
  - `siklar`: her seçenek için **1–2 cümle, 14–40 kelime**: seçenekteki şeyin ne olduğu/ne işe yaradığı ve bu durumda neden
    uygun ya da uygun olmadığı. Tek başına anlaşılır. Harf anma yok.
  - `cozum` 12–40 kelime. `ses_cozum` 2–3 cümle, 25–60 kelime, ses kurallarına uygun (rakam yok, harf anma yok).

## Bitirme
1. Dosyayı yaz. 2. `python3 scripts/ek_modul/dogrula.py <dosya>` çalıştır (çalışma dizini `meds/`). 3. HATA satırlarını düzelt,
0 HATA olana dek yinele. UYARI'ları da gözden geçir. 4. Son mesajında yalnız: dosya yolu, soru sayısı, doğrulayıcı sonucu ve
emin olamadığın/bilgi çerçevesinden saptığın yerler (varsa).

## "PDF ile" kipi (sesli ders kitapçıkla birlikte ilerler)
Ses (`ses.py`) ve ders kitapçığı (`pdf.py`) üretildikten SONRA: `.venv-ocr/bin/python scripts/ek_modul/pdf_esle.py --modul <modül>`
→ `pdf_esle.json` (klip başına sayfa, bölüm kutusu, satır kutuları, cümle zamanı, cümle → not maddesi). İkisinden biri yeniden
üretilirse betik yeniden çalıştırılır; `dogrula.py --modul` eskimiş eşlemede HATA verir. Eşlemenin tutması için `ses` cümleleri
ekran notundaki maddelerin sözcüklerini kullanmalıdır (zaten kural: hocanın sözcükleri anlatımda aynen geçer).

## Hoca soruları · "PDF ile" sesli çözüm (2026-11-10)
Hoca sesleri (`h-`/`hc-`) ve çözümlü kitapçık (`npx tsx scripts/ek_modul/foy_pdf.mts <modül> --cozumlu`) üretildikten SONRA:
`.venv-ocr/bin/python scripts/ek_modul/pdf_esle_hoca.py --modul <modül>` → `hoca_pdf_esle.json` (klip başına sayfa, soru bloğu,
cümle başına satırlar, cümle zamanı). Ekran: hoca soruları sayfasında "PDF ile" kipi (`EkPdfHoca.tsx`) + sesli ders düzeninde
oynatıcı (`EkSesliOynatici.tsx`: soru parçalı çubuk, atlama, hız). Kitapçık ya da ses değişirse betik yeniden çalıştırılır;
`dogrula.py --modul` eskimiş eşlemede HATA verir. Betik soru bloğunu sol kenardaki "N." satırından ve çözüm kutusunun zemin
renginden (#EEF3EE; hata notlu #FBEFE3) bulur: `cozumluBelge` biçimi değişirse betik de güncellenir.
