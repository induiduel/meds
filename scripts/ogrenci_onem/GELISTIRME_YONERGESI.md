# Yayımlanmış 2026-27 dersini öğrenci önem notuyla geliştirme yönergesi (yazar alt ajan)

Bağlam: AGENTS.md kural 28 + `docs/OGRENCI_ONEM_YONTEMI.md` §5. Ders zaten yayında (sesli ders, önem listesi, sesli çözücü, örnek sorular).
Amaç: geçmiş yıl öğrencilerinin en çok çalıştığı ve çıkmışta sorulan yerler (A/B birimleri) bu derste **yeterince ayrıntılı ve
vurgulu** olsun. Yalnız eksik olan eklenir; doğru ve yeterli olan dokunulmaz (kısmi düzeltme, TAM_HAT_HIZLI_AKIS §3).
Ders süresi kısıtı yok (kullanıcı: 5–10 dk uzayabilir); dolgu yasağı ve "hoca vurguladı" yasağı sürer.

## Önce oku (bu sırayla)
1. `python3 scripts/ogrenci_onem/oku.py --ders <k2-xx>` ve `docs/OGRENCI_ONEM/<k2-xx>.md` (tamamı).
2. Kapı çıktısı (koordinatör verir) — `kapi.py <k2-xx> --sayfalar <sayfalar.json>`: hangi A/B biriminin hangi bilgisi anlatımda / önemde / soruda yok.
3. Bu yılın PDF metni: `<sayfalar.json>` (sayfa → metin) ve görüntüler `meds_temp/ogrenci_ders/<k2-xx>/op/` ya da `onizle/` (şekilli sayfa görüntüden okunur).
4. Kurallar: `python3 scripts/tam_hat/kural_secici.py --oku anlatim` ve `--oku ornek_soru` listelerindeki dosyalar (en az: `docs/KURUL2_DERS_STANDARDI.md` §8,
   `docs/TURKCE_USLUP_STANDARDI.md`, `docs/SIK_ACIKLAMA_STANDARDI.md`, `docs/SORU_USLUBU.md`, `scripts/spot_cozucu/TALIMAT_ONEM.md`, `TALIMAT_COZUCU.md`).

## Kaynak kuralı
Eklenen her bilgi şu üçünden birine dayanır: (a) bu yılın (2026-27) slayt metni/görüntüsü, (b) bankadaki doğrulanmış çıkmışın doğru şıkkı,
(c) öğrenci el notu — yalnız (a) ya da (b) ile çelişmiyorsa ve tıbben doğruysa (ders belgesi §9 "KULLANMA" listesi kullanılmaz).
2026-27 slaytında karşılığı olmayan birim anlatıma girmez (önem listesine "geçen yıl sorulmuştu" notuyla girebilir). Uydurma yok.

## İşler
### A. Önem listesi — `meds_temp/spot_cozucu/<brans>/onem/<kod>.json` (k2noroloji: 2n01/2n02/2n03; k2genetik: 2g01)
- A/B birimine karşılık gelen mevcut maddeye `"ogrenci": {"oncelik": "A"|"B", "not": "<kısa kanıt: hangi çıkmış/işaret/el notu>"}` ekle.
- 2026-27 slaytında olup listede hiç karşılığı olmayan A birimi için yeni madde: TALIMAT_ONEM biçimi (alıntı bu yılın sayfasından,
  `ornek` 1 soru; mevcut kimlik düzenini sürdür). Puanı çıkmışlı maddenin altında, profil maddesinin üstünde.
