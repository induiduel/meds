# Kurul Otomasyon El Kitabı — Kurul 2 ve sonrası (işletim talimatı)

> **Kim okur:** bu projede çalışan her yapay zekâ oturumu ve yönetici. Kurul 2'den (26 Ekim 2026) itibaren içerik
> **insan müdahalesi olmadan** üretilir; bu belge hattın her aşamasını, kurallarını, kapılarını, zamanlamasını ve
> arızada ne yapılacağını tek yerde toplar. Neden-niçin ve yol haritası: `GELECEK_PLANLAMASI.md`. Makine okunur aşama
> listesi: `meds/otomasyon/hat.json` (`python3 meds/otomasyon/hat.py --liste`). Kullanıcı hataları defteri:
> `KURUL2_YAPILMAYACAK_HATALAR.md` (yeni hata bildirilince oraya madde + mümkünse kapı).
> Son güncelleme: 2026-10-20.

---

## 0. Değişmez kurallar (özet)

1. **Kaynak sadakati:** içerik yalnız hocanın PDF'inden (müfredat = PDF). Çıkmış sorular önemi belirler, bilgiyi değil.
   Standart kaynakla tamamlama yalnız `kanit.referans` ile ve raporda listelenerek.
2. **Kapı olmadan yayın yok:** her aşamanın doğrulayıcısı 0 HATA vermeden sonraki aşamaya geçilmez. Yazar ≠ denetçi.
3. **LLM yalnız Claude** (`claude -p`, dar izin listesi; kullanıcı kararı 2026-10-20). **Geçiş (kullanıcı kararı 2026-10-23):** maliyet katmanlı
   yönlendirici (`ICERIK_MOTORU_V3.md` §1) devreye girdikçe görev görev betik → ücretsiz bulut → Claude sırasına geçilir;
   bir görev yönlendiriciye bağlanana dek bu kural o görev için geçerlidir. Yerel GPU yasak (AGENTS.md 10;
   izinli 3 istisna: XTTS, EMA çözücü sesi, vurgu üretimi — koruyucu + saat kilidi ile).
4. **Kurul 1 verisine otomatik toplu müdahale yok.** Kurul 1 elle/eski hatta kalır; otomatik hatlar `k[2-6]` ile sınırlı.
5. **Türkçe üslup + şık açıklaması standardı** (`TURKCE_USLUP_STANDARDI.md`, `SIK_ACIKLAMA_STANDARDI.md`): Kurul 2+'da HATA.
6. **Kimlikler kalıcıdır** (§6). Yeniden üretim kimliği değiştirmez.
7. **Sessiz başarısızlık yasak:** boş girdi / servis hatası → çıkış ≠ 0, `hat.log`, panoda kırmızı.
8. **Kod dağıtımı tek sahipten, temiz worktree'den** (§10). Her kod dağıtımında `guncelleme_notu.json` `onem`+1 (Kural 13).
9. **Oturumlar arası tetikleme yok** (AGENTS.md 11).

---

## 1. Takvim ve kurul geçişi

| Ne | Nerede |
|---|---|
| Ders programı PDF → kurul tarihleri | `scripts/takvim/kurul_takvimi.py --yaz` → `src/data/kurul_takvimi.json` + `_ozet.json` (bozuk ayrıştırma eski takvimi ezmez) |
| Aktif / son sınav / arşiv kurul | Python `scripts/takvim/aktif_kurul.py [--son-sinav|--json]`, TS `src/services/kurulTakvimi.ts` |
| Kural | aktif kurul = sınav günü geçmemiş ilk kurul (sınav günü dahil); geçmişler arşiv |
| Tarihler (2026-27) | K1 →23 Eki · K2 26 Eki–4 Ara · K3 →22 Oca · K4 →5 Mar · K5 →22 Nis · K6 →11 Haz · final 28 Haz · büt 16 Tem |
| Ders kayıt defteri | `scripts/dersler/ders_kaydi.py --kurul N --yaz` → `src/data/dersler/kN.json` (kimlik `kN-NN`, kod `N<harf><sıra>`, ör. `2f01`). Branş harfleri tek kaynak: `src/data/dersler/branslar.json`; tanımsız branş/çift kod = HATA |
| Site | ana ekran kurul şeridi; `/gecmis-kurullar`; `?kurul=N` süzgeci (Sesli ders, En önemliler, Spotlar, Soru çözücü, Çıkmış, Öğren, Kazanımlar); örnek sorular K1–6 klasörlerinden |

---

## 2. Zamanlama (kim, ne zaman çalışır)

| Zaman | Nerede | Ne |
|---|---|---|
| sürekli, 50 dk'da bir | Oracle `meds-ders-isci` | Drive taraması → kuyruk → ders işçisi (günde ≤8, ders arası 60 dk; panel ayarları) |
| 10 dk'da bir | Oracle `meds-ders-yayin.timer` | `yayinla.py --sunucu` (onaylı taslaklar → kanonik veri; tur başına tek kurul) |
| 02:30 her gece (kaçırılırsa açılışta) | cihaz `meds-hat-gece.timer` | `hat.py --gece --kacirilan`: sağlık → göç → takvim → ders defteri → ders zinciri → hastalık zinciri → RAG → olası soru → içerik dağıtımı |
| 20:00 ve 23:30 | cihaz `meds-olasi-soru.timer` | olası soru (yeni kanıt yoksa saniyede biter; kilitli) |
| 3 saatte bir | cihaz crontab | RAG vektör eşitlemesi (`rag_vektor_hatti.py --oracle`) |
| saatte bir | cihaz `meds-ses-aktar.timer` | yerel sesleri Oracle'a taşıma |
| 03:30 | Oracle `meds-pg-yedek.timer` | veritabanı yedeği (7 gün) |
| (başka oturum) | `meds-cumle-zaman`, `meds-kelime-zaman-hat` | sesli ders cümle/kelime zamanlaması |

Elle çalıştırma: `python3 meds/otomasyon/hat.py --calistir <aşama>`; durum `--liste`; defter tutarlılığı `--dogrula`.

---

## 3. Ders hattı — aşama aşama (bir Kurul 2+ PDF'i Drive'a düşünce)

