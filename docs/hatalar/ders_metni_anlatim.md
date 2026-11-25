# Hata defteri — ders_metni_anlatim (anlatım metni, slayt sadakati, öğrenci denetçisi)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16; `hatalar/ders_metni.md` 3 konuya bölündü). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H2 — Türkçeye uymayan ifade ve iç etiketler (2026-10-18)

- **Görülen:** Sınav asistanı (Patoloji 08, "IL-6: karaciğerde akut faz yanıtı"): "IL-6 … salınır; **imzası** karaciğerde akut
  faz yanıtını uyarmaktır." ve "**Ayrım cümlesi:** ateşte IL-1 daha belirgin, akut fazda IL-6, nötrofil alımında IL-17."
- **Neden hata:** "imzası" İngilizceden çeviri mecaz; "Ayrım cümlesi:" yazarın iç etiketi, öğrenci anlamıyor. Metin EMA ile okunduğu
  için doğal olmayan cümle dinlerken daha da kötü duyulur.
- **Kurul 2'de doğrusu:** Doğal, eksiksiz, anlaşılır Türkçe; çeviri mecaz ve iç etiket yok; tam cümle.
  Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.
- **Kapı:** `meds/scripts/turkce_uslup.py` (liste her kalıbı yakalamaz; denetçi metni sesli okunuyormuş gibi okur).

### H4 — Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış")
- **Kök:** yazar ajan kendi notunu öğrenci metnine bırakıyor.
- **Kapı — EKLENDİ:** `turkce_uslup.py` kalıpları (Kurul 2+ HATA). **"Doğrusu: …" yasak DEĞİL**: şık açıklaması standardının parçası. "ajan" tıbbi terimdir.

### H9 — Görsel ya da bozuk OCR'lı sayfa içerikte yok
- **Kural:** metni zayıf sayfa görüntüden okunur; sayfa kapsaması ölçülür.
- **Kapı — EKLENDİ:** işçi denetleyicisi zaten her sayfayı haritada, her içerik sayfasını bir adım + bilgi maddesinde ve
  şekil/tablo sayfasını açıklamalı istiyor (%100 kapsama). Eklenen: görsel ağırlıklı ya da hoca vurgulu (≥3 renkli/kalın)
  sayfa "boş/kapak" diye atlanamaz (s.1–2 kapak muaf) — `denetle.py`, 2026-10-20.

### H22 — Sesli derste dolgu ve asılsız "hoca vurguladı" cümleleri (kullanıcı kuralı, 2026-10-22, KALICI)
- **Belirti:** K1 sesli derslerinde "hoca bunu ayrıca vurgulamıştır", "hocanın altını çizdiği nokta şudur" gibi dayanaksız,
  sürekli tekrar eden meta cümleler; kelime/dakika sınırına ulaşmak için eklenen, dersi uzatıp bağlamdan koparan dolgu.
- **Kural:** Amaç bilgiyi en kısa yoldan, doğru, açıklayıcı ve eksiksiz iletmek. Kelime alt sınırı ve süre hedef DEĞİLDİR;
  kısa ama eksiksiz metin doğrudur. Önem vurgusu yalnız dayanağı varsa (çıkmış soru, öğrenci notu, slayttaki işaret) ve
  kritik noktada yapılır; dayanağı yazılmadan "hoca vurguladı/işaretledi/altını çizdi" denmez. Tekrar, geçiş ve özet
  dolgusu ("şimdi gelelim", "bir kez daha hatırlatalım", "daha önce de söylediğimiz gibi") yasak.
- **Kapı — EKLENDİ:** `scripts/uretim/sesli_anlatim/metin_denetle.py` → `DOLGU` kalıpları HATA; "Burası önemli/çok önemli/sınavda
  sık" bölüm sayısının yarısını (en az 3) aşarsa HATA; kelime alt sınırı artık yalnız uyarı. K1 metinlerine toplu müdahale yok.

### H23 — Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin (İmmünofarmakoloji V2, kullanıcı, 2026-10-22)
- **Belirti:** İşaretli PDF'te sarı vurguların hepsi "işlendi" sayıldı, çapraz sarı şeritler kaçırıldı; metin "ce de iki" gibi
  okunuşla yazıldı; anlatım kopuk ve hızlıydı.
- **Kural (kullanıcı tanımı):** sarı ya da mavi ÇAPRAZ şerit/çizgi = hoca okumadı (anlatılmaz); metin üzerindeki YATAY
  çizgi/vurgu = okundu; yıldız, daire, "önemli", "bil", ünlem, altı çizili = önemli. Öğrenci notlu PDF önce sayfa sayfa
  işaret dökümüne (okundu/okunmadı/önemli/el yazısı) çevrilir, metin dökümden yazılır.
- **Yazım:** konuşma metni kısaltmaları yazımla tutar (CD2, IL-2); okunuşu EMA katmanı yapar (`modul_okunus.py`
  MODUL_ANAHTARLAR / Kurul 2+ uzun kısaltma yolu). Sayı, Yunan harfi ve simge yazıyla.
- **Anlatım:** akıcı, bağlantılı (ne → nasıl → nerede → yan etki); kısa kopuk cümle dizisi yasak.

