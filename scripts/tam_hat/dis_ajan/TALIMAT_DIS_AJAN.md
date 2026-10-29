# TALİMAT — Dış yapay zekâ ajanı: tam içerik hattı (tek, eksiksiz görev yönergesi)

> Bu metin sana verilen **görev yönergesidir**. Baştan sona oku. Burada yazmayan bir şeyi **yapma**; belirsiz bir şey varsa
> **dur ve kullanıcıya sor** (§11). Hızlı olmak için kalite kapılarını atlamak, gevşetmek ya da oyunlamak yasaktır; hız,
> yalnızca bağımsız işleri paralel yaparak ve hatalı parçayı tek başına düzelterek kazanılır.

## 0. Sen kimsin, ne yapıyorsun

- Sen Claude **değilsin**. Claude'un dersleri sitede zaten durur; sen **ayrı, etiketli bir taslak** üretiyorsun. Çıktın bir
  insan yönetici onaylayana dek öğrencilere **görünmez**.
- Başarı ölçütün: PDF'te yazanı, **PDF'te yazdığı kadarıyla**, doğru, anlaşılır ve eksiksiz anlatan bir ders paketi.
  Yeni bilgi icat etmek, "daha iyi olsun" diye eklemek **hata**dır. Kaynakta yoksa yazılmaz.
- Üç şeyi aklından çıkarma: **(1) kanıt önce, (2) küçük parti, (3) kapı geçmeden ilerleme yok.**

## 1. Mutlak kurallar (ihlal = işi durdur ve bildir)

1. Çıktın `<ders>-ag-<etiket>` anahtarıyla yaşar (örn. `k2-07-ag-gemini`). Mevcut bir anahtara yazmazsın. `v2`, `v3`, `-yeni` yok.
2. Yazabileceğin tek yer: `meds_temp/dis_ajan/<etiket>/<ders>/` (=`$W`) ve (yayın adımında) adında anahtarın geçtiği dosyalar.
3. Kaynak dışı bilgi yok. Her cümlenin **birebir alıntısı** olan bir PDF sayfası vardır.
4. İzinsiz LLM/API çağrısı, `rsync`/`scp` ile sunucuya dosya atma, kilit/maske/zamanlayıcı değiştirme **yok**.
5. Kapı eşiğini değiştirme, kapıyı atlama, kapıyı geçmek için sahte kayıt/çapa uydurma **yok**.
6. Kendi içeriğini "yayında/tamamlandı" diye sunma. Doğru ifade: "yönetici onayı bekliyor".
7. Ortak dosyalara (`interactive_learning_decks.json`, `site_ayar.json`, `hat.json`, `guncelleme_notu.json`, `AGENTS.md`, belgeler) **yazma**; değişiklik gerekiyorsa öneriyi `$W/ortak_degisiklik.json` dosyasına yaz ve kullanıcıya bildir.
8. Önem listesi, sesli çözücü, ders içerik paketi gibi **ön yüz paketine giren** dosyaları `src/data`'ya koyma; `$W`'da bırak.
9. Öğrenci notu katmanını yalnız kullanıcı isterse ekle.
10. Yerel GPU, Ollama, CUDA'lı PyTorch kendi başına kullanılmaz (yalnız AGENTS kural 10'daki yollarla).

## 2. Başlangıç — bu sırayla, hiçbirini atlama

```bash
E=gemini                 # kendi etiketin: a-z0-9, 2-12 harf, 'claude' olamaz
D=k2-07                  # ders kimliği (src/data/dersler/kN.json kayıt defterinden)
cd /home/indu/medsor/meds
# 2.1 Kendi git worktree'ni kur (başka oturumların düzenlemeleri senin çıktına karışmasın)
git worktree add ../meds-ajan-$E HEAD && cd ../meds-ajan-$E
W=/home/indu/medsor/meds_temp/dis_ajan/$E/$D; mkdir -p $W
# 2.2 Kimlik
echo "{\"ajan\":\"$E\",\"model\":\"<tam model adın>\",\"tarih\":\"$(date -I)\",\"surum\":\"1\"}" > $W/ajan.json
# 2.3 Anlama sınavı: %100 olmadan işe başlanmaz
python3 -I scripts/tam_hat/dis_ajan/anlama_sinavi.py sorular $W
#   $W/sinav_sorulari.json'u oku, cevapları $W/sinav_cevaplari.json'a {"q01": <seçenek sırası 0'dan>, …} yaz
python3 -I scripts/tam_hat/dis_ajan/anlama_sinavi.py puanla $W --ajan $E --ders $D
#   Yanlışta KURAL yazdırılır; kuralı oku, düzelt, yeniden puanla. Geçmeden devam ETME.
# 2.4 Hedefleri iş başında BİR KEZ yaz (sonra değiştirilemez). Yalnız proje kuralından gelen hedefi yaz: ornek_soru=51:100 (AGENTS kural 19).
#     anlatim_kelime YAZMA: sesli anlatımda kelime/dakika hedefi yoktur (kural 14); kullanıcı açıkça vermedikçe bu hedefi uydurma.
#     Kısmi çalışma (birkaç sayfa/test) ise hedefi kullanıcı söyler; söylemediyse hedef.json yazma, raporda «kısmi çalışma, hedef yok» de.
python3 -I scripts/tam_hat/dis_ajan/hedef.py yaz $W ornek_soru=51:100
# 2.5 Dosya anlık görüntüsü (iş başı)
python3 -I scripts/tam_hat/dis_ajan_kapisi.py --ajan $E --ders $D --anlik yaz
```

**`kural_secici.py --oku` kural METNİNİ değil DOSYA YOLLARINI listeler.** Listelenen her dosyayı **sonuna kadar** oku. Büyük dosyayı (örn. `docs/asama_kurallari/anlatim.md` ≈ 42 KB) Read aracında `offset`/`limit` ile 300'er satırlık parçalar hâlinde baştan sona oku; her parçadan sonra «okudum: dosya, satır a–b» diye not düş. Yarım okuyarak başlama.
Aşama kurallarını **o aşamaya gelince** oku: `python3 scripts/tam_hat/kural_secici.py --oku <kaynak|anlatim|ses|capa_cizim|ders_icerik|ogren_deste|ornek_soru|pdf_tasarim|yayin>`.
Bu çıktılar Claude'un gerçek hata defterinden çıkarılmış, **iyi/kötü örnekli** kurallardır; yazmadan önce ilgili listeyi oku.

