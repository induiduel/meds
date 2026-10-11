# MedSoru Canlı Sistem Mimarisi — Cihaz + Oracle + Cloudflare + Supabase

> Son güncelleme: 2026-10-11 · Durum: CANLI (doğrulandı)
> Bu dosya, "bilgisayar kapalıykende çalışsın" kurulumunun tamamını belgeler.
> Her aşama, komut ve adres burada kayıtlıdır.

---

## 1. Topoloji (tek bakış)

```
                    ┌──────────────────────────── Cloudflare ────────────────────────────┐
                    │  DNS: nofrostlife.com.tr ──► Tunnel ──┐                            │
                    │  DNS: api.nofrostlife.com.tr ──► Tunnel ──┤                        │
                    └────────────────────────────────────────┼───────────────────────────┘
                                                             │ (tunnel, içten dışa — gelen port kapalı)
              ┌──────────────────────────────────────────────▼────────────────────────────┐
              │  ORACLE Always Free (92.5.55.109 · Ubuntu 24.04 ARM · ~12GB RAM)          │
              │  Docker (medsoru-oracle): meds-server (:3000) + meds-tunnel + meds-embed (:8094, bge-m3) │
              │  Docker (supabase): 11 servis (db :5432, envoy :8000, studio...)         │
              │  Disk:    ~/medsor/{meds,meds_database*,meds_downloads,meds_temp}        │
              │  .env:    ~/medsor/meds/.env (LOCAL=Oracle local, CLOUD=realtime/yedek) │
              └──────────────────────────────┬───────────────────┬────────────────────────┘
                    rsync (kod+veri)         │                   │ Supabase Cloud
                                             │                   │ (auth + realtime)
              ┌──────────────────────────────▼───────────────────▼────────────────────────┐
              │  CİHAZ (düzenleme masası — kapalı olabilir, site etkilenmez)             │
              │  /home/indu/medsor · npm run dev (:3000) · git · rsync kaynağı           │
              └─────────────────────────────────────────────────────────────────────────┘
```

| Parça | Nerede yaşar | Bilgisayar kapalıyken |
|---|---|---|
| Site (`nofrostlife.com.tr`) | Oracle konteyner | Açık |
| API (`/api/*`, 5713 soru, 114 deste) | Oracle konteyner | Açık |
| `api.nofrostlife.com.tr` | Aynı Oracle (yedek adres) | Açık |
| Auth + realtime | Supabase Cloud | Açık |
| Kodun aslı + veri üretimi (pipeline, OCR, GPU) | Cihaz | Kapalı (sadece üretim durur) |
| GitHub Pages | Yedek (pasif) | Açık |

---

## 2. Oracle makine bilgileri

- IP: `92.5.55.109` · OS: Ubuntu 24.04.5 LTS (aarch64, Ampere) · RAM ~12GB
- SSH: `ssh -i /home/indu/medsor/ssh-key1.key ubuntu@92.5.55.109` (anahtar `chmod 400`)
- Ağ: VCN `medsoru-vcn` → subnet `public-subnet-1` (public) → route table
  `public-rt` (`0.0.0.0/0 → gateway1`) → security list ingress **22/80/443**
- Docker 29.9.0 + Compose v5.6.0 (resmi repo). `ubuntu` kullanıcısı docker grubunda.
- Gelen 3000 kapalı (bilerek): dış erişim yalnız Cloudflare Tunnel üzerinden.

## 3. Docker ile yönetim (Oracle)

> **Kural:** `-f` ile çağrılınca compose `.env` dosyasını compose klasöründe arar.
> Bu yüzden her komutta `--env-file /home/ubuntu/medsor/meds/.env` ŞART.

```bash
ssh -i ~/ssh-key1.key ubuntu@92.5.55.109   # önce bağlan (aşağıdakiler Oracle içinde)

cd /home/ubuntu/medsor/meds
C="docker compose --env-file /home/ubuntu/medsor/meds/.env -f deploy/oracle/docker-compose.oracle.yml"

$C ps                        # konteyner durumu
$C logs meds-server --tail 50          # sunucu günlüğü
$C logs meds-tunnel --tail 20          # tünel günlüğü (Registered + QUIC görmelisin)
$C up -d --build meds-server           # kod güncelleyince: yeniden derle + başlat
$C restart meds-server                 # yalnız yeniden başlat (derlemesiz)
$C up -d cloudflared                   # tüneli başlat/düzelt
$C stop / $C start                     # toptan durdur/başlat
docker stats --no-stream                # CPU/RAM kullanımı
df -h / && du -sh ~/medsor/*            # disk doluluk
curl -s http://127.0.0.1:3000/api/health  # içeriden sağlık kontrolü
```

