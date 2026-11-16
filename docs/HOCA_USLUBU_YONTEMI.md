# Hoca üslubu, kazanım haritası ve soru-yazım profili (2026-10-29)

> Amaç: tam içerik işçisi bir dersi, hocanın **neden / nasıl / hangi bilgilerle / ne zorlukta / hangi çeldiricilerle** soracağını bilerek anlatsın,
> öne çıkarsın ve örneklesin; örnek sorular hocanın çıkmışlarına benzesin; sınavda çıkabilecek diğer yerler de yakalansın.
> Kullanıcı kararı 2026-10-29. Kural: AGENTS.md madde 26. Hat betikleri: `scripts/hoca_profili/`. Veri: `src/data/hoca_profilleri/`. Okunabilir döküm: `docs/HOCA_USLUBU/<ders>.md`.

## 1. Ne üretildi

| Katman | Dosya | İçerik |
|---|---|---|
| Ders üslup profili | `src/data/hoca_profilleri/<ders>/uslup.json` | kök kalıbı payları, bilgi türü, bilişsel düzey, kök uzunluğu, şık ölçüleri (bileşik, sayısal, doğru-en-uzun, mutlak ifade, hepsi/hiçbiri, doğru şık konumu), çeldirici stratejisi, yıl kayması, tekrar oranı, güven |
| Konu kazanım haritası | `<ders>/kazanim_haritasi.json` | konu başına: **neden sorulur** (bilgi türü + bilişsel/tıbbi gerekçe), **nasıl sorulur**, **hangi bilgilerle** (çeldirici türleri), **zorluk**, **kaynağa bağımlılık**, tekrar eden çekirdek kavramlar (kaç kez, hangi yıllar, hangi kalıpla), tipik kök örnekleri |
| Okunur özet | `docs/HOCA_USLUBU/<ders>.md` | yukarıdakinin insan okuması + o dersin yazım kuralları |
| Genel taban | `_genel/uslup.json` | tüm derslerin ortalaması (veri az dersler için yedek) |
| Sınama | `_sinama.json`, `_model/satir_model.json` | geriye dönük sınama sonuçları, satır önem modeli |

Kapsam: 22 ders, 4.846 tekil çıkmış soru (aynı kök+doğru şık tek kayıt; `kez` = tekrar sayısı) + **2026-27 Kurul 1 sınavının 77 tam sorusu** (en yeni, en değerli veri).
Yeniden üretim: `python3 scripts/hoca_profili/uslup_analiz.py` (yeni çıkmış toplanınca/yeni sınav gelince çalıştır; LLM yok, ~1 dk).

## 2. Algoritmalar (neden birden çok)

Tek bir metin-benzerliği ölçüsü "bu bilgi neden soruldu"yu söyleyemez. Bu yüzden her soru birbirinden bağımsız beş açıdan ölçülür:

