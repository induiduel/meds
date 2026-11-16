

> Eski 64 bölüm `docs/DEGISIKLIK_ARSIV.md`'e taşındı (2026-11-16); burada son 20 bölüm.

## 2026-10-27 — k2-08 Beyin ve İskelet Sistemi Gelişimi Genetiği Faz C (aşama 12–16)
- Çizim 37 (14 kontur, 1 odak oku, 22 şablonlu panel; yeni şablon `tip_ozellik`); anlam denetimi iki bağımsız geçiş (23 panel tamam, düzeltmeler uygulandı), `cizim_kapisi` 0 HATA, `panel_sinama` 366/567/1100 px 0 hata. Resim sayfaları 24, 27, 68, 73, 78, 81, 82; s.15 fotoğrafları (aniridi) emin olunamadığı için çizilmedi. P81.C2 çapası `madde`den `resim`e çevrildi (Gowers fotoğrafı), işaret yenilendi.
- Önem 44 madde (hoca sınav yerleri + çıkmış `dogrudan` HPE siklops/DMD en üst bant), çözücü 28 soru, asistan 38 nokta; üç doğrulayıcı 0 HATA, 2 bağımsız denetçi GEÇER; ses EMA GPU (çözücü 252, asistan 244 klip). Quiz envanteri 227 atom (slayt iç çelişkili 13 atom `quiz_kullanimi: yasak`); quiz sorusu yok (yalnız Farmakoloji).
- Yeni hatalar: H114, H115.

## 2026-10-27 · Ders içerik sayfaları (k2-05 ilk ders) — yerel; commit/dağıtım yok
- **EMA terim okunuşu + ses temizliği + anlatım kurgusu + çizim renk/zoom/panel (2026-10-28, H128):** `terim_okunus.py` + `okunus/terim_okunus.json` (~600 terim + Latince kural motoru, `--denetle`/`--tara`), `ema_isci.py` Kurul 2+/modül yoluna bağlı + `ses_temizle`; `docs/ANLATIM_KURGU_STANDARDI.md` (TALIMAT_SESLI, TAM_HAT_HIZLI_AKIS, kural_secici anlatim aşamasına bağlı); `CizimLayer.tsx`/`pdfDoc.css` çok renk + marker boyama + panel erken açılış + kısa zoom yok; `cizim_uret.py`/`cizim_dogrula.py` renk/boya/resim, ZOOM_EN_AZ. Var olan derslerin sesi/çizimi yeniden üretilmedi (yeni derslerde geçerli). Commit/dağıtım yok.

- **Sesli ders ekranında okunuş sızıntısı (2026-10-28, H126):** `yazim_sozlugu.py` v2 `ses`↔`ekran` çiftlerinden gen sembolü yazımlarını çıkarır (hoks→HOX, paks altı→PAX6); sözlük yeniden üretildi, onem 520, dağıtıldı.

- **Belirti:** Ders ayrıntısında yalnız sesli ders/Öğren/çıkmış/yorum vardı; dersin terim, hastalık, spot, tablo, soru, kart içeriği ayrı sayfalarda yoktu.
- **Kök neden:** Ders paketi (taslak) üretilmişti ama ders sayfasına bağlanan ders-bazlı içerik katmanı yoktu.
- **Çözüm:** `scripts/ders_icerik_uret.py <kod> <key> <önem kodu> <önem dizini>` → `src/data/ders_icerik/<key>.json`; `DersIcerikV15.tsx` + `dersIcerik.ts` (`?b=terimler|hastaliklar|bilgiler|tablolar|sorular|kartlar`), `DersDetayV15` satırları paket varsa görünür. Yeni derse: betiği çalıştır, başka kod gerekmez.
- **Açık:** hasta/hastalık alanları yalnız taslakta dolu olanları gösterir; commit/dağıtım için `onem`+1 gerekir.