### Aşama A — Oracle: ders işçisi (`scripts/ders_isci/`)
1. **Tarama** (`izle.py`): yeni/değişen PDF (sha256) → `kuyruk.json`.
2. **Okuma** (`cikar.py`): `kaynak.md` (PyMuPDF; boş sayfa → Tesseract) + **`sayfalar.json`** (gerçek tablolar
   satır/sütun, görsel ağırlıklı sayfaların PNG'si `sayfa_goruntu/<n>.png`, hocanın renkli/kalın ifadeleri `vurgulu`).
   `kaynak.md`'ye dokunulmaz (alıntı denetimi ona bağlı).
3. **Bağlam** (`isle.py`): ders programı eşleşmesi → **ders defteri eşleşmesi** (numara/kod defterden; defterin temiz
   konusu kimliğe; eşleşme yoksa uyarı → otomatik onay kapanır), sözlük, hastalıklar, kazanımlar, çıkmış adayları.
4. **Yazar Claude** (`TALIMAT.md`): ders_paketi, deste (son slayt ders sonu oyunları), ders notu, örnek sorular, sözlük,
   hastalık önerileri, çıkmış bağları, bilgi havuzu. Görsel sayfaları Read ile görüntü olarak açar; tablolar
   `sayfalar.json`'dan; yalnız görselde görünen bilgi için `kanit: {"sayfa": n, "gorsel": "…"}`.
5. **Denetleyici** (`denetle.py`): alıntılar kaynakta, görsel kanıt yalnız görüntüsü olan sayfada, deste
   `validate_learning_decks.py --oyun-zorunlu` + **Kurul 2+: `--kurul2`** (Türkçe üslup + şık açıklama HATA). En çok 2 düzeltme turu.
6. **Sesli metin** (`TALIMAT_SESLI.md §v2`): Kurul 2+ **yalnız `konusma_v2.json`** (her cümle: kimlik, `ses` = doktorun
   anlatımı, `ekran` = madde, `duzey`, `vurgu` [terim/sayı/tuzak/çıkmış/tanım], `sayfa`, `slayt_adim`, `cikmis`, `spot`). Her ilgili çıkmış ilk geçtiği cümlede sesli anılır ("çıkmışta soruldu"; kapı `isle.cikmis_ses_kapsam`, H57).
   Kapı `konusma_v2.py --dogrula`; eski biçim (`konusma_metni.md` + `konusma_sayfalari.json`) **türetilir**.
7. **Otomatik onay** (`otomatik_onay_uygun`): Kurul 2+ · yeni ders · eşleşme yüksek · uyarı yok · denetim 0 HATA · sesli
   metin tamam → `karar.json` = onayla (panel ayarı `otomatik_onay`, kapatılabilir). Aksi hâlde yöneticiye bildirim + neden.

### Aşama B — Oracle: yayın (`yayinla.py --sunucu`, 10 dk)
- Tur başına **tek kurul** (en küçük önce; diğerleri sonraki tur). `kurula_bagla(k)`: s14/s16 yolları, defter ders listesi,
  `kurulN_ders_paketleri`, `summaries/kurulN.json`, `ornek_sorular/kN`, deste kurul adı.
- Kendi kapıları: kimlik tutarlılığı (`kNp-…`), defterde numara, sadakat eşiği, deste doğrulayıcı (`--kurul2`), s16 örnek
  soru denetimi. Takılırsa `yayin.json: denetim_hatasi` + bildirim.
- Yazar: deste, paket, ders notu/özet, örnek sorular, sözlük, çıkmış bağları, bilgi havuzu; v2 metin → `data/sesli_anlatim/v2/`;
  canlı derse ekleme + Emel/EMA ses işleri.
- Not: Oracle'da ön yüz **derlenmez**; yayımlanan içerik sitede, gece içerik dağıtımından (Aşama F) sonra görünür.

### Aşama C — Cihaz: ders zinciri (`otomasyon/ders_zinciri.py`, gece, ≤3 ders)
Yayın kaydı Oracle'dan salt-okunur okunur; her yayımlanmış Kurul 2+ dersi için (aktif kurul önce, önceki kurulun
yarımları da):
| Adım | İş | Kapı |
|---|---|---|
| hazirla | `kaynak.md` + `sayfalar.json` + görüntüler çekilir; çıkmış adayları (müfredat konusu = defter konusu; tekrar grupları); **önem haritası** (`scripts/onem/onem_haritasi.py`: sayfa başı 0–100 = çıkmış benzerliği × soruldu sayısı × yakınlık + hoca vurgusu); çıkmışsız ders UYARI | — |
| onem | Claude `spot_cozucu/TALIMAT_ONEM.md` (önem haritasına dayanır) | `onem_dogrula.py` (≤3 düzeltme turu) |
| cozucu | Claude `TALIMAT_COZUCU.md` | `cozucu_dogrula.py` |
| denetim | **bağımsız denetçi** Claude `DENETIM.md`; rapor `denetim/<kod>.md` zorunlu | iki kapı yeniden; geçerse `onayli.json` |
| birlestir | `birlestir.py k2<brans>` — **yalnız `onayli.json`'daki kodlar**; ardından `ogren_esle.py` ("Öğren'de bu bilgi") | çıktı var mı; **silme koruması** (ders/öğe sayısı düşerse yedek geri, kod 11) |
| asistan | `asistan_plan.py` → Claude `TALIMAT_ASISTAN.md` → `asistan_birlestir.py` (yalnız onaylı) | `asistan_dogrula.py` |
| ses | EMA: çözücü (`ses_kuyruk.sh`), asistan (`asistan_ses_kuyruk.sh`), Öğren adımları (`ogren_ses_uret.py --oracle`, Kurul 2+ `ema-2`). Kısaltmalar uzun harf okunuşuyla ("dee nee aa") | — |
| oracle | ses klasörleri Oracle'a; canlıda rastgele 5 klip yoklaması (kod 12); içerik sürüm kaydı (`icerik_setleri`) | kayıt yazılamazsa adım tekrar |
Durum `meds_temp/hat/dersler/<id>.json`. Kaynak değişince eski ara dosyalar `_eski/`, onay düşer, zincir baştan.
Art arda hata → 1/2/4/7 gün geri çekilme. Claude zaman aşımı 3 sa. Branş klasörü `k<N><slug>` (Kurul 1 klasörleri ezilmez);
sitede sekme, veri klasörü oluşunca kendiliğinden (`components/spots/brans.ts`).

### Aşama C2 — Otomatik Quiz ve Aktif Geri Çağırma (Active Recall) Hattı
Kurul 2+ derslerinde Sesli Ders (Audio Lesson) akışının doğal uzantısı olarak çalışan, çakışmasız 4 Fazlı Sıralı Pipeline (`scripts/quiz_motoru/`):
1. **Faz 1 - Tetikleme ve Kapsam Kontrolü (Drive Watcher & Scope Lock):**
   - Drive'a yeni ders materyali geldiğinde ders ve kurul kontrol edilir.
   - **Kapsam Kilidi (Scope Lock):** Quiz üretimi şimdilik **yalnızca `Farmakoloji` (`f`, `Tıbbi Farmakoloji`)** için aktiftir. Veri modelleri ve pipeline altyapısı tüm branşlara (Patoloji, Mikrobiyoloji, Biyokimya vb.) sadece konfigürasyon değişikliğiyle açılabilecek şekilde ders-bağımsızdır (`course-agnostic`).
2. **Faz 2 - Birleştirilmiş Derin Analiz (İşlem Tekrarını Önleme):**
   - Sesli ders için yürütülen çıkmış soru, kazanım ve slayt araştırması tekrar edilmez. Ortak analiz adımı `atomik_bilgi_envanteri.json` çıktısını üreterek hem Sesli Dersi hem de Quiz motorunu besler (**Single Source of Truth**). Kaynaktaki tüm ilaç, reseptör, enzim, protein, gen, hastalık, semptom, ADME, yan etki ve klinik notlar tekil bilgi birimleri olarak ayrıştırılır (Sıfır Halüsinasyon).
3. **Faz 3 - Sesli Dersin Tamamlanması (Öncelik Kilidi - Priority Lock):**
   - Sesli Ders (Audio Lesson) `COMPLETED` (onaylı `konusma_v2.json`, metin denetimi 0 HATA) olmadan Quiz soru üretim ajanları **KESİNLİKLE tetiklenemez**.
4. **Faz 4 - Otomatik Quiz Havuzu Üretimi (Batch Processing & 2x Çapraz Sorgulama):**
   - Sesli ders tamamlanır tamamlanmaz Quiz Ajanı (`TALIMAT_QUIZ.md`) devreye girer.
   - **$N \rightarrow \text{en az } 2N$ Çapraz Sorgulama:** Her atomik bilgi en az iki kez, zıt açıyla sorulur:
     * 1. Soru: Pozitif / Doğrudan / İsimden Özelliğe (`positive_direct`)
     * 2. Soru: Negatif / Ters Yönlü / Özellikten İsme (`negative_inverse`)
     * İki soru `question_pair_id` ile eşleşir.
   - **Batch Processing:** Token sınırına takılmamak ve eksiksiz üretim için en fazla 25 atomik bilgi (50 soru) per batch partileri halinde sırayla üretilir.
   - **Soru Yapısı:** 5-15 saniyede çözülebilen kısa active recall formatı. Solo çalışma ve eş zamanlı multiplayer modları destekler. Şık açıklamaları gerekçelidir.
   - **Kapı:** `python3 meds/scripts/quiz_motoru/quiz_dogrula.py <quiz_dosyasi>` 0 HATA.


### Aşama D — Cihaz: hastalık zinciri (`otomasyon/hastalik_zinciri.py`, gece)
Oracle önerileri (yalnız `k[2-6]-*`) → Claude `scripts/diseases/TALIMAT_SEMA2.md` → `yayinla.hastaliklari_uygula`
(`diseases.json` kirliyse bekler; denetim hatası artarsa geri alır) → Oracle `data/content/diseases.json` +
`POST /api/admin/icerik/diseases/degisti` (panel sırrı) → SSE `content_changed`.

### Aşama D2 — Cihaz: Patoloji Check Up (`otomasyon/checkup_zinciri.py`, gece)
Kurulda ≥3 bağımsız denetimden geçmiş patoloji dersi olunca ve onaylı küme/PDF'ler değişince Claude
`scripts/patoloji_checkup/TALIMAT_CHECKUP.md` → `src/data/patoloji_checkup/k<N>/` → `dogrula.py --kurul N` (geçmezse önceki
sürüm geri). Site: `/patoloji-check-up?kurul=N` (veri yoksa Kurul 1 gösterilir).