1. **Kök kalıbı sınıflayıcı** (kurallı): doğrudan, olumsuz, yanlış-bul, öncüllü, en_tipik, vaka, eşleştirme, tanım, sayı, doğru_ifade — "nasıl sorulur".
2. **Bilgi türü sınıflayıcı** ("neden sorulur"): mekanizma, tanı/ayırıcı, tanımlayıcı bulgu, ilaç yan etki/endikasyon, etiyoloji/risk, sınıflama/ad, epidemiyoloji sayı, önleme, prognoz/komplikasyon, tanım. Her tür için **bilişsel/tıbbi gerekçe** (`NEDEN` sözlüğü) tutulur: mekanizma → neden-sonuç muhakemesi; tanı → doğru tetkik/tanı kararı; yan etki → hasta güvenliği; sayı → pre-test olasılık…
3. **Bilişsel düzey** (Bloom'dan türetilmiş 3 basamak): L1 hatırlama, L2 anlama/ilişki (mekanizma, ayırıcı, öncüllü, yanlış-bul), L3 uygulama/klinik muhakeme (vaka). NBME rehberi uygulama düzeyini önerir; hocanın gerçek dağılımı profilde ölçülür, kendi tercihimiz değil.
4. **Şık/çeldirici ölçümü** (NBME/Haladyna kusur ve tasarım listeleri): uzunluk CV'si, doğru-şık-en-uzun ipucu, bileşik şık ("X + Y"), sayısal yakın değer, mutlak ifade tuzağı, hepsi/hiçbiri, çeldirici-doğru jeton örtüşmesi (= komşu kavram ailesi).
5. **Tekrar kümeleme** (Jaccard ≥ 0,5): yıllar arası aynı kavramın yeniden sorulması → "çekirdek kavram"; kümelerin hangi kalıplarla sorulduğu (aynı bilgi farklı kalıba çevrilir = ters yön/kopya-çevirme).
6. **Dönem kayması**: 2023+ ile öncesi karşılaştırılır (≥8 puan fark işaretlenir). Web taramasının uyarısı: "soru biçimi konu aynı kalsa bile değişebilir; eski sınavlar yanıltabilir".
7. **Kaynak bağımlılığı**: çıkmışın ders özetinde kanıt benzerliği (`ozetKaniti`) — kanıtlı oran düşükse hoca slayt dışı çıkarım ya da ayrı kaynak soruyor demektir.

Satır düzeyi ek model (`satir_model.py`): ders metninin satırlarını biçim + işaret sözcüğü + ders içi tekrar sinyaliyle puanlayıp "soruya müsait yer" adayı çıkarır (`onem_puanla.py`).

Araştırma notları (web, 2026-10-29): NBME *Constructing Written Test Questions* (6. bas.) ve tıp eğitimi madde-yazım rehberleri — çeldirici makul ve benzer içerikte, şıklar dilbilgisel paralel, uygulama düzeyi, "non-functional distractor" zayıf; her çeldirici ~%5–25 seçilmeli. Tahmin yazınında: az örnekten (1–2 sınav) çıkan örüntü gürültüdür ve profesör rotasyonu/müfredat kayması önceki vurguyu eskitir → bu belgedeki **güven düzeyi ve ölçülmüş sınır** zorunlu alanlardır.

## 3. Sınama sonuçları (gerçek, geriye dönük; `_sinama.json`, `satir_model.py --cv/--holdout`)

**A. Üslup profili — 2026-27 Kurul 1'i hiç görmeden tahmin** (JSD, küçük = iyi; ders profili ↔ genel profil):
Enfeksiyon 0,071 ↔ 0,101 · Halk Sağlığı 0,211 ↔ 0,262 · Tıbbi Genetik 0,129 ↔ 0,202 · Patoloji 0,134 ↔ 0,180 · Üroloji 0,067 ↔ 0,115.
**5/5 derste ders profili genel profilden daha iyi tahmin ediyor** → "her dersin kendine özgü üslubu var" varsayımı veriyle doğrulandı. (n_yeni 6–21: küçük; Halk Sağlığı n=6 zayıf kanıt.)

**B. Kavram tekrarı:** 2026-27 sorularının **%17'si** (Genetik %33, Enfeksiyon %26, Halk Sağlığı %17, Üroloji %9, Patoloji %0) eski bir çıkmışla aynı kavram; başka dersin çıkmışlarıyla taban çizgisi %0.
Yorum: çıkmışlar yönü gösterir ama sınavın ~%80'i yeni kavramdır → **çıkmışa eşleşmeyen yerleri üslup + bilgi türü + hocanın seçim kalıbıyla yakalamak şarttır**; yalnız çıkmış eşleştirmek yetmez.

**C. Satır önem modeli** (ders özetlerinde, dosya-bazlı 5 katlı, sızıntısız; kaynak satırın en iyi sıraya girme isabeti, rastgele ilk-%20 = %23,5):
yalnız tekrar sinyali AUC 0,73 / ilk-%20 %48 · biçim+işaret 0,63 / %43 · birleşik sıra ortalaması 0,71 / %47 · tam LR 0,66 / %43 (SGD aşırı uyum; birleşik sıra seçildi). Dersler: Genetik 0,78, Patoloji 0,68, Farmakoloji 0,65, İç Hast. 0,65, **Halk Sağlığı 0,49 (sinyal yok)**.
**Ama 2026-27 K1 yeni ders notlarında (biçimi farklı, n=61) hepsi rastgele düzeyinde** (AUC 0,50; ilk-%20 %23). Sebep: model eski özet biçiminde (derinlik, kalın) eğitildi; yeni notlar paragraf/tablo ağırlıklı, kaynak satırı jeton-eşlemesiyle zor bulunuyor, n küçük. → Satır modeli **kanıtlanmış bir önem belirleyici değildir**.

## 4. Çıkarım — işçi bunu nasıl kullanır

**Güvenilir (ölçüldü): ders-düzeyi üslup profili ve konu kazanım haritası.** Yazım hedefi olarak bağlayıcıdır.
**Güvensiz (ölçüldü): satır puanı.** Yalnız aday listesi; her aday kanıt ister (sarı/kalın/tekrar, hoca sesi, çıkmış eşlemesi, tıbbi gerekçe). Kanıtsız satıra "önemli" damgası YASAK.

### 4.1 Aşama aşama (tam hat, E1–E2)
1. **Kaynak/hazırlık (E1):** `python3 scripts/hoca_profili/profil_oku.py --ders "<ders>" --konu "<konu>"` → özet (≤ 30 satır). `--json` ile makine okuması.
2. **Önem/vurgu listesi:** önce kanıtlı eşleme (çıkmış + hoca sesi + öğrenci notu). Sonra **profilin bilgi türü payına göre boşluk taraması**: konuda profilin ilk 3 bilgi türüne uyan ve çıkmışla eşleşmemiş satırlar için `onem_puanla.py <metin> --ders ...` adayları, her adayın neden o bilgi türüne girdiği yazılı gerekçeyle (kanıt satırı: "tür: ilac_yan_etki, sayfa N") eklenir. Eklenen önem "çıkmışta yok, profilden önerildi" etiketi alır (`kanit: profil`), puanı çıkmış eşlemeli maddenin altında kalır.
3. **Anlatım:** konunun **ilk 2 bilgi türü** anlatımda açık yer alır (mekanizma konusuysa zincir adım adım; ayırıcı konusuysa karşılaştırma tablosu; ilaç konusuysa yan etki/endikasyon). Tekrar eden çekirdek kavramlar (`cekirdek_kavramlar`) anlatımda en az bir kez örnekle işlenir ve sesli derste vurgulanır (vurgu yalnız kanıtlıysa; "hoca vurguladı" yasağı sürer).
4. **Örnek sorular:** (a) kalıp, bilgi türü ve düzey payları profile ±10 puan; (b) çekirdek kavram başına ≥2 soru, farklı kalıpla (kopya+çevirme, birleştirme, ters yön, ters ad — Patoloji için ayrıca `PATOLOJI_HOCA_SORU_MANTIGI.md`); (c) çeldirici stratejisi profildeki paya uyar (`ayni_ailede_komsu_kavram`, `bilesik_yer_degistirmeli`, `sayisal_yakin_deger`); (d) kaynağa bağımlılığı düşük konuda (özet kanıtlı <%30) en az bir soru slayttan bir mantık adımı ileri (`cikarim`); (e) yeni 2026-27 örneklerinin biçimi (bileşik şık, "en tipik") eski yıllardan farklıysa **yeni** yıl payı esas alınır.
5. **Kapı:** `python3 scripts/hoca_profili/profil_kapisi.py <ornek_sorular.json> --ders "<ders>"` (soru_uslup.py'ye EK). Güven yüksek + ≥20 soru → sapma HATA ("N soru şu türe çevrilmeli", yalnız o kadar soru yeniden yazılır); orta/düşük → UYARI. `hepsi/hiçbiri` her zaman HATA.
6. **Denetçi:** bağımsız denetçi profil özetini de görür: "hocanın bu konuda sorduğu bilgi türleri anlatımda ve sorularda var mı, eksik/yığılma var mı".

### 4.2 Hocanın soru nedenleri (kazanım haritasının dili)
Her konu için şu beş soru yanıtlanmış olmalı (haritada alanı vardır): **Neden bu bilgi?** (`neden_sorulur`) · **Nasıl?** (`nasil_sorulur`) · **Hangi bilgilerle?** (`hangi_bilgilerle`: çeldirici kaynağı) · **Zorluk?** (`zorluk`: L1/L2/L3 + tekrar) · **Kaynağa bağımlılık?** (`kaynaga_bagimlilik`).

## 5. Güven düzeyleri
`yuksek` n≥120 · `orta` 40–119 · `dusuk` <40. Düşük güvende ders profili yerine `_genel` + konu başlığı kullanılır; kapı yalnız UYARI. Konu haritasında n<3 konu yoktur (genel profile düşer). Yeni kurul sınavı geldikçe (Kurul 2 patoloji vb.) profil **yeniden hesaplanır**; ilk Kurul 2 çıkmışı gelince bu belgenin §3'ü yeniden koşulup güncellenir.

## 6. Bilinen sınırlar (gizleme yok)
- 2026-27 holdout küçük (Patoloji 21, Enfeksiyon 19, Genetik 12, Üroloji 11, Halk Sağlığı 6): üslup kayması kanıtı **yön gösterir, kesinlik değildir**.
- Bilgi türü/kalıp sınıflayıcıları kural tabanlıdır; `tanim_kavram` (%32) ve `dogrudan` (%40) "diğer" çöp kutusudur — bu payı yüksek çıkan dersler gerçekte daha çeşitli olabilir.
- Hoca bilgisi soru verisinde yok: profil **ders düzeyindedir**, ders içinde birden çok hoca varsa konu haritası daha doğrudur. 2018–2020 yıllar ağırlıklıdır; 2023+ az (dönem kayması alanı).
- Satır modeli yalnız aday üretir (§3C). Yeni ders notlarının biçimine uyarlı yeniden eğitim ancak 2026-27 etiketli (kaynak satırı elle doğrulanmış) veri artınca yapılabilir; yapılırsa yeniden holdout şart.
- Konu adları yıllar arasında farklıdır; konu eşleşmesi jeton Jaccard ≥0,34'tür. Eşleşmeyen konu ders profiline düşer.

## 7. Hoca-tahmin hattı ve test turları (2026-10-29, ikinci aşama)
Konu bazlı haritalama güçlendirildi: ders adına/hocaya bağlı değil, **dersin satırlarına en yakın 40 geçmiş çıkmış** (bge-m3) "yerel profil" olarak çıkarılır (`tahmin_girdisi.py`). Hocanın soracağı yerleri bulmak için kural: `docs/HOCA_TAHMIN_REHBERI.md` (v5). Girdi: `python3 scripts/hoca_profili/tahmin_girdisi.py <ders.md> --ders ... --konu ... --cikti <klasör>` (meds/.venv-ocr/bin/python).
**2026-27 ile kör sınama (6 tur, yargıç ajanı):** K=10–18 tahminle sorunun bilgisini yakalama **%62,5 (hiç ayarlanmamış bekletilmiş 22 ders)** ve **%69 (geliştirme, ders adı düzeltmesi sonrası)**; aynı K ile rastgele %12–26, algoritma tek başına %25–55. Ayrıntı, hatalar ve sınırlar: `docs/HOCA_USLUBU/TEST_TURLARI.md`. §3C'deki "satır modeli güvenilmez" uyarısı **yeni biçimli notlar için anlamsal-tekrar tabanlı birleşik sıra ile revize edildi**: aday listesi rastgeleden iyidir (elle etiketli: ilk-10 %53), ama önem kararını LLM yazar + gerekçe + kanıt verir.
