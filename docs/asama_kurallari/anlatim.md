# Aşama kuralları — anlatim

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 30 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

### H2 — Türkçeye uymayan ifade ve iç etiketler (2026-10-18)
- **Kurul 2'de doğrusu:** Doğal, eksiksiz, anlaşılır Türkçe; çeviri mecaz ve iç etiket yok; tam cümle.
  Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.
- **Kapı:** `meds/scripts/turkce_uslup.py` (liste her kalıbı yakalamaz; denetçi metni sesli okunuyormuş gibi okur).


- H4 — Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış") — betik denetler: `turkce_uslup.py`
- H9 — Görsel ya da bozuk OCR'lı sayfa içerikte yok — betik denetler: `denetle.py`
- H22 — Sesli derste dolgu ve asılsız "hoca vurguladı" cümleleri (kullanıcı kuralı, 2026-10-22, KALICI) — betik denetler: `scripts/uretim/sesli_anlatim/metin_denetle.py`
### H23 — Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin (İmmünofarmakoloji V2, kullanıcı, 2026-10-22)
- **Kural (kullanıcı tanımı):** sarı ya da mavi ÇAPRAZ şerit/çizgi = hoca okumadı (anlatılmaz); metin üzerindeki YATAY
  çizgi/vurgu = okundu; yıldız, daire, "önemli", "bil", ünlem, altı çizili = önemli. Öğrenci notlu PDF önce sayfa sayfa
  işaret dökümüne (okundu/okunmadı/önemli/el yazısı) çevrilir, metin dökümden yazılır.

### H24 — Kısa özet derste önemli yerler atlandı, slaytla ilişkisiz/kopuk anlatım (Patoloji V2, kullanıcı, 2026-10-23)
- **Kural:** kısa sürüm slayt sırasını izler; önem listesinin (`src/data/<branş>_onem/`) TAMAMI ve her çıkmış konu içinde
  anlatılır; konu ne → neden/nasıl → sınav ayrıntısı sırasıyla kapanmadan geçilmez; soru dili ve şık yankısı yasak; uzunluk
  V1'in %45–65'i ("çok kısalt" diye madde atma). Yazar + bağımsız denetçi (kapsama dökümü + kaynak karşılaştırması) zorunlu.

### H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)


### H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")


### H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)


### H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.



### H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.


### H112 · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram tanımsız, gen sembolü okunuşu çözülemedi (2026-10-27, k2-08)
- **Kural:** sesle okunan metinde aynı sözcük iki ayrı kavramı gösteriyorsa yazım ayrıştırılır; sayısal/ekzon gibi kavram ancak tanımından sonra kullanılır; "hoca da ... söyledi" yalnız slaytın vermediği ek bilgi ya da sınav vurgusu içerdiğinde yazılır.


### H127 · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi (2026-10-28, k2-05 Nörolojik Muayene, sayfa 32–33)
- **Kalıcı çözüm ve kural (`KURUL2_DERS_STANDARDI.md` §8.12, tam metin orada):** Şekil (çizim, şema, tablo, panel, ok/etiket) kaynaktır ve anlatılır. Deney/muayene görseli: ne sınanır, nasıl, normal, her patolojik panel ne demek, karıştırılan çift. Çok panelde her panel adlandırılıp karşılaştırılır; yalnız adı geçen test 1–2 cümleyle tanımlanır, uydurulmaz. Kaçamak meta cümle ("yorumuna girmez") ve yalnız betimlemeyle biten şekil paragrafı YASAK. Lazer/kontur anlatılan panele gider (bir cümle = bir panel); denetçi şekilli her sayfanın görüntüsüne bakar, eksik panel → GEÇMEZ.

### H434 — Sesli derste "bu hastalıkta" gibi adsız göndermeler hangi hastalığın kastedildiğini karıştırıyordu (2026-10-28, kullanıcı bildirdi)
- **Çözüm/kural:** Her yeni paragraf/bölüm hastalığı veya kavramı adıyla anar; adsız gönderme (bu hastalıkta/durumda/tümörde, burada, bunlarda…) parça başında yasak. `metin_denetle.py` BAGLAMSIZ kapısı HATA verir; KURUL2_DERS_STANDARDI §8.13 ve ANLATIM_KURGU_STANDARDI'na yazıldı. Denetçi her paragrafı tek başına okuyup konuyu çıkarabilmeli.