### H24 — Kısa özet derste önemli yerler atlandı, slaytla ilişkisiz/kopuk anlatım (Patoloji V2, kullanıcı, 2026-10-23)
- **Belirti:** "%50 kısa" hedefli V2'lerde önem maddeleri ve çıkmış bilgileri atlandı; paragraflarda çıkmıştan koparılmış tek
  cümleler ("çıkmış soruda doğru önerme…", "… değildir" diye şık sayma), konu ortasında başka konudan bilgi; bir slayttan tek
  satır okunup başlığı bile açıklanmadan başka konuya geçildi.
- **Kural:** kısa sürüm slayt sırasını izler; önem listesinin (`src/data/<branş>_onem/`) TAMAMI ve her çıkmış konu içinde
  anlatılır; konu ne → neden/nasıl → sınav ayrıntısı sırasıyla kapanmadan geçilmez; soru dili ve şık yankısı yasak; uzunluk
  V1'in %45–65'i ("çok kısalt" diye madde atma). Yazar + bağımsız denetçi (kapsama dökümü + kaynak karşılaştırması) zorunlu.
- **Uygulama:** `meds_temp/sesli_anlatim/v3_pat/{TALIMAT,DENETIM}.md`, blok için `meds_temp/blok_ozet_v2/EK_V2.md`.
- **Ek tuzaklar:** ders–PDF eşlemesi içerikle doğrulanır (k1-65 Meme Kanseri Öğren destesi 33) Benign PDF'ine bağlıydı →
  sesli V2/V3 sanal deste `k1p-k1-65-…-sesli-v2`); kitte slayt metni yoksa (k1-66) PDF metni ayrıca verilir.

## H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)
- Gemini Flash-Lite bazı çözücü partilerini ve bir sesli bölümü baştan sona harfsiz yazdı ("dogum", "bagli", "oykusu");
  hiçbir kapı yakalamadı, partiler KABUL edildi (önceki e07 çözücü ve k1-64 sesli sınamalarında da vardı; yalnız geçici kopya).
- Ortak kapı `cekirdek.turkce_katlama`: sözlük paketin kendi girdisinden; girdide Türkçe harfle geçen kelimenin katlanmış
  biçimi ≥3 kelimelik bir alanda ≥2 kez varsa HATA (İngilizce alıntı, kimlik/tür alanı, büyük harfli OCR yanlış alarm vermez).
- Kabul edilmiş iş yeniden kullanılırken `yonlendir.kapi` ile güncel kapılardan geçirilir; geçemezse "yeniden" koşar.
- Betik onarımı `cekirdek.ses_onar` (SES_ONAR görevleri): ses alanlarında kısaltma/Roma rakamı `modul_okunus.donustur`
  ile ("MSH" → "mee see haa"); modelin üç turda düzeltemediği "büyük harfli kısaltma" hatası kalktı.
- Öncüllü soruda "kökle uzunluk uyumsuz" hatasına düzeltme ipucu eklendi (kok_ses öncüllerin hepsini okur).

## H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")
- k2-02'de 56 içerik sayfasının 12'si anlatılmamış, 19 sayfa tek cümleyle geçilmişti; "kısa ve öz" + paralel üretimde kapı yoktu.
  Kapı `isle.sesli_kapsam` (sayfa + derinlik). Kelime/dakika hedefi YOK; derinlik bilgi maddesi sayısından.

## H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)
- Bütün betik kapıları 0 HATA iken bağımsız tıbbi denetim (PDF ile satır satır) buldu:
  - s.63 Tablo 25.3 (görüntü): droperidol premedikasyon/sedasyon/antiemetik dozları **midazolama** yazılmış; kart, soru,
    checkpoint ve sesli metne yayılmış. Aynı tablonun opioid yarısı atlanmış.
  - s.6 "en zayıf desfluran" ↔ s.13 Tablo 25.1 MAK azot protoksit >100: iki zıt cevap öğretiliyordu. Kural: hocanın
    çelişkisi tek cümlede uzlaştırılır (halojenli uçucular içinde desfluran; tüm inhalerler içinde N₂O), kesin spot yapılmaz.
  - Tablodaki 0 değeri "seyrek" diye okunmuş (midazolam bradikardi); "(Katzung)", "standart kaynaklara göre" ekleri sızmış.
- Kural: Kurul 2+ her derste yayından önce PDF'le karşılaştıran bağımsız tıbbi denetim (ayrı oturum, yazar ≠ denetçi)
  zorunlu; görsel tablo satırı ilaç/değer eşlemesi görüntüden tek tek doğrulanır. Bulgular düzeltilip kapılar yeniden koşulur.

## H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Belirti:** Kullanıcı uyarısı: *"Son eklenen dersler hep eksik anlatılmış içeriklerinin neredeyse %60'ı yok"*. 37 sayfalık amfi dersi yalnızca 74 cümle ve 839 kelime (~6.7 dakika) ile geçiştirilmiş; slaytlardaki kimyasal gruplar, spesifik formülasyonlar (Anestol, EMLA, Jetex, Lidestol, Lincaine, LMX-4, Vemcaine), subkutan maksimum doz tablosu (Ultrakain, Citanest, Marcaine, Naropin), potens katsayıları (tetrakain/bupivakain 16 kat), difüzyon ve iyonizasyon eğrileri (pKa 7.9 lidokain vs 8.1 bupivakain), toksisite basamakları, diazepam premedikasyonu ve %20 intravenöz lipid emülsiyon protokolü sesli anlatımda yer almamıştı.
- **Kök neden:** Taslak ve sesli metin üretiminde sayfa başına mekanik olarak tam 2 kısa cümle yazan bir şablon kullanılmış; bu şablon kapıların asgari kelime/sayfa şartlarını yüzeysel olarak karşılasa da gerçek amfi anlatımının %60–75'ini dışarıda bırakmıştı.
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.