- Kapı: `python3 scripts/spot_cozucu/onem_dogrula.py` (betiğin `--help`'ine bak; dosya yolu ya da branş) 0 HATA.
### B. Sesli çözücü — `meds_temp/spot_cozucu/<brans>/cozucu/<kod>.json`
- A'da yeni eklenen her `ornek` soru için TALIMAT_COZUCU biçiminde kayıt (`ref` "o:<madde_id>:1", ipucu, siklar, cozum, ses metni).
  Var olan kayıtlara dokunma. Kapı: `cozucu_dogrula.py` 0 HATA. (Ses + `birlestir.py` koordinatörde.)
### C. Örnek sorular — `src/data/ornek_sorular/k2/<anahtar>.json`
- Kapı listesinde sorusu eksik A birimine 2 (farklı kalıp: doğrudan, yanlış-bul, vaka, ters yön), B birimine 1 soru; ders belgesi §2 soru payı ve §7
  "notta olmayan ama sorulmuş" çıkmışların bilgisi. Notta yapıştırılmış çıkmış birebir kopyalanmaz. Toplam 50 < n ≤ 100 (100'ü geçme; 50'nin
  altındaysa ≥51'e tamamla, öncelik A/B birimlerinde). Biçim dosyadaki mevcut sorularla aynı (id sırası sürer, kazanım bağı, sik_aciklamalari).
- Kapılar: `python3 scripts/tam_hat/soru_uslup.py <dosya>`, `python3 scripts/sik_aciklama.py <dosya>` (ya da `--help`), `scripts/turkce_uslup.py`; 0 HATA.
### D. Anlatım — `data/sesli_anlatim/metin/<anahtar>.md` + `data/sesli_anlatim/v2/<anahtar>.json` (İKİSİ BİRLİKTE, aynı metin)
- Kapının eksik dediği bilgi 2026-27 slaytında ya da çıkmışta dayanaklıysa ilgili paragrafa eklenir: tanım → ayırt edici nokta → sayı/ölçüt →
  karıştırılan komşu kavram (yalnız kaynakta olan). "Ders yalnız adını verir/adlarıyla sayar" türü geçiştirme cümlesi, kavram notta/çıkmışta
  tanımıyla geçiyorsa silinip tanımla değiştirilir (H446).
- Vurgu cümlesi: "Bu bilgi çıkmış sınavda sorulmuştur" yalnız doğrulanmış çıkmışta (`seviye: dogrudan`); "geçen yılın öğrencileri bu bilgiyi en
  önemli yerler arasına aldı" türü cümle derste en çok 2 kez, yalnız A biriminde.
- Yeni paragraf açma yerine var olan paragrafa cümle eklemeyi tercih et (çapa/çizim/ses en az bozulsun). Paragraf başında adsız gönderme yasak (H434).
- v2: yeni cümle kimliği dersin kullanılmamış bir sonraki numarası (`k2-05-cNNNN`), `ses` tek cümle, `ekran` kısa madde, `slayt` çapası
  (`satir` o sayfanın metninden BİREBİR) ya da `null`; paragraf metni = cümlelerin `ses`lerinin birleşimi (md ile birebir).
- Kapılar: `python3 scripts/sesli_anlatim/metin_denetle.py <md> --yazim` (yoksa `--help`), `konusma_v2.py --dogrula <klasör>` (klasöre
  `konusma_v2.json` + kaynak.md koy), `turkce_uslup`, ve `python3 scripts/ogrenci_onem/kapi.py <k2-xx> --sayfalar <sayfalar.json>` → 0 HATA
  (kalan HATA'nın gerekçesi: bu yıl slaytta yok / kaynak yok — yazılı).
- Değişen paragrafların dizinlerini (0'dan, md'deki sırayla) ve eklenen cümle kimliklerini rapora yaz (koordinatör ses/çapa/çizimi yalnız onlar için yürütür).

## Yapma
- Ses üretme, `ders-ekle`, `birlestir.py`, commit, dağıtım — koordinatörün işi.
- Var olan doğru içeriği yeniden yazma; metni kısaltma; başka dersin dosyasına dokunma.

## Rapor (Türkçe, kısa)
Katman başına: eklenen/değişen kayıt sayısı + kimlikler, kapı sonuçları (komut + çıktı son satırı), değişen paragraf dizinleri, kaynak gösteremediğin için
atladığın birimler ve gerekçesi.