## 2026-10-27 · Ders içerik paketi 6 Kurul 2 dersine + sesli soru çözücü erişimi
- 6 dersin (k2-01,02,03,04,07,08) paketi `scripts/ders_icerik_uret.py` ile yayındaki deste/havuz/terim katmanından üretildi; kapı `ders_icerik_dogrula.py` (çözücü yoksa HATA). **k2-01'in Öğren destesi, havuzu ve çözücüsü yok → paketi yalnız terim/kısaltma; kapı HATA verir, tam içerik işçisi üretmeli.**
- Yeni sayfalar: Sıralamalar ve listeler (sıra türü numara/alfa/azalan/madde), Mini sorular; karşılaştırma tablosunda terazi simgesi.
- Sesli soru çözücü erişimi: ders ayrıntısı satırı, oynatıcıda "Önce soru çözücüyle dene" (başlamadan), ders bitince "Ders bitti" kartı (`cd:bitti` olayı, `dersCozucu.ts` başlık eşlemesi).
- Talimatlar: AGENTS kural 23, el kitabı §19 11a/11b, `docs/DERS_ICERIK_BICIMI.md`.
- Önleme: yeni dersin çözücüsü `src/data/k*_cozucu/index.json`'a, başlığı ders başlığıyla birebir, eklenmeden erişim satırı görünmez.