## H112 · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram tanımsız, gen sembolü okunuşu çözülemedi (2026-10-27, k2-08)
- **Belirti:** bağımsız denetçi tur 1 KALIR: "tip bir kollajen" ile "osteogenezis imperfekta tip bir" aynı sesle okunup karışıyor; distrofinin işlevi ve "okuma çerçevesi" anlatılmadan ekzon rakamları verilmiş; sklerotom/dermatom/miyotom türevsiz; kraniyoraşizis tanımı anensefaliyle çakışıyor; WT1 "çifte ve te bir" çözülemedi; "Hoca da ... söyledi" onaylama cümleleri bilgi taşımayıp dolgu hissi veriyor.
- **Kök neden:** slayt satırı sırasıyla yazılırken ses dinleyicisinin görmediği ayrım (tip/tür) ve kilit kavramın önceden tanımı atlandı; Hoca atfı "her yerde ekleyelim" refleksiyle kuruldu.
- **Çözüm:** kollajen için "birinci/üçüncü tür", hastalık için "birinci tip" kullanıldı; okuma çerçevesi ve distrofin işlevi kısaca tanımlandı; somit türevleri, kraniyoraşizis tanımı düzeltildi; W harfi "duble ve" okunur; yalnız yeni bilgi (ayırt edici vurgu, klinik örnek, tedavi) taşıyan hoca atıfları kaldı. Tur 2 GEÇER (%90 yanıtlanabilirlik).
- **Kural:** sesle okunan metinde aynı sözcük iki ayrı kavramı gösteriyorsa yazım ayrıştırılır; sayısal/ekzon gibi kavram ancak tanımından sonra kullanılır; "hoca da ... söyledi" yalnız slaytın vermediği ek bilgi ya da sınav vurgusu içerdiğinde yazılır.

## H127 · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi (2026-10-28, k2-05 Nörolojik Muayene, sayfa 32–33)
- **Belirti:** VIII. sinir slaytında Rinne/Weber diyapazon çizimleri (mastoid → kulak önü; verteks + normal / iletim tipi / sensörinöral üç panel) vardı. Anlatım "Bu çizimde testlerin nasıl uygulandığı gösterilir" deyip geçti; testin neden yapıldığı, hangi panelin hangi sonucu gösterdiği söylenmedi. Önceki paragraf "ders bunların nasıl yorumlandığına girmez, yalnız adlarını verir" dedi.
- **Kök neden:** yazar "kaynak dışı bilgi yasak" kuralını yalnız slayt YAZISINA uyguladı; şekil, çizim, fotoğraf ve tablodaki bilgiyi kaynak saymadı. Yazıda yorum olmayınca çizimdeki normal/patolojik ayrımı da "kaynakta yok" diye atladı ve boşluğu meta cümleyle kapattı. Kapılar (metin_denetle, turkce_uslup, denetçi) bu kaçamak cümleyi yakalamıyordu; denetçi slayta bakmadan okuduğu için şeklin anlatılmadığını göremedi.
- **Kalıcı çözüm ve kural (`KURUL2_DERS_STANDARDI.md` §8.12, tam metin orada):** Şekil (çizim, şema, tablo, panel, ok/etiket) kaynaktır ve anlatılır. Deney/muayene görseli: ne sınanır, nasıl, normal, her patolojik panel ne demek, karıştırılan çift. Çok panelde her panel adlandırılıp karşılaştırılır; yalnız adı geçen test 1–2 cümleyle tanımlanır, uydurulmaz. Kaçamak meta cümle ("yorumuna girmez") ve yalnız betimlemeyle biten şekil paragrafı YASAK. Lazer/kontur anlatılan panele gider (bir cümle = bir panel); denetçi şekilli her sayfanın görüntüsüne bakar, eksik panel → GEÇMEZ.
- **Otomatik kapı:** `metin_denetle.py` kaçamak meta cümleyi HATA sayar (`KACAMAK` kalıpları); yalnız betimleme cümlelerinden oluşan kısa şekil paragrafını UYARI olarak gösterir.
- **Uygulama:** k2-05 v1 korunur; `k2-05-norolojik-muayene-v2` klipli ses + taşınan katmanlarla yeniden kuruldu, 31–32. paragraflar bu kurala göre yeniden yazıldı.

