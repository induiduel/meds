# MedSoru

Tıp Fakültesi Dönem 3 kurul sınavları için ortak soru havuzu. Öğrenciler sınavdan çıkınca
hatırladıkları parçaları girer ("ACE inhibitörü kuru öksürük sorusu çıktı"); sistem fakültenin
kendi ders materyallerinde (slayt, PDF, özet, amfi kaydı) ve çıkmış sorularda ilgili yeri bulur,
soruyu bu kaynaklara dayanarak yeniden kurar.

## Açık veri API'si

Giriş gerektirmeyen, salt okunur veri API'si `/v1/` altında sunulur. Kurullar, güncel ve
çıkmış sorular, ders notları, özetler, öğrenme bağlantıları ve arama için tüm yollar, filtreler
ve örnekler [API kataloğunda](docs/API_KATALOG.md) yer alır.

## Nasıl çalışır

```
Öğrenci parçası ──► RAG arama (BM25, yerel indeks) ──► en alakalı kaynaklar
                                                        │  çıkmış soru / slayt / özet / amfi kaydı
                                                        ▼
                                 AI (Gemini → Groq yedek) soruyu kaynaklara dayanarak kurar
                                                        │
                                                        ▼
                         Soru kökü + 5 şık + açıklama + "Dayandığı kaynaklar"
```

1. **Ders materyali yükleme:** Admin, ders notlarını (PDF/PPTX → sayfa metni) yükler
   (`POST /api/lecture-notes`, masaüstü klasör tarayıcısı veya Drive senkron scriptleri).
   Veri `data/lecture_notes.json` içinde tutulur.
2. **İndeksleme:** `src/services/localRagEngine.ts` çıkmış soruları, slayt sayfalarını, özetleri ve
   transkriptleri parçalara (chunk) böler ve bellekte BM25 indeksi kurar. Türkçe için karakter
   katlama (ö→o, ı→i), tam kelime ve 5 harflik kök birlikte kullanılır; "böbreğin", "bobrek", "böbrekte" aynı terime düşer.
   İndeks server açılışında ve yeni ders notu yüklendiğinde yenilenir.
3. **Arama:** `src/services/ragService.ts` → `searchRagChunks`. Sadece insan yazımı kaynaklar
   (çıkmış soru, slayt, özet, transkript) döner; AI'nın kendi önceki çıktıları kaynak sayılmaz.
   Aynı destenin tekrar yüklenmiş kopyaları tekilleştirilir.
4. **Soru kurma:** Aşağıdaki akışların hepsi bulunan kaynakları prompt'a koyar. Rekonstrüksiyon ve
   "AI ile tamamla" ayrıca AI'dan hangi kaynağa dayandığını (`usedSources`) ister ve bunu arayüzde gösterir:

| Özellik | Endpoint |
|---|---|
| Rekonstrüksiyon (ana buton) | `POST /api/questions/:id/ai-reconstruct` |
| Soruyu düzenle / optimize et | `POST /api/ai/optimize-question` |
| Katkı ekranında "AI ile tamamla" | `POST /api/ai/quick-assist` |
| Gelişmiş soruya yükselt | `POST /api/ai/upgrade-advanced-question` |
| Slayttaki "soru sor" kutusu | `POST /api/rag/ask` |
| Katkı ekranında "Geçmiş sınavlarda benzer sorular" (AI yok, sadece arama) | `POST /api/past-questions/similar` |

## Çıkmış soru dosyalarını eşleştirme

```bash
npx tsx scripts/link-exam-questions.mts <dosya-veya-klasör> --out rapor.json
```

PDF/DOCX içindeki soruları ayırır (sınav sistemi çıktısı, numaralı liste, satır içi şıklar) ve her soru için:
havuzda aynısı var mı (`same` / `likely` / `new`), en benzer çıkmış sorular ve ilgili ders slaytı/özeti.
AI kullanmaz. Taranmış (metin katmanı olmayan) PDF'ler "OCR gerekli" olarak raporlanır.

Not: `data/lecture_notes.json` içine "ders notu" olarak yüklenmiş sınav dosyaları (sayfalarının çoğu soru olan
notlar) otomatik ayıklanır ve ders materyali olarak gösterilmez (`ragService.getExamDumpNoteIds`).

## Mimari

| Katman | Yer | Not |
|---|---|---|
| Frontend | `src/` (React 19 + Vite + Tailwind 4) | GitHub Pages'e deploy edilir |
| Backend | `server.ts` (Express, port 3000) | Yerel PC'de çalışır, Cloudflare tunnel ile dışarı açılır |
| AI sağlayıcı | `src/services/aiProvider.ts` | Gemini key havuzu → Groq yedek. Key'ler **sadece** server `.env`'inde |
| RAG | `src/services/localRagEngine.ts`, `src/services/ragService.ts` | Yerel BM25; sonuç yoksa Supabase pgvector |
| Veri | `data/*.json`, Supabase, Firebase | Yerel JSON birincil, buluta mirror edilir |
| Scriptler | `scripts/` | Tek seferlik veri işleme (OCR, Drive senkron, deck üretimi) |

Tarayıcı hiçbir zaman AI sağlayıcısını doğrudan çağırmaz; tüm AI istekleri backend'den geçer
(`POST /api/ai/generate` genel proxy). Frontend server'a ulaşamazsa AI özellikleri çalışmaz.

## Kurulum

```bash
npm install
cp .env.example .env     # key'leri doldur
npm run dev              # http://localhost:3000 (Vite middleware ile)
```

- `npm run build`: frontend'i `dist/`e derler. `dist/` varsa server production modunda onu sunar.
- `npm run lint`: `tsc --noEmit`
- `npm run rag:index`: Supabase'e embedding yükler (opsiyonel bulut arama için)

GitHub Pages'teki frontend, Ayarlar'dan girilen özel API adresi (tunnel URL'i) üzerinden
yerel server'a bağlanır (`src/services/api.ts` → `getCustomApiUrl`).

## Bilinen eksikler

- **Yetkilendirme zayıf:** `requireAdmin` sadece `x-admin-email` header'ına bakıyor ve loopback IP'ye
  izin veriyor; tunnel trafiği loopback'ten geldiği için pratikte açık. AI endpoint'lerinde
  rate limit yok.
- **Veri kirli:** aynı desteler birden fazla kez yüklenmiş, "ders notu" havuzunda çıkmış soru PDF'leri ve
  WhatsApp dökümleri (kişisel veri içerebilir) var, sayfaların ~%13'ü boş (OCR başarısız).
- `server.ts` hâlâ ~4.8k satır; route modüllerine bölünmeli.
- Eski git geçmişinde sızdırılmış API key'leri var; ilgili key'ler iptal edilmeli.