## 3. Çalışma biçimi: KANIT ÖNCE, METİN SONRA (her yazım aşamasında)

Her bölüm (≈3–5 PDF sayfası) için üç dosya, bu sırayla:

**(a) `$W/kanit_<bolum>.json`** — sayfadan birebir kopyala:
```json
[{"id":"k1","bilgi":"Drosophilada 8 homeotik gen saptanmıştır.","s":9,
  "alinti":"Drosophilada 8 homeotik gen saptanmıştır ve bunların her birinin farklı vücut segmentleriyle ilişkili olduğu belirlenmiştir."}]
```
- `alinti` = `sayfalar.json` o sayfasından **kopyala-yapıştır** (özet/çeviri değil). Alıntı birden çok satıra yayılabilir; satır sonları ve çoklu boşluklar kapıda tek boşluğa indirilir, yani sayfadaki sözcük sırasını bozmadan kopyalaman yeter. Madde imi harfi (`o`) ve sayfa numarasını alıntıya katma.
- **Bir cümleyi/maddeyi yarım alıntılama:** sayfadaki cümlenin anlamlı kısmının hepsi alıntıda olmalı; kapsam kapısı cümlenin sözcüklerinin %60'ının alıntıda olmasını ister. Bilgiyi bölmek gerekiyorsa iki kanıt kaydı yaz. `bilgi` = o alıntının tek düz cümlelik özeti.
- Bilgideki her sayı alıntıda olmalı. Emin değilsen o kaydı yazma.

**(b) `$W/uretim_<bolum>.json`** — yazdığın her cümle bir kanıta bağlı:
```json
[{"id":"u1","p":1,"metin":"Ökaryotlarda gen ifadesini embriyonik gelişim boyunca düzenleyen proteinlere homeodomain proteinleri denir.","kanit":["k0"]},
 {"id":"u2","p":1,"metin":"Drosophilada 8 homeotik gen saptanmıştır; her biri farklı bir vücut segmentiyle ilişkilidir.","kanit":["k1"]}]
```
- `p` = paragraf numarası (aynı paragrafın cümleleri aynı `p`). **Paragraf "Bu/Bunlar/Şu/O/Ayrıca/Ancak" ile başlayamaz**: dinleyici ne kastedildiğini bilmez; konuyu adıyla an. Cümleleri kaynak sırasını izleyerek diz; tanım ve kavram, kendisini kullanan cümleden önce gelir.
- Kanıtı olmayan cümle **yazılmaz**. Olumsuzluk, sayı ve yön (artar/azalır) kanıttakiyle **aynı** kalır.
- Kanıtın olumsuz olduğu halde cümle olumsuz değilse kapı durdurur; kasıtlıysa `"olumsuz_gerekce"` yaz.

**(c) Kapı — her bölümden hemen sonra:**
```bash
python3 -I scripts/tam_hat/dis_ajan/bolum_kontrol.py $W <bolum> $W/sayfalar.json <ilk>-<son> <orijinal.pdf>
#   örn: ... bolum1 $W/sayfalar.json 9-12 /home/indu/medsor/meds_temp/ogrenci_ders/k2-08/orijinal.pdf
```
Resimli sayfayı sen aramazsın: KAPSAM adımı PDF'teki resimleri (`pdfimages`) kendisi bulur, şekil dosyası eksikse SEKIL-01 verir; resim bulunmayan sayfalar için şekil dosyası yazmazsın. **KANIT** (alıntı sayfada birebir mi), **TUTARLILIK** (cümle–kanıt uyumu, üslup, paragraf başı, kısaltma yazımı), **KAPSAM** (sayfadaki her cümle anlatıldı mı; resimli her sayfa için şekil dosyası var mı), **METİN** (sitenin gerçek ses denetimi `metin_denetle.py`).
Bilerek anlatmadığın cümle için `$W/atla_<bolum>.json`: `[{"s":12,"parca":"cümleden ayırt edici parça","neden":"≥10 karakterlik gerekçe"}]` (yalnızca gerçekten bilgi taşımayan öğeler: başlık, sayfa no, süs; **bilgi atlamak için gerekçe uydurma**).
- `GEÇTİ` olmadan sonraki bölüme geçme. `HATA` varsa mesajdaki **kimliği** düzelt (yalnız onu), komutu yeniden çalıştır.
- Aynı hata **3. kez** gelirse dur, kullanıcıya hata + denediklerini yaz.

Bölüm dosyalarından **ders metni** `metin.md`'de birleştirilir: `# Başlık`, `@@ Bölüm`, paragraf (§5 anlatım kartı).

### Sık hata mesajları ve karşılıkları

| Kod | Anlamı | Yapacağın |
|---|---|---|
| KANIT-04 | `belirsiz` kayıt kullanılamaz | Kaydı sil, o bilgiyi anlatma, raporda "belirsiz" yaz |
| KANIT-08 | Alıntı sayfada birebir yok | Sayfa metninden yeniden kopyala; bulamazsan kaydı at |
| KANIT-09 | Bilgideki sayı alıntıda yok | Sayıyı alıntıdan al |
| URETIM-02 | Cümlenin kanıtı yok | Kanıt ekle ya da cümleyi sil |
| URETIM-04 | Cümledeki sayı kanıtta yok | Sayıyı kanıttaki değerle düzelt |
| URETIM-05/06 | Olumsuzluk kanıtla uyuşmuyor | Olumsuzluğu kanıttaki gibi taşı |
| URETIM-07 | Artış/azalış ters | Yönü kanıttaki gibi yaz |
| URETIM-08 | Cümle kanıtla konu olarak örtüşmüyor | Doğru kanıtı bağla ya da cümleyi kanıta indir |
| URETIM-09 | Çeviri mecaz / iç etiket | Doğal, düz Türkçeyle yaz |
| URETIM-10 | Dolgu / kaçamak cümle | Cümleyi sil ya da yeni bilgi taşıyan cümleyle değiştir |
| URETIM-14 | (uyarı) ardışık cümleler aynı sözcüklerle başlıyor | Cümleleri çeşitlendir ya da birleştir |
| URETIM-15 | Kısaltma büyük harfle ya da uydurma okunuşla yazılmış | `okunus_oner.py` çıktısını AYNEN yaz (§4b) |
| TANIM-01…08 | Tanım cümlesi kuralı ihlali | §4c |
| URETIM-12 | Cümlede paragraf numarası (`p`) yok | Her cümleye `p` ver |
| URETIM-13 | Paragraf bağlamsız zamirle başlıyor | Konuyu adıyla anarak başlat |
| KAPSAM-00 | `atla` kaydı eksik | `parca` ve ≥10 karakter `neden` yaz |
| KAPSAM-01 | Sayfadaki cümle anlatılmamış | Kanıt + cümle ekle; bilgi değilse gerekçeyle `atla` |
| SEKIL-01 | Resimli sayfada şekil dosyası yok | §6'daki prosedürle şekli oku, dosyayı yaz |
| SEKIL-02 | Şekil dosyası boş | Kayıt ekle ya da `okunamadi:true` + neden |
| HEDEF-04 | Sayısal hedef toleransın dışında | Yalnız sapan bölümü düzelt |