## H434 — Sesli derste "bu hastalıkta" gibi adsız göndermeler hangi hastalığın kastedildiğini karıştırıyordu (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Yeni parçaya geçildiğinde "bu hastalıkta…" diye başlayan cümlelerde öğrenci, derste birden çok hastalık anlatıldığı için hangisinden söz edildiğini kaçırıyordu.
- **Kök neden:** Yazım yalnız yazıyı okuyan biri için akıcıydı; gönderme önceki cümleye bağlı. Sesli dinlemede parça sınırında bağlam kopuyor, kapılar bu kalıbı denetlemiyordu.
- **Çözüm/kural:** Her yeni paragraf/bölüm hastalığı veya kavramı adıyla anar; adsız gönderme (bu hastalıkta/durumda/tümörde, burada, bunlarda…) parça başında yasak. `metin_denetle.py` BAGLAMSIZ kapısı HATA verir; KURUL2_DERS_STANDARDI §8.13 ve ANLATIM_KURGU_STANDARDI'na yazıldı. Denetçi her paragrafı tek başına okuyup konuyu çıkarabilmeli.

## H438 — Anlatım slaytın söylediğini tersine çevirdi (k2-01, 2026-10-29)
- **Belirti:** s.4 slaytı "BT, MR tanının doğru olduğunu göstermek için çekilir" derken anlatım "BT ve MR bu hastalıkları doğrulamak için çekilmez" dedi; öğrenci çelişki gördü.
- **Kök neden:** yazar "yapısal nedeni dışlamak" yorumunu öne çıkarırken slayt cümlesini olumsuza çevirdi; denetçi slayt satırıyla anlatım cümlesinin yönünü (olumlu/olumsuz) kıyaslamadı.
- **Çözüm/önleme:** cümle slayt ifadesine döndürüldü ("tanının doğru olduğunu göstermek için çekilir"), açıklama sonraki cümlede ("başka yapısal nedeni dışlamak"). Anlatım slayttaki hükmü yorumlayabilir ama **yönünü tersine çeviremez**; denetçi her sayfada slayt cümlesi ↔ anlatım cümlesi olumsuzluk kıyası yapar. Değişen cümlenin EMA klibi yeniden üretilmelidir.

## H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Belirti:** k2-05 Nörolojik Muayene anlatımında "Spastisite ve rijidite kas tonusunun artmasıdır; ders ikisini yalnız adlarıyla sayar."
  Oysa 2025-26 öğrenci notunda rijidite = "agonist ve antagonist kaslarda birlikte tonus artışı" (el notu + yıldız) ve çıkmışta tam bu
  soruldu; 2. motor nöronda fasikülasyon, spastisite = 1. motor nöron, intensiyonel tremor da notta işaretli/çıkmışta var, anlatımda yok.
- **Kök neden:** işçi önemi yalnız bu yılın slayt metni + çıkmış eşlemesinden kuruyordu; slaytta yalnız adı geçen kavramın hocanın derste
  verdiği ve öğrencinin not ettiği tanımı kaynak sayılmıyordu. Geçmiş yıl öğrenci derlemeleri (hangi yer çalışıldı, hangi soru yapıştırıldı)
  hatta hiç girmiyordu; kapsam kapıları konu düzeyinde ölçtüğü için "rijidite" sözcüğünün geçmesini kapsam sandı.
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/uretim/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).
- **Ek (2026-10-30, kapı):** `kapi.py` ilk sürümü sesli metni (okunuşla: "Düşen", "müsküler") yazılı çıkmışla ("Duchenne muskuler")
  karşılaştırıp anlatılmış bilgiyi "yok" sayıyordu (k2-08). Çözüm: v2 `ekran` maddeleri (yazımla) da aday cümledir. Önleme: sesli metinle
  yazılı kaynağı karşılaştıran her kapı ekran/yazım katmanını da okur; kapıyı geçmek için sesli metin yazıma çevrilmez (H23).

## H473 — Ders notu sadakati eşiğin altında: "Ek bilgi" etiketleri ve meta cümleler (2026-11-02)

- **Belirti:** k2-10 yayını "ders notu sadakati 0.757 < 0.8" ile reddedildi.
- **Kök neden:** Ders notu yazarı slayt dışı hoca açıklamalarını "Ek bilgi:" etiketleriyle ve "Çıkmış sorularda … cevabıdır;
  çeldiriciler …" gibi süreç cümleleriyle ekledi; sadakat ölçütü (s14.fidelity: not köklerinin slaytta geçme oranı) bunları kaynak
  dışı sayar. Kısa (26 sayfa) slaytta oran hızla düşer.
- **Çözüm:** etiketler ve meta cümleler kaldırıldı, anekdotlar kısaltıldı, slayt sözcükleri kullanıldı → 0.855 (eşik gevşetilmedi).
- **Önleme:** Ders notu yalnız slayt bilgisinin redaksiyonudur; hoca açıklamaları sesli anlatımda ve hoca vurguları listesinde yer
  alır. Ders notunda süreç/meta cümlesi ("çıkmışta şu sorulmuştur", "slaytta yazılı değildir") yazılmaz.

## H477 — Asıl hoca derse girmediğinde sınav kaynağı (2026-11-03, Beyin ve Sinir Cerrahisi k2-12/13/14)
- **Durum:** derse başka hoca (Zeynep) kendi slaytlarıyla girdi; sınavı asıl hoca (Sinan Apaydın) kendi slaytlarından hazırlıyor.
- **Kural:** sınavı hazırlayan hocanın slaytı tek kaynaktır (anlatım, soru, önem); derse giren hocanın slaytı/sesi yalnız önem ipucudur,
  metinde "hoca vurguladı" denmez, onun slaytında olup sınav hocasının slaytında olmayan bilgi eklenmez. Kullanıcının bildirdiği geçmiş
  sorudan slaytta karşılığı olmayan (servikal travmada immobilizasyon) anlatıma uydurulmaz, kullanıcıya bildirilir.