### Aşama D3 — Cihaz: ders bilgi deposu (`scripts/dersler/bilgi_deposu.py`, gece)
**Her PDF bir kez okunur:** yalnız ders işçisi (`cikar.py`) ve yalnız PDF karması değişince. Sonraki her ürün depodan beslenir:
`meds_database_v2/ders_bilgi/<ders>/manifest.json` (kaynak klasörleri, karmalar) + `ozet.md` (bilgi paketi, önem puanları,
tablolar, hoca vurgusu, görsel sayfalar, çıkmışlar — her satır `kod:sayfa`). Girdiler değişmezse yeniden derlenmez.
Python: `from bilgi_deposu import ozet_yolu, manifest`. Yeni üretici yazarken PDF'i açma, depoyu kullan.

### Aşama D4 — Cihaz: kurul kampı (`otomasyon/kamp_zinciri.py`, gece)
Kurul 1 dahil (K1 dersleri bilgi deposunda: 64 ders, branş klasörlerinden kesin eşlemeyle; 2026-10-20). Hoca tüyoları: öğrenci önerir (`POST /api/kamp/tuyo-oner`), yönetici onaylar ya da doğrudan ekler (Yönetim › Kamp tüyoları;
`/api/admin/kamp/*`); defter `data/kamp/tuyolar.jsonl` (yalnız eklenir). Branşta ≥1 onaylı tüyo + deposu hazır ders olunca:
Claude `scripts/kamp/TALIMAT_KAMP.md` (yalnız depo özetleri + onaylı tüyolar) → `scripts/kamp/dogrula.py` (her kaynak
`kod:sayfa` ders metninde, her onaylı tüyo işlenmiş, şık açıklaması, üslup; ≤3 tur) → EMA `scripts/kamp/ses.py` →
`src/data/kamp/k<N>/<brans>.json` + Oracle `data/kamp/ses/`. Kapı geçmezse yayımlanan kamp değişmez + bildirim.
Site: `/kamp?kurul=N`, `/kamp/<N>/<brans>` (sesli anlatım, kalıp kartları, deneme). Kurul 1 TBG genetik kampı ayrı sayfasında kalır.

### Aşama E — RAG ve diğerleri
RAG vektörleri 3 saatte bir + gece. Kimlik çözücü `/api/k/:id`, kısa bağlantı `/k/<id>`.

### Aşama F — Cihaz: gece içerik dağıtımı (`otomasyon/icerik_dagit.py`)
Oracle `dist/dagitim.json` damgasındaki **canlı commit**'ten temiz worktree → Oracle `src/data` birebir + panel katmanı +
zincir çıktıları → `npm run build` → yalnız `dist` (+ zincir veri klasörleri) Oracle'a. Canlı kod kirli dağıtılmışsa ya da
damga yoksa **atlar (kod 3, panoda)**. Uzak rsync Oracle yayın kilidini tutar. Commit / `onem` artırımı yapmaz.

---

## 4. Olası soru motoru (sınav günü ve sonrası)
1. Öğrenciler sınavdan sonra soruları ekler (sınav günü + 7 gün "Kaçıncı soruydu?" alanı öne çıkar).
2. `scripts/olasi_soru/gece.sh` (20:00, 23:30, 02:30): Oracle'dan `questions.json` + soru defteri + ekran geri bildirimi
   salt-okunur çekilir (çekilemezse DUR) → `topla.py` (TR saatiyle sınav 10:00 sonrası kayıtlar; kök/sürüm/parça/şık/uydu/
   cevap/yorum/defter/geri bildirim → kanıt; numaralı → yuva, numarasız → bge-m3 en yakın yuva; uzlaşı) → yeni kanıt
   varsa Claude `TALIMAT.md` (kanıt > ders > çıkmış) → `dogrula.py` (kimlik `kN-os-NNN`, kanıt bağı, şık açıklama + üslup)
   → `data/olasi_sorular/kN.json` (yerel + Oracle) → `yayinlanan_iz.txt` (yalnız başarıdan sonra).
3. Ekran `/olasi-sorular?kurul=N`: çöz, açıklama, "Buydu / Bu değildi / Düzeltme öner" (IP başına saatte 30) → ertesi
   sentezde kanıt (doğrulanmamış; tek kaynaktan çoklu oy tek sayılır).

---

## 5. Yapay zekâ talimat dosyaları
| Dosya | Kim çalıştırır | Üretir |
|---|---|---|
| `scripts/ders_isci/TALIMAT.md` | Oracle ders işçisi (Claude Opus 5.5) | ders paketi, deste, not, örnek soru, sözlük, hastalık, bağlar |
| `scripts/ders_isci/TALIMAT_SESLI.md` (+§v2) | ders işçisi, ayrı oturum | konuşma metni (Kurul 2+: `konusma_v2.json`) |
| `scripts/spot_cozucu/TALIMAT_ONEM.md` | ders zinciri | önem listesi + örnek sorular + çıkmış seçimi |
| `scripts/spot_cozucu/TALIMAT_COZUCU.md` | ders zinciri | sesli çözücü |
| `scripts/spot_cozucu/DENETIM.md` | ders zinciri (bağımsız denetçi) | düzeltme + `denetim/<kod>.md` |
| `scripts/spot_cozucu/TALIMAT_ASISTAN.md` | ders zinciri | sesli sınav asistanı |
| `scripts/diseases/TALIMAT_SEMA2.md` | hastalık zinciri | şema 2 hastalık profili |
| `scripts/olasi_soru/TALIMAT.md` | olası soru gece işi | olası sorular |
Gözetimsiz Claude izin listesi: `Read,Write,Edit,Glob,Grep,Bash(python3 *)` (+ yerel API `curl -s http://127.0.0.1:3000/*`).
İzin dışı komut takılmadan reddedilir (sınandı); talimatlar yalnız `python3` ile çalışan kapılara dayanır.

---

## 6. Kimlik standardı (deeplink `/k/<kimlik>`)
`k2-07` ders · `k2-07-p12` sayfa · `k2-07-b034` bilgi maddesi · `k2-07-c0142` sesli cümle (`-p012` paragraf, `-b03` bölüm) ·
`k2-07-d-s05` deste adımı · `k2-07-s01` spot · `k2-07-q05` çözücü sorusu · `k2-07-os-012` örnek soru · `k2-os-037` olası soru ·
`t-<slug>` terim · `h-<slug>` hastalık. Kalıcı: düzeltmede değişmez, eklenen yeni numara alır, silinen numara yeniden kullanılmaz.
Kurul 1 sesli dersleri geri dolduruldu (69 ders, 21.272 cümle; `data/sesli_anlatim/v2/`).