Günlük akış şablonları:
- `meds-server`: `⚠️ .env içinde hiç AI anahtarı yok` → AI anahtarı eksik (işlevsel, acil değil).
- `meds-tunnel`: `ERR Failed to...` → token/DNS sorunu; `Registered tunnel connection` → sağlıklı.

## 4. Kod gönderme (cihaz → Oracle)

1. Cihazda değiştir + dene (`npm run dev`, `tsc`, `vite build`).
2. Aktar (cihazdan — `src/data` DAHİL, `node_modules/dist/data/.git` HARİÇ):
```bash
rsync -avz --exclude='/node_modules' --exclude='/dist' --exclude='/dist-gh' \
 --exclude='/data' --exclude='/.git' --exclude='/models' --exclude='/training_data' \
 --exclude='/linux' --exclude='.venv*' --exclude='__pycache__' --exclude='*.log' \
 --exclude='/supabase-server/volumes' --exclude='/supabase-server/backups' \
 --exclude='/cloudflared.exe' --exclude='src/data/decks/items' --exclude='/.env' \
 -e "ssh -i /home/indu/medsor/ssh-key1.key" \
 /home/indu/medsor/meds/ ubuntu@92.5.55.109:/home/ubuntu/medsor/meds/
```
> **`.env` ASLA ezilmez:** Oracle `.env` dosyasına token + yol düzeltmeleri işlendi;
> rsync her zaman `--exclude='/.env'` ile çalışır (cihaz `.env`i Oracle'ınkinin üstüne yazmasın).
3. Oracle'da derle + başlat:
```bash
$C up -d --build meds-server && sleep 25 && curl -s http://127.0.0.1:3000/api/health
```
> DİKKAT: `--exclude='data'` (tırnaksız/ankrajsız) yazma — `src/data`yı da eler, derleme 51 hatayla patlar.

## 5. Veri eşitleme (cihaz ⇆ Oracle)

- Birincil veri: `meds/data/*.json` (kullanıcılar, sorular, yorumlar, müzik…).
- `deploy/oracle/sync-data.sh` (cihazdan):
  - `./sync-data.sh --to-oracle` → cihaz Oracle'a yazar + Oracle sunucuyu restart eder.
  - `./sync-data.sh --from-oracle` → Oracle cihazı yazar.
  - Her çalışta `~/meds-data-backup/<tarih>/` altına yedek alır.
- Hariçler: `local_rag_chunks.json` (78MB, Oracle'da yeniden üretilir), `*.legacy_backup.json`, loglar.
- Büyük klasörler (`meds_database*`, `meds_downloads`, `meds_temp` — ~2.8GB) ilk kurulumda
  tek seferlik rsync ile gönderildi; sonrası değişince aynı komut tekrarlanır.
- Kural: iki tarafta aynı anda yazma — önce çek, sonra yaz. Supabase tabloları bu işin dışındadır.

## 6. Veritabanlarını nereden yönetirsin

Üç katman var, üç ayrı kapı:

1. **Site yönetim konsolu (günlük işler):** `https://nofrostlife.com.tr/manage`
   Artık Oracle'a bağlı. Sorular, onaylar, raporlar, yorumlar, kullanıcılar — her şey buradan.
   Eskiden olduğu gibi çalışır, adres değişmedi.
2. **Supabase Cloud (auth + realtime):** `supabase.com` → `kgutsltgmqbnlxcnzrtl` projesi →
   Table Editor (`users`, `past_questions`, auth kullanıcıları) + Authentication (kullanıcılar)
   + Realtime (canlı olaylar). Oracle `localActive=false` ile doğrudan buraya yazar.
   Yerel Docker Supabase artık devrede DEĞİL (cihazda duruyor ama Oracle kullanmıyor).
3. **Ham dosyalar (acil durum):** SSH ile `~/medsor/meds/data/*.json` (asıl kayıtlar bunlar;
   Supabase bunların mirror'udur). Konteyner içinden bakmak için:
   `docker exec meds-server sh -c 'ls /app/data | head'`.

## 7. Cloudflare tarafı

- Tunnel: `oracle-medsor` (Zero Trust → Networks → Tunnels). Token Oracle `.env`de
  (`CLOUDFLARE_TUNNEL_TOKEN`, 2026-10-11 girildi).
- Public hostnames (aynı tünelde): `api.nofrostlife.com.tr → http://meds-server:3000`,
  `nofrostlife.com.tr → http://meds-server:3000`.
- DNS: apex + api `Tunnel` tipinde (Proxied). Eski GitHub Pages A kayıtları silindi.
- Eski `sds` tüneli ve alt kayıtları (agent/dash/manage…) duruyor — dokunulmadı.
- SSL/TLS: Full. Tünel bağlantısı VM içinden dışa (QUIC) kurulur; gelen port gerekmez.

## 8. .env düzeni

- Cihaz `.env`: yerelde kalır (yerel Supabase, `/home/indu` yolları).
- Oracle `.env`: cihazdan türetildi (`/home/ubuntu` yolları, `APP_URL=https://api.nofrostlife.com.tr`,
  `SUPABASE_URL`/`LOCAL_SUPABASE_URL` = Cloud, `MEDSORU_API_PASSWORD` cihazla AYNI).
- Sırlar git'e girmez. Oracle `.env` değişirse: `$C restart meds-server`.

## 8b. Local Supabase (Oracle) + bge-m3

- Yığın: `~/medsor/meds/supabase-server` (cihazla birebir aynı compose; envoy :8000,
  db :5432, studio…). 11/11 servis healthy olmalı (`docker ps` ile bak).
- Veri: cihazdan `pg_dump -Fc` → Oracle'da `pg_restore` ile taşındı (2026-10-11:
  `rag_chunks` 70752, bge-m3 62967, e5 70752). Sonrası cihazda biriken vektörler için
  `rag_bge_m3_test_backfill.py` artımlı modu kullanılır.
- `meds-server` → `LOCAL_SUPABASE_URL=http://host.docker.internal:8000`
  (compose'da `extra_hosts` var) + `LOCAL_SUPABASE_KEY` = local `service_role` anahtarı.
  `localActive=true` olmalı (`/api/health` içinde görünür).
- Anlık işlemler (auth/realtime) hâlâ Cloud'dan (`CLOUD_*` anahtarları yerinde).
- `meds-embed` (bge-m3 sorgu gömme, :8094): `Dockerfile.embed` imajı, model ilk açılışta
  `meds-embed-models` volume'üne iner. Test: `POST :8094/embed` → 1024 boyut.
- local Supabase sıfırlanırsa: `docker compose down` + `volumes/db/data` sil + `up -d db`
  (init ~1 dk) + dump'tan restore. `down -v` YAPMA (config volume'leri de siler).
- Studio (veritabanı yönetimi): Oracle içinde `:8000` arkasında; dışarıdan bakmak için
  SSH tüneli: `ssh -L 8000:localhost:8000 ubuntu@92.5.55.109` → tarayıcıda
  `http://localhost:8000` (anahtar: supabase-server `.env`).

## 9. Arıza → ne yapmalı

| Belirti | Bakılacak yer | Çözüm |
|---|---|---|
| Site açılmıyor | `docker logs meds-tunnel` (Registered var mı?) | Yoksa token/DNS; varsa `meds-server` logu |
| API 500 / boş | `docker logs meds-server` | Çoğu `.env` eksikliği (anahtar/parola) |
| Veriler eski | En son rsync zamanı | §4 + §5 tekrarla |
| Disk doluyor | `df -h`, `docker system df` | `docker system prune -a`, eski backup'ları sil |
| Oracle komple ölü | Cloudflare 502 + SSH yok | OCI konsoldan reboot; açılmıyorsa DNS'i geçici GitHub Pages'e çevir |

## 10. Dosya haritası (bu kurulumun ürettikleri)

- `meds/deploy/oracle/README.md` — ilk kurulum rehberi
- `meds/deploy/oracle/SISTEM_MIMARISI.md` — bu dosya (çalışan sistemin kaydı)
- `meds/deploy/oracle/Dockerfile.oracle` — Node 24 imajı (yalnız API katmanı)
- `meds/deploy/oracle/docker-compose.oracle.yml` — meds-server + cloudflared
- `meds/deploy/oracle/oracle-setup.sh` — VM ilk kurulum (Node/PM2 alternatifi, Docker yolunda kullanılmadı)
- `meds/deploy/oracle/sync-data.sh` — çift yönlü veri eşitleme
- `meds/deploy/oracle/create-vcn.sh`, `fix-route.sh` — ağ kurulumunda kullanıldı (tek seferlik)
- `meds/.dockerignore` — imajı küçük tutar
- `meds/.github/workflows/deploy-oracle.yml` — push→SSH deploy (Secrets ister: ORACLE_HOST/USER/KEY)
- `meds/src/config/deployment.ts` — canlı host Oracle'a düşer, localhost aynı-köken kalır
