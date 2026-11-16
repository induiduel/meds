# deploy/oracle/ — Oracle dağıtımı

- `dagit.sh` TEK dağıtım yolu; `deploy-code.sh` onun çağırdığı alt adım. `systemd/` birimler, `docker-compose.oracle.yml`, `Dockerfile.*`.
- `tasinan_yollar.txt` eski → yeni betik yolları; `db-yonet.sh` veritabanı tüneli; `sync-*.sh` veri eşitleme.

## Kurallar
- Önce commit + `git push origin main`, sonra `bash deploy/oracle/dagit.sh`; `deploy-code.sh`'ı doğrudan çalıştırma (kirli ağaçta reddedilir).
- Her dağıtımda `guncelleme_notu.json` `onem` +1 ve Türkçe başlık/maddeler (AGENTS kural 13).
- `git add -A` YASAK; yol listesiyle sahnele (H583, kapı D9).
- Dağıtımdan sonra Oracle'da en az bir zamanlayıcı birimini gerçekten çalıştırıp günlüğü oku (H579).
- Oracle `.env` LLM anahtarları kullanıcı istemeden açılmaz (AGENTS kural 20).
- Ayrıntı: `deploy/oracle/README.md`, `docs/hatalar/dagitim_sunucu.md`.