### H438 — Anlatım slaytın söylediğini tersine çevirdi (k2-01, 2026-10-29)
- **Çözüm/önleme:** cümle slayt ifadesine döndürüldü ("tanının doğru olduğunu göstermek için çekilir"), açıklama sonraki cümlede ("başka yapısal nedeni dışlamak"). Anlatım slayttaki hükmü yorumlayabilir ama **yönünü tersine çeviremez**; denetçi her sayfada slayt cümlesi ↔ anlatım cümlesi olumsuzluk kıyası yapar. Değişen cümlenin EMA klibi yeniden üretilmelidir.


### H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/uretim/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).

### H473 — Ders notu sadakati eşiğin altında: "Ek bilgi" etiketleri ve meta cümleler (2026-11-02)
- **Önleme:** Ders notu yalnız slayt bilgisinin redaksiyonudur; hoca açıklamaları sesli anlatımda ve hoca vurguları listesinde yer
  alır. Ders notunda süreç/meta cümlesi ("çıkmışta şu sorulmuştur", "slaytta yazılı değildir") yazılmaz.


### H477 — Asıl hoca derse girmediğinde sınav kaynağı (2026-11-03, Beyin ve Sinir Cerrahisi k2-12/13/14)
- **Kural:** sınavı hazırlayan hocanın slaytı tek kaynaktır (anlatım, soru, önem); derse giren hocanın slaytı/sesi yalnız önem ipucudur,
  metinde "hoca vurguladı" denmez, onun slaytında olup sınav hocasının slaytında olmayan bilgi eklenmez. Kullanıcının bildirdiği geçmiş
  sorudan slaytta karşılığı olmayan (servikal travmada immobilizasyon) anlatıma uydurulmaz, kullanıcıya bildirilir.


### H486
- **Önleme:** anlatım denetiminin `denetim.json` tıbbi bulguları ve `rapor.md` "slayt çelişkisi" listesi her sonraki katman yazarının istemine
  zorunlu girdi olarak konur; ders başına soru katmanı denetçisi (`GOREV_DENETCI_SORU_K2_B3.md`) bu listeyi tek tek arar.


### H488 — Slayt fotoğrafı ters yorumlandı: hipotonik bebek "tonus artışı" diye anlatıldı (k2-16 s.9, 2026-11-05)
- **Kural:** fotoğraf/klinik görünüm anlatan her cümlede yazar ve denetçi sayfa görüntüsüne bakar; görsel yorumu hoca dökümüyle çelişirse hoca + görüntü kazanır, envanter tanımı tek başına dayanak değildir. Denetçi yönergesine "görsel–anlatım yön kontrolü (artış/azalma, sağ/sol, normal/patolojik)" maddesi eklenir.


### H512 — Anlatım parçalara bölünerek yazdırılınca ara resim adımı düştü (k2-21)
- **Önleme:** B1 bölünürse ara resim ayrı bir alt görev olarak MUTLAKA açılır; yayın öncesi kontrol listesinde `python3 scripts/uretim/ara_resim/dogrula.py <key>` çalıştırılır ve `src/data/ara_resim/<key>.json` yoksa ders tamamlandı sayılmaz.


### H531 — Hoca sesi sonradan gelen yayımlanmış derste anlatım baştan yazılmaz; kısmi revizyon ve tekrar dolgusu tuzağı (2026-11-10)
- **Çözüm/önleme:** Akış: A1b (ses_hizasi + hoca_vurgulari + "Anlatıma eklenecekler") → `yayinla.py kimlik` → yalnız var olan paragraflara ekleme (yeni paragraf/silme/sıra değişikliği yok) → birleştirme sonrası eski kimlikleri metinle geri yazma (`meds_temp/ogrenci_ders/k2-58/is/hoca_rev.py kimlik`) → bağımsız denetçi (yalnız değişen cümleler) → `yayin_hazirla_destesiz.sh` → `klip_tasi.py <key> --eski <eski.md>` → `sesli_yayinla.py` (EMA yalnız değişen klipleri üretir: 4–9 klip) → Oracle `meds-cumle-zaman` + `meds-kelime-zaman-hat`. `hoca` alanına yalnız `tur: sinav` bağlanır (`yayinla.py yaz` dogrulaması HATA verir); bilgiyi tekrar eden vurgu cümlesi yazılmaz, yalnız alan bağlanır; hocanın "sınavda çıkar" demesi doğrulanmış çıkmış değildir.



