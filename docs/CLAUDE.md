# docs/ — proje belgeleri

- `HARITA.md` (otomatik): her belgenin konusu ve nereden anıldığı — önce buraya bak, yalnız işinin belgesini aç.
- `KURUL2_YAPILMAYACAK_HATALAR.md` hata dizini → ayrıntı `hatalar/<konu>.md` (16 dosya).
- Standartlar: `KURUL2_DERS_STANDARDI.md`, `TAM_HAT_HIZLI_AKIS.md`, `KURUL_OTOMASYON_EL_KITABI.md`, `CIZIM_KURALLARI.md`, `KURALLAR_OGREN_QUIZ.md`.
- `HOCA_USLUBU/`, `OGRENCI_ONEM/` ders başına belgeler; `arsiv/` eski belgeler.

## Kurallar
- Çözülen her hata: belirti + kök neden + kalıcı çözüm/önleme → `hatalar/<konu>.md` + dizine tek satır + `DEGISIKLIK_KAYDI.md`.
- Dizin ↔ hatalar tutarlılığı: `python3 scripts/hat/tam_hat/kural_secici.py --denetle`.
- Belge ekleyince/silince `python3 scripts/altyapi/belge_haritasi.py`; token tavanları D6 (`python3 scripts/kapilar/yapi_koruma.py`).
- Belgeyi baştan sona okuma; ilgili bölümü aç.
