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