## H486
- **Belirti (2026-11-04):** k2-07 (genel anestezik) anlatımı ve örnek soruları bağımsız denetimde KALIR: remifentanil "plazma kolinesterazıyla"
  yıkılıyor, sugammadex için iki farklı derin blok dozu, süksinilkolin "asetilkolin reseptörünü taklit eder", sugammadex reseptör antagonisti gibi.
  k2-15'te önem yazarı anlatımda zaten ayıklanmış çelişkili slayt satırından ("kısa psikotikte takipte çoğunlukla şizofreni") madde ve soru kurdu.
- **Kök neden:** yazar slayttaki yanlış/çelişkili satırı (s34 remifentanil, s48–s56 doz, s45 kısa psikotik) olduğu gibi aktardı; anlatım
  denetiminde düzeltilen hata listesi sonraki katmanların (soru, önem, çözücü) yazarlarına verilmedi.
- **Çözüm:** anlatım düzeltildi + yeniden denetim GEÇER; örnek sorularda 6 ifade düzeltildi; k2-15 önem/çözücü maddesi yeniden yazıldı.
- **Önleme:** anlatım denetiminin `denetim.json` tıbbi bulguları ve `rapor.md` "slayt çelişkisi" listesi her sonraki katman yazarının istemine
  zorunlu girdi olarak konur; ders başına soru katmanı denetçisi (`GOREV_DENETCI_SORU_K2_B3.md`) bu listeyi tek tek arar.

## H488 — Slayt fotoğrafı ters yorumlandı: hipotonik bebek "tonus artışı" diye anlatıldı (k2-16 s.9, 2026-11-05)
- **Belirti:** sesli derste "Slayttaki fotoğraflarda tonus artışının görünümü vardır: bükülü ekstremitelerle yatan bir bebek…" cümlesi; fotoğraf aslında karın üstünden tutulunca sarkan (gevşek) bebek = hipotoni. Hoca kaydı da "tonus azsa hipotonik bebek" diyor.
- **Kök neden:** A1a sayfa envanterinde `gorsel_aciklama` görüntü tahminle yazıldı ("fleksiyon postüründe bebek, spastik tutum örnekleri"); anlatım yazarı ve çapa bu tanımı slayta yeniden BAKMADAN kullandı; anlatım denetçisi görseli hoca dökümüyle karşılaştırmadı. Yanlışı ancak çizim ajanı fotoğrafa kontur çizerken gördü.
- **Çözüm:** cümle, ekran, çapa `sekil`, envanter tanımı düzeltildi; kısmi yeniden yayın (değişen paragraf EMA + cümle/kelime zamanı + çapa/çizim).
- **Kural:** fotoğraf/klinik görünüm anlatan her cümlede yazar ve denetçi sayfa görüntüsüne bakar; görsel yorumu hoca dökümüyle çelişirse hoca + görüntü kazanır, envanter tanımı tek başına dayanak değildir. Denetçi yönergesine "görsel–anlatım yön kontrolü (artış/azalma, sağ/sol, normal/patolojik)" maddesi eklenir.

