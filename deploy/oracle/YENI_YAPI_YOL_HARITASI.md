# YENİ YAPI YOL HARİTASI — Temiz repo + Ayrı veritabanı + Ayrı yedek

> Durum: PLAN (2026-10-11). Hiçbir kod/config değiştirilmedi; bu dosya dışında yazma yapılmadı.
> İlke: **sıfır veri kaybı** — her fazın başında yedek + sayaç, sonunda doğrulama + geri dönüş yolu.
> Hedef: küçük, kullanıcı verisi içermeyen, amaca uygun repo; anlık+geçmiş tüm veri DB'de; yedek apayrı klasörde.

---

## 0. Bugünün fotoğrafı (ölçülen gerçekler)

- Repo çalışma ağacı (`.git` hariç): **19GB** — bunun 2.2GB `supabase-server/`(çoğu volumes),
  1.3GB `node_modules`, 1.2GB `dist/`, 434MB `dist-gh` (üçü de git'te YOK, doğru).
- Git'te TAKİPLİ en büyük bloblar (tarihçe dahil, tekrarlı sürümler):
  `src/data/interactive_learning_decks.json` 82MB, `data/pastQuestions.json` 70MB,
  `src/data/pastQuestions.json` 60MB — her commit ~80MB şişiriyor, push'ta GH uyarısı veriyor.
- `data/` çalışma ağacı 380MB (en büyükler: `local_rag_chunks.json` 104MB [gitignore'lı ama takipte],
  `pastQuestions.json` 71MB, `*.bak*`/`*.backup*` ~70MB toplam, `lecture_notes.*` ~80MB).
- `src/data` 386MB (derleme için ŞART: 82MB deck + 74MB `decks/` + 71MB pastQuestions + 32MB lecture_notes …).
- Kodda okunan env anahtarı: **48 benzersiz isim** (envanter §6). Sabit yol varsayımı: 30+ nokta
  (`/home/indu/...`, `C:\Users\indui\...`, `127.0.0.1:809x`, `:11434`) — çoğu env override'lı, çalışıyor ama kirli.
- Tablolar: **14** (+2 RPC `match_rag_chunks_*`, +1 HNSW). Servisler: Oracle'da 3 (app) + 11 (supabase).
- `.env` cihaz 104 satır / Oracle 58 anahtar / `.env.example` 60 satır (şablon geride!).

## 1. Hedef şema

```
┌─ GitHub (temiz repo, ~150-250MB klon) ─────────────────────┐
│ kod + şema(migration) + şablon(.env.example) + tohum(seed) │
│ doc + deploy betikleri. VERİ YOK, SECRET YOK.              │
└───────────────┬────────────────────────────┬───────────────┘
        rsync kod            pg_dump/restore · sync-*.sh
                │                            │
┌───────────────▼────────────┐   ┌───────────▼────────────────┐
│ ORACLE (canlı)             │   │ CİHAZ (üretim masası)      │
│ ~/medsor/{meds,meds_db..}  │   │ /home/indu/medsor/{...}    │
│ local Supabase (büyük veri)│   │ local Supabase + GPU boru  │
└───────────────┬────────────┘   └───────────┬────────────────┘
                │  her fazda sayaç+md5       │  her fazda sayaç+md5
┌───────────────▼────────────────────────────▼────────────────┐
│ YEDEK (repo DIŞI, iki kopya):                              │
│  cihaz: /home/indu/medsor-yedek/<tarih>/ · Oracle: ~/meds-backup/<tarih>/ │
│  + Supabase Cloud (auth/realtime mirror, ücretsiz katman)  │
└────────────────────────────────────────────────────────────┘
```

## 2. Repoda KALACAKLAR (takip devam)

- `server.ts`, `src/`, `index.html`, `public/` (CNAME dahil), `vite.config.ts`, `package*.json`, `tsconfig`.
- `supabase/migrations/` (şema = kod; yeni migration buraya, sırayla).
- `meds/docs/` + `meds/deploy/oracle/*.md` + `AGENTS.md` tarafı doc'lar.
- `scripts/` (üretim boru hattı) — CİHAZDA çalışır; Oracle'a rsync'lenir ama çalıştırılmaz (etiketlenecek).
- `curriculum/`, `firebase.json`, `firestore.rules`, `vercel` yok.
- **Tohum (seed) dosyaları** — ilk açılışta boş DB'yi dolduran MİNİMAL set (tutulacak, küçük):
  `data/committees.json` (yoksa üretilecek — kurul listesi kodda sabit zaten),
  `data/interactive_decks_registry.json` (12KB), `data/drive_sync_settings.json` (575B).
  Kural: tohum ≤1MB, içinde kullanıcı verisi YOK.

## 3. Repodan ÇIKACAKLAR (takip dışı + `.gitignore`)

| Dosya/klasör | Boyut | Nereye taşınır | Not |
|---|---|---|---|
| `data/pastQuestions.json` + `src/data/pastQuestions.json` + `.bak*` | ~200MB | DB (`past_questions`) + yedek klasörü | ÜÇ kopya var! Tekilleştirilecek (§5) |
| `data/local_rag_chunks.json` | 104MB | Yeniden üretilir (indeks) — yedeklenmez | Zaten gitignore'lı ama takipte → `git rm --cached` |
| `data/lecture_notes*.json`, `*.backup*`, `*.bak*` | ~150MB | DB (`lecture_notes`) + yedek | Legacy yedekler ayıklanacak (son 1 jenerasyon yedeğe) |
| `data/*.json` geri kalanı (kullanıcı/jurnal: comments, votes, feedback, queue, notifications, music, users) | ~30MB | DB tabloları + yedek | Tablo karşılığı §5 matriksinde |
| `src/data/lecture_notes.json` (32MB), `ornek_sorular/` (15MB), `summaries/` (11MB), `kazanimlar/` (13MB) | ~70MB | **KARAR GEREKİR:** derlemede gömülüyor. Seçenek A: git-lfs. Seçenek B: derlemede DB/API'den çek (büyük refactor). Seçenek C: repo'da tut (pragmatik; bunlar kullanıcı verisi DEĞİL, müfredat içeriği) — **öneri: C + lfs yok** |
| `interactive_learning_decks.json` (82MB) | 82MB | Aynı: C (tek kaynak, derleme şartı) | Değişiklikte parça-commit (sıkıştırılamaz, kabul) |
| `get-pip.py` (kök) | 26bin satır | SİL (pip kurucusu, yanlışlıkla inmiş) | Tek komutluk temizlik |
| `models/`, `training_data/`, `linux/`, `.venv*/`, `dist*/`, `node_modules/` | — | Zaten ignore'lı, dokunma | |

`.gitignore` eklenecekler: `data/*.json` (tohum allowlist hariç: `!data/committees.json` vb.),
`src/data/*.bak*`, `*.dump`, `/meds_backup/`, `.env.oracle`, `deploy/oracle/*.token`.

## 4. Yedek düzeni (repo dışı)

- Cihaz: `/home/indu/medsor-yedek/<YYYYMMDD_HHMM>/` — `backup.sh` (DB dump `-Fc` + `data/*.json` tar.gz + `.env` ŞİFRELİ kopya + `supabase-server/.env` + `local-supabase-keys.json` + SHA256 manifest).
- Oracle: `~/meds-backup/<tarih>/` — aynı içerik, Oracle tarafı.
- Zamanlama: kod/veri değişikliğinden ÖNCE (her sync/deploy fazı başında otomatik), + haftalık cron.
- Saklama: son 4 tam + son 30 günün DB dump'ı (farklı boyut: tam ~350MB, rag_chunks-only ~250MB).
- Geri dönüş testi: 3 ayda bir yedekten BOŞ dizine restore provası (kanıt: sayaçlar).

## 5. Veri tekilleştirme + DB matriksi (hangi veri nerede yaşar)

| Veri | Bugün (dağınık) | Hedef (tek doğruluk kaynağı) | Senkron yönü |
|---|---|---|---|
| Çıkmış sorular | data+src/data+git+localDB+cloudDB (5 kopya!) | `past_questions` (local birincil, cloud mirror) | cihaz→Oracle (dump), Oracle→cihaz (çekme) |
| Güncel havuz | data/questions.json + localDB | `questions` (aynı) | aynı |
| Raporlar | JSON kolon (+yeni tablo) | `past_question_reports` + JSON kolon (çift yazma korunur) | aynı |
| Ders notları | 4 kopya | `lecture_notes` | aynı |
| RAG chunk+vektör | localDB (+cihaz cache) | localDB (`rag_chunks`), cache `meds_database/derived` (yedeklenir, git YOK) | `sync-vectors.sh` |
| Kullanıcılar | users.json+localDB+cloudDB+Firebase Auth | Firebase Auth (kimlik) + `users` (profil, çift mirror) | çift yönlü dikkat (uid çakışmaz) |
| Yorum/oy/feedback/müzik/bildirim | JSON dosyaları | JSON (cihaz+Oracle rsync) + ilgili DB kolonu varsa mirror | `sync-data.sh` (mevcut) |
| Öğren desteleri (82MB) | src/data (tek kaynak ✓) | DEĞİŞMEZ (repo'da kalır, §3-C) | kodla birlikte rsync |
| Drive ham PDF'ler | meds_downloads (683MB) | Disk (yedeklenir), git YOK (zaten yok) | tek seferlik + artımlı |

## 6. Key/secret envanteri ve saklama matrisi (DEĞERSİZ — yalnız isim+kural)

Kodun okuduğu 48 anahtar grupları:
- **AI (sunucu-tarafı, ASLA VITE_ ile):** `GEMINI_API_KEY`, `GEMINI_FREE_KEY_*`, `GEMINI_BILLED_KEY`,
  `GROQ_API_KEY[_2]`, `OPENROUTER_API_KEY`, `MUSE_SPARK_API_KEY/BASE_URL`, `OPENCODE_API_KEY`,
  `HF_TOKEN[_MEDS2|_MEDS3_WRITE]`, `MEDS_CMD_MODELS`, `MEDS_FREE_ONLY`, `MEDS_LLM_BACKEND`,
  `OLLAMA_URL/HOST`, `STUDIO_*`. Fallback sırası aiProvider'da sabit (Gemini→Groq→Spark→Ollama).
  **BULGU:** `src/services/api.ts` `import.meta.env.VITE_GEMINI_API_KEY` okuyor — istemciye anahtar
  sızma vektörü; plana alındı (§8-K3).
- **Supabase:** `SUPABASE_URL/KEY/SECRET/PUBLISHABLE` (klasik), `LOCAL_SUPABASE_*` (local),
  `CLOUD_SUPABASE_*` (online), `POSTGRES_*`, `JWT_SECRET/KEYS/JWKS`, `ANON_KEY`, `SERVICE_ROLE_KEY`,
  `DASHBOARD_*`, `VAULT_ENC_KEY`, `PG_META_CRYPTO_KEY`, `PGRST_*`, `KONG_*`, `S3_*`, `SMTP_*` (iki dosyada).
- **Site:** `MEDSORU_API_PASSWORD` (cihaz=Oracle AYNI olmalı — yazma kimliği),
  `APP_URL`, `EMAIL_FROM`, `NODE_ENV`, `PORT=3000` (değişmez).
- **Yollar:** `MEDS_PROJECT_ROOT/DATABASE_DIR/TEMP_DIR/DOWNLOADS_DIR/CORE_DIR/DEEPSEEK_DIR/TRANSCRIPTIONS_DIR`,
  `MEDS_DATABASE_V3_EXPORT/V3_RAG_CHUNKS/GEMINI_V3_METADATA_DIR`.
- **Arama:** `MEDS_EMBED_URL`, `MEDS_VECTOR_*` (6 anahtar), `MEDS_V2SEARCH_URL`, `MEDS_SEM_URL`.
- **Tunnel:** `CLOUDFLARE_TUNNEL_TOKEN` (yalnız Oracle `.env`, git YOK, yedekte ŞİFRELİ).

Saklama kuralları:
1. Üç kopya kuralı: her secret (a) çalıştığı makinenin `.env`inde, (b) şifreli yedekte, (c) SADECE insan-kaynaklı olanlar (API anahtarları) sağlayıcı konsolunda. Asla git'te, asla chat log'unda tam değer.
2. `.env` dosyaları: `meds/.env` (cihaz), `~/medsor/meds/.env` (Oracle) — ikisi de `deploy-code.sh`/`sync` dışında (exclude ✓). Şablon: `.env.example` (şu an 60 satır, 104 satırlık gerçeğin gerisinde → **güncellenecek**, değersiz).
3. Kayıp anahtar prosedürü: sağlayıcı konsolundan yenile → iki `.env`e işle → ilgili servisi restart → health kontrol. Parola (`MEDSORU_API_PASSWORD`) değişirse İKİ taraf aynı anda.
4. SSH: `ssh-key1.key` (cihaz→Oracle, `chmod 400`, repo DIŞI `/home/indu/medsor/` ✓) · GitHub SSH (cihazda) ·
   Oracle'da GitHub anahtarı YOK (rsync yolu; git-pull'a geçilirse salt-okunur deploy-key) · Cloudflare kimliği dashboard (token dosyası yok).

## 7. Kod değişiklik listesi (dosya:satır — hepsi env'leştirme, davranış aynı)

1. `server.ts:8158` `/home/indu/medsor/meds_database` → `MEDS_DATABASE_DIR` default'u ortama göre
   (`/home/ubuntu/...` Oracle'da; genel fallback `./meds_database`).
2. `src/services/localRagEngine.ts:40,262` (`C:\...`, `/home/indu/...deepseek`) → `MEDS_*` env (zaten çoğu var, eksikler eklenecek).
3. `src/services/geminiV3DataService.ts:5,9` → `MEDS_DATABASE_V3_EXPORT` (+yeni `MEDS_DEEPSEEK_META_DIR`).
4. `src/services/transcriptionService.ts:21`, `serverLectureNotes.ts:20` (C:\...) → `MEDS_*` (fallbacklar dursun, sıra: env→platform→legacy).
5. `server.ts:1327,1373,1388` (`:8092`, `:8093` servisleri) → Oracle'da YOK: istek gelirse zamanında düşmeli
   (mevcut try/catch + timeout korunacak; health'e "v2/sem kapalı" bilgisi eklenecek).
6. `aiProvider.ts:204`, `studioAiService.ts:15`, `autoErrorRepairEngine.ts:586` (`:11434` Ollama) →
   Oracle'da Ollama YOK: `generateResilientMedicalAi` zaten cloud'a düşüyor (doğrulandı) — kod değişmez,
   yalnız `MEDS_LLM_BACKEND=cloud` Oracle `.env`de sabitlenecek.
7. `scripts/semantic/deploy/meds-v2semantic.service:8-11` + `watchdog.py:231` (sabit `/home/indu` pathleri) →
   bu üniteler ORACLE DIŞI etiketlenecek (cihaz-only), Oracle imajına GİRMEYECEK (`.dockerignore` + doc).
8. `scripts/deck_generators/*` sabit `src/data/decks/items` pathleri → `MEDS_PROJECT_ROOT` göreli (cihazda çalışıyor, bozulmasın diye testli).
9. `Dockerfile.oracle`: `ARG VITE_ORACLE_API_URL` eklenecek (şu an kod-default `https://api...` çalışıyor ama
   build'e gömülmeli; apex tek-adres düzeninde `https://nofrostlife.com.tr` olacak).
10. `api.ts` içindeki `VITE_GEMINI_API_KEY` okuma (3 nokta) → KALDIRILACAK (istemciye secret gömülmesin;
    yerine `/api/ai/*` proxy kullanılacak — zaten var).

## 8. Docker/Supabase/AI/Oracle hata-matriksi (kesinti davranışı)

| Hat | Koparsa ne olur | Koruma (mevcut + eklenecek) |
|---|---|---|
| Tunnel (cloudflared) | Site dışarı kapalı, API GH Pages'ten de ölür | `restart:unless-stopped` ✓ + health'e tunnel durumu + GH Pages yedek DNS talimatı (doc) |
| meds-server | 502 | `unless-stopped` ✓ + `/api/health` + `deploy-code.sh --build` tek komut kurtarma |
| supabase-local (db/rest) | Vektör+mirror durur, JSON okuma SÜRER (site açık) | Kodda try/catch fallback ✓ (doğrulandı) + `db-audit.ts` cron (günde 1, log) |
| supabase-online | Auth/realtime aksar, local SÜRER | Aynı fallback (ters yön) — test edilecek (faz 4) |
| meds-embed | Vektör kolu BM25'e düşer (site açık, kalite düşer) | Mevcut sessiz-fallback ✓ + model volume kalıcı ✓ |
| Ollama (cihaz) | Oracle etkilenmez (hiç bağlı değil) | — |
| AI anahtarları biterse | AI özellikleri durur, CRUD sürer | 4-katman fallback ✓ + kota alarmı (öneri: `/api/health`e AI katman durumu) |
| Disk dolarsa (%66→) | Önce build cache, sonra DB yazamaz | `builder prune` cron + 80% alarm eşiği (öneri) + log rotation ✓ var |

Kaynak limitleri (EKLENECEK — şu an YOK, siteyi komşu işten korur):
`meds-server: cpus 1.5, mem 3G` · `meds-embed: cpus 1.0, mem 3G` · `supabase-db: mem 2G` (compose `deploy.resources.limits`).

## 9. Faz planı (sırayla, her faz bağımsız geri dönüşlü)

- **F0 — Tam yedek + sayaçlar (1 saat):** `backup.sh` yazılır; cihaz+Oracle tam yedek; sayaç manifestosu
  (pq=5713, chunks=70752/bge=62967, decks=114, md5 listesi). Doğrulama: yedekten BOŞ klasöre açma provası.
- **F1 — Repo temizliği (2 saat):** `.gitignore` (§3) → `git rm --cached` (SADECE listeye uygunlar) →
  tohum dosyaları yazılır → commit+push. Doğrulama: fresh `git clone` + `npm ci` + `tsc` + `vite build` GEÇER
  (CI'da da). Geri dönüş: `git revert`.
- **F2 — Kod env'leştirme (§7, 1-2 gün):** dosya dosya, her biri `tsc`+uç test. Davranış değişmez.
  Doğrulama: cihaz `npm run dev` + Oracle `deploy-code.sh --build` ikisi de yeşil.
- **F3 — Secret düzeni (§6):** `.env.example` tamamlama (104 satırın değersiz karşılığı) +
  `.env.oracle.example` güncelleme + parola-parite kontrol betiği. Doğrulama: iki `.env` anahtar-diff'i
  (değer YOK, isim var) + health iki tarafta.
- **F4 — DB ayrıştırma:** `sync-data.sh` (JSON) + `sync-vectors.sh` (rag) + yeni `sync-db.sh`
  (kalan tabloların dump/restore'u) + yön kuralı doc'a (son-yazan-kazanır + çakışma yasağı).
  Doğrulama: `db-audit.ts` 9/9 + sayaç eşitliği.
- **F5 — Docker sertleştirme (§8):** limitler, backup cron, prune cron, audit cron, tunnel-health.
  Doğrulama: `docker stats` + 7 günlük gözlem.
- **F6 — Yedek provası + final:** F0 yedeğinden tam restore provası (ayrı dizin), yol haritası kapatma,
  `DEGISIKLIK_KAYDI` + `SISTEM_MIMARISI` güncelleme.

## 10. Yasaklar ve kritik uyarılar

1. `.env*` asla `git add` edilmez (`.gitignore` + `deploy-code.sh` exclude + commit-öncesi `git status` bak).
2. Token/parola chat'e YALNIZ ilk kurulumda, sonrasında YOK (rotasyon prosedürü §6-3).
3. `down -v` supabase dizininde YASAK (config volume'leri siler) — yalnızca `down`.
4. İki tarafta aynı anda yazma YASAK (önce çek/bildir, sonra yaz).
5. `src/data/decks/items/` ve `interactive_learning_decks.json` tek-kaynak kuralı korunur (AGENTS.md).
6. Oracle'da GPU/Ollama varsayan script ÇALIŞTIRILMAZ (watchdog, pipeline_runner, training).
7. Her faz bitmeden SONRAKİ faza geçilmez; sayaç tutmuyorsa faz BAŞARISIZDIR.

## 11. Açık kararlar (kullanıcı onayı gereken)

- K1: `src/data` büyükleri repo'da mı (C) / lfs mi / API'den mi? Öneri: C.
- K2: Geçmiş git şişkinliği temizlensin mi (filter-repo)? Öneri: HAYIR (risk > fayda).
- K3: `VITE_GEMINI_API_KEY` istemci okuması kaldırılsın mı? Öneri: EVET (F2'de).
- K4: Yedek şifreleme parolası nerede saklansın? Öneri: cihazda kâğıt + Oracle `.env`de DEĞİL ayrı dosya.
- K5: Otomatik deploy (GitHub→Oracle SSH) açılsın mı? Öneri: secrets girilince EVET, rsync birincil kalır.

---

## 12. Revizyon (2026-10-11, gece) — Tam proje toparlama kapsamı

> Kontrol sonucu: §0–§11 **repo + Oracle + secret** ekseninde doğru ve geçerli; ancak plan yalnız `meds/` repo'sunu
> kapsıyor. Repo DIŞI kök klasör, cihaz servisleri, derleme birikimi, Oracle trafik yükü ve hata-önleme kapıları
> eksikti. Aşağıdaki T-fazları F-fazlarını **tamamlar**, yerine geçmez. Ölçümler 2026-10-11 gece (salt-okunur).

### 12.1 Düzeltmeler / eksik bulgular (ölçülen)

| # | Bulgu | Ölçüm | Etki |
|---|---|---|---|
| B1 | `vite.config.ts:33` `emptyOutDir: false` → her derleme hash'li parçaları biriktiriyor | `dist/assets` **9420 dosya, 1.2GB** | Oracle imajı/rsync şişer, disk dolar (§8 disk satırı bunu atlamış) |
| B2 | Kök (`/home/indu/medsor/`) dağınık: 12 `patch_*/fix_*/apply_*/update_builder.py`, `scripts/` (208 tek seferlik betik, `apply_web_grounded_party1..22` vb.), `src/data/decks` (başıboş), `packages/` (13 — asıl yer `meds/src/data/decks/packages` 30), `splash_box*.png`, `rag-project/` (venv) | — | Hangi dosya canlı belli değil, ajanlar yanlış yere yazıyor |
| B3 | `ssh-key1.key` proje kökünde (izin 400 ✓ ama proje ağacında) | — | Yanlış rsync/zip ile sızma riski → `~/.ssh/` |
| B4 | `yedek/` **1.2GB** proje içinde (§4'teki "repo dışı yedek" hedefine aykırı); `meds_temp/supabase_local.dump` 330MB, `meds_database/backups` 72MB, `meds/data/*.backup*` 6 dosya | — | Yedek ≠ çalışma verisi; sync'e karışıyor |
| B5 | Veri klasörü sayısı: `meds_database`, `_v2`, `_core`, `_v3_export`, `meds_export`, `meds_temp`, `meds_downloads` (7) | 1.2G+168M+122M+18M+106M+940M+682M | Tek-kaynak belirsiz; §5 matrisi yalnız repo verisini kapsıyor |
| B6 | Cihazda 12 `meds-*` servis: üç ayrı vektör sunucusu (`meds-embed` :8091, `meds-v2search`, `meds-v2semantic`), GPU (RTX 4060) var ama `.env` ile kapalı (`MEDS_DISABLE_GPU`); `meds-phases` elle kipte boşta, `meds-watchdog` olmayan `meds-ollama` konteynerini denetliyor; :8094 bge-m3 süreci ünitesiz (yeniden başlatmada düşer) | — | RAM/CPU israfı, arıza yüzeyi |
| B7 | Belge dağınıklığı: kökte 6 md (`GEMINI.md`≠`AGENTS.md`, `INTERAKTIF_OGRENME_REHBERI.md` ↔ `meds/docs/OGREN_ETKILESIM_REHBERI.md`), `DEGISIKLIK_KAYDI.md` 1412 satır/216KB | — | Ajan bağlamı şişer, çelişen kurallar |
| B8 | Oracle'da istek başına büyük JSON: deste 82MB kaynak, `pastQuestions` 71MB, `kazanimlar/k1.json` bölünmedi (kayıt satır 43) | decks önbelleksiz 1–1.7s | Tünel + CPU yükü |

### 12.2 T-fazları (F-fazlarıyla birlikte sıra)

Başlama koşulu (hepsi): paralel oturum boşta · `meds/` git ağacı temiz/commit'li · uzun rsync/derleme yok.
Kalıcı silme her zaman **önce `/home/indu/medsor-yedek/<tarih>/`e taşı → 7 gün gözlem → onayla sil**.

- **T0 — Tam envanter (salt-okunur, her an):** her dosya/klasör için "canlı mı" tespiti: kod referansı (grep `server.ts`,
  `src/`, `scripts/`, systemd `ExecStart`, compose), son değişim tarihi, boyut. Çıktı: `meds/docs/ENVANTER.md` tablosu
  (KALIR / TAŞI / ARŞİVLE / SİL-ADAYI). Kullanıcı onayı bu tablo üzerinden alınır.
- **T1 (= F0) — Yedek:** F0'a ek olarak `yedek/` klasörü repo dışına (`/home/indu/medsor-yedek/`) taşınır; `ssh-key1.key` → `~/.ssh/`
  (`deploy-code.sh`/`sync-*.sh` yol güncellemesiyle aynı adımda).
- **T2 — Kök temizliği:** kökte yalnız `meds/`, veri klasörleri, `AGENTS.md`, `PROJE_TANITIMI.md`, `DEGISIKLIK_KAYDI.md` kalır.
  Tek seferlik betikler → `meds/scripts/archive/<tarih>/`; başıboş `src/`, `packages/` → içerik `meds/src/data/decks/packages` ile
  diff'lenir, fark yoksa arşiv. `get-pip.py`, `.commandcode/` → sil-adayı.
- **T3 (F1 ile birlikte) — Derleme birikimi:** `emptyOutDir` false kalabilir (eski SW istemcileri için) ama `scripts/prune-dist.mjs`:
  son 2 derlemenin manifest'inde olmayan + 7 günden eski parçaları siler; `deploy-code.sh --build` sonunda çağrılır. Hedef dist < 250MB.
- **T4 (F4 ile birlikte) — Veri klasörü birleştirme:** hedef 3 kök: `meds_downloads/` (ham, salt-ekle), `meds_work/` (= temp1-3 + state + logs,
  yeniden üretilebilir), `meds_database/` (yayın; `v2`, `core`, `v3_export`, `export` alt klasör olarak). Önce env değişkeni + symlink
  ile geçiş (kod kırılmaz), betikler yeni yola çekildikten sonra symlink kalkar. `supabase_local.dump` ve `backups/` → yedek klasörü.
- **T5 — Cihaz servis sadeleştirme:** üç vektör sunucusu tek `meds-embed`'e (e5 + FAISS tek süreç) birleştirme değerlendirmesi;
  GPU yoksa `meds-gpuguard`/`meds-phases` GPU adımları devre dışı (ünite `Condition`). Her servis `MemoryMax`/`CPUQuota`.
  **Çalışan servis durdurmak/değiştirmek kullanıcı onaylı.**
- **T6 — Oracle yük azaltma:** (a) statik `dist/assets` için `Cache-Control: public, max-age=31536000, immutable` + Cloudflare önbellek
  kuralı (tünelden geçmeden kenarda sunulur); (b) büyük JSON'lar için ön-sıkıştırılmış `.br` dosyası + ETag/304; (c) `kazanimlar` ve
  `pastQuestions` ders/kurul bazlı parçalama (istemci yalnız açtığını çeker); (d) `/api/decks` ve arama sonuç önbelleği (LRU, TTL);
  (e) `/similar` gibi yavaş uçlara zaman aşımı + istemci iptali. Doğrulama: aynı 10 istek seti önce/sonra süre + Oracle CPU.
- **T7 — Hata önleme kapıları:** tek komut `npm run check` = `tsc` + `validate_learning_decks.py` + pastQuestions şema doğrulayıcı
  (5 şık, cevap ∈ şıklar, kurul kodu biçimi, tekil id) + `db-audit.ts` + 375px taşma testi (mümkünse Playwright). `deploy-code.sh`
  bunu geçmeden derlemez. Veri yazan her betik atomik yazım + yazım öncesi otomatik yedek kullanır (ortak yardımcı).
- **T8 — Belge sadeleştirme:** `DEGISIKLIK_KAYDI.md` → son 14 gün kalır, eski girdiler `meds/docs/kayit_arsivi/YYYY-MM.md`;
  `GEMINI.md`/`INTERAKTIF_OGRENME_REHBERI.md` kuralları `AGENTS.md`/rehbere birleştirilir (çelişki listesi kullanıcıya);
  `PROJE_TANITIMI.md` yeni klasör düzeniyle güncellenir.
- **T9 (= F6) — Son doğrulama:** sayaçlar (pq=5713, deste=114, chunks=70752/bge 62967) + `npm run check` + Oracle health/deste/arama
  + fresh clone derlemesi. `SISTEM_MIMARISI.md` ve bu dosya kapatılır.

Önerilen sıra: T0 → T1/F0 → T2 → F1+T3 → F2 → F3 → F4+T4 → T5 → F5+T6 → T7 → T8 → T9.
Her faz sonunda `DEGISIKLIK_KAYDI.md`'ye kayıt; sayaç tutmazsa durulur.

### 12.3 İlerleme (2026-10-11 gece)

- **T0 ✓** `meds/docs/ENVANTER.md` (öneri tabloları + §9'da 14 karar kalemi).
- **T1/F0 ✓** `deploy/backup.sh` → `/home/indu/medsor-yedek/20261011_2008/` (db.dump 345MB + data + src_data, SHA256 ✓, pg_restore listesi 63 tablo, geri açma provası pq=5713). Secret'lar K4 kararına kadar yedeğe girmez.
  Proje dışına taşınan 1.8GB (`yedek/`, `supabase_local.dump`, `ozet_satir_yedek`, `meds_database/backups`, iki `.bak_manual_import`) — liste: `medsor-yedek/proje_disina_tasinan_20261011/TASINANLAR.tsv`. SSH anahtarı `~/.ssh/medsor-oracle.key` (deploy-code/sync-vectors/SISTEM_MIMARISI güncel, SSH doğrulandı).
- **T2 (kısmi) ✓** kök `patch_*/fix_*/apply_fixed/update_builder.py` + başıboş `src/` → `medsor-yedek/arsiv_kok_20261011/`. Kök `scripts/` ve `packages/` BEKLİYOR (k1-30…42 paketleri yanlış cwd yüzünden köke yazılmış; önce paket yeniden üretim kararı).
- **T3 ✓** `scripts/prune-dist.mjs` (erişilebilirlik BFS + son 2 derleme defteri + 24s tampon); `postbuild` ve `build:gh-pages` sonuna bağlandı. dist 1.2GB→459MB, dist-gh 434→111MB. §12.2'deki "7 gün" kuralı yerine derleme-sayısı kuralı (bayatların hepsi <7 gün olduğu için).
- **deploy-code.sh rsync** artık `/.env.*`, `*.bak*`, `*.backup*`, `get-pip.py`, `.agents/.claude/.github`, `scripts/archive`, `scripts/semantic/data` göndermiyor.
- **Oracle'da bekleyen (kullanıcı eli/izni):** önceki rsync artıkları uygulama ağacında duruyor: `.env.cloud.bak` (secret kopyası), `src/data/pastQuestions.json.bak_manual_import` 61MB, `scripts/semantic/data` 108MB, `.agents` + `.claude` 2×20MB → `~/meds-backup/`e taşınmalı.
- Doğrulama: validator 114 deste 0 HATA · tsc 0 · yerel+canlı health 200.

### 12.4 İlerleme (2026-10-11 gece, devam) — kullanıcı kararları uygulandı

- K/kararlar: eğitim ortamı silindi · GH Pages kaldırıldı · yerel GPU yasak · kelime 60–250 · kalıcı CPU embed servisi.
- T2 ✓ (paketler tek kaynağa bağlandı, kök `packages/` arşivde) · T3 ✓ · T5 kısmi ✓ (GPU servisleri kalktı; embed birimleri sınırlı; 3 vektör sunucusu birleştirme hâlâ açık) · T6 kısmi ✓ (kaynak tavanları; önbellek/parçalama açık) · T8 kısmi ✓ (kural belgeleri birleşti; kayıt arşivleme açık).
- Yeni araçlar: `deploy/backup.sh`, `deploy/oracle/db-yonet.sh`, `scripts/db_analiz/analiz.py`, `scripts/build_deck_packages.py`, `scripts/prune-dist.mjs`.
- Açık: T4 (veri klasörü birleştirme), T7 (`npm run check` kapısı + CSS sınıf çakışma denetimi), F1 (git'ten büyük veri çıkarma), F2 (env'leştirme), Oracle'da `--delete`li kod eşitleme, DB analizi → birleştirme/silme (kullanıcı en sona bıraktı).

### 12.5 Ders işçisi (2026-10-12)

- Drive izleme → taslak (Oracle, `meds-ders-isci`, Claude aboneliği, 01–08) → Yönetim "Yeni dersler" onayı → **B2 yayın ✓** (`scripts/ders_isci/yayinla.py`, cihazda; yayın kaydı `scripts/ders_isci/yayin_kaydi.json`). İlk yayın: k1-67 Gebelik Hastalıkları.
- Site verisi yazarları toptan ezmeye karşı korundu: s16 site dışa aktarımı yalnız upsert, s15 kapalı (`MEDS_S15_ZORLA=1`), s13/learn_links/checklist yayın kaydına saygılı.
- Açık: hastalık önerilerini şema 2'ye çevirip `diseases.json`'a ekleme; yayını Oracle'da otomatik çalıştırma (şimdilik cihazda, onaydan sonra elle); e5 RAG vektörlerinin yeniden üretimi.
