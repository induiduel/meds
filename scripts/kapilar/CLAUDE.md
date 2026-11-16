# scripts/kapilar/ — kapı girişi

- `kos.py` + `matris.json`: aşama → kapı komutu eşlemesi (tek giriş).
- `yapi_koruma.py`: D1 deste deposu, D2 `parents[N]`, D3 taşınan yollar, D4 hata dizini, D5 src/data yazımı, D6 token bütçesi,
  D7 HARITA'sız alt dizin, D8 haritalar bayat, D9 gizli/≥5 MB sahneleme, D10 (UYARI) veri bakımı: `data/backups`+`_yedek` >300 MB ya da src/data↔data aynı >5 MB kopya
  (`scripts/altyapi/veri_bakim.py denetle`; izin listesi yalnız azalır). Pre-commit `.githooks/pre-commit` (`--hizli`).
- `ders_pdf_kapisi.py`, `pdf_basim_kapisi.py`.
- `uc_denetim.py` (`kos.py uc`, H596): aynı yöntem+yol iki kez tanımlı uç ve kimlik kademesiz >10 MB genel gövde tavanı.
- `kos.py` çıkış kodları (H597): 0 = 0 HATA, 1 = içerik hatası, 2 = çağrı/girdi yolu yok, 70 = kapı çöktü (içerik hatası değil).
- `butce.py` + `butce.json` (`kos.py butce`): ilk yük JS/CSS gzip, dosya sayısı, en büyük tembel parça, src/data en büyük, zorunlu okuma + aşama kelime; tavan yalnız azalır (`--guncelle` aşağı çeker, yükseltme elle + `_gerekce`).
- Ses aşaması: `kos.py ses hedef=<kök|ders anahtarı>` → `scripts/uretim/ses_ortak/ses_kapisi.py` (bozuk/yarım/sessiz/biçim/düzey;
  2026-11-16 ölçümü 11.000 örnekte yanlış alarm %0; sesli ders düzey farkı yalnız UYARI). Oracle boyut: `ses_kapisi.py oracle --hepsi`.

## Kurallar
- Kapı eşiğini gevşetmek, kapıyı atlamak YASAK; muafiyet yalnız satır parçasıyla ve gerekçeyle (H581).
- Yeni koruma eklerken yanlış alarm oranı ölçülür.
- D8 bayatsa: `python3 scripts/altyapi/belge_haritasi.py`; D4: `python3 scripts/hat/tam_hat/kural_secici.py --denetle`.
- Çalıştır: `python3 scripts/kapilar/yapi_koruma.py` → 0 HATA. Ayrıntı: dosyanın baş yorumu, `docs/hatalar/dagitim_sunucu.md`.
