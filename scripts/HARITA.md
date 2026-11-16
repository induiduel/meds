# `meds/scripts/` Haritası — hangi iş nerede (2026-11-16 yeniden yapılandırma)

> Modelin doğru betiği **tek okumada** bulması için. Önce bu dosyayı oku; klasörleri gezme.
> Eski yol → yeni yol tam listesi: `deploy/oracle/tasinan_yollar.txt` (eski belge/hafıza notlarındaki yolları buradan çevir).

## Düzen
```
scripts/
├── kok.py          konum-bağımsız kök: SCRIPTS / MEDS / PROJE (yeni betikler parents[N] KULLANMAZ — aşağıya bak)
├── HARITA.md       bu dosya
├── kapilar/        tek kapı girişi: kos.py + matris.json (aşama → kapı komutu)
├── hat/            içerik hattının orkestrasyonu
├── uretim/         içerik üretimi (ders, soru, ses, çizim, önem, çözücü ...)
├── altyapi/        servis, dağıtım, derleme, veri hattı, arama
├── moduller/       site özelliklerinin araçları (soru havuzu, composer, sözlük, hastalık, sağlık, ölçüm)
├── arsiv/          ÖLÜ kod — hiçbir şey çağırmaz; tsc ve Oracle gönderiminden dışlı. Yeni iş BURAYA BAĞLANMAZ.
└── *.py / *.mjs    kök kütüphaneler ve tek dosyalık araçlar (sik_aciklama, turkce_uslup, validate_learning_decks,
                    ders_icerik_*, build_* ...). Çok sayıda betik bunları adıyla import eder.
                    `deste_deposu.py` = Öğren destelerinin TEK okuma/yazma noktası (sunucu eşi src/services/desteDeposu.ts);
                    interactive_learning_decks.json'ı doğrudan açmak YASAK.
```

## hat/ — orkestrasyon (tam hat tek giriş: `hat/tam_hat/kosucu.py`)
- `tam_hat/` — **içerik üretiminin tek hattı** (`mod.py` katmanlar, `baglam.py` read-once, `hazirlik.py`, `ders_kilit.py`). Önce burası.
- `takvim/` (aktif kurul) · `dersler/` (ders kayıt defteri) · `onem/` · `oncelikli_dersler/` · `olasi_soru/` (gece.sh) ·
  `paket/` (.medspak) · `quiz_motoru/` (quiz KAPALI, kural 19)

## uretim/ — içerik üretimi
- Ders: `ders_isci/` (yayinla.py, denetle.py) · `sesli_anlatim/` (EMA/XTTS işçisi, cümle/kelime zamanı, pdf_isaret, terim) ·
  `ders_analizi/` · `ders_icerik/` · `ders_video/` · `ogren_ses/` · `ek_modul/`
- Görsel: `cizim/` (cizim_kapisi, TALIMAT_CIZIM) · `kroki/` · `ara_resim/` · `lottie/` · `kmb/`
- Soru/çözücü: `spot_cozucu/` (ses.py, onem_dogrula, cozucu_dogrula) · `patoloji_cozucu/` (cozucu_ses_gpu.sh) ·
  `patoloji_cozucu_alt/` · `patoloji_soru_isci/` · `patoloji_onem/` · `patoloji_checkup/` · `sinav_spotlari/` · `cikmis_paket/`
- Hoca/öğrenci: `hoca_profili/` · `hoca_ara_soru/` · `hoca_vurgu/` · `ogrenci_onem/` · `ogrenci_drive/`
- Kamp/tekrar: `son_prova/` · `blok_ozet/` · `kamp/` · `tekrar_analizi/`
- Çıkmış: `cikmis_dizin/` · `cikmis_2627/` · Arşiv dersleri: `arsiv_25_26/` (adı arşiv ama CANLI üretim)
- Hastalık: `akbc_disease_pipeline.py` (AKBC hastalık profili hattı)
- Konu özel: `ileri_tumor_genetigi/` · `tumor_immuno_builder/` · `arzu/` (özel katman; sürüm notunda anılmaz)

## altyapi/ — servis, dağıtım, veri
- Servisler (systemd): `agents/` (embed_server, gpu_guard, watchdog, pipeline_runner) · `v2/` + `semantic/` (**paket**:
  `cd scripts/altyapi && python -m v2 …` / `-m semantic.server`; birimlerde `WorkingDirectory=…/scripts/altyapi`) ·
  `opendesign/` (köprü kaynağı; çalışan kopya `~/.local/bin`, kur.sh) · `yedek/`
- Veri/arama: `pipeline/` (Drive → downloads → temp → database) · `advanced_ai/` (rag_vektor_hatti.py …) · `search/` · `db/` · `db_analiz/`
- Derleme/sınama: `vite/` (splitLearningDecks, surumDosyasi — vite.config.ts buradan import eder) · `design/` (kontrast kapısı) ·
  `perf/` · `cevrimdisi_sinama/` · `v15/` · `fixtures/` · `artifact_studio/` · `claude_eklenti/`
- Tek dosyalık: `gpu_recovery.sh` (GPU kurtarma) · `rag-yeniden-parcala.mts` (RAG yeniden parçalama)
- Belgeler: `belge_haritasi.py` → `docs/HARITA.md` (belge eklenince yeniden çalıştır)

## moduller/ — site özellik araçları
`recall/` (soru havuzu motoru) · `composer/` · `sozluk_v2/` · `diseases/` · `saglik/` · `eval/` (`npm run eval:*`)

## Çalışma verisi kod değildir
Bir betiğin üretim/ara verisi `meds_temp/<modül>/` altında yaşar (ör. `meds_temp/son_prova/`, `meds_temp/blok_ozet/`,
`meds_temp/tekrar_analizi/`); kod yalnız burada (git). Veri klasörünü ortam değişkeniyle değiştirilebilir yap
(`SON_PROVA_KOK`, `BLOK_OZET_KOK`, `TEKRAR_KOK`). Kodu meds_temp'e kopyalayıp oradan çalıştırma (çift kopya yasak).

## Yeni betik eklerken (ZORUNLU)
1. Doğru grubu seç (yukarıdaki tablo); tek seferlik deneme/göç ise doğrudan `arsiv/`'e değil, işi bitince arsiv'e taşı.
2. Kök yolu **asla** `Path(__file__).parents[N]` ile hesaplama; `kok.py` kullan:
   ```python
   import sys as _sys
   from pathlib import Path as _Path
   _d = _Path(__file__).resolve().parent
   while not (_d / "kok.py").exists() and _d != _d.parent:
       _d = _d.parent
   if str(_d) not in _sys.path:
       _sys.path.append(str(_d))
   import kok as _kok  # _kok.MEDS, _kok.SCRIPTS, _kok.PROJE
   ```
3. Kardeş modüle yol: `_kok.SCRIPTS / "uretim" / "kroki"` (grup segmenti dahil). Modülün kendi dosyaları: `Path(__file__).parent`.
4. Bu haritaya bir satır ekle. Taşıdığın/yeniden adlandırdığın her yolu `deploy/oracle/tasinan_yollar.txt`'ye yaz
   (Oracle'daki eski kopya dağıtımda arşive alınır).
5. Yol süpürmesi yapacaksan sed `[a-z]` aralığı Türkçe yerelde "i"yi atlar (H577) → Python ya da `LC_ALL=C`.
