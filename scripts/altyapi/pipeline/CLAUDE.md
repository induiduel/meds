# scripts/altyapi/pipeline/ — veri hattı

Akış: Drive → `meds_downloads` (ham) → `meds_temp` (ara) → `meds_database` (temiz). Kapsam: Dönem 3.
`00-init` iskelet, `01-inventory` envanter (`_manifest.json`), `02-download` artımlı indirme
(`_downloads.json` durum; ücretsiz herkese açık indirme, olmazsa `GOOGLE_SERVICE_ACCOUNT_FILE`).
Eski Supabase verisinin tam dökümleri `meds_temp/yedek/supabase_oncesi_20261012/` altında saklanır (silinmez).
