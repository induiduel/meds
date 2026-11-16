# scripts/kapilar/ — kapı girişi

- `kos.py` + `matris.json`: aşama → kapı komutu eşlemesi (tek giriş).
- `yapi_koruma.py`: D1 deste deposu, D2 `parents[N]`, D3 taşınan yollar, D4 hata dizini, D5 src/data yazımı, D6 token bütçesi,
  D7 HARITA'sız alt dizin, D8 haritalar bayat, D9 gizli/≥5 MB sahneleme. Pre-commit `.githooks/pre-commit` (`--hizli`).
- `ders_pdf_kapisi.py`, `pdf_basim_kapisi.py`.

## Kurallar
- Kapı eşiğini gevşetmek, kapıyı atlamak YASAK; muafiyet yalnız satır parçasıyla ve gerekçeyle (H581).
- Yeni koruma eklerken yanlış alarm oranı ölçülür.
- D8 bayatsa: `python3 scripts/altyapi/belge_haritasi.py`; D4: `python3 scripts/hat/tam_hat/kural_secici.py --denetle`.
- Çalıştır: `python3 scripts/kapilar/yapi_koruma.py` → 0 HATA. Ayrıntı: dosyanın baş yorumu, `docs/hatalar/dagitim_sunucu.md`.
