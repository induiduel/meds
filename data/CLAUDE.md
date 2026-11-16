# data/ — sunucunun yerel JSON veritabanı ve çalışma verisi

- Asıl kayıtlar `*.json` (havuz, kullanıcı, yönetim); `content/` içerik katmanı farkları (Oracle'da kalıcı katman).
- Çözücü/asistan sesleri `*_cozucu/ses/`, `*_asistan/ses/`, `sesli_anlatim/ses/` — git dışı, Oracle'a rsync.
- `local_rag_chunks.json` (~100 MB, git dışı) sunucu açılışında yeniden üretilir.

## Kurallar
- `git add -A` YASAK (H583): gizli anahtar (`.kimlik_anahtari`), kayıtlar ve sesler depoya gider; yol listesiyle sahnele. Kapı D9.
- Sunucu açılışı buraya yazar; sonra `git status` bak, istenmeyen veri değişikliğini geri al.
- Boş sonuçla veri üzerine yazma; dev dosyaları bütün okuma, `jq` ile dilimle.
- Çalışma/ara veri `meds_temp/<modül>/`'e, buraya değil. Ayrıntı: `docs/hatalar/dagitim_sunucu.md` (H583).