## 4. Evre kartları (sırayla; her kartın sonunda "BİTTİ ÖLÇÜTÜ" sağlanmadan sonrakine geçme)

### E0 — Hazırlık (kaynak çıkarma)
- Girdi: kullanıcının söylediği PDF/dosya eşleşmesi (hangi dosya hangi ders). Belirsizse **sor**.
- Komut: `python3 scripts/tam_hat/hazirlik.py $W --ders $D`. Çıktı: `sayfalar.json`, `op/s-NNN.png`, öğrenci notu/hoca dökümü (varsa).
- **Ders profili (§4e):** `meds_temp/ders_profili/<ders>/` varsa `$W/profil/` olarak kopyala ve `hoca_uslubu.md` + `kazanim_haritasi.json`'u baştan sona oku; yoksa raporda «profil yok» yaz.
- BİTTİ: `sayfalar.json` dolu, görüntü sayısı = sayfa sayısı. PDF'i **sayfa başlıklarıyla** doğrula (dosya adına güvenme).

### E1 — Kaynak paketi
- Değerlendirme paketi: hoca vurguları (zaman damgalı alıntı), çıkmış eşleme (`s`, birebir `kanit`, `seviye`, `dogrulandi`).
- Kapı: `python3 scripts/ogrenci_drive/degerlendirme_dogrula.py` (paket yoluyla). BİTTİ: 0 HATA.
- Çıkmış vurgusu yalnız doğrulanmış eşlemeye dayanır; vektör benzerliğiyle "çıkmış" yazma.

### E2 — Anlatım (sesli ders metni)
- Önce `$W/anlatim_plani.md`: bölüm listesi, her bölümün sayfa aralığı ve **tanımlanacak terimler** (ilk geçişte açıklanır).
- Sonra §3'teki kanıt→üretim→kapı döngüsü bölüm bölüm. Metin kuralları: öğreten üslup, dolgu yok, "hoca vurguladı" yalnız
  hoca dökümünde zaman damgalı alıntı varsa; aynı sözcük iki ayrı kavram için kullanılıyorsa ayrıştır ("birinci tür/birinci tip");
  kilit kavram tanımlanmadan sayısal ayrıntıya girilmez; her cümle tek bir düşünce, ≤25 kelime.
- Kapılar: her bölüm bitince `bolum_kontrol.py` (bölüm bazında); **tüm bölümler bittikten sonra** birleştirilmiş `metin.md` için bir kez `python3 scripts/sesli_anlatim/metin_denetle.py $W/metin.md` ve `hedef.py kontrol $W anlatim_kelime=<ölçülen>` — ölçüm: `python3 -I scripts/tam_hat/dis_ajan/hedef.py say $W/metin.md` (başlık ve `@@` satırları hariç; `wc -w` KULLANMA). Her hedefi ilgili evrede ölç: anlatım hedefi E2'de, `ornek_soru` hedefi yalnız E4'te.
- **Tanım cümlesi (isteğe bağlı, §4c):** ilk geçişte anlaşılmayan terim için sözlükten türeyen kısa tanım.
- BİTTİ: tüm bölümler GEÇTİ + `metin_denetle` 0 HATA + kapsam: PDF'in her içerik sayfası ya anlatıldı ya da gerekçeyle atlandı.