### H512 — Anlatım parçalara bölünerek yazdırılınca ara resim adımı düştü (k2-21)
- **Belirti:** Kullanıcı: "hipnotik dersinde neden ara resim yok?" — k2-21 sesli derste hiç ara resim yoktu.
- **Kök neden:** k2-21 anlatımı güvenlik filtresine takıldığı için B1 görevi (anlatım + ara resim tek ajan) yerine sayfa aralıklarına bölünmüş üç ajana yalnız anlatım yazdırıldı; koordinatör ara resim adımını parçalara vermedi ve yayın öncesi `ara_resim/dogrula.py` çalıştırılmadı.
- **Kalıcı çözüm:** Ara resimler v2 yayımlandıktan sonra ayrı adımda üretildi (paragraf dizini yayındaki v2'den).
- **Önleme:** B1 bölünürse ara resim ayrı bir alt görev olarak MUTLAKA açılır; yayın öncesi kontrol listesinde `python3 scripts/uretim/ara_resim/dogrula.py <key>` çalıştırılır ve `src/data/ara_resim/<key>.json` yoksa ders tamamlandı sayılmaz.

### H531 — Hoca sesi sonradan gelen yayımlanmış derste anlatım baştan yazılmaz; kısmi revizyon ve tekrar dolgusu tuzağı (2026-11-10)
- **Belirti:** Dört ders "hoca sesi yok" diye yayımlanıp EMA'lanmışken ses geldi. İlk revizyonda yazar ajanlar (k2-58, k2-22) bilgiyi zaten veren cümlenin ardından "Hoca bunu da saydı/tekrar etti" cümlesi ekledi; k2-58'de doğrulanmış çıkmışı olmayan fetal alkol sendromu için "sınavda soruldu" dendi; k2-24'te bozuk dökümdeki "okuyla" sözcüğü "görme yolları" diye tahmin edildi; k2-23/k2-58'de `tur: anlatim` kaydı uydurma kategoriyle `hoca` alanına bağlandı.
- **Kök neden:** "hoca katmanını ekle" görevi vurgu cümlesini amaç sanıyor; `hoca` alanının yalnız sınav vurgusu için olduğu ve dayanaksız/yinelenen vurgu cümlesinin H22 dolgusu sayıldığı istemde yoktu. `v2_birlestir.py` cümle kimliklerini her koşuda sıfırdan numaralıyor; kimlik korunmazsa klip/çapa/çıkmış bağları kayar.
- **Çözüm/önleme:** Akış: A1b (ses_hizasi + hoca_vurgulari + "Anlatıma eklenecekler") → `yayinla.py kimlik` → yalnız var olan paragraflara ekleme (yeni paragraf/silme/sıra değişikliği yok) → birleştirme sonrası eski kimlikleri metinle geri yazma (`meds_temp/ogrenci_ders/k2-58/is/hoca_rev.py kimlik`) → bağımsız denetçi (yalnız değişen cümleler) → `yayin_hazirla_destesiz.sh` → `klip_tasi.py <key> --eski <eski.md>` → `sesli_yayinla.py` (EMA yalnız değişen klipleri üretir: 4–9 klip) → Oracle `meds-cumle-zaman` + `meds-kelime-zaman-hat`. `hoca` alanına yalnız `tur: sinav` bağlanır (`yayinla.py yaz` dogrulaması HATA verir); bilgiyi tekrar eden vurgu cümlesi yazılmaz, yalnız alan bağlanır; hocanın "sınavda çıkar" demesi doğrulanmış çıkmış değildir.


### H628 — Ders analizi: ham iç etiketler sesli okundu, kanıtsız "hoca en çok soruyor" 43 derste yayındaydı (2026-11-18)

- **Belirti:** `ders_analizi/k2-35.json` ve `k2-36.json` ses alanlarında "Tanım: Atom: k2-36-a01." okunuyordu; k2-20/k2-40'ta ham profil anahtarı ("ilac_yan_etki"); 43 derste "…ayrı not et; hoca en çok bunu soruyor." cümlesi vardı.
- **Kök neden:** Üretici (`uret.py`) paket başvurusunu atom metnine çevirmiyor, odağı dal profilinden alıp kanıtsız hoca iddiası ekliyor ve `--dogrula` bunları yakalamıyordu.
- **Çözüm:** Üretici düzeltildi (atom metni, ham çıkmıştan öncül/olumsuz sayımı, kesik cümle ve iç etiket kapısı, sürüm 2); yayındaki 43 dosyadan kanıtsız cümle çıkarıldı, k2-35/k2-20/k2-40 onarıldı; `--dogrula` tüm derslerde 0 HATA.
- **Kural:** Ders analizinde "hoca …" iddiası yalnız doğrulanmış kanıtla yazılır; ses alanında iç etiket, ham anahtar ve rakam bulunmaz; üreticiyi değiştirince `uret.py --dogrula` bütün derslerde koşulur.

### H642 — Ekleme tabanlı anlatım revizyonunda klip_tasi katmanları boşaltıyor, 6000 kelime tavanı zenginleştirmeyi kesiyor (2026-11-21, k2-46)

- **Belirti:** k2-46 Sempatomimetikler'e paragraf içi 68 cümle eklenince `klip_tasi.py` değişen 49 paragrafın çapa/çizim/hizalama/vurgu/çıkmış konum kaydını boşalttı (hizalamaya önceki sayfa `guven 0`); `metin_denetle.py` 6384 kelimede "kelime > 6000" HATA verdi; `klip_tasi`'den önce yazılan vurgu katmanı silindi.
- **Kök neden:** `klip_tasi.py` paragrafı yalnız metni birebir aynıysa taşıyor, cümle kimliğine bakmıyor. `metin_denetle` tavanı sayfa sayısından bağımsız 6000 (H618 değişkeni hat dışında verilmiyor). Vurgu dizini eski metne göre denetleniyor.
- **Çözüm:** Katmanlar revizyon öncesi anlık görüntüden cümle kimliğiyle geri yazıldı (`meds_temp/ogrenci_ders/k2-46/is/rev.py`); kapılar `MEDS_METIN_MAX_W=<sayfa×140>` ile koşuldu (eşik gevşetilmedi, H618 formülü); vurgu `klip_tasi` sonrası `KV.vurgu_turet` ile.
- **Kural:** Ekleme tabanlı revizyonda (H531) sıra: anlık görüntü → ekleme → `klip_tasi` → katmanları kimlikle geri yaz → vurgu türet → kapılar. 60+ sayfalı derste `MEDS_METIN_MAX_W` hat ve yayın komutlarında aynı değerle verilir. Kalıcı kod düzeltmesi (2026-11-23): `klip_tasi.py` yalnız cümle eklenmiş paragrafı (`cumle_esle`: eski cümleler aynen + aynı sırada) cümle düzeyinde taşır; gerçek tur verisinde (k2-58/21/41) elle kimlikle geri yazımla 1.031/1.031 çapa ve 40/40 çıkmış konumu birebir aynı çıktı. Elle `rev.py` geri yazımı artık gerekmez; eklenen cümleye yalnız sayfa çapası konur, madde/resim çapası ayrıca yazılır.

### H643 — Farmakoloji zenginleştirme turu: çıkmış rozetleri hiç görünmüyordu, eski çalışma klasörü yeni metni ezdi (2026-11-22)

- **Belirti:** (1) k2-33, k2-39, k2-41'de `cikmis_konum` dosyasında `p/c/metinHash` yoktu; canlı derste 19+17+10 doğrulanmış çıkmış rozeti hiç görünmüyordu. (2) k2-39 yayınında `sesli_yayinla.py` eski `anlatim/v2/` klasörünü okudu; yeni metin `is/v2dizin/`'deydi, yerel metin/v2 eski hâline döndü (Oracle'da `metinDegisti:false`). (3) `kos.py anlatim` yayındaki eski metinlerde de 20–40 "kısaltma okunuşu" HATA veriyor.
- **Kök neden:** (1) Bu derslerin çıkmış dosyası elle yazılmış, `cikmis_konum.py` yerleştirme adımı hiç koşulmamış; sunucu `metinHash` eşleşmeyince dosyayı sessizce atlıyor, kapı yok. (2) `sesli_yayinla.py` `--v2` klasöründeki `konusma_metni.md`'yi yerel `metin/`'in üstüne yazar; işçi farklı klasörde çalışınca bayat kopya kazanır. (3) Kapı `metin_denetle`'yi `--yazim` olmadan çağırıyor; eski derslerin kısaltmaları o kipte HATA.
- **Çözüm:** Çıkmışlar soru listesi korunarak (id/kök/cevap aynı) yeni metne cümle kimliğiyle yerleştirildi, `metinHash` sunucu algoritmasıyla yazıldı; canlıda 18/17/10. k2-39 doğru klasörle yeniden yayımlandı.
- **Kural:** Yayından önce `curl /api/canli-ders/<key>` `cikmisKonum` sayısı `cikmis_konum` dosyasındaki soru sayısıyla (karantina hariç) karşılaştırılır; `null` ise ders tamamlanmış sayılmaz. `sesli_yayinla.py --v2` klasöründeki `konusma_metni.md` kelime sayısı yerel `metin/<key>.md` ile aynı olmadan çalıştırılmaz. `kos.py anlatim` metin kapısı `--yazim` kipiyle hizalanacak (açık iş).
- **Ek (3) — commit'siz yayın dağıtımla geri alındı:** `sesli_yayinla.py` yeni metni Oracle'a yazdı, EMA sesi yeni metinden üretildi; ama commit yapılmadan başka oturumun `dagit.sh`'si (`deploy-code.sh` [1b] git'teki `metin/hizalama/vurgu/capa/cizim/cikmis_konum`'u Oracle'a yazar) eski metni geri getirdi. Cümle/kelime zamanı eski metne göre ölçüldü, takip kapısı 8 derste T1/T3/T5 HATA verdi. **Kural:** `sesli_yayinla.py` sonrası ses beklenmeden metin katmanları hemen commit + push edilir; zamanlamadan önce `wc -w` ile Oracle metni yerelle karşılaştırılır. Ayrıca `while read` döngüsünde `ssh -n` kullan (yoksa stdin yutulur, yalnız ilk ders işlenir).

- **Ek (4) — anlatım kapısı okunuşu değil yazımı denetliyordu:** `kos.py anlatim` (`anlatim_kapi.py`) `metin_denetle`'yi `--yazim` kipi olmadan çağırıyordu; k2-07/09/21/58'de GABA, NMDA, MSS, P450, faz II gibi 110 kısaltma HATA sayıldı. Oysa Kurul 2+ derslerde EMA'ya `ses_metin.hazirla` okunuşu gider ("gaba", "nee mee dee aa", "pee dört yüz elli", "faz iki"); ses doğruydu. **Çözüm:** kapı `ses_metin.yol_sec(ders=key) == "uzun"` ise okunuş kipine geçer (Kurul 1 eski davranışta). Gevşeme yok: rakam/simge/Yunan harfi yine HATA (deneme: 3/3 yakalandı).
- **Ek (5) — `satir` biçimli eski çapalar anlamsal kapsamada %0–2 sayılıyordu:** k2-33/k2-45 çapaları `satir` (kaynak.md parçası) taşıyor, `madde` dizini yok; `capa_dogrula` yalnız madde/resim/kutu sayıyor. Canlı işaret `pdf_isaret.capa_maddeleri` ile bunları zaten maddeye çeviriyordu. **Çözüm:** aynı eşleme + "parçanın tüm kökleri tek maddede sırasıyla geçiyorsa o madde" kuralıyla `madde` alanı yazıldı (k2-45 %90, k2-33 %87; uydurma çapa yok, yazarın seçtiği satır). **Kural:** eski biçimli çapa kapsama HATA'sında çapa yeniden yazılmadan önce `satir`→`madde` çevirisi denenir.

### H644 — Basit dilli V2 sürümlerinde denetçinin en sık yakaladığı üç hata: tekrar eden ek cümle, aralığı tek sayıya indirme, İngilizce harf okunuşu (2026-11-22, psikiyatri 16 ders)

- **Belirti:** 16 psikiyatri dersinin "çok basit dil" V2'si anlatım kapısından 0 HATA geçtiği hâlde bağımsız denetçi her derste KALIR verdi (toplam ≈190 bulgu): eklenen açıklama cümlesi bir önceki V1 cümlesini başka sözcüklerle yineliyordu; "yüzde yetmiş–seksen" "yüz kişiden yetmiş beşi" diye tek sayıya indirildi, kaynakta olmayan örnek sayılar ("on yaşında", "kırk dakika") eklendi; kısaltmalar "dee see mee" gibi İngilizce harf adlarıyla yazıldı; "neden" açıklaması diye kaynakta olmayan akıl yürütme eklendi (acilde beklemek zarar verir, histeri = konversiyon).
- **Kök neden:** `anlatim_kapi.py` tekrarı, aralık bozulmasını, kaynak dışı çıkarımı ve okunuş dilini ölçmez (yalnız rakam/kısaltma biçimi ve satır çapası). Sadeleştirme isteği yazarı "açıkla, neden'ini söyle" yönüne iter; kaynağın söylemediği nedeni üretmek bu yönün doğal hatasıdır.
- **Çözüm:** Her ders için bağımsız denetçi → `denetim.json` (kimlik + tam öneri cümlesi ya da SIL) → `meds_temp/psikiyatri_v2/uygula.py` (kimlikle uygular, çıkmış/hoca alanlı cümleyi silmez) → kapı → değişen kimliklerin yeniden denetimi. Denetçinin kendi önerisi de tekrar üretebildi (k2-11, k2-19 ikinci tur) — ikinci tur atlanmaz.
- **Kural:** Basit dil sürümünde ek cümle önceki cümleyi yinelemez; aralık iki sınırıyla aktarılır, örnek sayı uydurulmaz; kaynağın söylemediği neden kurulmaz; kısaltma Türkçe okunur (di es em). V1 cümlesi aynen kalırsa çizimi `cizim_tasi.py` taşır.

### H645 · PDF işareti "yalnız sayfa"ya düşüyordu (2026-11-23)
- **Belirti:** Psikiyatri V2'lerin 10'unda takip kapısı T5: işaretlerin %5–20'si yalnız sayfa vurgusu; k2-15'te tablo cümlesi komşu sayfaya işaretlendi.
- **Kök neden:** `pdf_isaret.py` PDF kelimesini yalnız boşlukla böler ("EKT(elektrokonvülzif" → kök `ekt(e`), konuşma tarafı noktalamadan da böler; çapa satırı tutmuyordu. Kısa başlık çapası ("Nöroplastisite") uzun maddenin parçasıyken ≥0,5 oran kuralı reddediyordu. `tablo` çapalı sayfada find_tables tablo görmeyince satır denenmeden ±1 sayfadaki görsele kaçılıyordu. V2'de boş `satir`lı açıklama cümleleri de vardı.
- **Çözüm:** PDF kelimesi `KELIME` ile parçalanır; tüm kökleri sırayla geçen kısa çapa kabul; tablo çapasında önce aynı sayfanın satırları; boş çapa aynı paragraf+sayfadaki önceki (yoksa sonraki) çapalı satırı devralır (`meds_temp/psikiyatri_v2/capa_miras.py`, `miras:1`). 16 V2: T5 0 HATA.
- **Kural:** Eklenen açıklama cümlesi açıkladığı slayt satırına çapalanır; boş `satir` bırakılmaz. Tablo çapasına satır da yazılır.

### H667 · Üç Kurul 2 psikiyatri dersinde metin vurgusu neredeyse yoktu (2026-11-25)
- **Belirti:** Sesli derste k2-42 Nörogelişimsel, k2-43 Konsültasyon-Liyezon, k2-45 İntihar (V1 ve V2) metninde renkli vurgu paragrafların yalnız 8–11'inde vardı (öteki derslerde hemen hepsinde).
- **Kök neden:** Ekran vurgusu `konusma_v2.vurgu_turet` ile cümlelerin `vurgu`/`cikmis` alanlarından türetilir. Bu üç dersin `konusma_v2.json`'unda yazar cümlelere `vurgu` etiketi koymamıştı (360 cümlenin 10'u); yalnız çıkmışa bağlı cümleler vurgulandı. V2 sürümü V1'in boş alanlarını aynen devraldı. Hiçbir kapı vurgu yoğunluğunu ölçmüyor.
- **Çözüm:** Her cümleye ses metninde harfi harfine geçen terim/tanım/sayı/tuzak etiketi yazıldı (V2'de %55–62 cümle; V1 aynı kimlikli cümlelerden aldı), eski etiketler korundu, `vurgu/<key>.json` `vurgu_turet` ile yeniden üretildi; vurgulu paragraf 11→40, 11→26, 8→39; aralıklar API paragraf metniyle birebir hizalı.
- **Kural:** Kurul 2+ derste cümlelerin en az ~%40'ı `vurgu` taşımalı; `metin` `ses` içinde birebir geçmeli (okunuşu farklı kısaltmada ses biçimi: "Viski ar"). Yayından önce vurgulu paragraf oranı denetlenir.
