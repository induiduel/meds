# Yetim sesli anlatım katmanları — arşiv (2026-11-16)

Taşıma tarihi: 2026-11-16. Silinmedi; geri almak için dosyayı aynı adla `data/sesli_anlatim/<katman>/` altına geri taşıyın.

Canlılık ölçütü: anahtar `dersler.json`, `kayit.json`, `v2/`, `ses/<key>/` içinde yoksa VE hiçbir kod yolu (server/src/scripts,
`src/data/son_prova`, arşiv senkronu) o anahtarı okumuyorsa yetimdir.

| Dosya | Neden yetim |
|---|---|
| metin/k2-07-genel-anestezik-ilaclar.md | Eski slug; canlı ders `k2-07-genel-anestezik-ilaclarin-farmakolojisi` (dersler.json + v2). Eski anahtar hiçbir listede/kodda sesli ders anahtarı olarak geçmiyor. |
| kelime_zaman/k2-07-genel-anestezik-ilaclar.json | aynı |
| capa/k2-07-genel-anestezik-ilaclar.json | aynı |
| isaret/k2-07-genel-anestezik-ilaclar.json | aynı |
| cizim/k2-07-genel-anestezik-ilaclar.json | aynı |
| hizalama/k2-07-genel-anestezik-ilaclar.json | aynı |
| terim/k2-07-genel-anestezik-ilaclar.json | aynı |
| kisaltma/k2-07-genel-anestezik-ilaclar.json | aynı |
| kisaltma_elle/k2-07-genel-anestezik-ilaclar.json | aynı |

Korunanlar (yetim SAYILMADI): v2'si olmayan ama `dersler.json`'da olan 58 ders (v1 geri dönüşü); Son Prova / Blok özet
partları k1-81…k1-97 (canliDers.ts ayrıştırır, `src/data/son_prova/k1` anar); `kelime_zaman/k1-59-immunofarmakoloji-v2`
(`scripts/uretim/sesli_anlatim/modul_okunus.py` MODUL_ANAHTARLAR); `gunluk/y25-*` (arsiv_yayinla.py bilerek eşitler);
`kisaltma_elle/y25-*` (kisaltma_sozlugu.py arşiv dersleri için okur).
Oracle: deploy-code.sh yalnız adlı katman klasörlerini eşitler, `/data` genel dışlı — bu klasör gönderilmez.
