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
3. **LLM yalnız Claude** (`claude -p`, dar izin listesi; kullanıcı kararı 2026-10-20). Yerel GPU yasak (AGENTS.md 10;
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
   anlatımı, `ekran` = madde, `duzey`, `vurgu` [terim/sayı/tuzak/çıkmış/tanım], `sayfa`, `slayt_adim`, `cikmis`, `spot`).
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

### Aşama D — Cihaz: hastalık zinciri (`otomasyon/hastalik_zinciri.py`, gece)
Oracle önerileri (yalnız `k[2-6]-*`) → Claude `scripts/diseases/TALIMAT_SEMA2.md` → `yayinla.hastaliklari_uygula`
(`diseases.json` kirliyse bekler; denetim hatası artarsa geri alır) → Oracle `data/content/diseases.json` +
`POST /api/admin/icerik/diseases/degisti` (panel sırrı) → SSE `content_changed`.

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
`sesli_anlatim/metin_denetle.py` · `sesli_anlatim/konusma_v2.py --dogrula` · `spot_cozucu/{onem,cozucu,asistan}_dogrula.py` ·
`patoloji_cozucu/okunus_denet.py` · `sinav_spotlari/dogrula.py --kurul2` · `olasi_soru/dogrula.py` ·
`diseases/hastalik_profilleri.py denetle` · `yayinla.py` (kimlik/sadakat/defter) · `otomasyon/hat.py --dogrula`.

## 9. İzleme ve müdahale
- **Pano:** Yönetim › Hat (`/manage/hat`): aşama durumu, son başarı, son kod (kırmızı = hata, 3 = atlandı, 10 = bağımlılık düştü), günlük.
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
- **Prova:** `otomasyon/prova.py` — yayımlanmış bir dersi sahte Kurul 2 dersi olarak tam zincirden geçirir, canlıya
  göndermez (`provak2`, çıktılar `meds_temp/prova/<zaman>/`).

## 10. Çok oturum ve dağıtım kuralları
- Kod dağıtımı: **temiz worktree** (`/home/indu/medsor/meds-dagitim`, `git checkout -f --detach <commit>`) →
  `deploy/oracle/deploy-code.sh` (cihaz kilidi `${XDG_RUNTIME_DIR}/medsor-deploy.lock`; Oracle kilidi `/tmp/meds-deploy.lock`).
  Önce `guncelleme_notu.json` `onem`+1 commit. Dağıtım `dist/dagitim.json` damgasını yazar.
- Canlı sürüm commit'lenmiş bir commit'e karşılık gelmeli; çalışma ağacından kirli dağıtım içerik dağıtımını durdurur.
- Karışık dosyada yalnız kendi parçanı sahnele (`git apply --cached`), sahnelenmiş ağacı `git checkout-index` ile ayrı
  klasörde `tsc` ile sına. Toplu "bekleyen tüm değişiklikler" commit'leri başkasının yarım işini taşır — kaçın.
- Oracle'a tek dosya gönderiminde rsync saat damgasını korur: sunucu kodu gönderdiysen `meds-app`'i yeniden başlat ve uçla doğrula.
- `dist` `emptyOutDir:false`: eski parçalar kalır; derleme sınamasında yalnız güncel parçaya bak.

## 11. Yeni kurul başlarken kontrol listesi (K3…K6)
1. `kurul_takvimi.py` (program değiştiyse) → `ders_kaydi.py --kurul N --yaz` → tanımsız branş varsa `branslar.json`'a ekle.
2. `ders_zinciri.py --kurul N --durum` — defter ve paketler görünüyor mu.
3. Drive'da `Kurul N/` klasörü; işçi günlüğünde eşleşme güveni.
4. İlk dersten sonra: panoda zincir adımları; `/soru-cozucu?kurul=N`, `/en-onemliler`, sesli ders, olası soru boş durumları.
5. Kurul sınavı günü: olası soru akşam çalıştırmaları; ertesi gün `/olasi-sorular?kurul=N`.
6. Sınavdan sonra kurul arşive geçer (`/gecmis-kurullar`), aktif içerik bir sonraki kurula.

## 12. Açık kapılar (hata defteri H7–H12)
Düzeltme yayılımı (tek soru kimliği, H7) · PDF içerik tekrarı (H8) · sayfa kapsama ≥%90 (H9) · çıkmış anahtar çelişkisi
karantinası (H10) · türev veri hash tutarlılığı (H12) · `vurgu_uret.py` hatta alınması · deste `versionGroup` kapısı ·
kelime zamanlaması yalnız cihazda (cihaz kapalıyken gecikir).

## 13. Bilinçli olarak elle kalan
Kod dağıtımı (`esitle_dagit`). Kurul 1 içerik düzeltmeleri. Test bankası Kurul 2+ kapsamı (geliştirme bekliyor).
