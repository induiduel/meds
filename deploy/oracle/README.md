# Oracle Always Free + Cloudflare Named Tunnel — MedSoru canlı kurulumu

Hedef mimari (kullanıcı kararı):
- Kod: GitHub `main` tek doğruluk kaynağı. Cihaz pushlar, Oracle çeker.
- Veri: `meds/data/*.json` hem cihazda hem Oracle'da durur, `sync-data.sh` ile çift yönlü eşitlenir.
- Veritabanı: aynı makinede `meds-pg` konteyneri (Postgres 17 + pgvector). Supabase 2026-10-12'de kaldırıldı; canlı yayın Postgres NOTIFY → SSE.
- Canlı API: `https://api.nofrostlife.com.tr` → Oracle `localhost:3000` (Named Tunnel, sabit adres).
- Frontend: GitHub Pages (`nofrostlife.com.tr`) aynen kalır; canlı hostta API adresi
  girilmediyse istemci otomatikman Oracle'a düşer (`src/config/deployment.ts`).
- Cihazda geliştirme: `npm run dev` → `http://localhost:3000`, etkilenmez.

## 0. Oracle VM oluşturma (henüz yoksa, ~10 dk)

1. Oracle Cloud → Compute → Create Instance:
   - Image: **Ubuntu 24.04** (ARM Ampere `VM.Standard.A1.Flex`: 4 OCPU / 24 GB önerilir;
     ARM istemezsen `VM.Standard.E2.1.Micro` AMD).
   - Boot volume: **100 GB** (ücretsiz kotanın içinde).
   - VCN: varsayılan; Subnet **public** olsun, public IP otomatik atansın.
   - SSH: kendi `~/.ssh/id_ed25519.pub` anahtarını ekle (yoksa `ssh-keygen -t ed25519`).
2. Security List (VCN → Security Lists → Ingress):
   - `0.0.0.0/0` TCP **22** (SSH), **80**, **443** (Cloudflare geri-dönüş / health).
   - Not: Named Tunnel kullanılacağı için 3000'i dünyaya açma.
3. Bağlan: `ssh -i ~/.ssh/id_ed25519 ubuntu@<ORACLE_PUBLIC_IP>`

## 1. Oracle ilk kurulum (VM içinde tek komut)

```bash
git clone https://github.com/<kullanici>/meds.git ~/meds
cd ~/meds/meds/deploy/oracle
chmod +x oracle-setup.sh sync-data.sh
./oracle-setup.sh
```

Script şunları yapar: Node 20, PM2, cloudflared kurulumu, repo `npm ci`,
`npm run build`, PM2 ile `meds-server` başlatma, `pm2 startup` + `pm2 save`.

## 2. Cloudflare Named Tunnel (sabit `api.` adresi)

Cloudflare Zero Trust Dashboard → Networks → Tunnels → **Create tunnel** → ad: `medsoru-oracle`.
VM'de verilen komutu çalıştır (`cloudflared tunnel login` + `cloudflared tunnel create`
çıktısındaki Tunnel ID'yi not et), sonra:

```bash
sudo mkdir -p /etc/cloudflared
sudo cp ~/meds/meds/deploy/oracle/cloudflared-config.example.yml /etc/cloudflared/config.yml
sudo nano /etc/cloudflared/config.yml   # tunnel: <ID>, credentials-file yolunu yaz
sudo cloudflared tunnel route dns medsoru-oracle api.nofrostlife.com.tr
sudo systemctl enable --now cloudflared
curl -s http://127.0.0.1:3000/api/health   # VM içinden OK olmalı
curl -s https://api.nofrostlife.com.tr/api/health  # dışarıdan OK olmalı
```

`config.yml` içeriği örnek dosyadadır: ingress `api.nofrostlife.com.tr → http://localhost:3000`,
`manage.nofrostlife.com.tr → http://localhost:3000` (aynı sunucu, yol bazlı ayrım istemcide).

## 3. Ortam değişkenleri (`.env` iki yerde ayrı yaşar)

- Cihaz: mevcut `meds/.env` aynen kalır (yerel meds-pg `DATABASE_URL`, yerel yollar).
- Oracle: `~/meds/meds/.env` dosyasını `.env.oracle.example` dosyasına bakarak doldur.
  Kritik farklar: `APP_URL=https://api.nofrostlife.com.tr`,
  `MEDS_PG_PASSWORD` = meds-pg parolası (compose `DATABASE_URL`'i bundan kurar), `MEDSORU_API_PASSWORD` cihazla
  **aynı** olmalı (yoksa yazma istekleri 401 yer).
- Sırlar asla git'e girmez (`.gitignore` zaten `.env*` kapsıyor).

## 4. Günlük kullanım

| İş | Komut |
|---|---|
| Cihazda geliştir | `cd meds && npm run dev` (localhost:3000) |
| Canlıya kod gönder | `git push origin main` → Oracle'da `cd ~/meds && git pull && cd meds && npm ci && npm run build && pm2 restart meds-server` (veya deploy-oracle workflow otomatik yapar) |
| Veriyi Oracle'a gönder | `./sync-data.sh --to-oracle` (cihazdan) |
| Veriyi Oracle'dan çek | `./sync-data.sh --from-oracle` (cihazdan) |
| Oracle durumu | `pm2 status && systemctl status cloudflared --no-pager` |
| Log | `pm2 logs meds-server --lines 80` |

> **ÖNEMLİ (compose çağrısı):** `-f deploy/oracle/...` ile çağrılınca compose `.env` dosyasını
> compose dosyasının klasöründe arar. Bu yüzden TÜM compose komutlarında
> `--env-file /home/ubuntu/medsor/meds/.env` bayrağı ŞART:
> `docker compose --env-file /home/ubuntu/medsor/meds/.env -f deploy/oracle/docker-compose.oracle.yml up -d`

## 5. Otomatik kod deployu (opsiyonel ama önerilir)

`.github/workflows/deploy-oracle.yml` push sonrası Oracle'a SSH ile girip pull+build+restart yapar.
GitHub → repo Settings → Secrets and variables → Actions'a ekle:
`ORACLE_HOST`, `ORACLE_USER` (ubuntu), `ORACLE_SSH_KEY` (private key).
İstemiyorsan dosyayı sil, manuel `git pull` yeterli.

## 6. Veri senkron notları

- `sync-data.sh` rsync + `--backup` kullanır; üzerine yazmadan önce
  `~/meds-data-backup/<tarih>/` altına yedek alır.
- Eşitlenmeyenler: `node_modules`, `dist`, `*.log`, `data/local_rag_chunks.json`
  (78 MB, Oracle'da yeniden üretilir), `*.legacy_backup.json`.
- Çakışma kuralı: son yazan kazanır (iki tarafta aynı anda yazma yapma;
  önce çek, sonra yaz). meds-pg tabloları bu scriptin dışındadır (sunucu JSON'dan kendisi eşitler).

## 7. Doğrulama listesi

- [ ] `https://api.nofrostlife.com.tr/api/health` → `status: online`
- [ ] `https://nofrostlife.com.tr` aç, Ayarlar'da API adresi boşken sorular geliyor (Oracle'a düştüğünü Network sekmesinde `api.nofrostlife.com.tr` çağrısından gör)
- [ ] Cihazda `npm run dev` hâlâ localhost:3000'de çalışıyor
- [ ] `sync-data.sh --to-oracle --dry-run` fark listesi mantıklı
- [ ] Cihaz kapalıyken telefondan site açılıyor
