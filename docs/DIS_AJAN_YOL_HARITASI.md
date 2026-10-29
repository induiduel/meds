# Dış yapay zekâ ajanları için tam içerik işçisi yol haritası (kullanıcı kararı 2026-10-29)

> **Ajana verilecek asıl görev yönergesi:** `scripts/tam_hat/dis_ajan/TALIMAT_DIS_AJAN.md` (başlangıç komutları, kanıt→üretim→kapı döngüsü, evre kartları, hata mesajı tablosu, belirsizlik tablosu, rapor şablonu). Bu belge gerekçe ve mimaridir; ajan talimatı ile birlikte okunur.

> Bu belge **Claude dışındaki** her ajan (Gemini, GPT, DeepSeek, Qwen, Antigravity, OpenCode modelleri…) içindir.
> Amaç: aynı PDF'ten ders üretirken Claude'un izlediği yolu hatasız izlemek. **Önce bu belgeyi baştan sona oku, sonra
> `AGENTS.md`, `docs/KURUL_OTOMASYON_EL_KITABI.md` §19–20, `docs/TAM_HAT_HIZLI_AKIS.md`,
> `docs/KURUL2_YAPILMAYACAK_HATALAR.md`'yi aşama listeleriyle (§3) oku.** Kullanıcı talimatı vermeden başlama (AGENTS kural 20/22).

## 0. Değişmez dört kural

1. **Etiketli, ayrı veri.** Çıktın `<ders>-ag-<etiket>` anahtarıyla yaşar (örn. Gemini → `k2-07-ag-gemini`). Etiketin
   kendi adındır: a-z0-9, 2–12 harf, `claude` olamaz. Claude'un `k2-07` dersine, ya da başka ajanın `-ag-` anahtarına
   **bir bayt bile yazmazsın**.
2. **Üstüne yazma yok, sürüm artırma yok.** `v2`, `v3`, `-2`, `-yeni` YOK. Anahtar zaten varsa sunucu 409 verir; yeniden
   denemek istiyorsan kullanıcıdan yeni etiket iste (örn. `gemini2`). Hata düzeltmesi aynı anahtarın **çalışma
   klasöründe** yapılır, yayına geçmeden önce.
3. **Yönetici onayına kadar öğrenciye kapalı.** `ders-ekle` `ajan` alanıyla çağrılınca sunucu `sesli:`, `deste:`, `paket:`
   anahtarlarını kendiliğinden `yalniz-yonetici` yapar. Sen bu durumu **açamazsın**; panel › Site › Görünürlük'ten yalnız
   yönetici `acik` yapar. Kendi içeriğini "tamamlandı, yayında" diye sunma: "yönetici onayı bekliyor" de.
4. **Kapı geçmeden yayın yok.** Bütün betik kapıları 0 HATA + §9 bağımsız denetim GEÇER olmadan `ders-ekle` çağrılmaz.
   Kapıyı gevşetmek, atlamak, eşik oynamak, çapa/kayıt uydurmak YASAK (H59, H123).

## 1. Kendini tanıt, klasörünü kur

```bash
E=gemini            # kendi etiketin
D=k2-07             # ders kimliği (kayıt defterinden: src/data/dersler/kN.json)
W=/home/indu/medsor/meds_temp/dis_ajan/$E/$D
mkdir -p $W
echo '{"ajan":"'$E'","model":"<tam model adı>","tarih":"'$(date -I)'","surum":"1"}' > $W/ajan.json
```