### H607 — Arşiv metin üretimi görsel/şema sayfalarında "yanıt yok" verip sayfayı anlatımsız bırakıyordu; ders yayına giremiyordu (2026-11-17)
- **Önleme kuralı:** Üretim adımı yayın kapısı denetimlerini kendi içinde koşmadan "0 HATA" demez; boş yanıt = yeniden dene + kısa istem; yazısız görselde yalnız bölüm/komşu başlık bağlamı, kaynak dışı bilgi yok.


### H628 — Ders analizi: ham iç etiketler sesli okundu, kanıtsız "hoca en çok soruyor" 43 derste yayındaydı (2026-11-18)
- **Kural:** Ders analizinde "hoca …" iddiası yalnız doğrulanmış kanıtla yazılır; ses alanında iç etiket, ham anahtar ve rakam bulunmaz; üreticiyi değiştirince `uret.py --dogrula` bütün derslerde koşulur.


### H642 — Ekleme tabanlı anlatım revizyonunda klip_tasi katmanları boşaltıyor, 6000 kelime tavanı zenginleştirmeyi kesiyor (2026-11-21, k2-46)
- **Kural:** Ekleme tabanlı revizyonda (H531) sıra: anlık görüntü → ekleme → `klip_tasi` → katmanları kimlikle geri yaz → vurgu türet → kapılar. 60+ sayfalı derste `MEDS_METIN_MAX_W` hat ve yayın komutlarında aynı değerle verilir. Kalıcı kod düzeltmesi (2026-11-23): `klip_tasi.py` yalnız cümle eklenmiş paragrafı (`cumle_esle`: eski cümleler aynen + aynı sırada) cümle düzeyinde taşır; gerçek tur verisinde (k2-58/21/41) elle kimlikle geri yazımla 1.031/1.031 çapa ve 40/40 çıkmış konumu birebir aynı çıktı. Elle `rev.py` geri yazımı artık gerekmez; eklenen cümleye yalnız sayfa çapası konur, madde/resim çapası ayrıca yazılır.


### H643 — Farmakoloji zenginleştirme turu: çıkmış rozetleri hiç görünmüyordu, eski çalışma klasörü yeni metni ezdi (2026-11-22)
- **Kural:** Yayından önce `curl /api/canli-ders/<key>` `cikmisKonum` sayısı `cikmis_konum` dosyasındaki soru sayısıyla (karantina hariç) karşılaştırılır; `null` ise ders tamamlanmış sayılmaz. `sesli_yayinla.py --v2` klasöründeki `konusma_metni.md` kelime sayısı yerel `metin/<key>.md` ile aynı olmadan çalıştırılmaz. `kos.py anlatim` metin kapısı `--yazim` kipiyle hizalanacak (açık iş).

### H644 — Basit dilli V2 sürümlerinde denetçinin en sık yakaladığı üç hata: tekrar eden ek cümle, aralığı tek sayıya indirme, İngilizce harf okunuşu (2026-11-22, psikiyatri 16 ders)
- **Kural:** Basit dil sürümünde ek cümle önceki cümleyi yinelemez; aralık iki sınırıyla aktarılır, örnek sayı uydurulmaz; kaynağın söylemediği neden kurulmaz; kısaltma Türkçe okunur (di es em). V1 cümlesi aynen kalırsa çizimi `cizim_tasi.py` taşır.


### H645 · PDF işareti "yalnız sayfa"ya düşüyordu (2026-11-23)
- **Kural:** Eklenen açıklama cümlesi açıkladığı slayt satırına çapalanır; boş `satir` bırakılmaz. Tablo çapasına satır da yazılır.


### H667 · Üç Kurul 2 psikiyatri dersinde metin vurgusu neredeyse yoktu (2026-11-25)
- **Kural:** Kurul 2+ derste cümlelerin en az ~%40'ı `vurgu` taşımalı; `metin` `ses` içinde birebir geçmeli (okunuşu farklı kısaltmada ses biçimi: "Viski ar"). Yayından önce vurgulu paragraf oranı denetlenir.


### H683 — Anlatımda bir sayfanın bütün cümleleri tek cümleyle ezildi, kapı geçti (2026-11-25, k2-59 p015)
- **Kural:** Toplu düzeltme betiği tek kayda uyan anahtarla (cümle kimliği) değiştirir; önek/kalıp eşlemesiyle toplu ezme yapılmaz. Kapı geçse de denetçi aşaması atlanmaz.