## 2026-10-27 · k2-01 Nörolojik Hastaya Yaklaşım — tam hat (AGENTS kural 22), yayında
- Katmanlar: Öğren destesi (14 slayt + oyun sayfası), 51 örnek soru (kaynak 9 slayt: standart 50–100'e giriyor), sözlük, hastalıklar, bilgi havuzu, ders içerik paketi (`ders_icerik_dogrula` 0 HATA), önem listesi 2n01 (24 madde), sesli çözücü 2n01 (23 soru, 207 EMA klibi GPU), sınav asistanı 2n01 (23 soru, 190 klip). Sesli ders/çıkmış/terim/kısaltma/çizim önceden vardı. Quiz envanteri: Farmakoloji dışı (kural 19) — atomik envanter paket.json'da.
- Denetim: yazar + 2 bağımsız denetçi; ikincisi slayt 1 klinik kararda **ters bayrak** buldu (H120) → düzeltildi, `validate_learning_decks.py` `klinik-karar-bayrak` kapısı eklendi.
- `birlestir.py`/`asistan_birlestir.py` 2n02'yi değiştiriyordu (kaynak çıkmışlar yok) → 2n02/2n03 dosyaları korundu, yalnız 2n01 + index girdileri alındı. Önleme: tek ders eklerken birleştiriciyi tüm dizinde çalıştırıp farkı kontrol et, değişen eski dersi geri yükle.
- Açık/küçük (denetçi GEÇER-dışı notlar): örnek soru Q14 A şıkkı (epilepsi) ayırt ediciliği, Q25 D/kuyruk cümleleri, asistan 2n01-01 cümle 2 ("lokalizasyon ve nedeni" öykü unsuru gibi okunuyor), paket `medicalTerms` slayt 7 piramidal/serebellar. Slayt dışı çeldirici (Guillain-Barré, Alzheimer, ALS) açıklamaları ders kitabı düzeyinde tek cümle.
- Saat kilidi (`nvidia-smi -lgc`) bu oturumda uygulanamadı (sudo); koruyucu etkindi.

## 2026-10-27 — Sınama dersi Öğren kitaplığında ayrıldı
- `LearnLibraryV12`: `sinama` işaretli desteler "Sınama — test verisi" bölümüne taşındı (en sonda). `ornek_sorular/k2/index.json` k2-07 girdisine `sinama:true`. Dağıtılmadı (onem artmadı); `vite build` yapıldı.

## 2026-10-28 · Özel sohbet ayarları (paylaşım, bildirim, durum, ATP temaları) — yerel; commit/dağıtım yok
- **İstek:** özel sohbete paylaşım (sayfa, soru, favori, çıkmış soru, terim), anlık bildirim, son görülme/çevrimiçi/okunma saati ve ATP ile açılan 3 arka plan.
- **Sunucu** (`toplulukSohbet.ts`, `deploy/pg/sql/topluluk_sohbet.sql`): `topluluk_mesajlar.ek` (jsonb; `ekTemizle` yalnız uygulama içi `/…` adres kabul eder), `sohbet_uyeleri.okundu_zaman/sessiz/tema`, `sohbet_durum` (son görülme, `gizli` karşılıklı). Yeni uçlar: `POST /sohbet/nabiz`, `/sohbet/ayar`, `/sohbet/:id/ayar`. Mesajda diğer üyelere `notifyStudent` (dakikada tek, sessiz mod hariç). `okundu` yalnız işaret ilerlerse yayın yapar (yayın döngüsü olmasın).
- **Tema kilidi:** `tanim.json` › kilitler `sohbet_tema_kalp/tibbi/papatya` (tur `icerik`, 150/200/150 mol); sunucu tema kaydında `basarimMotor.kilitAcikMi` ister. **Oracle'da `data/basarim/tanim.json` üst katmanı varsa bu üç kilit oraya da eklenmeli**, yoksa tema "kilit yok" sayılıp bedava açılır.
- **Ön yüz:** `SohbetEkleri.tsx` (paylaşım paneli/kartı, tema seçici, `SohbetZemin` SVG desenleri; renkler paletin `--color-accent` belirteçlerinden), `ToplulukV15.tsx`, `styles/v15/sohbet-ayar.css`.
- **Açık:** `onem` 509 yapıldı; Oracle’da tanim.json üst katmanı YOK (src sürümü kullanılır); sunucu kodu değiştiği için `systemctl --user restart meds-web` gerekir; girişli tarayıcı sınaması yapılamadı.

## 2026-10-28 — Önbellek sınıfları + açılış hızlandırma
- sw.js v17: kalıcı sınıflı önbellekler `medsor-tasarim-v1` (CSS, yazı tipi, ikon, görsel, Google Fonts) ve `medsor-kod-v1` (JS parçaları, pdf.js). SW sürümü artınca silinmez; özetli adres değişince (yalnız o dosya değişince) yenilenir; etkinleşmede `cevrimdisi-manifest.json`'da olmayan /assets/ kayıtları budanır. Veri (`medsoru-data-*`) ve kabuk (`medsoru-static-*`) ayrı kalır.
- Kök neden (yavaş açılış): her SW sürümü/UpdatePrompt tüm runtime önbelleğini (CSS+JS+yazı tipi) siliyordu → her güncellemede tasarım baştan iniyordu.
- server.ts: kabuk ve dist JSON'ları `no-store` yerine `no-cache` (ETag/304); surum.json ve manifest yanlışlıkla 1 yıl önbellekleniyordu.
- Lottie: 8 animasyon JSON'u statik içe aktarılıyordu (açılışta 353 KB) → isteğe bağlı dinamik içe aktarma (1,5 KB).
- Doğrulanmadı: SW önbellek davranışı tarayıcı panelinde (SW kaydı ortamda reddedildi); canlıda bakılmalı.

## 2026-10-28 — Yıldızlı paragraflar (H127)
- Bugün sayfasına gruplu yıldızlı paragraflar bölümü; sesli derste "Bu ders" kapsamı; silme mezar taşı + en yeni kazanır birleştirmesi (userKvSync, whatsappService süzgeci).

## 2026-10-28 — H431 Kişi Etkinlik sekmesi
- `peopleInsights.ts` `/olaylar` uç noktası sayfa ziyaretlerini (`kv.medsoru_etkinlik_v1`) birleştirir; kök neden ve kural `KURUL2_YAPILMAYACAK_HATALAR.md` H431. onem +1, dağıtıldı.

## 2026-10-29 — Patoloji hocası soru mantığı analizi + Patoloji Soru İşçisi (yerel; commit/dağıtım yok)
- **İstek:** Kurul 1 2026-27 patoloji sınavı yeni/zor kalıpla geldi; hocanın seçim mantığı Kurul 2+ vurgu/örnek soru/çıkabilecek soru üretimine bağlansın.
- **Analiz:** `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` (34 soru; 4'ü toplanmadı, 9'u kısmi — küçük örneklem uyarısı). Ana bulgular: genişlik (26 derse ~1'er soru), bileşik şık %14→%40, "en tipik/en olası" kökü %12→%45, tek geçen ad/eponim ters sorma, çeldirici = aynı dersin komşu kavramları. Slayt biçimi zayıf sinyal: kırmızı satırların %42'si (cevap satırlarında %62), sarı dolgu cevap satırlarında seyrek (%5), başlıktan soru çıkmadı.
- **İşçi:** `scripts/patoloji_soru_isci/` — `hazirla.py` (önem adayı + çeldirici havuzu, LLM yok), `dogrula.py` (≥2 soru/önem noktası, farklı kalıp, komşu-kavram çeldirici, ipucu sızıntısı kapısı), `profil.json`, `TALIMAT.md` (yazar+denetçi akışı). LLM adımı yalnız elle komutla (kural 20).
- **Açık:** henüz hiçbir Kurul 2 patoloji dersi için soru üretilmedi (kullanıcı komutu bekliyor); Kurul 2 çıkmışı gelince profil yeniden hesaplanmalı; 58/62/65/66 numaralı soruların metni toplanırsa analiz güncellenmeli.

## 2026-10-29 (2) — Patoloji hoca mantığı v2 + Kurul 2 ilk hoca-üslubu sorular (yerel; commit/dağıtım yok, UI'ya bağlanmadı)
- **Derin analiz:** 35 PDF biçim işaretli döküm (`scripts/patoloji_soru_isci/dokum.py`), 30 sorunun her biri için 4 ajanla kaynak slayt/dönüşüm/eski çıkmış ilişkisi (`docs/PATOLOJI_SORU_ESLEME_TABLOSU.md`). v1 düzeltildi: sarı dolgu satırlarının %72'si kısa yapı etiketi ("Ancak:/İstisna:/Sonuç:/Not:"), soru etiketin ALTINDAKİ satırdan çıkıyor; kalın/`***`/tekrar güçlü sinyal; hoca 3 dönüşüm kullanıyor (kopya+çevirme, birleştirme, ters yön/ad); 5/30 soru slayt dışı çıkarım içeriyor; her derse ~1 soru.
- **İşçi güncellendi:** `hazirla.py` (etiket altı, tekrar, `***`, üç biçim), `dogrula.py` (açıklama sonu kalıp tekrarı kapısı), `profil.json` (ters_yon, yanlis_bul), `TALIMAT.md`.
- **Üretim:** `src/data/hoca_uslubu_sorular/k2/` — k2-03: 12 önem noktası/24 soru, k2-04: 13 nokta/27 soru. Yazar + 2 tur bağımsız denetçi; ikinci tur sonrası düzeltmeler yalnız kapılardan geçti (üçüncü denetim yok).
- **Kurallar bağlandı:** AGENTS.md kural 25, `docs/SORU_USLUBU.md` Patoloji bölümü (kural_secici ornek_soru aşaması okur), el kitabı 11c.
- **Açık:** bu sorular henüz sitede/Öğren'de gösterilmiyor (ekran bağlantısı yok); dagıtım yok. Kalan Kurul 2 patoloji dersleri PDF'i gelince aynı akış çalıştırılır. `soru_uslup.py` bu şemayla uyumsuz (107 HATA) — bu katman için çalıştırılmadı.

## 2026-10-29 (3) — Hoca üslubu sorular Örnek sorular ekranına bağlandı (yerel; commit/dağıtım yok)
- `KazanimSorulariView.tsx`: `src/data/hoca_uslubu_sorular/k<N>/<ders>.json` dosyaları derse sentetik son kazanım olarak ("Hoca", no 900, "Hocanın üslubunda çıkabilecek sorular") eklenir; soru kimliği `<k2-NN>-qhNN` (ilerleme sayacı `-q` önekiyle sayar); ders listesi soru sayısına eklenir; "K900" yerine "Hoca üslubu" gösterilir. `tsc` 0 hata, `vite build` tamam; yerel 3000'de k2-04 (12+27=39 soru) çözme kipinde doğrulandı. Yalnız ön yüz: sunucu yeniden başlatma gerekmedi.
- **Açık:** dağıtım yok (onem artmadı); k2-03 aynı yolla görünür (ekranda ayrıca açılmadı); ders işçisinin canlı içerik yolu (`/api/content/ornek`) hoca katmanını bilmez, ders canlı içerikle değişirse katman istemcide yine eklenir.

## 2026-10-29 (4) — Hoca üslubu soruları görünür yapıldı (kullanıcı "göremedim" dedi)
- **Belirti:** canlıda "Hoca" etiketli sorular fark edilmedi. **Kök neden:** grup dersin en sonuna (K1–K3'ten sonra) eklenmişti ve ders kartında hiçbir ipucu yoktu; sayılar doğruydu (k2-04 39 soru) ama etiket yalnız ders içinde küçük rozetti. **Çözüm:** `KazanimSorulariView.tsx` — grup en üste, kartta "Hoca üslubu · N yeni soru", kazanım sayısına +1. **Önleme:** yeni içerik katmanı eklenince ders kartında ve ders içinde ilk görünümde işaretlenir.

## 2026-10-29 (5) — Hoca üslubu sorular ders sayfasının "içerikler" bölümüne (kullanıcı bildirdi)
- **Belirti:** sesli ders/ders sayfasında "Bu dersin içerikleri › Soru çöz › Örnek sorular" içinde hoca soruları yoktu; kart sayı bile göstermiyordu. **Kök neden:** hoca katmanını yalnız `KazanimSorulariView` (Örnek sorular ekranı) okuyordu; ders sayfası ayrı yoldan (`dersIcerik.ts › dersSorulariGetir`, `DersIcerikV15`, `DersDetayV15`) örnek soru okur. **Çözüm:** `dersSorulariGetir` hoca kazanımını (no 900, "Hoca") en üste ekler, `Soru` şık şık açıklama gösterir, içerik kartı "N hoca üslubu" yazar (`hocaSoruSayisi`). **Önleme:** yeni soru katmanı eklenince örnek sorunun TÜM okuma yolları (Örnek sorular ekranı + ders sayfası içerikleri + çözücü) kontrol edilir.

## 2026-10-29 (6) — Ayrı "Hoca soruları" kartı + Sesli hoca çözücü (EMA, GPU) — kullanıcı isteği
- **İstek:** ders sayfası "Bu dersin içerikleri" ekranından hoca soruları ayrı ulaşılsın; sesli çözücü + EMA sesi GPU'da.
- **Yapılan:** "Örnek sorular"dan ayrıldı; kartlar "Hoca soruları" (`?b=hoca`, `hocaSorulariGetir`) ve "Sesli hoca çözücü" (`dersHocaCozucu`, branş `k2patolojihoca`, kod 2h01/2h02; `brans.ts` SLUG_AD adı). Çözücü hattı `scripts/patoloji_soru_isci/cozucu_kur.py` (iskele → TALIMAT_COZUCU yazımı → dogrula → birlestir). EMA klipleri GPU'da üretildi (`cozucu_ses_gpu.sh … ses.py --brans k2patolojihoca`; 459 klip ≈ 1 dk; kart 77 °C'ye çıktı, koruyucu etkindi). 51 soru, bağımsız denetimde 24 KALIR → düzeltildi (ipucu sızıntısı 14, ders dışı bilgi, bozuk kelime).
- **Hata (kök neden):** yazar betiği "şık" → "seçenek" değiştirirken "yaklaşık" içindeki "şık"ı da bozmuştu ("yaklaseçenek"); sözcük sınırı olmadan toplu değiştirme yapılmaz — kapıya eklenmedi, bağımsız denetçi yakaladı. **Önleme:** metin dönüştüren betiklerde `\b` sözcük sınırı + sonrasında bozuk kelime taraması.
- **Not:** ders kodu `<kurul>h<sıra>` (2h01…) — normal patoloji çözücü kodlarıyla (2p01) karışmaz, ilerleme ayrı.

## 2026-11-09 (3) — Soru dışa aktarıcı: PDF tasarım ve çıktı seçenekleri (H521, kullanıcı isteği "daha fazla PDF çıkartma özelliği ve özelleştirme")
- **Yapılan (`src/components/v15/soruAktar/ayar.ts`, `belge.ts`, `SoruAktarV15.tsx`, `styles/v15/soruaktar.css`):**
  * Yaprak düzeni `yaprak` (tek · iki · kitapçık): `yaprakOlcu()` yaprak ölçüsü/ölçek, `belgeHtml` sayfaları `.yp` yaprağa `transform:scale` ile yerleştirir; kitapçık sırası ön [n-1-i, i], arka [i, n-1-i] (4'ün katına boş sayfa). Yalnız PDF/yazdırma (`bicim==='pdf'`); Office tek sayfa kalır. Önizleme `yaprakSayisi()` ile "Yaprak x / y · n sayfa" gösterir.
  * Çift yüz `ciftYuz`: `.pg.cift` çift sayfalarda sol/sağ kenar takası; kapak varsa ardına boş sayfa (yalnız HTML listesine eklenir, sayfa modeli değişmez). Kesim çizgileri `kesimCizgi` (ızgara `.izg.kes .hc{outline:dashed}`).
  * Başlık `baslikStil` (çizgi/bant/kutu/sade) + `baslikHiza`; logo `logo` (data: adresi, `LogoSec` canvas ile ≤900×360 px, ≤160 KB, PNG→JPEG), `logoYer`, `logoYuk`; alt bilgi üç bölge `altMetin/altOrta/altSag` + `yerTutucu()` ({sayfa} {toplam} {tarih} {baslik} {altbaslik} {soru}), `sayfaNoYer`, `sayfaNoBicim`, `altCizgi`; `notAlani` (mm, `govde` düşer, `.pg-not` çizgili); `desen` (çizgili/kareli/noktalı, renk ögesi `desen`); kapak `kapakStil` (sade/bant/zemin) + `kapakNot` (yer tutuculu).
  * Soru bloğu: `soruKutu` (çerçeve/zemin/kart) + `kutuIc` + `kutuYaricap` (çözüm kutusu, hücre çerçevesi ve başlık kutusuna da uygulanır), `asiliGirinti` (kök `display:flex`, `--nw` numara genişliği; kök metni artık `<span class="km">` içinde), `sikAralik` (pt; eski `paragraf*0.6` yerine), `sikOran`, `cozumStil` (bant/kutu/zemin/üst çizgi). Yeni renk ögeleri: `baslikZemin`, `kutuKenar`, `kutuZemin`, `desen`, `notCizgi`, `kesim`.
  * Dışa aktarım: `cikti` (hepsi/sorular/çözümler) + `sayfaAralik` → `ciktiSuz()` sayfa modelini süzer (önizleme ve üç biçim); `ozelCss` belge CSS'ine eklenir (önizleme, ölçüm, PDF aynı). Tasarım modları `akademik`, `kesilir`. Önizleme yakınlık %50/%150.
- **Hata ve kök neden (ilk denemede):** asılı girintide kök `display:flex` yapılınca kök metni sarmalanmamış metin düğümüydü; `<b>` parçaları ayrı flex ögesi oldu, numara noktası alt satıra düştü. **Çözüm:** kök metni `.km` span'ına alındı, `.no{flex:0 0 auto;white-space:nowrap}`. Kapak alt satırı `altMetin`'i ham yazıyordu → `yerTutucu` uygulandı. **Önleme:** flex'e alınan her satırda metin düğümleri bir öğeye sarılır; yer tutucu kullanan her alan tek yardımcıdan geçer.
- **Doğrulama:** `tsc` 0, `vite build`; 3000'de önizleme HTML'i `/api/pdf/render` ile basıldı (2'li 14 yaprak, kitapçık 14 yaprak; `pdftoppm` ile sayfa görüntüleri incelendi). Word/PowerPoint yeni kutu/logo/yaprak özelliklerini almaz (panelde yazılı). Commit/dağıtım YAPILMADI; `guncelleme_notu.json` onem 673 hazır.

## 2026-11-09 (4) — Sesli ders dışa aktarımında çıkmış sorular soru kartı olarak (H522, kullanıcı isteği "çıkmış soruları pdf çıkartırken daha düzgün bir format ile sun")
- **Belirti:** Sesli ders metni PDF'inde "Bu dersten çıkmış sorular" eki numaralı madde + alt madde "Cevap:" olarak düz akıyordu: Romen rakamlı önermeler (I. II. III.) tek satırda birbirine giriyor, yıl köke yapışık, "Kurgu Soru:" kökün içinde, cevap sıradan bir madde gibi görünüyordu.
- **Kök neden:** `canliDersDisaAktar.ts::cikmisMd` çıkmışları motorun genel madde Markdown'ıyla yazıyordu; `metinDisaAktar` motorunda soru için ayrı bir blok türü yoktu.
- **Çözüm:** Motora `soru` blok türü eklendi (`?# no | yıl | etiket` + kök satırı + `?- önerme` + `?+ soru cümlesi` + `?= cevap`; üretici yardımcısı `soruSatirlari`, kök ayrıştırıcı `soruKokParcala`: "Kurgu Soru:" etiketi, Romen önermeleri ayrı satır, sondaki soru cümlesi ayrı). PDF'te kart: vurgu renkli numara rozeti, sağ üstte yıl ve "Kurgu soru" etiketi, asılı kök, girintili önermeler (Romen işareti kalın), soru cümlesi, sol şeritli "Cevap" kutusu, ince ayırıcı; kart tek sayfaya sığıyorsa bölünmez, cevap şeridi hiç bölünmez. TXT/MD/DOCX'te aynı yapı (DOCX stilleri SoruKok/SoruOnerme/SoruCevap). Ek başına bir giriş cümlesi (soru sayısı, yıllar) eklendi.
- **Önleme:** Çıkmış/örnek soru yazan her dışa aktarım üreticisi `soruSatirlari` ile kart bloğu yazar; genel madde biçimiyle soru yazılmaz. Sınama: scratchpad `cikmis/sina.mts` ile 4 biçim üretildi, PDF görüntüsü incelendi (Romen ayrımı "IV. Klorazepat / Bu cümleye göre…" dahil).


## 2026-11-10 — Taş Masası: Yedili Okey, Takım Yedili, 101 Okey, Uno (onem 680)
- **İstek:** okey taşlı çok oyunculu gerçek zamanlı oyun (ana mod jokersiz 7 taş, per aç/işle, zorunlu hamle cezaları), takım modu, 101, Uno; bot, istatistik, durdur/devam/bitir, 2B/3B, temalar.
- **Mimari:** sözleşme `src/services/masa/tipler.ts`; saf kural motorları `src/services/masa/motor/{yedili,yuzbir,uno}.ts` (+ `*Asistan.ts` istemci ipuçları, `*.sinama.ts` → `npx tsx`); oda sunucusu `src/services/masa/sunucu.ts` (`/api/masa/ws`, `/api/masa/{odalarim,istatistik,davet}`; odalar RAM + meds-pg `masa_oda`, el sonuçları `masa_el`/`masa_el_oyuncu`, şema `deploy/pg/sql/masa.sql` açılışta); istemci `src/services/masa/istemci.ts` (`useMasa`); arayüz `src/components/masa/` (kabuk, `okey/`, `uno/`) + `src/styles/masa/`.
- **Oyunlar sayfası:** `/oyunlar` artık `MasaView`; eski soru yarışmaları bayrak `oyun_eski` (varsayılan kapalı) ya da `?eski=1`. Yeni bayrak `oyun_masa` (kapatınca masa uçları reddeder).
- **Kural kararları (kullanıcı):** 104 taş; ihlalde her zorunluluk için −5 + 1 ceza taşı + sıra geçer; yığın bitip kimse oynayamazsa berabere (herkes kalan taş kadar eksi); **seriyi bölerek işleme** (kopya taş serinin ortasına işlenir, seri ikiye bölünür, parçalar ≥3) — bu olmadan botlu ellerin ~%95'i berabere bitiyordu (ölçüm: 2–4 oyuncuda bitirme ~%56–58, 6 oyuncuda %26).
- **Kök neden notu (açılış yarışı):** sunucu yeniden başlayınca istemci, odalar meds-pg'den yüklenmeden `katil` gönderiyor ve "masa yok" alıp kodu unutuyordu → `katil` odalar yüklenene dek tek odayı veritabanından okur (`tekYukle`).
- **Yerel sınama kimliği:** `.env` `MEDS_MASA_TEST=1` + `?masatest=<ad>` (yalnız yerel; Oracle'a konmaz).
- **Doğrulama:** üç motor sınaması geçti (yedili 40 sınama + 5.000 botlu el, 101 ve Uno birim + rastgele + bulanık); gerçek sunucuda botlu maçlar soketten uçtan uca; tarayıcıda (başsız Chrome, dokunma olayları) merkez/lobi/masa/sonuç 1024×768, 820×1180, 375×812, 1440×900.
- **Sınanmayan / bilinen sınır:** gerçek tablet/iOS, ses, arkadaş daveti gönderimi, dolu istatistik ekranı (sınama kimliği REST'te geçmez); 3B taşlar gerçek küp değil (perspektif + katmanlı gölge); 5–6 oyuncuda berabere hâlâ çoğunluk; 101'de 4 oyuncuda ellerin ~2/3'ü deste bitişiyle kapanır (gerçek 101 deste boyu).

## 2026-11-10 — Taş Masası: Taş Domino açılış çökmesi (H524, onem 684)
- **Belirti:** canlıda Taş Domino masası `Cannot read properties of undefined (reading 'length')` ile çöküyordu.
- **Kök neden:** `MasaUstCubuk.tsx:49` Uno dışındaki her oyunu okey görünümü sayıp domino oyuncularında olmayan `cezalar` alanını okuyordu.
- **Çözüm:** `o.cezalar?.length`. Yalnız bu satır işlendi; dosyadaki öteki işlenmemiş değişiklikler (tahta oyunları çalışması) çalışma ağacında duruyor.

## 2026-11-10 — Ek modül hoca sorularına hata notları (onem 709)
- **İstek:** kampçılık hoca çalışma sorularında tespit edilen hatalı yerlerin altına hata + doğrusu + neden hatalı + neden yine de yazıldığı; EMA sesi buna göre.
- **Veri:** üç alt ajan 480 soruyu taradı; 14 soruya `hata: {hata, dogrusu, neden, yazilma}` (bosluk 5/38, dy-dagcilik 30/47/60/64/89/97, dy-kamp 9/20/43/51, cs5-zor 8/9). Hocanın anahtarı değiştirilmedi. Önceki şüphelilerden bosluk-40, cs3-47/53, dy-kamp-84, cs5-zor-4 hata değil diye elendi.
- **Ekran/ses/PDF:** `EkHoca` cevaptan sonra `.ekm-hata` kutusu; `ses.py hata_ses()` hc- klibinin sonuna okur (14 klip GPU'da yeniden); `ekFoyBelge.cozumluBelge` hata kutusu, çözümlü PDF yeniden.