- **Yazabileceğin yerler:** `$W/` (her ara dosya) ve yayın aşamasında yalnız adında `$D-ag-$E` geçen dosyalar.
- **Yazamayacakların:** `src/data/**` içindeki mevcut dosyalar, `interactive_learning_decks.json`, `site_ayar.json`,
  `hat.json`, `guncelleme_notu.json` (onem'i yalnız Claude/kullanıcı artırır), `data/**` mevcut dosyalar, `*.md` belgeler,
  `AGENTS.md`. Aşağıdaki ders-dışı ortak dosyaya ihtiyaç duyarsan **dur ve kullanıcıya yaz**.
- Çalışma bitince `python3 scripts/tam_hat/dis_ajan_kapisi.py --ajan $E --ders $D` — izinsiz dosya değişimi, eksik
  `ajan.json`, var olan anahtar varsa HATA verir.

## 2. İş akışı (Claude ile aynı evreler; sıra TAM_HAT_HIZLI_AKIS.md)

| Evre | Ne yapılır | Çıktı (`$W/` altında) | Kapı |
|---|---|---|---|
| E0 | `scripts/tam_hat/hazirlik.py <klasör> --ders $D` (PDF metni, sayfa görüntüleri, öğrenci notu, hoca dökümü) | `sayfalar.json`, `op/s-NNN.png` | dosyalar var |
| E1 | değerlendirme paketi, `soru_uslup_ornek.py` | `paket.json`, `soru_uslubu.json` | `scripts/ogrenci_drive/degerlendirme_dogrula.py` |
| E2 | anlatım planı → anlatım; Öğren destesi; örnek sorular; çözücü; envanter | `anlatim_plani.md`, `metin.md`, … | `metin_denetle.py`, `turkce_uslup`, `validate_learning_decks.py --oyun-zorunlu --kurul2`, `soru_uslup.py`, `kaynak_kapisi.py`, `cozucu_dogrula.py` |
| E3 | ses + zaman + çıkmış chip + terim/kısaltma + ders içerik paketi | — | `ders_icerik_dogrula.py` |
| E4 | çapa → çizim | `capa.json`, `cizim.json` | `capa_dogrula.py`, `cizim_kapisi.py` 0 HATA |
| E5 | `pdf_tarama.py`, tek bağımsız denetim | `denetim.json` | GEÇER |
| E6 | `ders-ekle` (`ajan` alanlı) → canlı doğrulama | — | `dis_ajan_kapisi.py --yayin --canli …` |

Her evrede yalnız o evrenin kural listesini oku: `python3 scripts/tam_hat/kural_secici.py --oku <aşama>`.
Tüm defteri bellekte tutmaya çalışma; unutursan kapı seni yakalar, ama hata yazıldıktan sonra düzeltmek pahalıdır.

## 3. Prompt'u nasıl algılarsın (hata azaltma kuralları)

- **Önce görevi tek cümleyle yaz** ("k2-07 PDF'inden, `-ag-gemini` etiketli, 15 sayfa anlatım yazıyorum"). Kullanıcının ya da
  bu belgenin söylemediği hiçbir şeyi yapma; söylenmeyen şey = yapma. Emin değilsen **soru sor**, tahmin etme.
- **Sayısal hedefler** (kelime, öge, soru sayısı): hedefi önce yaz, bitince say, sapmayı raporla. ±%10 tolerans (anlatımda ±%20)
  yalnız sayıda geçerlidir; tıbbi yanlış, kaynak dışı bilgi, ileri sızıntı, üslup ihlalinde tolerans yoktur.
- **Kaynak sadakati:** her cümlenin bir PDF sayfası (`s`) vardır. Sayfada olmayan bilgiyi genel tıp bilgisinden yazma;
  kaynak yoksa "kaynakta yok" diye işaretle ve atla. Sayfa numarası uydurmak, `gorsel: true` bayrağını gerekçesiz koymak yasak.
- **İleri sızıntı yok:** bir etkileşim/soru yalnız o slayta ve öncesine kadar anlatılanı kullanır (AGENTS 7). İpucu cevabın
  kelimesini/kökünü içermez.
- **Türkçe:** doğal, eksiksiz; çeviri mecaz ("imzası", "motoru", "freni") ve iç etiket ("Kısa formül:", "Akılda tut:") yok.
  Dolgu yok: "hoca vurguladı" yalnız hoca dökümünde zaman damgalı alıntı varsa.
- **Küçük parti çalış:** bölüm bölüm yaz, her bölümden sonra kapıyı çalıştır. 30 sayfalık metni tek seferde üretme.
- **Kapı hatası = yalnız o parçayı düzelt.** Hata mesajındaki kimlik/bölümü yeniden yaz, kalan kısma dokunma; sonra kapıyı
  yeniden çalıştır. Aynı hatayı üçüncü kez alırsan dur, kullanıcıya hatayı ve denediklerini yaz.
- **Eski çıktılara güvenme:** bağlamın dolunca önceki karar ve sayıları hatırlamaya çalışma; dosyadan yeniden oku.
- **Kendi çıktını kendin onaylama:** "GEÇER" kararını yazar ajan veremez; denetçi ayrı bir oturum/alt ajandır (§9).

## 4. Görselleri (PDF sayfaları, şekiller, tablolar) doğru algılama

Çoğu hata, sayfa görüntüsünü yüzeysel okumaktan çıkar. Sırayla:

1. **Önce metin katmanı:** `sayfalar.json` o sayfanın yazısını verir. Görüntü bu metni **doğrulamak/tamamlamak** içindir;
   metinde olmayan şekil içeriği (ok yönü, etiket, tablo satırı) için görüntüyü oku.
2. **Görüntüyü parçala:** sayfa görüntüsünü üst/orta/alt ya da sol/sağ olarak kırp ve her kırpığı ayrı oku
   (`op/s-NNN.png` yüksek çözünürlüktür). Tek bakışta "genel olarak şunu gösteriyor" yetmez.
3. **Okuduğunu yaz, sonra yorumla:** şekildeki her etiketi, ok başlangıç→bitiş, renk ve numarayı bir listeye yaz
   (`$W/sekil_s-NNN.json`: `{"nesne","konum","etiket","iliski"}`). Yorum (hastalık, mekanizma) bu listeden çıkar.
4. **Emin olamadığını söyle:** okunamayan etiketi tahmin etme; `"belirsiz": true` yaz, anlatımda o ayrıntıyı kullanma.
5. **Çift okuma:** şekilden çıkan her kayıt `gorsel: true` taşır; bağımsız denetçi aynı kırpığı yeniden okur.
   İki okuma uyuşmuyorsa kayıt atılır.
6. **Öğrenci notu / işaretli sayfa:** işaret (daire, altçizgi, fosforlu) PDF'in özgün metnine göre ayırt edilir; öğrencinin el
   yazısı özgün içerikle karıştırılmaz ve **yalnız kullanıcı isterse** kullanılır (öğrenci notu katmanı).

## 5. Çizim ve lazer (en hataya açık aşama — dikkatle)

Önce `docs/CIZIM_KURALLARI.md` ve `scripts/cizim/TALIMAT_CIZIM.md` (madde 21–30) oku. Özet:

- **Şekil anlatan cümlede** lazer görselin üstüne gider ve **anlatılan parçayı** (lezyon, yapı, bölge, tablo satırı) kontur
  ya da okla gösterir. Bütün resmi çevreleme, resim içine panel kurma, yalnız metin satırını boyama yapma.
- **Koordinat yöntemi:** `op/s-NNN.png` üstünde parçanın kutusunu piksel olarak bul, sayfa genişlik/yüksekliğine böl,
  0–1 oranı yaz. Bulduğun kutuyu **kırpıp yeniden bak**: kırpıkta anlatılan şey duruyor mu? Durmuyorsa koordinat yanlıştır.
- **Tek cümle = tek çizim.** Çizim yalnız o an konuşulan cümleye aittir; önceki cümlenin çizimini yayma, sonrakini erken
  gösterme, iki konumu aynı anda işaretleme (AGENTS 18).
- **Çapa uydurma yok:** her cümleye madde/M0/`resim: 0` basarak kapıyı geçmek yasaktır (AGENTS 17).
- Bitince `python3 scripts/cizim/cizim_kapisi.py <anahtar> --kok <veri kökü>` 0 HATA; ardından `panel_sinama.mjs`.
  Kapı HATA verirse çizimi **gerçekten** düzelt; kapıyı yumuşatma.
- Çizimi yapamayacağını düşünüyorsan (görsel okuyamıyorsun, koordinat bulamıyorsun) çizim katmanını **boş bırak ve raporla**.
  Yanlış çizim, çizimsizden kötüdür.

## 6. Yazım standartları (kısa; ayrıntı ilgili belgelerde)

- **Anlatım:** `# Başlık` + `@@ Bölüm` + paragraf; önce `anlatim_plani.md`. Öğreten, hoca örnekleri korunmuş, ilk geçişte zor
  terim açıklanmış (ANLATIM_KURGU_STANDARDI.md).
- **Öğren destesi:** slayt başına 4–6 etkileşim, 60–250 kelime, madde imli anlatım, sıfır tekrar, son slayt oyun sayfası;
  deste **yalnız** `$W/deste.json`'a yazılır — `interactive_learning_decks.json`'a elle EKLEME (kullanıcı/Claude birleştirir).
- **Örnek sorular:** önem listesinin tamamı + ayrıntı %40, 50<n≤100; yalnız ders notundaki bilgi; her şık için 2–3 cümle
  (ne/ne işe yarar/neden doğru-yanlış); "cevabı değil" geçiştirmesi yasak (SIK_ACIKLAMA_STANDARDI.md, SORU_USLUBU.md).
- **Çözücü, terim, kısaltma, ders içerik paketi:** her kaydın sayfası (`s`) ve slayt numarası (`adim`) vardır.

## 7. Veri çakışmasını önleme (teknik)

- Anahtar ad uzayı: tüm yeni dosyalar `<ders>-ag-<etiket>` taşır (`metin/`, `hizalama/`, `capa/`, `cizim/`, `ses/`, `ders_icerik/`,
  `ornek_sorular/`, `cozucu/`). Ortak (çok dersli) dosyaya satır eklemen gerekiyorsa **ekleme**; ajan çıktısını
  `$W/ortak_degisiklik.json`'da öner, birleştirmeyi Claude/kullanıcı yapar.
- Sunucu tarafı koruma (`/api/sesli-anlatim/ders-ekle`): `ajan` alanı zorunludur, anahtar biçimi `k<N>-<no>-ag-<etiket>`
  olmalı, aynı anahtar varsa 409, `claude` etiketi 400; ders `yalniz-yonetici` doğar. Claude'un `k2-07`'si için `ajan` alanıyla
  çağrı **zaten reddedilir** (anahtar uyuşmaz).
- **Ön yüz paketine giren içerik onaydan ÖNCE `src/data`'ya girmez (sızıntı kuralı):** önem listesi, sınav asistanı, sesli çözücü
  (`src/data/*_cozucu`, `*_onem`) ve ders içerik paketi (`src/data/ders_icerik`) Vite paketine gömülür; görünürlük süzmesi bunlarda
  yalnız tarayıcıdadır, sunucu kapısı yoktur. Bu yüzden ajan bu katmanları `$W/` altında bırakır; yönetici dersi onaylayınca Claude
  `-ag-` adıyla `src/data`'ya taşır. Aksi halde öğrenci içeriği paketten okuyabilir.
- `site_ayar.json` ortak dosyadır: ajan bunlara yazmaz. Görünürlük anahtarları sunucu
  tarafından eklenir.
- Oracle'a doğrudan dosya kopyalama (`rsync`, `scp`) yok; yalnız `ders-ekle` ve kapının izin verdiği uçlar.
- GPU yalnız AGENTS kural 10'daki istisna yoluyla (`meds-gpuguard` etkin); yerel LLM yok; `MEDS_LLM_ELLE=1` kilidini
  kullanıcı komutu olmadan açma.

## 8. Yayın adımları (kullanıcı komutuyla)

1. Tüm kapılar 0 HATA, `denetim.json` GEÇER.
2. `python3 scripts/tam_hat/dis_ajan_kapisi.py --ajan $E --ders $D` → GEÇTİ.
3. `ders-ekle` isteği: `{ "key": "$D-ag-$E", "ajan": "$E", "no": …, "baslik": "<Ders başlığı> [<Ajan> taslağı]", "metin": …, "sayfalar": …, "dosya": … }`.
   Başlığa ajan etiketi ve "taslak" yaz; yönetici panelde ayırt etsin.
4. `python3 scripts/tam_hat/dis_ajan_kapisi.py --ajan $E --ders $D --yayin --canli <adres>` → canlıda `yalniz-yonetici` ve
   öğrenci isteğinde 403.
5. Kullanıcıya rapor: üretilen katmanlar, atlananlar ve **nedenleri**, kapı çıktıları, açık sorular. "Yönetici onayı bekliyor."

## 9. Bağımsız denetim (son çare; asıl güvence §12'dir)

> Kullanıcı kararı 2026-10-29: kalite ikinci ajanla sonradan yakalanarak değil, ilk ajanın **hatasız yazmasıyla** sağlanır. §12 uygulanmışsa denetçi zorunlu değildir; kullanıcı isterse yapılır.

Yazan oturum denetçi olamaz. Ayrı bir oturum/alt ajan, **öğrenci rolünde** ders boyunca okuyup aşağıyı sırayla denetler:
tıbbi doğruluk ve kaynak sadakati → anlaşılırlık (ilk geçişte tanımsız terim) → soru kalitesi (çeldirici gücü, çıkmış üslubu)
→ Türkçe/dolgu → çizim doğruluğu (gerçek sayfa görüntüsünde). Çıktı `denetim.json`:
`{"karar":"GEÇER|KALIR","bulgular":[{"katman","kimlik","sorun","oneri"}]}`. KALIR ise yalnız bulgulardaki kimlikler düzelir.

## 10. Yönetici onayı (kullanıcı için)

- İçerik panelde (**İçerik › Sesli dersler**, **Site › Görünürlük**) `k2-07-ag-gemini` olarak görünür, rozet `yalniz-yonetici`.
- Onay = o üç anahtarı (`sesli:`, `deste:`, `paket:`) `acik` yapmak. Reddetme = anahtarı `gizli` bırakmak ya da silmek.
- İki sürüm (Claude + ajan) birlikte açıksa öğrenci iki ayrı ders görür; kullanıcı hangisinin açılacağına karar verir.

## 11. Dur ve sor listesi

Şu durumlarda **işi durdur, kullanıcıya yaz**: PDF-ders eşlemesi belirsiz; kapı üç kez aynı hatayı veriyor; ortak dosyaya
yazmak gerekiyor; sunucu 409/400 veriyor; görüntüyü okuyamıyorsun; kaynak dışı bilgi eklemek zorunda kalıyorsun; kapı
eşiğini değiştirmek geliyor aklına; izin alınmamış bir LLM/API çağrısı gerekiyor.

## 12. Önleyici yazım protokolü — hata sonradan yakalanmaz, baştan üretilemez kılınır

Zayıf bir modelin hata yapma biçimleri bellidir: kaynakta olmayanı yazmak, olumsuzlamayı/sayıyı/ok yönünü çevirmek, kuralı
unutmak, kapıyı en sonda çalıştırıp çok parçayı birden bozmak, görseli tahminle okumak. Her biri için mekanik bir önlem:

1. **Kanıt önce, metin sonra.** Bir bölüm yazmadan önce `$W/kanit_<bolum>.json` kurulur: her bilgi satırı
   `{"bilgi","s","alinti","gorsel"}`; `alinti` `sayfalar.json` o sayfasından (±1) **birebir kopyalanmış** bir parçadır
   (şekilden okunduysa `sekil_s-NNN.json` kaydından). Betik alıntının sayfada gerçekten geçtiğini denetler; geçmiyorsa satır
   geçersizdir. Anlatım/soru/terim **yalnız bu kanıt satırlarından** kurulur; kanıtı olmayan cümle yazılmaz.
2. **Taşınan kelimeler aynen kalır.** Alıntıdaki olumsuzluk ("değil", "-sız/-siz", "yok", "azalır/artar"), sayı, birim, yüzde, ok
   yönü, tür/gen/ilaç adı yazılan cümlede **aynı** olur. Betik, alıntıdaki bu simgelerin cümlede de bulunduğunu denetler
   (yeni kapı: `kanit_tutarlilik`); uyuşmayan cümle bölüm bitmeden işaretlenir.
3. **Mikro görev + anında kapı.** Bir seferde en çok bir bölüm (≈3–5 sayfa). Bölüm biter bitmez kapılar çalışır; HATA varsa o
   bölüm düzelmeden **sonrakine geçilmez**. Hata birikip toplu düzeltme yok; düzeltme tek bölümle sınırlı kalır.
4. **Yazarken tarama, sonda değil.** Yasak desen taraması (çeviri mecaz, iç etiket, dolgu, "hoca vurguladı" dayanaksız, ipucu
   sızıntısı) her paragraf yazıldığında çalışır (`turkce_uslup`, `metin_denetle`); ajan sonuca bakmadan devam etmez.
5. **İşe başlamadan anlama sınavı.** Ajan, `KURUL2_YAPILMAYACAK_HATALAR.md`'den üretilen çoktan seçmeli 15–20 soruyu
   (ör. "bu cümlede hangi ihlal var?") yanıtlar; betik puanlar, **%100 değilse iş başlamaz**. Yanlış cevaplanan kural ajanın
   önüne yeniden konur.
6. **İyi–kötü örnek çifti.** Her aşama kartı (kural_secici çıktısı) bir gerçek hata ve düzeltilmiş hâli (H maddesi) taşır; ajan
   yazmadan önce o aşamanın çiftini okur. Soyut kural değil, somut örnek.
7. **Görsel: iki yoldan okuma, uyuşmazsa kullanma.** Şekil etiketleri hem metin katmanından (pdftotext/OCR) hem görüntüden
   çıkarılır; iki liste betikle karşılaştırılır. Yalnız ikisinde de geçen etiket/ilişki kullanılır, kalan `belirsiz` sayılır ve
   anlatılmaz. Çizim koordinatı kırpık görüntü + etiket metniyle doğrulanır; doğrulanamayan çizim yapılmaz.
8. **Soru: cevap kanıtsız olmaz.** Her soru `dogruKanit` (alıntı + sayfa) ve her çeldirici için yanlış olma gerekçesinin alıntısını
   taşır; kanıt betikle doğrulanır. "En uzun şık doğru" gibi kalıp ipuçları `soru_uslup.py` ile yazarken denetlenir.
9. **Yetenek eşiği.** Ajan başta kendi görsel okuma yeteneğini 3 sayfalık sınama okumasıyla (bilinen cevaplı) gösterir; geçemezse
   çizim/şekil katmanları üretilmez ve rapora yazılır — yanlış çizim, çizimsizden kötüdür.
10. **Kayan hedef yok.** Sayısal hedefler (kelime, öge, soru) iş başında bir kez `hedef.json`'a yazılır; kapılar bunu okur. Ajan
    hedefi sonradan değiştiremez.

Kalan risk (dürüst not): kaynağın kendisi yanlışsa ya da ajan bir alıntıyı **doğru alıntılayıp yanlış yorumlarsa** (kanıt
yerinde ama sonuç yanlış) betik bunu görmez. 2. madde olumsuzluk/sayı/yön çevirmelerini kapatır; yorum hatası için son örneklem
kontrolü kullanıcı kararıdır (§9, isteğe bağlı).

### 12.1 Araçlar (yazıldı ve sınandı, 2026-10-29)
`scripts/tam_hat/dis_ajan/`: `kanit_dogrula.py` (alıntı sayfada birebir mi), `kanit_tutarlilik.py` (sayı/olumsuzluk/yön/konu örtüşmesi + üslup/dolgu),
`bolum_kontrol.py` (ikisini tek komutla), `anlama_sinavi.py` + `sinav_bankasi.json` (22 soru, %100 şart, yanlışta kural gösterilir),
`hedef.py` (imzalı sayısal hedef, ±%10/±%20 tolerans), `dis_ajan_kapisi.py` (izin kümesi, iş başı anlık görüntü, sınav ve hedef denetimi).
Her hata mesajı kod taşır ve "Yapılacak:" ile çözümü söyler; ajan talimatındaki tablo bu kodlara bakar.

**Bilinen sınır:** kapı kanıt–cümle *uyumunu* ve kaynağa bağlılığı denetler; alıntıyı doğru kopyalayıp yanlış yorumlamayı (kanıt yerinde, sonuç yanlış) görmez.
Anlama sınavı şıklarında yalnız doğru cevap özeti saklanır (açık cevap anahtarı yok) ama kararlı bir ajan kaba kuvvetle geçebilir; sınav dürüst ajanı kurala yönlendirmek içindir.

## 13. Kapı kataloğu (2026-10-29 sonu) ve bilinen sınırlar
**Kapılar:** anlatım — KANIT-00..09, URETIM-01..15, TANIM-01..09, NITELE-01, NEDEN-01/02, KAPSAM/SEKIL, METİN; içerik — BAG-01..05, SORU-01/02/04..09, PROFIL-00..02, SIK, IPUCU, DESTE-01; çizim — CIZIM-01..13 (+ `karar.json`); izolasyon — `dis_ajan_kapisi.py` (anlık görüntü, izinli dosya kümesi, anlama sınavı imzası talimat sürümüne bağlı, hedef kilidi, metin bütünlüğü, canlı kilit). Patoloji dersleri ek olarak `patoloji_soru_isci` + `profil_kapisi` (talimat E4a-PAT; `patoloji_donustur.py` köprüsü).
**Ölçülen kalite (k2-29, aynı görev, tek deneme):** Haiku ilk geçişte kusursuz soru oranı ≈6/10 (4 soruda cevap–kök kaynak bağı yok, 6 kapı turu), Sonnet 10/10 (3 tur). Sonuç: ağır işler (örnek soru, çözücü, çizim) Sonnet/Opus düzeyinde ajanla yürütülür; Haiku yalnız kapının işaretlediği tek soruyu yeniden yazmak için.
**Betikle yakalanamayanlar:** doğru alıntıyla yanlış yorum, tıbbi kesinlik farkı (örn. «dural damar» ↔ orta meningeal arter), hoca üslubuna tam uyum (profil UYARI'ları), görsel çizimin doğru yapıyı çevrelediği (bindirme görüntüsüne bakılır). Bunlar yayın öncesi Claude/kullanıcı son okumasına bağlıdır.
**Yayın öncesi kontrol listesi:** `dis_ajan_kapisi.py --ajan <etiket> --ders <ders> --yayin --canli <adres>` GEÇTİ; kod değişikliği (`sesliAnlatim.ts`, `siteAyar.ts`) dağıtılmadan `ders-ekle` ajan alanı canlıda çalışmaz: commit + `guncelleme_notu.json` onem+1 + `dagit.sh` + `systemctl --user restart meds-web` (yerel sınama için).
