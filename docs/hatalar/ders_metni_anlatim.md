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