## 7. Veritabanı
Göçler `deploy/pg/sql/goc/NNNN_ad.sql` (yalnız ekler; idempotent; commit'lenmiş olmalı) → `scripts/db/goc.py --uygula
[--oracle]` (tek işlem, `schema_migrations`); gece `db_goc` aşaması. İçerik sürümleri `icerik_setleri` (0001), yazıcı
`scripts/db/icerik_kaydi.py`. JSON dosyaları üst düzey `surum` taşır; okuyucular bilinmeyen alanı yok sayar.

## 8. Kalite kapıları (hepsi 0 HATA)
`validate_learning_decks.py [--oyun-zorunlu --kurul2]` · `turkce_uslup.py` · `sik_aciklama.py` · `ders_isci/denetle.py` ·
`sesli_anlatim/metin_denetle.py` (H22 dolgu/asılsız vurgu kapısı) · `sesli_anlatim/konusma_v2.py --dogrula` · `spot_cozucu/{onem,cozucu,asistan}_dogrula.py` ·
`patoloji_cozucu/okunus_denet.py` · `sinav_spotlari/dogrula.py --kurul2` · `olasi_soru/dogrula.py` ·
`diseases/hastalik_profilleri.py denetle` · `yayinla.py` (kimlik/sadakat/defter) · `otomasyon/hat.py --dogrula`.

## 9. İzleme ve müdahale
- **Pano:** Yönetim › Hat (`/manage/hat`): aşama durumu, son başarı, son kod (kırmızı = hata, 3 = atlandı, 10 = bağımlılık düştü), günlük.
  **Dersler** sekmesi: Kurul 2+ ders × aşama matrisi (`GET /api/admin/hat/dersler`, `src/services/hatActionsRoutes.ts`;
  işçi/yayın sütunları Oracle taslaklarından SSH ile salt-okunur, zincir sütunları `meds_temp/hat/dersler/<id>.json`).
  Ders eylemleri kuyruğa yazılır (`meds_temp/hat/eylemler/`), `otomasyon/hat_eylem.py` geçici `meds-hat-eylem` birimiyle
  sırayla işler, gece hattı sürerken bekler: **sürdür** (`ders_zinciri.py --ders`; Oracle aşamasında takılan ders işçinin
  `yeniden`/`yeniden-dene` uçlarıyla), **denetçiye gönder** (`--adim denetim`, geçerse birleştirme ve sonrası yeniden),
  **baştan üret** (iki adım: 1) Oracle ders işçisi `POST /kuyruk/<is>/yeniden-uret` — `scripts/ders_isci/api.py`, cihazdan
  `ssh medsor-oracle docker exec meds-ders-isci` ile iç API'ye — aynı PDF'i yeniden okuyup paketi baştan üretir; iş
  yayımlanmışsa bugünün tarihiyle YENİ kimlikli iş açılır (yayinla.py yayımlanmış is_id'yi yeniden yayımlamaz; aynı gün
  ikinci baştan üretim 409), eski taslak/iz silinmez, yayinla.py yazmadan önce kendi yedeğini alır; `hat_eylem.py`
  işçiyi 60 sn'de bir yoklar, en çok 8 sa; kodlar 20 işçi okunamadı/ret/uç dağıtılmamış, 21 işçide taslak yok, 22 işçi
  3 denemede üretemedi, 23 reddedildi/yayın denetimi, 24 otomatik onay yok (yönetici onayı), 25 zaman aşımı — bunlarda
  cihaz zinciri çalışmaz; 2) yeni paket `yayinlandi` olunca cihaz: ara çıktılar `_eski/<kod>-<zaman>-bastan/`, durum
  `dersler/_eski/`, onay düşer, zincir baştan), **yayından çek**
  (kod `onayli.json`'dan çıkar → birleştiriciler yeniden; yedek `meds_temp/hat/yayindan_cekilen/`; başka ders etkilenirse geri
  alınır; `cekildi` işaretli ders zincirde kendiliğinden yeniden yayına girmez; Oracle'daki Öğren destesi/ders paketi geri
  alınmaz). Kapılar atlanmaz; Kurul 1 dersleri eylem kabul etmez; Oracle'da pano salt okunur.
  **Şimdi çalıştır** (sayfa üstü, iki dokunuş): `POST /api/admin/hat/gece/calistir` → `systemctl --user start --no-block
  meds-hat-gece.service` (zamanlayıcının birimi, `--gece --kacirilan`: bugün başarıyla geçmiş aşamalar atlanır). Birim zaten
  çalışıyorsa ya da `meds-hat-eylem` işleyicisi sürüyorsa 409; durum `GET /api/admin/hat/gece`, çalışırken pano 10 sn'de bir yoklar.
- **Sağlık:** `python3 meds/otomasyon/saglik.py` (canlı API, Oracle SSH, 3000, vektör, EMA, disk + **kapı öz-sınaması**:
  üslup/şık/v2 kapıları iyi-kötü örnekle; arıza = `kapi_ariza`, içerik reddi sanılmaz).
- **Sık durumlar:**
  | Belirti | Yapılacak |
  |---|---|
  | `icerik_dagit` kod 3 "damga yok / kirli" | temiz worktree'den kod dağıtımı (§10) |
  | ders zincirinde ders "N kez hata, gün bekliyor" | `meds_temp/spot_cozucu/<brans>/claude.log` + kapı çıktısı; düzelt, `ders_zinciri.py --ders kN-NN` |
  | yayın `denetim_hatasi` | panelde hatalar; düzelt/yeniden işle |
  | otomatik onay yok | bildirimdeki neden (eşleşme düşük, uyarı, güncelleme modu) → panelden karar |
  | Oracle ulaşılamıyor | Oracle Cloud konsolundan yeniden başlat; gece işleri kaçırılanı sonraki çalışmada tamamlar |
- **Oracle işçi provası** (yayınsız): kapsayıcıda `MEDS_ISCI_DIR=/tmp/isci-prova` + `isle.isle(job)` (`konu_zorla` ile K2 dersi,
  `isle.bildir` bastırılır) → taslağı ana makineye kopyala → `yayinla.uygula([taslak], …, deneme=True)`. 2026-10-20: TAMAM.
- **Kamp provası:** `MEDS_KAMP_API=http://localhost:3000 otomasyon/kamp_zinciri.py --kurul N --brans B --prova`.
- **Prova:** `otomasyon/prova.py` — yayımlanmış bir dersi sahte Kurul 2 dersi olarak tam zincirden geçirir, canlıya
  göndermez (`provak2`, çıktılar `meds_temp/prova/<zaman>/`).

## 10. Çok oturum ve dağıtım kuralları
- Kod dağıtımı: **yalnız `bash deploy/oracle/dagit.sh`** (önce commit + push; `onem`+1). Kilidi bekler (≤30 dk), origin/main →
  temiz worktree `/home/indu/medsor/meds-dagitim` → `deploy-code.sh` (onaylı mod). Durma kodları: 75 kilit, 77 canlı commit
  hedefte yok, 78 canlı kirli, 79 `onem` artmamış (`--sessiz` küçük düzeltme). `deploy-code.sh` doğrudan: kirli ağaç 76,
  canlıyı geri alacaksa 77 (acil `--kirli-izin`). Dağıtım `dist/dagitim.json` damgasını yazar; eşitleme commit'i main'e gider.
- Canlı sürüm commit'lenmiş bir commit'e karşılık gelmeli; çalışma ağacından kirli dağıtım içerik dağıtımını durdurur.
- Karışık dosyada yalnız kendi parçanı sahnele (`git apply --cached`), sahnelenmiş ağacı `git checkout-index` ile ayrı
  klasörde `tsc` ile sına. Toplu "bekleyen tüm değişiklikler" commit'leri başkasının yarım işini taşır — kaçın.
- Oracle'a tek dosya gönderiminde rsync saat damgasını korur: sunucu kodu gönderdiysen `meds-app`'i yeniden başlat ve uçla doğrula.
- `dist` `emptyOutDir:false`: eski parçalar kalır; derleme sınamasında yalnız güncel parçaya bak.

## 10b. Sınav günü kontrol listesi (her kurul)
1. Sınav sabahı: `/` ana ekranda kurul şeridi "Soru ekle"ye çağırır; sınav günü + 7 gün "Kaçıncı soruydu?" alanı öne çıkar.
2. 20:00 ve 23:30: olası sorular kurulur (`meds-olasi-soru.timer`); 02:30 gece hattı tekrar dener. Yöneticiye kontrol listesi bildirimi.
3. Ertesi sabah: `/olasi-sorular?kurul=N` — güven, kanıt sayısı; öğrenci geri bildirimi ertesi sentezde kanıt.
4. Bildirim "henüz set yok" derse: Yönetim › Hat (olasi_soru kodu), `meds_temp/olasi_soru/kN/claude.log`, `dogrula.txt`.

## 11. Yeni kurul başlarken kontrol listesi (K3…K6)
1. `kurul_takvimi.py` (program değiştiyse) → `ders_kaydi.py --kurul N --yaz` → tanımsız branş varsa `branslar.json`'a ekle.
2. `ders_zinciri.py --kurul N --durum` — defter ve paketler görünüyor mu.
3. Drive'da `Kurul N/` klasörü; işçi günlüğünde eşleşme güveni.
4. İlk dersten sonra: panoda zincir adımları; `/soru-cozucu?kurul=N`, `/en-onemliler`, sesli ders, olası soru boş durumları.
5. Kurul sınavı günü: olası soru akşam çalıştırmaları; ertesi gün `/olasi-sorular?kurul=N`.
6. Sınavdan sonra kurul arşive geçer (`/gecmis-kurullar`), aktif içerik bir sonraki kurula.

## 12. Açık kapılar
Yok — hata defterindeki H3–H13 maddelerinin hepsi otomatik kapıya ya da izlemeye bağlandı (ayrıntı
`KURUL2_YAPILMAYACAK_HATALAR.md`). Kelime zamanlaması yalnız cihazda üretilir; cihaz kapalıyken gecikir ama sağlık
denetimi Kurul 2+ eksikliğini sabah bildirir.

## 13. Bilinçli olarak elle kalan
Kod dağıtımı (`esitle_dagit`). Kurul 1 içerik düzeltmeleri. Çıkmış anahtar karantinasının sitede uygulanması (öneri +
bildirim otomatik; gizleme/düzeltme kararı yöneticinin). Genetik sınav kampı (K1'e özgü).

## 14. Bildirimler (panel › bildirimler, `otomasyon/bildir.py`)
- **Sabah özeti** (her gece, başarılı geçse de): aşama sonuçları, son 24 saatte zinciri tamamlanan dersler, güncellenen
  kamp / Check Up / olası soru setleri, sağlık, takvim (`hat.py sabah_ozeti`).
- **Sınav günü kontrol listesi** (bir kez, sınav günü 20:00): soru girişi, olası soru saatleri, ertesi sabah bakılacaklar;
  **ertesi gün**: olası soru setinin durumu (`scripts/olasi_soru/gece.sh`; işaret `meds_temp/olasi_soru/sinav_gunu_bildirimleri.json`).
- Çıkmış anahtar çelişkisi → karantina önerisi; kamp kapıdan geçmezse; gece aşaması başarısızsa (sabah özetinde). Sağlık: kapı arızası, Kurul 2+ türev veri eksikliği (cümle/kelime zamanı, PDF işareti).

### Sağlık kapıları ek (2026-10-20, H16–H17)
- `saglik.py` artık ders kayıt defterinde kimlik/kod/branş numarası çiftini (`kayit_defteri`) ve EMA alt süreç okunuş
  ayarını (`kapi_ariza`) denetler; ikisi de sabah özetinde sorun olarak görünür.
- K2+ sesli ders listesinde branş numarası kayıt defterinden gelir (`canliDers.ts`); Drive `NN)` öneki kullanılmaz.

## Son Prova ve anlamsal slayt çapası — Kurul 2+ (2026-10-21)
Kurul 1'de iki iş elle (alt ajanlarla) yapıldı; Kurul 2'den itibaren hatta bağlıdır.

### Son Prova (`son_prova` aşaması, `otomasyon/son_prova_zinciri.py`)
- **Ne zaman:** aktif kurulun sınavına **9 gün** kala (dahil) her gece; gece başına en çok 5 sa (`MEDS_SON_PROVA_SAAT`),
  kalan partlar ertesi gece. Elle: `python3 meds/otomasyon/son_prova_zinciri.py --kurul 2 [--part KEY] [--zorla]`;
  deneme: `--kuru` (yalnız akış), `--prova` (ilk part; src/data, data/, Oracle'a dokunmaz).
- **Plan:** `scripts/son_prova/plan_kurul.py` — ders kayıt defteri sırası + bilgi deposu (`ders_bilgi/<id>/`: kaynak.md
  `=== SAYFA N ===`, önem, çıkmış), soru havuzu `src/data/k<N><slug>_cozucu/`. Part ≤ 9.000 kelime, branş içinde eşit
  boy; anahtar `k<N>-81…99-son-prova-<slug>[-<no>]` (ders kimlikleri ≤ 70 ile çakışmaz; canliDers.ts branş adını
  `branslar.json`'dan alır). Bilgi deposu olmayan ders partlara girmez, bildirimde listelenir.
- **Sınav dağılımı:** fakülte duyurusu `src/data/son_prova/k<N>/sinav.json` (`{"noroloji": 20, …}`, branş slug'ı) —
  **yönetici yazar**; yoksa ders saatinden tahmin + bildirim (denemeler yanlış dağılımla kurulur, duyuru gelince
  `--zorla` gerekmez: soru_dagit her gece yeniden çalışır).
- **Adımlar:** yazar Claude (TALIMAT + YENI_SORU, yazar grubu ≤3 ders, bir ders = bir aşama) → kapı `dogrula.py <dosya>`
  → bağımsız denetçi Claude (DENETIM + YENI_DENETIM, H19 çıkmış anahtarı) → `dogrula.py --part` PART 0 HATA → `derle.py`
  → özet PDF (`pdf_kirp.mjs`) → **tüm partlar hazırsa** `soru_dagit.py` + EMA (`yeni_ses.py`, `SON_PROVA_KOK`) →
  Oracle (metin/hizalama/vurgu/özet PDF/ses rsync, `ders-ekle` yalnizEma). Yarım Son Prova yayınlanmaz.
- Çalışma klasörü `meds_temp/son_prova_k<N>/` (betikler oraya kopyalanır, talimat yolları çevrilir; `iz.txt` ders
  kümesi değişmedikçe partı yeniden yazdırmaz; değişirse eski part `_eski/`'ye). `src/data/son_prova/k<N>/` gece
  içerik dağıtımıyla (`icerik_dagit.py`) sitede yayınlanır.
- Kurul 1 Son Provası `meds_temp/son_prova/` (elle plan.py) olarak kalır; genelleştirilen betikler K1 çıktısını bayt bayt
  aynı üretir (2026-10-21 sınaması: 14 part doğrulama sonucu aynı, farmakoloji derlemesi birebir).

### Anlamsal slayt çapası (`ders_zinciri` son adımı `capa`)
- Sesli dersin her cümlesi slayttaki madde (M#) / resim (R#) kutusuna ya da elle kutuya bağlanır; resim anlatımında
  hareketli imleç (`yol`). Döküm `scripts/sesli_anlatim/capa_dok.py` (Oracle API ile), yazar Claude
  `scripts/sesli_anlatim/TALIMAT_CAPA.md`, kapı `capa_dogrula.py` (mdSha1, paragraf/cümle sayısı, sayfa/madde/resim
  aralığı, ≥%70 anlamsal kapsama). Çıktı cihaz + Oracle `data/sesli_anlatim/capa/<key>.json`; Oracle
  `meds-cumle-zaman` zamanlayıcısındaki `pdf_isaret.py --hepsi` 30 dk içinde işaretlere çevirir.
- Metin değişirse (mdSha1 tutmaz) eski çapa yok sayılır; ders yeniden üretilirse zincir baştan → çapa da yeniden.

## 15. Görev sözleşmesi — modelden bağımsız LLM işleri (`otomasyon/gorev.py`, 2026-10-23, R0)
Tasarım: `ICERIK_MOTORU_V3.md` §1 ve §14. Bir LLM işi = **görev** (`otomasyon/llm/gorevler.json` kaydı + `otomasyon/llm/gorevler/<id>.py`)
× **hedef** (kimlik). Model dosya sistemi görmez; tek bir `paket.md` okur, kısa etiketli (S1, Q1 …) JSON yazar; kimlik, koordinat,
birleştirme ve doğrulama betiktir.
| Komut | Ne yapar |
|---|---|
| `gorev.py yap <gorev> <hedef> [--denetle] [--cikis DİZİN]` | hazırla → çalıştır → (bağımsız denetim) → (uygula) |
| `gorev.py hazirla <gorev> <hedef> [--ayar adet=2]` | çözücü: `meds_temp/gorev/<is_id>/paket.md` (aynı girdi → aynı is_id) |
| `gorev.py calistir <is_id> [--katman B\|Ü\|C\|elle] [--aile groq]` | yönlendirici: betik → ücretsiz bulut aile aile (≤2 düzeltme turu) → Claude (bütçeli) |
| `gorev.py derle <is_id> [--cevap DOSYA]` | elle/dış LLM cevabını derle + doğrula (her LLM, web sohbeti dahil) |
| `gorev.py uygula <is_id> [--cikis DİZİN] [--k1-izin]` | yedekli yazım; `denetim_zorunlu` görevde denetim `gecer` şart; Kurul 1'e yalnız `--k1-izin` |
| `gorev.py durum`, `defter`, `sinama` | son işler; görevler + kalan Claude bütçesi; model çağırmayan öz-sınama |
- Görevler (R0): `parca_sorusu` (bölüm → 1–6 soru, kimlik `kN-NN-bNN-psN`, çıktı `ders_bilgi/<ders>/l2/parca_sorulari/`),
  `sik_aciklama` (örnek soru şık açıklamaları; mevcut zaten standartsa model çağrılmaz), `denetim` (başka işin bağımsız denetimi,
  yazarın model ailesi hariç). Kural parçaları `otomasyon/llm/kurallar/*.md` (tek yerde; paketlere betikle eklenir).
- Çıkış kodları: 0 · 1 kapı/ret · 3 elle bekliyor · 4 Claude bütçesi doldu (ertesi gün; Ü cevapları önbellekte) · 5 model yanıt yok.
- Bütçe `otomasyon/llm/butce.json` (günlük Claude çağrısı, varsayılan 12), sayaç `meds_temp/state/claude_butce.json`;
  önbellek `meds_temp/llm_onbellek/`; günlük `meds_temp/gorev/gunluk.jsonl` (`cagri`, `model_uyari`, `claude_hata`).
- Gece: `gorev_sinama` aşaması (`hat.json`) öz-sınamayı koşar; HATA = görev kapısı arızası.
- Yeni görev: kayıt + modül (`hazirla/derle/dogrula/tersine/ozet/uygula`, isteğe bağlı `betik`) + `sinama/ornekler.json`'a iyi
  örnek ve en az 3 kötü örnek (kapı her şeyi geçirmesin, H5). Mevcut zincirler (onem, çözücü, asistan…) henüz `claude -p` ile
  çalışır; R3 gölge kipinde sırayla bu sözleşmeye taşınır.

## 16. Kroki zinciri — L0 / L1 (R1 + R2, `kroki` aşaması, 2026-10-23)
Tasarım: `ICERIK_MOTORU_V3.md` §2, §12, §15, §16. Model yok; ortam `meds/.venv-ocr` (PyMuPDF, OpenCV, SciPy), vektör bge-m3 CPU
(tek dosyalık önbellek `meds_temp/kroki/vektor_onbellek.sqlite`). Gece: `kroki` aşaması → `scripts/kroki/zincir.py`.
| Betik | Ne yapar | Çıktı |
|---|---|---|
| `scripts/kroki/l0.py --ders kN-NN` | PDF bir kez: kelime/satır/blok kutuları, vurgulu, resim, tablo (cikar.py ölçütü), zemin ışıklılığı, varlıklar, sayfa izi (SimHash + pHash); OCR yalnız metinsiz resme; önceki L0 ile eşleşen "aynı" sayfanın OCR/roi/egri/ok'u TAŞINIR | `ders_bilgi/<ders>/l0/sayfalar.json`, `sayfa_eslesme.json` (aynı/değişmiş/yeni + eski kimlik takma adları) |
| `scripts/kroki/ok.py` | vektör çizimden oklar (çizgi + üçgen/dart baş, blok ok, ⊣), uçlar doğrultu konisinde metin BLOĞUNA | L0 `ok[]` (`guven`: çizgi yüksek, blok düşük) |
| `scripts/kroki/som.py` | resim içi bölgeler (Canny + kontur), numaralı kopya (SoM) | L0 `roi[]`, `meds_temp/kroki/<ders>/som/pNN.webp` |
| `scripts/kroki/egri.py --sinama` / `--ders --sayfa --yaz` | grafik eğrisi (ızgara/eksen atılır, sütun izi, tepe/çukur, yükseliş/iniş) — kapı: kapsama, isabet, tekillik | L0 `egri[]` |
| `scripts/kroki/ogrenci_not.py --ders --not NOT.pdf` | öğrenci notu: sayfa izi eşleme + ECC hizalama + mevcut mürekkep kuralları; yazı uyumu < %85 sayfa yazılmaz | `l1/ogrenci_not/<not_sha>.json` (canlı katmana yayın ayrı karar) |
| `scripts/cikmis_dizin/dizin.py` | çıkmış dizini (Dönem 3, aile, varlık, bge-m3), ters dizinler; değişen çıkmış → etkilenen dersler | `meds_database_v2/cikmis_dizin/`, `meds_temp/cikmis_dizin/degisen.json` |
| `scripts/cikmis_dizin/plan.py --ders [--tam]` | hedefli tarama: branş/kurul + varlık kesişimi → yalnız adaylarda vektör; `--tam` kaçanı ölçer | `l1/tarama_plani.json` |
| `scripts/cikmis_dizin/kanit.py --ders [--olc]` | soru → doğru/çeldirici bölgesi (sözcüksel + anlamsal şart, kesin/olası/bağsız), çelişki kapısı, tekrar listesi | `l1/kanit.json` |
- Zincir: `scripts/kroki/zincir.py [--kurul N|--ders]` — L0 → ok/SoM → dizin → plan (TEK DERS kuralı tüm dersleri birlikte
  görür; konu kilidi) → kanıt. Artımlı koşu saniyeler. PDF bulunamayan/içerikle doğrulanamayan ders HATA değil
  `meds_temp/kroki/eksik_kaynak.json` (2026-10-23: k1-06, k1-47).
- Kanıt güven katmanları: `kesin` (sözcüksel + anlamsal) → bilgi amaçlı; `tekrar: true` (kesin + cevabın tüm kökleri + en
  benzer sayfa) → öğrenciye otomatik tekrar kartı (K1 kabul %98,8); `olasi`/olumsuz kök → R4 `kanit_bagla` görevi.
- Vektör servisleri CPU kotalı (bge 2 CPU): ilk kurulum uzun (dizin 40 dk, sayfalar ~35 dk); önbellek
  `meds_temp/kroki/vektor_onbellek.sqlite` silinmemeli.
- Kurul 1 dahil çalışır: yalnız OKUR ve kendi `l0/`, `l1/` klasörlerine yazar (içerik dosyalarına dokunmaz).
- Tuzaklar: sayfa izi her yerde aynı girdiden (`l0.metin_izi`: sözcükler `sort=True`) — farklı metin kaynağı aynı PDF'i bile
  "yeni" gösterir; `find_tables` süs kutularını tablo sanar (ölçüt şart); fotoğraf OCR'ı harf yığını üretir (`ocr_anlamli`);
  sayfa dışı (negatif koordinat) çizimler ok değildir; dikdörtgen köşesi ⊣ sanılmasın (bağımsız çubuk şartı).

## 17. Gölge kipi ve görev devri (R3 + R4, 2026-10-23)
- **Gölge (`golge` aşaması, `otomasyon/golge.py`):** her gece küçük, belirlenimci örneklemlerle (tarih tohumlu; Kurul 1
  salt okunur, çıktılar `meds_temp/`) görevleri yalnız ücretsiz katmanda koşar; kayıt `meds_temp/golge/<gün>.jsonl`, özet
  `meds_temp/golge/ozet.json` (son 30 gün: kapı oranı, tur, bağımsız denetim, referans uyumu, modeller). Eşik
  (`gorevler.json` → `gecis_esigi`, varsayılan ≥30 örnek, kapı %95, denetim %90, referans %95) aşılınca görev
  "GEÇİŞE HAZIR" görünür — **öneridir**; Claude zincirindeki bir adımın bu göreve devri kullanıcı kararıdır.
  Referanslar: `kanit_bagla` → örnek sorunun elle konan kanıt sayfası; `som_sec` → k1-03 s16 elle doğrulanmış 5 sorgu.
- **Görev modu:** `gorevler.json` → `mod: aktif|golge`. `aktif` görev gece politikasıyla gerçek veriye uygulanır.
- **Gece politikası (`gorev_gece` aşaması, `otomasyon/llm/gece.py --parti 20`):** şimdilik `kanit_bagla`: Kurul 2+ derslerinin
  olası/bağsız kanıtları 6'lık partilerle; geçen sorular uygulanır, hatalılar (≤ yarısı) partiden düşer ve sonraki
  gece yeniden sorulur (kısmi kabul). Kurul 1 yalnız `--k1`. Kod 4/5 = kota; kalan sonraki gece.
- **Model kararları kalıcı:** `l1/kanit_model.json` (PDF karmasıyla); `kanit.py` yeniden koşunca kararları yeniden uygular,
  PDF değişince yok sayar. Tekrar kartı model kararında da yalnız cevabın TÜM kökleri birimdeyse (olumsuz kökte hiç).
- **Görsel görev `som_sec`:** yalnız Gemini görsel (`cloud_llm.vision_ocr(..., mime=)`) ya da elle; Claude araçsız
  çağrıda görüntü görmez. Seçim `l1/som_secim.json`. Model "yok" derse çizim yedek kipe (halka) düşer.
- Yeni görev eklerken `sinama_ornekleri(meta)` (paket veriden kuruluyorsa) ya da `sinama/ornekler.json` (sabit) zorunlu.

## 18. Önem listesi ve soru çözücü görev yolu (R4, 2026-10-23)
- **Görevler:** `onem_listesi` (sayfa grubu başına: ≤10 sayfa / ≤2.600 sözcük; hedef madde/örnek/zorluk ders düzeyinden
  belirlenimci paylaşılır) ve `cozucu_sorusu` (4'lük parti; soru kümesi resmî `cozucu_dogrula.beklenen` ile aynı).
  Model alıntı metnini değil satır etiketini (L12) seçer; soru/şık/anahtarı çözücüde betik kopyalar.
- **Kapı:** resmî `onem_dogrula.py` / `cozucu_dogrula.py` parçaya uygulanır (ders düzeyi kurallar birleştirmede) + ek betik
  kapıları: bağlı çıkmış maddeyle ÇÖZÜLEBİLMELİ (doğru cevabın kökü detayda; olumsuz kökte öteki şıklardan ≥2'si),
  parça özetinde "sayfa/parça" yok. Pakette dersin TÜM çıkmışları etiketli (örnek soru hiçbiriyle aynı bilgiyi sormasın).
- **Birleştirme `otomasyon/llm/spot_birlestir.py onem|cozucu W kod`:** puan bantları (modelin sırası korunur), doğru harf
  dengesi (şık yer değiştirme), örnek üst sınırı, çıkmış–çıkmış tekrarının `tekrar:<id>` ile elenmesi, başlık/özet/"neden
  önemli"; resmî doğrulayıcı 0 HATA değilse hedef dosya değişmez. Çözücüde `sorunlu` işaretli soru önem listesinden de çıkar.
- **Yürütücü `otomasyon/llm/spot_zinciri.py onem|cozucu W kod [--golge] [--katman Ü]`.** Ders zinciri `gorevler.json` →
  `mod`: `aktif` = adım görev yoluyla; `golge` (varsayılan) = Claude adımı + aynı adım ücretsiz katmanda `W/_golge/`
  aynasında, kıyas `meds_temp/golge/<gün>.jsonl` (`zincir_onem`: madde sayısı, çıkmış karar uyumu). Geçiş kullanıcı kararı.
- Ölçüm (K1 e07 Sifiliz, sınama klasörü, canlıya yazılmadı):
  - önem, ilk kapılarla: 2 parça yalnız Ü (7 çağrı, ~10 dk), birleşik liste resmî kapıdan 0 HATA (22 madde, 16 örnek);
  - önem, çözülebilirlik + tekrar kapılarıyla: Ü son 1–4 hatayı kapatamadı, Claude yedeği 3 çağrıyla bitirdi → 0 HATA
    (23 madde, 13 bağlı / 4 elenen çıkmış). Claude'un K1 listesiyle çıkmış karar uyumu 12/17; "PDF dışı" kararları iki
    Claude koşusu arasında da değişiyor (sınırda kararlar);
  - çözücü: 32 soru, 12 parti, 25 Ü çağrısı (~31 dk), Claude 0, resmî kapı 0 HATA. Kapıdan geçen ama yargı gerektiren
    kusurlar görüldü (yazım hatası, eşanlamlıyla sızan ipucu, "sınavlarda sıkça" genellemesi) → zincirin Claude bağımsız
    denetim adımı korunur.
- Yönlendirici düzeltme turu artık o ana kadarki EN İYİ cevabın üstüne ister (tam yeniden yazımda 1 → 7 hata gerilemesi görüldü).
- Öz-sınama: `sinama/veri/spot/` (e07 girdileri + altın parça/çözücü) — `onem_listesi`, `cozucu_sorusu` dahil 7 görev 0 HATA.

### 18.1 Kurul 2 provası ve kapasite (2026-10-23)
- Prova: `nice .venv-ocr/bin/python -u otomasyon/prova.py --is <yayın işi> --gorev --sesli --ses-yok` (Claude'suz; çıktı
  `meds_temp/spot_cozucu/provak2`, yeniden koşmadan önce klasörü `meds_temp/prova/`'ya taşı). Sonuçlar ve kapasite:
  `ICERIK_MOTORU_V3.md` §20. Ücretsiz katman ≈ günde 2 ders; kota dolunca iş "hazır" kalır, ertesi koşu önbellekten sürer.
- Ortak kapılar (her görev, `yonlendir.kapi`): görev `dogrula` + iç etiket sızıntısı + Türkçe harf kaybı; ses alanları
  `cekirdek.ses_onar` ile betikle onarılır. Kabul edilmiş iş yeniden kullanılırken güncel kapılardan yeniden geçer.
- Ücretsiz zincir: Gemini → Groq → OpenRouter (Nemotron 3 Ultra, Gemma 4 31B); Zen kapalı (`MEDS_CLOUD_ZEN=1`).

### 18.2 Ajan katmanı (2026-10-24, kullanıcı kararı)
- LLM gerektiren görevleri yalnız **OpenCode CLI** (`/opt/OpenCode/resources/opencode-cli run --agent plan`, ücretsiz DeepSeek
  ve GLM) yürütür; OpenCode yetmezse (limit, hata, kapı geçilemedi) bu makinede **yerel Claude** (`claude -p`, 12/gün).
  Doğrudan API zinciri ve Command Code/Antigravity kapalı. Ayar `otomasyon/llm/butce.json`, ayrıntı `ICERIK_MOTORU_V3.md` §21.
- Denetim ders başına toplu; düzeltme turu yalnız hatalı ögeleri gönderir.
- **Profiller (2026-10-24):** `python3 meds/otomasyon/gorev.py profil [ad]` — karma | opencode | antigravity | claude |
  commandcode | oturum. `oturum`: hat paketleri kuyruğa yazıp bekler, bir Claude Code oturumu `/kuyruk` ile çözer
  (`ICERIK_MOTORU_V3.md` §21.1–21.2).

> Canlı çizim/işaretleme kuralları (bütün dersler): `docs/CIZIM_KURALLARI.md`.

### 18.3 Canlı çizim ve sesli ders ekranı (2026-10-24, k2-02 sınamasından; bütün dersler)

- **Kurallar:** `docs/CIZIM_KURALLARI.md` (tek kaynak), model talimatı `scripts/cizim/TALIMAT_CIZIM.md` (1–26), hata defteri H40–H52 + H59.
- **Sıkı kapı (H59, 2026-10-25):** `cizim_uret` + `panel_sinama` sonrası `scripts/cizim/cizim_kapisi.py <key>` 0 HATA olmadan
  çizim yayına gitmez (ders zinciri çıkış 15; arşivde `arsiv_yayinla.py` paket üretmez). Kurallar `CIZIM_KURALLARI.md` §10.
  Kapı eşiği gevşetilmez; düşen ders `sekil_cizim.py onar` (arşiv) ya da ilgili partinin silinip yeniden üretilmesiyle düzeltilir.
- **Akış (ders zinciri `cizim` adımı):** `cizim_uret.py` → sayfa partileri Claude (görüntüye bakarak; şablon seçer, uygun
  şablon yoksa `yeni_sablon` önerir) → `cizim_dogrula.py` kapısı → yeni şablon kaydı (`sablonlar.json`) → bağımsız tıbbi anlam
  denetimi (tamam/düzelt/sil, önbellek `<is>/anlam_denetimi/`) → yerleşim (rota, etiket, panel sürümü, ek alan) →
  `panel_sinama.mjs` (366/567/1100 px; 0 hata) → cihaz + Oracle.
- **Yeniden kullanım (az limit):** parti çıktıları ve anlam denetimi önbellekli; yerleşim/tasarım kuralı değişince
  `cizim_uret.py` aynı `--is-dizini` ile Claude çağırmadan saniyeler içinde yeniden yerleştirir. Yalnız içerik kuralı
  değişen sayfaların partisi silinip yeniden üretilir (`parti*/cizim.json` → `cizim_onceki.json`).
- **Sınama araçları:** `panel_sinama.mjs <ders>` (yerleşim), canlı denetleyici (masaüstü + telefon, örtme ve yazı kesişimi;
  oturumdaki tarayıcıda) — yayından sonra bir kez.
- **Ekran:** izleme düzeni (anlatılmayan paragraflar soluk, slayt %60), telefonda görünüm döngü düğmesi, sayfa takibi
  kare kare kaydırma + ekran ölçümü (program kaydırması takibi durdurmaz), kelime takipçisi harfleri kapatmaz.

## 19. Elle ders üretimi — işçisiz (kullanıcı kararı 2026-10-27; ilk uygulama k2-01 Nörolojik Hastaya Yaklaşım)

> **Sıra/paralellik/okuma/düzeltme biçimi (2026-10-28):** `docs/TAM_HAT_HIZLI_AKIS.md` — adım 1–4 E0 hazırlık betiğiyle
> (`scripts/tam_hat/hazirlik.py`) paralel yürür; yeni kapılar `soru_uslup.py`, `kaynak_kapisi.py`, `pdf_tarama.py`.

LLM otomasyonu kapalıdır (AGENTS kural 20). Yeni ders, kullanıcı hangi dosyanın hangi ders olduğunu söyleyince bu oturumda
üretilir. Arşiv (`y25-*`) içeriği kopyalanmaz. Anahtar ve kod ders kayıt defterinden (`src/data/dersler/kN.json`).

1. **Kaynak:** okul PDF'i (`ogrenci_drive.py` lister ile okul Drive'ı `1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W`), öğrenci notu ve hoca
   kaydı (öğrenci Drive'ı) → `meds_temp/ogrenci_ders/<ders>/`. Eşleme sayfa başlıklarıyla doğrulanır.
2. **Öğrenci notu:** `kroki/ogrenci_not.py` + sayfa görüntüleri elle okunur (hizalama reddettiği sayfa atlanmaz).
3. **Hoca kaydı:** `ogrenci_drive/hoca_dokum.py` (CPU, `MemoryMax=4G`, döküm sürerken `tsc` çalıştırma — H81). Anlaşılmayan
   döküm "hoca vurguladı" dayanağı olmaz.
4. **Çıkmış:** bankada konu + slayt metniyle aday → her soru elle doğrulanır (`s`, `kanit`, `seviye`, `dogrulandi`) — H79.
5. **Değerlendirme paketi:** `meds_database_v2/ders_bilgi/<ders>/degerlendirme/paket.json` → `degerlendirme_dogrula.py` 0 HATA.
6. **Anlatım:** `# Başlık` + `@@ Bölüm` + paragraf; dolgu yok, "çıkmış sınavda sorulmuştur" yalnız `seviye=dogrudan`.
   Kapılar: `metin_denetle.py`, `turkce_uslup.denetle`, bağımsız denetçi alt ajanı (GEÇER).
7. **Yayın:** Oracle `POST /api/sesli-anlatim/ders-ekle` (`key`, `no`, `baslik`, `metin`, paragraf başına `sayfalar`, `dosya`
   {path: drive_root göreli, name, pages, fileId}). Öğren destesi yoksa PDF `lecturePdfLocator.ts` `SANAL_DESTELER`
   (`k<N>p-<key>`) ile bağlanır ve hizalamadaki `deckId` buna çevrilir (yoksa PDF ve işaret açılmaz).
8. **Ses:** ders-ekle EMA işini kuyruğa koyar; bu PC'deki `meds-ema` alır. Ardından Oracle `sudo systemctl start
   meds-cumle-zaman` (cümle zamanı + PDF işareti) ve yerelde `kelime_zaman.py --key <k> --oracle` (CPU, systemd-run).
9. **Çıkmış/terim/kısaltma:** `cikmis_konum/<key>.json` (metinHash = sunucu paragraf hash'i, p/c yeni metinden),
   `kisaltma_sozlugu.py otomatik`, `terim_sozlugu.py dok` → oturumda `terimler.json` → `dogrula --yaz`. Betikler ders bilgisini
   API'den okur: yerelde yoksa `ssh -L 3310:127.0.0.1:3000 medsor-oracle` + `MEDS_API=http://127.0.0.1:3310`.
10. **Çapa + çizim:** `capa_dok.py` → oturumda çapa (`TALIMAT_CAPA.md`) → `capa_dogrula.py` → çizim partileri oturumda
    (`TALIMAT_CIZIM.md`, 27–30: tasarım kataloğunun tamamı) → `cizim_uret.py` yerleşim → `panel_sinama.mjs` + `cizim_kapisi.py` 0 HATA.
11a. **Ders içerik paketi (ZORUNLU, 2026-10-27):** `python3 scripts/ders_icerik_uret.py <key>` → `src/data/ders_icerik/<key>.json`, ardından
    `python3 scripts/ders_icerik_dogrula.py <key>` 0 HATA. Biçim ve kaynak kuralı `docs/DERS_ICERIK_BICIMI.md`; eksik/boş bölüm gerekçeyle raporlanır.
    Ders Öğren destesi ve bilgi havuzu olmadan paket boş kalır — önce deste + havuz üretilir.
    **Kaynak bilgisi kuralı (2026-10-28, ZORUNLU):** paketteki her terim/bilgi/hastalık/önemli kaydı PDF sayfasını (`s`) ve Öğren slaytını (`adim`) taşır;
    ekranda "Slayt s.N" görünmeyen kayıt HATADIR (kullanıcı k2-05'te gördü). Sıra: `ders_icerik_adim.py <key>` → `ders_icerik_kaynak.py <key>`
    (eksik `s`'yi slayttan yazar) → `ders_icerik_dogrula.py` 0 HATA. Slayt/PDF'te adı geçmeyen genel kayıt ("Checkpoint", "Afferent / efferent" gibi
    iskelet ya da kaynaksız terim) üretilmez, bulunduysa silinir; sayfa uydurmak YASAK. Konu/branş bilgisi (hastalık `kat`) boş bırakılmaz.
11b. **Sesli örnek soru çözücü (ZORUNLU, 2026-10-27):** her ders için kaynak gösteren, şık şık açıklamalı çözücü (`TALIMAT_COZUCU.md`,
    `cozucu_dogrula.py` 0 HATA, bağımsız denetçi, EMA GPU sesi §19 adım 8). `ders_icerik_dogrula.py` çözücü yoksa HATA verir; çalıştığı canlıda denenir.
11. **Kayıt + dağıtım:** veriler `data/sesli_anlatim/*/<key>` olarak commit, `guncelleme_notu.json` onem+1, `dagit.sh`; canlı API'de
    ders, ses, PDF (`/api/lecture-pdf/deck/<deckId>/0` 200), çıkmış, işaret, terim, kısaltma doğrulanır.



### PDF akışı için etiketleme (2026-10-27)
`ders_icerik_uret.py` sonunda `ders_icerik_adim.py` çalışır: her kayda `adim` (slayt no) yazılır; `ders_icerik_dogrula.py` eksik/eşlenemeyen `adim`'de HATA verir. PDF: `npx tsx scripts/ders_pdf.mts <key>`; ekranda ders sayfası › Ders PDF'i. Ayrıntı: `DERS_ICERIK_BICIMI.md`.

> **Karşılaştırma/tablo uyarısı (H118):** karşılaştırma ve tablo ögeleri doğal Türkçe ve tıbbi olarak anlamlı olmalı; "Anatomik basamak mı, muayene başlığı mı?" türü meta sınıflama yazılmaz (üretici de eler). Bkz. `KURUL2_YAPILMAYACAK_HATALAR.md` H118.

## 20. Klipli sesli ders (2026-10-28; yalnız bu tarihten sonra eklenen dersler)

- Bayrak: `data/sesli_anlatim/dersler.json` → `klip: true` (`ders-ekle` yeni derse kendisi koyar). Eski derslere bayrak konmaz.
- Üretim: EMA işçisi paragraf başına kayıpsız PCM klip üretir (`ses/<key>/.klip/<özet>.pcm`); metin düzeltilip yeniden
  kuyruğa alınınca yalnız özeti değişen paragraflar seslendirilir, tam MP3 kliplerden tek kodlamayla yeniden kurulur
  (ek yerinde tık/boşluk yok). `KLIP_SURUM` (ema_isci.py) ses işleme değişince artırılır → tüm klipler yenilenir.
- Zaman: `kelime_zaman.py` klip başına göreli kelime zamanını `klip_zaman/<key>.json`'da saklar; yalnız yeni klipleri
  Whisper'dan geçirir. `cumle_zaman.py` her seferinde tüm sesi işler (saniyeler). Çizim/çapa/işaret paragraf/cümle
  sırasına bağlıdır, saniyeye değil; ses yeniden kurulunca kayma olmaz.
- Metin düzeltmesi sırası: (1) `metin/<key>.md` düzenlenir, (2) `python3 scripts/sesli_anlatim/klip_tasi.py <key>`
  (eski metin git HEAD'den ya da `--eski`) hizalama/çapa/işaret/çizim/vurgu/çıkmış konumu/v2 kayıtlarını aynen kalan
  paragraflara taşır, özgünleri `.tasima_yedek/`'e alır, değişen/yeni paragraf dizinlerini listeler (çıkış 2),
  (3) yalnız o paragraflar için çapa, çizim (`cizim_kapisi.py` 0 HATA), çıkmış konumu, v2 yazılır, (4) `pdf_isaret.py`
  (tümü), (5) ses kuyruğu → yalnız yeni klipler, (6) `cumle_zaman.py` + `kelime_zaman.py` (yalnız yeni klipler Whisper).

## 21. Canlı içerik katmanı denetimi (2026-10-28, H130)
- Panel düzenlemeleri `data/content/<rel>.fark.json` (kayıt düzeyinde fark) olarak durur; okuma kaynak + fark birleşimidir.
- Dağıtımdan önce: `python3 scripts/icerik_katman.py denetle` (yerelde) → 0 HATA. Oracle'da tam kopya kalırsa
  `content-overlay-sync.sh` ([0b]) durur; `python3 scripts/icerik_katman.py goc --veri <data> --kaynak <src/data>` ile çevrilir.