### E3 — Öğren destesi (mini soru, boşluk doldurma, doğru-yanlış, aktif hatırlama… hepsi deste içindedir)
- **Önce oku:** `docs/OGREN_ETKILESIM_REHBERI.md` (≈42 KB; §2'deki parça parça okuma kuralı) ve gerçek biçim örneği `scripts/tam_hat/dis_ajan/ornekler/deste_ornek.json` (depodan alınmış 2 slayt; alan adlarını AYNEN kopyala).
- **Çıktı:** `$W/deste.json` (tek deste; `id`: `k2p-<ders>-ag-<etiket>`). Slayt: `title`, madde imli `synthesisNarrative` (60–250 kelime, yalnız kanıtlı bilgi), `pdfSayfalari`, `slideNumber`, 4–6 `interactiveElements` (tek tipe yığılma yok; aynı slaytta en çok 1 `causal_chain`).
- **Kazanım ve gerçekçilik:** her etkileşim o slaytın kanıtına bağlı tek bir kazanımı pekiştirir. Etkileşimde yalnız o slayt ve öncesinde anlatılan bilgi kullanılır (**ileri sızıntı yok**). Vaka/senaryo gerekiyorsa gerçekçi, kısa klinik tablo; **absürt, fantastik ya da müfredat dışı örnek, uydurma isim/olay yok.** Çeldiriciler öğretilmiş komşu kavramlardan gelir. İpucu cevabın sözcüğünü/kökünü/sayısını içermez.
- **Kanıt zinciri:** `$W/kanit_deste.json` (alıntılar) ve `$W/iddia_deste.json`:
  `[{"id":"i1","eleman":"s1","metin":"<synthesisNarrative cümlesi AYNEN>","kanit":["k1"]},{"id":"i2","eleman":"s1.e0","metin":"<sorunun/açıklamanın cümlesi AYNEN>","kanit":["k2"]}]`
  `eleman`: slayt anlatımı için `s<slideNumber>`, etkileşim için `s<slideNumber>.e<sıra 0'dan>`.
- **Kapılar (bu sırayla):** `python3 scripts/validate_learning_decks.py $W/deste.json --kurul2` (0 HATA; tam derste ayrıca `--oyun-zorunlu`) →
  `python3 -I scripts/tam_hat/dis_ajan/icerik_kontrol.py deste $W/deste.json $W/iddia_deste.json $W/kanit_deste.json $W/sayfalar.json` (0 HATA).
  Hata varsa yalnız hatanın gösterdiği slayt/etkileşimi düzelt.

### E4 — Örnek sorular ve sesli çözücü
**E4a Örnek sorular**
- **Önce oku:** `docs/SORU_USLUBU.md`, `docs/SIK_ACIKLAMA_STANDARDI.md`; biçim örneği `scripts/tam_hat/dis_ajan/ornekler/ornek_soru_ornek.json` (alanları AYNEN kopyala). Üslup örnekleri: `python3 scripts/tam_hat/soru_uslup_ornek.py $W` → `$W/soru_uslubu.json`; yalnız onu örnek al.
- **Çıktı:** `$W/ornek_sorular.json` (ders dosyası biçimi: `kazanimlar[].sorular[]`; soru `id`: `<ders>-ag-<etiket>-q01`…). Her soru: `kazanim`, `zorluk`, kısa `soru` kökü, 5 şık (A–E), `dogru`, `aciklama`, her şık için `sik_aciklamalari`.
- **Kısaltma yazımı:** ekran metnidir; kısaltma ve gen adları PDF'teki gibi (`HOX`, `OTX1`, `BT`). Okunuşla (hoks, o te iks) YAZMA.
- **Çıkmış tarzı ve muhakeme:** her soru **≥2 ayrı bilgiyi birleştirir** (zor soruda ≥3; kapı SORU-01): bulgu→mekanizma, iki komşu kavramı ayırt etme, «hangisi yanlıştır», vaka→tanı/sonraki adım. Kısa «hangisidir / hangi gen?» ezber kökü soruların en çok %25'i (SORU-02). Kök cevabın sözcüklerini taşımaz (SORU-04). Sorular kanıtın tek sayfasına yığılmaz (SORU-05). **Ne sorulur:** slaytın başlık/kalın/tekrar/tablo/şema ile öne çıkardığı ve tıbbi olarak sınavda çıkması en olası bilgi; ayrıntı sorusu değil. `ders profili` (§4e) varsa her soruya `kazanim_id` yaz.
- **Kapı nüansları:** her iddia yalnız KENDİ bağlı kanıtına göre denetlenir (soru bütününe göre değil); olumsuz sözcük («değil, yok, olmaz») kanıtta yoksa yazılmaz, yanlış şıkkı «… yanlıştır» diye bitir; sayı sözcükleri (iki, üç) sayı sayılır; «her, anterior, temel, akut» gibi niteleyiciler kanıtta yoksa yazılmaz. Soru kökü «X, Y'nin türüdür» gibi bir ilişkiyi kanıtta AÇIKÇA yazmıyorsa o soruyu yazma (ör. «homeodomain = transkripsiyon faktörü» sayfada yazmıyorsa çıkarım olur).
- **SORU-06 (cevap–kök ortak kanıt):** doğru şıkkın ayırt edici sözcükleri ile soru kökünün sözcükleri aynı alıntıda birlikte geçmelidir. Geçmiyorsa soru bir çıkarımdır: ilişkiyi söyleyen alıntıyı (gerekirse iki sayfadaki cümleleri tek kanıtta birleştirmeden, ama aynı cümlede söyleyen alıntıyı) bağla ya da soruyu kaynakta açıkça yazan ilişkiye göre yeniden kur. Terim adını soran soruda (örn. «bu olguya ne denir?») adın geçtiği alıntı da kanıta bağlanır.
- **Şık kalitesi (SORU-07/08/09):** şıkta «kaynakta/slayt/belirtilmez/fark yok» gibi gönderme ya da dolgu şık yok; mutlaklaştırılmış («yalnız, hiçbir, hepsi») çeldirici soru başına en çok 1, kalanlar öğretilmiş komşu kavramdan; şık açıklaması «… yanlıştır / Doğru seçenek budur» kalıbıyla bitmez, mekanizma anlatır. Soru kökü tek konuyu sorar: ilgisiz iki konuyu («amino uçları ile OTX genleri») tek köke bağlama; birleştirme yalnız aynı konunun ardışık maddeleri içindir.
- **Üslup kapısı girdisi:** `soru_uslubu.json` için `cikmis_aday.json` E0 `hazirlik.py` çıktısıdır; yoksa E0'ı çalıştır, çalıştıramıyorsan raporda «üslup kapısı çalışmadı» yaz.
- **Kalite:** yalnız PDF'te anlatılan bilgiden (müfredat dışı/spekülatif bilgi YOK); ezber değil mekanizma/ayırıcı tanı/muhakeme; en az 2 güçlü çeldirici öğretilmiş komşu kavramdan; doğru şık en uzun olmasın; kökte «derste», «slayt», «hoca», «sayfa N» yok; vaka kökü gerçekçi ve kısa (uydurma/absürt hasta, isim, olay yok). Her şık açıklaması 2–3 cümle: kavram NE / ne işe yarar / bu soruda neden doğru-yanlış (**«cevabı değil», «… olarak geçmez» yasak**).
- **Kanıt zinciri:** `$W/kanit_soru.json`, `$W/iddia_soru.json` (`eleman` = soru `id`; soru kökü, doğru şık metni, `aciklama` ve **her şık açıklaması** AYRI iddia, her biri kanıtlı).
- **Kapılar:** `python3 scripts/tam_hat/soru_uslup.py $W/ornek_sorular.json --uslup $W/soru_uslubu.json` (n<20 ise set payı UYARI) →
  `python3 -I scripts/tam_hat/dis_ajan/icerik_kontrol.py ornek $W/ornek_sorular.json $W/iddia_soru.json $W/kanit_soru.json $W/sayfalar.json` (şık açıklama standardını da denetler).

**E4a-PAT Tıbbi Patoloji dersi (AGENTS kural 25) — E4a yerine bu akış:**
1. Önce oku: `docs/PATOLOJI_HOCA_SORU_MANTIGI.md`, `docs/PATOLOJI_SORU_ESLEME_TABLOSU.md`, `scripts/patoloji_soru_isci/TALIMAT.md` (tamamı), ve hocanın gerçek soruları: `python3 scripts/hoca_profili/profil_oku.py --ders "Tıbbi Patoloji" --konu "<ders konusu>"` (+ `src/data/hoca_uslubu_sorular/k2/` örnekleri; kalıbı öğren, KOPYALAMA).
2. `meds/.venv-ocr/bin/python -I scripts/patoloji_soru_isci/hazirla.py "<ders.pdf>" $W/patoloji_isci --n 12` → `paket.json`. Önem adaylarını PDF'le gözden geçir (sarı = yapı etiketi, altındaki satır önemlidir; kırmızıyı «önemli» sayma).
3. `$W/sorular.json` (patoloji biçimi) yaz: her önem noktasına ≥2 soru, farklı kalıpta; 3 dönüşüm (kopya+çevirme, birleştirme, yön değiştirme); kök 7–18 kelime; şıkların ~%30–50'si bileşik; çeldirici aynı dersin komşu kavramı (`celdirici_kaynak` ≥3 sayfa); doğru şık en uzun değil.
4. Kapılar sırayla, hepsi 0 HATA: `python3 scripts/patoloji_soru_isci/dogrula.py $W/sorular.json $W/patoloji_isci/paket.json` → `python3 scripts/hoca_profili/profil_kapisi.py --ders "Tıbbi Patoloji" …` (kullanımını dosyadan oku) → `python3 scripts/tam_hat/dis_ajan/patoloji_donustur.py $W/sorular.json $W/ornek_sorular.json <ders>-ag-<etiket>` → kanıt zinciri (`kanit_soru.json`, `iddia_soru.json`) → `icerik_kontrol.py ornek …` (SORU-01/06 bu biçimde de geçerli; `kazanim_id` = onem_id, profil haritası yok → UYARI normal).
5. Bu iki kapı takımı BİRBİRİNİN yerine geçmez: patoloji kapısı hoca üslubunu, dış ajan kapısı kaynağa sadakati denetler.

**E4b Sesli soru çözücü**
- Biçim örneği `scripts/tam_hat/dis_ajan/ornekler/cozucu_ornek.json` ve `scripts/spot_cozucu/TALIMAT_COZUCU.md` (tamamını oku). `klip` (ses zamanı) alanını **sen yazmazsın**, site hattı üretir.
- **Çıktı:** `$W/cozucu.json` = `{"kod","no","baslik","klasor","sorular":[{"no","tur":"ornek","zorluk","soru","secenekler","dogru","ipucu","siklar":{A..E}}]}`. `ipucu` doğru şıkkın sözcüklerini içermez, mantığı hatırlatır; `siklar` her şık için 2–3 cümle (standart yukarıdaki gibi).
- **Kısaltma yazımı:** soru, şık, ipucu ve açıklama metinleri EKRANDA da okunur; kısaltma ve gen adları PDF'teki gibi yazılır (`HOX`, `HOXD13`, `OTX1`, `BT`, `ARAS`) — depodaki gerçek soru/çözücülerde de böyledir. Sesi site hattı üretir. Okunuşla yazma kuralı (§4b) YALNIZ sesli anlatım metni (`metin.md`) içindir.
- Kanıt zinciri `kanit_cozucu.json` + `iddia_cozucu.json` (`eleman`: `no<soru no>`). Kapı: `icerik_kontrol.py cozucu $W/cozucu.json $W/iddia_cozucu.json $W/kanit_cozucu.json $W/sayfalar.json` (şık standardı + ipucu sızıntısı dahil).
- `scripts/spot_cozucu/cozucu_dogrula.py` ders klasörü yapısı ister; onu yayın aşamasında Claude çalıştırır.

### E5 — Çapa ve canlı çizim
- **Önce oku:** `scripts/cizim/TALIMAT_CIZIM.md` ve `docs/CIZIM_KURALLARI.md` (tamamı, parça parça) ve `sablonlar.json`. Çizim zenginleştirmedir. **«Emin değilsen çizme» yalnız anatomik kontur/akış/eğri içindir.** Metin ağırlıklı sayfada sınıflama, neden→sonuç, karşılaştırma ya da tek değer anlatan cümleye **şablonlu panel (`sema` + `sablon`)** çizilir (Claude'un k2-08 çiziminde sayfaların ≈%40'ı böyledir). Boş `cizim.json` yalnız sayfada gerçekten ilişki anlatan cümle yoksa kabul edilir.
- **Ders profili:** `meds_temp/ders_profili/<ders>/` varsa (kullanıcı hocanın üslubunu/kazanım haritasını buraya koyar) E0'da `$W/profil/`ye kopyala; çizim için de önemli kazanımların sayfalarında çizimi atlama.
- **Girdi (parti klasörü):** `sayfalar.md` (cümleler `P#.C#: [0]kelime [1]kelime …`), `sNN.png` (numaralı kutulu sayfa görüntüsü), `sNN.txt` (`M#` yazılı satırlar, `R#: resim [x0,y0,x1,y1]` resim kutuları). **Görüntüyü AÇ ve bak**; koordinatı `kirp.py` ile kırpıp doğrula (§6).
- **Önce karar:** `<parti>/karar.json` — sayfadaki HER cümle için `{"cumle","iliski":"siniflama|neden_sonuc|karsilastirma|deger|sekil|yok","cizim":true|false,"neden_yok":"çizim yoksa ≥40 karakter TIBBİ gerekçe"}`. Önce ilişkiyi belirle, sonra şablonu seç (`sablonlar.json`'daki `ne_zaman` alanına göre).
- **Çıktı:** `<parti>/cizim.json` = `{"komutlar":[{"cumle","bas","son","sayfa","tur":"kontur|akis|egri_faz|sema", …}]}`. `bas/son` = cümledeki kelime numaraları. Tür kuralları TALIMAT_CIZIM.md'dedir; özet: **kontur** resim kutusu (R#) içinde ve gerçek kenarın üstünde 5–20 nokta; **akis** uçları gerçek yazı/çizim üstünde, `kaynak_metin/hedef_metin` slaytta YAZILI ifade; **sema** yalnız o cümleye kadar anlatılmış terimlerle (ileri sızıntı yok); cümle başına ≤2, sayfa başına ≤8 komut.
- **Tıbbi sadakat kontrol listesi (her komut için, çizmeden önce):** (1) çizimin gösterdiği ilişki cümlede AYNEN söyleniyor mu; (2) panel/ok etiketleri yalnız bu cümleye kadar anlatılmış slayt terimleri mi; (3) ok yönü neden→sonuç yönünde mi, kaynak slayttaki yönle aynı mı; (4) kontur gerçekten cümlenin anlattığı yapıyı mı çevreliyor (komşu yapı değil); (5) renk anlamı sayfa içinde tutarlı mı; (6) çizimi sesi kapalı biri sadece görseline bakarak anlayabilir mi. Birinde bile «hayır/emin değilim» ise o komutu yazma (anatomik kontur/akış) ya da şablonlu panele çevir.
- **Panel hücresi yazımı (Sonnet testinde çıktı):** sayfalar.md'deki cümleler sesli okunuşla yazılıdır («o te iks»); ileri-sızıntı kapısı panel sözcüklerini onunla karşılaştırır. Bu yüzden (a) hücredeki sözcükleri cümledeki biçimiyle AYNEN al («ifade edilir», «edilen» değil — ek farkı başka sözcük sayılır), (b) yalnız gen adından oluşan hücreye cümlede geçen bilinen bir sözcük ekle («OTX2 geni, gelişim sırasında»), (c) kapıyı geçmek için anlamı bozma; geçemiyorsa şablonu değiştir. Gen adı panelde PDF yazımıyla (OTX2) görünür. `R#: resim` olarak listelenen ama gerçek görsel olmayan metin kutusu (yalnız yazı çerçevesi/süs) resim sayılmaz; üstüne kontur/akış çizme.
- **Dal etiketleri tekrar etmez:** `tek_neden_cok_sonuc`'ta her dal kendi bilgisini taşır («orta beyin anomalisi», «serebellum anomalisi»); üç dalda aynı «anomali» sözcüğü yazma. Üç ayrı alan için aynı kökten üç sonuç gerçekten anlatılıyorsa bu şablon uygundur, yoksa `siniflama`.
- **Kontur yöntemi (Haiku testinde sayfa 78'de doğru çıktı):** noktaları gözle tahmin etme. `kirp.py` ile yapıyı kırp, kenarı bulup (ör. OpenCV Canny + en büyük kontur, `.venv-ocr`) kenar boyunca 8–12 nokta örnekle, sonra kontur çizimini s78.png üstüne bindirip (overlay) görüntüyü AÇ ve yapıyı gerçekten çevreliyor mu bak. Kapı kenar üstünde olmayı ölçer, doğru yapıyı çevrelediğini ölçmez; o kontrolü bindirmeyi bakarak sen yaparsın. Yardımcı betiklerini $W içinde tut, parti klasörüne yalnız cizim.json/karar.json koy.
- **Güzel çizim:** panel azı dört kutu/öğe, kısa etiket (≤3 sözcük), kutular ve oklar çakışmaz, sayfanın boş yerinde durur, aynı sayfada aynı kavram hep aynı renk. Sayfada ilişki anlatan her cümleyi en iyi gösteren şablonu `sablonlar.json` `ne_zaman` alanından seç; her cümleye zorla çizim koyma, ama ilişkisi güçlü cümleyi çizimsiz de bırakma.
- Şekil anlatan cümlede lazer görselin üstünde anlatılan parçayı işaretler; bütün resmi çevreleme, metin satırını boyama, tek cümleye iki ayrı konum yasak. Çapa/madde uydurup kapsamı şişirme yasak.
- **`resim` alanı:** sayfada TEK resim kutusu varsa `resim` yazma. Birden çok kutu varsa `sNN.txt`'deki `R#` numarasını yaz; `sNN.txt`'deki etiketi AYNEN yaz (`R0` olabilir): kapı etiketi doğrulayıcının sıra sayısına kendisi çevirir. Kapı «sNN.txt'de yok» derse etiketi txt'den kopyala.
- **Kapı:** `.venv-ocr/bin/python -I scripts/tam_hat/dis_ajan/cizim_kontrol.py <parti>/cizim.json <parti>/sayfalar.md <orijinal.pdf> <sayfa> <parti>/sNN.txt` (0 HATA; `karar.json` ile tutarlı olmalı). Gerçek kapı `cizim_dogrula.py`'dir; geçmeyen komutu düzelt ya da sil, kapıya dokunma.

### E6 — Yayın ve rapor (§8–§10)

## 4b. Sesli okunuş — YALNIZ sesli anlatım metni (`metin.md`); soru/çözücü/deste ekran metninde PDF yazımı kalır — sitenin gerçek hattı (yayınlanmış k2-08 dersi ve `metin_denetle.py` ile doğrulandı)
Metin EMA ile seslendirilir ve sitenin ses denetimi (`metin_denetle.py`, `--yazim` YOK) **büyük harfli kısaltmayı HATA sayar**: kısaltma ve gen/protein sembolleri
**doğal Türkçe okunuşla** yazılır, sayılar yazıyla: `HOXD13` → «hoks de on üç», `OTX2` → «o te iks iki», `MSX1` → «me se iks bir», `HOX` → «hoks».
- **Okunuşu UYDURMA.** Her kısaltma için `python3 -I scripts/tam_hat/dis_ajan/okunus_oner.py <KISALTMA>` çalıştır, çıktıyı AYNEN yaz. Kapı URETIM-15, kanıttaki kısaltmanın okunuşu araç çıktısından farklıysa (ör. «otiks», «dê on üç») ya da kısaltma büyük harfle yazılmışsa durdurur.
- **Karma yazım da kısaltmadır:** kaynakta «Hox», «Otx», «Pax» gibi küçük harfli yazılmış gen adı da sese gider; bunlar da `okunus_oner.py` çıktısıyla yazılır, aynı metinde «Hox» ile «hoks» karışmaz (kapı bunu yakalamaz, sen tutarlı ol).
- Araç çıktısı sana yanlış geliyorsa (ör. tanınmış bir kelime gibi okunan bir gen) kendin değiştirme; kullanıcıya sor.
- Yunan harfi ve simge (%, →, ↑) yazıyla (alfa, yüzde…). Yalın sayılar yazıyla (`sekiz`, `beş`); sayı kapısı yazıyla yazılmış sayıyı da kanıttaki rakamla karşılaştırır.
- Bölüm kapısı (`bolum_kontrol.py`) bu denetimi kendisi çalıştırır; tüm metin için: `python3 scripts/sesli_anlatim/metin_denetle.py $W/metin.md` (`--yazim` kullanma).
- Not (kullanıcıya açık soru): H23 defteri «kısaltmayı yazımla tut» diyor, yayınlanmış k2-08 ve gerçek hat okunuşla yazıyor; burada gerçek hat uygulanır.

## 4c. Tanım cümlesi — anlatımı öğretici kılmak, ama müfredatın içinde kalarak
Kanıt zinciri yalnız slaytta yazanı söyler; slaytın kullandığı ama açıklamadığı terim için dinleyiciye kısa bir tanım verebilirsin. Bu **sınırlı** bir istisnadır:
1. **Kaynak = müfredat sözlüğü.** `python3 -I scripts/tam_hat/dis_ajan/sozluk_ara.py <terim>` ile ara. Sözlükte yoksa tanım YAZILMAZ ("BULUNAMADI" yazar). Kendi tıp bilginden tanım üretmezsin.
2. **Kayıt biçimi:** `{"id":"u4","p":2,"tur":"tanim","terim":"homeotik transformasyon","sozluk":"<araçtaki anahtar AYNEN>","metin":"…","kanit":["k3"]}`; `kanit` terimin geçtiği alıntıdır.
3. **Cümle sözlük tanımından türer** (kök örtüşmesi ≥ %50), ≤ 35 kelime, **rakam yok, örnek/senaryo yok** («örneğin», «diyelim», «bir hasta…» yasak), yeni kısaltma/gen adı yok. Sözlük tanımındaki ek örnek cümlelerini ("Sineklerde anten yerine bacak oluşması…") alma.
4. Bölümdeki cümlelerin **en çok %20'si** tanım olabilir. Aynı terimi iki kez tanımlama.
5. Tanım cümlelerini raporda ayrı listele (terim, sözlük anahtarı); yönetici gözden geçirir.
6. Tanım bir **kazanım** terimidir; müfredattan uzaklaşan, ders konusuyla bağı olmayan terim tanımlanmaz.


## 4d. Öğretici anlatım — gerçek bir dersten daha anlaşılır, ama sıfır tıbbi hata
Hedef: dinleyen, hocadan dinlemiş olmaktan **daha iyi** anlasın. Bunun yolu süslemek değil, **sıralamak ve açmaktır**; yeni tıbbi bilgi eklemek değildir.
1. **Bölüm yapısı:** (a) bölümün neyi anlattığını söyleyen tek cümle; (b) kavramı kuran cümleler (ne, nerede, ne yapar); (c) mekanizma adım adım, her adım ayrı cümle ve önceki adıma bağlı; (d) klinik karşılık/sonuç; (e) kaynağın kendi vurguladığı noktayı kısa toparlayan bir cümle (yeni bilgi taşımalı, önceki cümleyi tekrar etmemeli).
2. **İlk geçişte zor terim:** slaytın tanımlamadan kullandığı ve dinleyicinin bilmeyebileceği terim için §4c'deki sözlük tanımı (en çok %20).
3. **Sıra bilgiyi öğretir:** önce genel çerçeve, sonra ayrıntı; karşılaştırma varsa iki tarafı art arda ve aynı ölçütlerle söyle («A şöyle, B ise şöyle»).
4. **Bağlaç mantığı kanıtlıdır:** «bu nedenle / sonucunda / yol açar» yalnız kanıtın o ilişkiyi söylediği yerde. İlişki iki ayrı alıntıdan çıkıyorsa `"cikarim": true` ve ≥2 kanıt (kapı NEDEN-01/02).
5. **Niteleyici sadakati:** «her, tüm, yalnız, genellikle, otozomal dominant, proksimal…» gibi kapsam/kesinlik/yer/kalıtım sözcüğü kaynakta aynen yoksa YAZILMAZ (kapı NITELE-01). Çoğu tıbbi hata burada çıkar.
6. **Benzetme/örnek/hikâye yok.** Mecaz, günlük hayat örneği, uydurma hasta yok. Anlaşılırlık sade cümle ve doğru sıradan gelir.
7. **Bitirmeden kendi kendine oku:** her bölümü, konuyu bilmeyen bir tıp öğrencisi gibi baştan sona oku. Bir yerde «bu neydi?» diye takıldıysan o terimin tanımını ekle ya da cümleyi böl. Sonra her cümleyi kanıtıyla yan yana koyup «kanıt bunu **gerçekten** söylüyor mu, yoksa ben mi yorumladım?» diye tek tek sor; yorumsa sil ya da `cikarim` yap.

## 4e. Ders profili — hocanın üslubu ve kazanım haritası (kullanıcı verir)
Kullanıcı bazı derslere `profil/` klasörü koyar (`$W/profil/`): `hoca_uslubu.md`, `kazanim_haritasi.json` (biçim: `scripts/tam_hat/dis_ajan/ornekler/profil_ornek/`) ve varsa çıkmış soru örnekleri. Varsa:
- **Oku ve uygula:** soru kökü, çeldirici seçimi ve dil `hoca_uslubu.md`'ye uyar; üslup örneğini kopyalama, kalıbını öğren.
- **Kazanım haritası soru seçimini yönetir:** her soruya `kazanim_id` yaz; `onem: yuksek` kazanımlara en az 1, `hoca_vurgu: true` olanlara en az 2 soru (kapı PROFIL-01/02). Haritada olmayan, slaytta da önemsiz bir ayrıntıdan soru yazma.
- **Kaynak sınırı değişmez:** profil yalnız NEYİ ve NASIL sorulacağını söyler; bilgi hâlâ yalnız PDF kanıtından gelir. Profil ile PDF çelişirse PDF'e uy ve çelişkiyi raporla.
- Profil yoksa kapı yalnız UYARI verir; önemi slaytın kendi vurgusundan (başlık, kalın, tekrar eden, tablo/şema, «önemli» ibareleri) ve tıbbi ağırlıktan çıkar.

## 5. Anlatım kartı (kısa)
1. Bölüm açılışı 1–2 cümle tanım. 2. Mekanizma/aşama tane tane. 3. Klinik bağ ya da sınav spotu (yalnız kaynak/hoca/çıkmış dayanaklıysa).
4. Önceki bölümün cümlesini tekrar etme. 5. Ses ile okunacağını unutma: kısaltmaları, gen sembollerini, rakamları sesli okunuşuyla düşün.
6. Aynı özneyi ardışık 3+ cümlede aynı sözcüklerle başlatma (robotik); paragraf içinde «bu genler», «bunlar» gibi zamir serbest, paragraf başında yasak.
7. Çeviri mecaz ("imzası", "motoru", "freni", "çapası") ve iç etiket ("Kısa formül:", "Akılda tut:") yok.

## 6. Görsel okuma ve çizim — adım adım (en hataya açık yer)

**Görsel okuma (resim bulunan HER sayfada; `bolum_kontrol` resimli sayfaları kendisi bulur):**
1. `sayfalar.json` metnini oku. 2. `op/s-NN.png`'yi parçala: `python3 -I scripts/tam_hat/dis_ajan/kirp.py $W/op/s-12.png 0 0 1 0.5` (oranlar 0–1; sol-üst 0,0) ve her kırpığı ayrı aç/oku. Önce üst/orta/alt, sonra ayrıntılı bölgeler.
3. Gördüğünü **liste** olarak `$W/sekil_s-NN.json` dosyasına yaz (NN iki haneli: `sekil_s-09.json`, `sekil_s-12.json`):
```json
[{"nesne":"şematik çizim: Hox gen kümesi","konum":"0.05,0.45,0.95,0.75","etiket":"HOXA … HOXD","iliski":"yalniz-goruntude"}]
```
   - `konum` = `x0,y0,x1,y1` 0–1 oran (sol-üst 0,0). `iliski` yalnız şu üç değerden biri: `metin-katmaninda-var` | `yalniz-goruntude` | `celisiyor`.
4. `metin-katmaninda-var` olanlar anlatımda kullanılabilir. `yalniz-goruntude` olanı yalnız görüntüde net okunuyorsa ve kırpıkta tekrar doğruladıysan kullan; `celisiyor` ise kullanma, kullanıcıya bildir.
5. Emin olmadığın hiçbir şeyi (ok yönü, renk anlamı, numara) yazma. Görüntüyü hiç okuyamıyorsan dosyaya `{"okunamadi": true, "neden": "…"}` yaz ve o şekle dayanan bir şey anlatma.

**Çizim/lazer (yalnız görsel okumayı geçtiysen):**
1. Cümle şekil anlatıyor mu? Hayır → çizim yok. Evet → anlatılan **parçayı** bul.
2. Parçanın kutusunu `op/s-NNN.png` üzerinde piksel olarak belirle; sayfa genişlik/yüksekliğine bölüp 0–1 oranına çevir.
3. Kutuyu **kırp ve yeniden bak**: anlatılan şey kırpıkta duruyor mu? Durmuyorsa koordinat yanlış, yeniden bul.
4. Bütün resmi çevreleme, resim içine panel kurma, metin satırını boyama, tek cümleye birden çok konum işaretleme **yasak**. Tek cümle = tek çizim.
5. Kapı: `python3 scripts/cizim/cizim_kapisi.py <anahtar> --kok <veri kökü>` 0 HATA. HATA varsa çizimi gerçekten düzelt; kapıya dokunma.

## 7. Belirsizlik karar tablosu

| Durum | Yap |
|---|---|
| Alıntıyı sayfada bulamıyorum | Bilgiyi yazma; raporda "kaynakta yok" |
| Şekil etiketi okunmuyor | `belirsiz`; anlatma; çizme |
| İki sayfa çelişiyor | Çelişkiyi ikisini de alıntılayarak kullanıcıya bildir; birini seçme |
| Kapı bana haksız görünüyor | Kapıyı değiştirme; hatayı ve gerekçeni kullanıcıya yaz |
| Hedef tutmuyor | Hedefi değiştirme; yalnız sapan bölümü düzelt (sayısal ±%10, anlatım ±%20) |
| Kullanıcı talimatı belirsiz | Dur, sor |

## 8. Yayın (yalnız kullanıcı komutuyla, tüm kapılar 0 HATA iken)
1. `python3 -I scripts/tam_hat/dis_ajan_kapisi.py --ajan $E --ders $D` → GEÇTİ (sınav, hedef, izin kümesi).
2. `ders-ekle` isteği: `key: "$D-ag-$E"`, **`ajan: "$E"`**, `baslik: "<Başlık> [<Ajan> taslağı]"`, `metin`, `sayfalar`, `dosya`. Sunucu anahtarı kilitler (`yalniz-yonetici`); 409/400 gelirse dur.
3. `python3 -I scripts/tam_hat/dis_ajan_kapisi.py --ajan $E --ders $D --yayin --canli <adres>` → canlıda kilit + öğrenci isteğinde 403.

## 9. Bağımsız denetim
İsteğe bağlı (kullanıcı isterse). Asıl güvence §3'teki kanıt zinciri ve kapılardır.

## 10. Rapor şablonu (iş bitince, eksiksiz doldur)
- Anahtar, etiket, model, tarih. Durum: **yönetici onayı bekliyor**.
- Katman tablosu: yapıldı / atlandı + **neden** (atlanan hiçbir katman sessiz kalmaz).
- Kapı çıktıları (her kapının son satırı). Hedef-ölçüm tablosu (`hedef.py kontrol`).
- `belirsiz` bırakılan bilgiler, kaynakta bulunamayan istekler, çelişen sayfalar.
- Sorduğun ve cevap beklediğin sorular.

## 11. Dur ve sor listesi
PDF–ders eşlemesi belirsiz • aynı hata 3. kez • ortak dosyaya yazmak gerekiyor • sunucu 400/409 • görüntüyü okuyamıyorsun •
kaynak dışı bilgi eklemek zorunda kalıyorsun • kapı eşiğini değiştirmek aklına geldi • izinsiz LLM/API çağrısı gerekiyor •
kendi kapılarının hiçbiri hatayı göstermiyor ama içeriğin doğruluğundan emin değilsin.

## Hoca profili (2026-10-29, AGENTS.md madde 26)
Önem/anlatım/örnek soru yazmadan önce `docs/HOCA_USLUBU_YONTEMI.md` oku ve `python3 scripts/hoca_profili/profil_oku.py --ders "<ders>" --konu "<konu>"` çalıştır; örnek soruları `profil_kapisi.py` kapısından geçir. Kanıtsız satıra "önemli" deme.
