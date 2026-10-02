/**
 * ==============================================================================
 * DeepSeek Data Ingestion, Attribution & RAG Chunking Service
 * (src/services/deepseekDataService.ts)
 * ==============================================================================
 * Bu servis:
 * 1. C:\Users\indui\Desktop\meds_database\deepseek_data klasöründeki tüm dosyaları
 *    (.json, .md, .txt vb.) otomatik olarak okur ve ayrıştırır.
 * 2. DeepSeek tarafından düzenlenmiş/üretilmiş tüm verilere açıkça kaynak ve katkı
 *    etiketi ekler (source: 'deepseek', contributor: 'DeepSeek AI', isContribution: true).
 * 3. Verileri türlerine göre sınıflandırır (soru, özet, klinik vaka, spot bilgi vb.)
 *    ve sistem veri tabanına (data/deepseek_contributions.json) kaydeder.
 * 4. RAG sistemine 'deepseek_contribution' kategorisinde optimize parçalar (chunks)
 *    olarak aktarır ve tüm yapay zeka modelleri (Gemini, Groq DeepSeek, Claude vb.)
 *    tarafından öncelikli zeminleme kaynağı olarak kullanılmasını sağlar.
 * 5. Klasörü anlık olarak izler (watch); yeni dosya bırakıldığında otomatik işler.
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
export const DEEPSEEK_DATA_DIR = process.env.MEDS_DEEPSEEK_DIR || 'C:\\Users\\indui\\Desktop\\meds_database\\deepseek_data';
const DEEPSEEK_CONTRIBUTIONS_FILE = path.resolve(DATA_DIR, 'deepseek_contributions.json');

export interface DeepSeekItem {
  id: string;
  source: 'deepseek';
  contributor: string;
  isContribution: true;
  attributionBadge: string;
  itemType: 'question' | 'summary' | 'note' | 'pearl' | 'chunk' | 'raw_text';
  committeeId?: string;
  discipline?: string;
  topic?: string;
  title: string;
  content: string;
  rawPayload?: any;
  metadata: {
    sourceFile: string;
    fileFormat: string;
    importedAt: string;
    targetRole?: string;
    model?: string;
    stem?: string;
    options?: any[];
    correctAnswer?: string;
    explanation?: string;
    tags?: string[];
    [key: string]: any;
  };
  hash: string;
  createdAt: string;
  updatedAt: string;
}

export interface DeepSeekSyncResult {
  success: boolean;
  filesScanned: number;
  itemsIngested: number;
  chunksCreated: number;
  fileList: string[];
  lastSyncedAt: string;
  message: string;
}

function hashText(text: string): string {
  return crypto.createHash('md5').update(text.trim()).digest('hex');
}

// In-memory store
let cachedDeepSeekItems: DeepSeekItem[] = [];
let lastSyncTimestamp: string | null = null;
let isScanning = false;

/**
 * Load cached contributions from data/deepseek_contributions.json
 */
export function loadDeepSeekContributions(): DeepSeekItem[] {
  if (cachedDeepSeekItems.length > 0) return cachedDeepSeekItems;

  if (fs.existsSync(DEEPSEEK_CONTRIBUTIONS_FILE)) {
    try {
      const raw = fs.readFileSync(DEEPSEEK_CONTRIBUTIONS_FILE, 'utf-8');
      cachedDeepSeekItems = JSON.parse(raw);
      return cachedDeepSeekItems;
    } catch (e: any) {
      console.warn('[DeepSeekService] deepseek_contributions.json okunamadı:', e.message);
    }
  }
  return [];
}

/**
 * Save items to data/deepseek_contributions.json
 */
export function saveDeepSeekContributions(items: DeepSeekItem[]): void {
  try {
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    fs.writeFileSync(DEEPSEEK_CONTRIBUTIONS_FILE, JSON.stringify(items, null, 2), 'utf-8');
    cachedDeepSeekItems = items;
  } catch (e: any) {
    console.error('[DeepSeekService] Dosya kaydedilemedi:', e.message);
  }
}

/**
 * Ensure the target directory exists and has a README descriptor
 */
export function ensureDeepSeekFolder(): void {
  try {
    if (!fs.existsSync(DEEPSEEK_DATA_DIR)) {
      fs.mkdirSync(DEEPSEEK_DATA_DIR, { recursive: true });
    }

    const readmePath = path.join(DEEPSEEK_DATA_DIR, 'README_KULLANIM_KILAVUZU.md');
    if (!fs.existsSync(readmePath)) {
      const guide = `# MedSoru DeepSeek Veri Havuzu (deepseek_data)

Bu klasör, **DeepSeek AI** tarafından analiz edilmiş, düzenlenmiş, redakte edilmiş veya özetlenmiş tüm tıbbi verilerin toplanma alanıdır.

### Desteklenen Dosya Formatları:
1. **JSON Formatı (.json):**
   - **Soru Havuzu:** \`[ { "stem": "Soru metni...", "options": [{"key":"A","text":"..."}, ...], "correctAnswer": "A", "explanation": "Açıklama...", "discipline": "Tıbbi Patoloji", "committeeId": "donem3-kurul1" } ]\`
   - **Hazır RAG Parçaları:** \`[ { "title": "...", "content": "...", "discipline": "...", "committeeId": "..." } ]\`
   - **Ders Özetleri:** \`{ "title": "...", "discipline": "...", "content": "..." }\`

2. **Markdown Formatı (.md):**
   - Başlıklar (\`#\`, \`##\`), soru kökleri, seçenekler veya amfi ders notu özetleri.
   - Her başlık otomatik olarak mantıksal RAG parçalarına (chunk) ayrılır.

3. **Düz Metin Formatı (.txt):**
   - Paragraflar ve boşluklarla ayrılmış tıbbi notlar veya soru taslakları.

### Sistem Nasıl İşler?
- Bu klasöre bir dosya eklediğinizde veya güncellediğinizde sistem **otomatik olarak algılar**.
- Tüm verilere **"DeepSeek Katkısı"** etiketi (\`source: 'deepseek'\`, \`contributor: 'DeepSeek AI'\`) verilir.
- Veriler anında **RAG Vektör Arama Motoru** içine entegre edilir.
- Soruların yeniden düzenlenmesi veya sınav çözümlerinde **tüm yapay zeka modelleri (Gemini, Groq DeepSeek, Claude)** bu toplanan verileri birincil zeminleme (ground truth) olarak referans alır.
`;
      fs.writeFileSync(readmePath, guide, 'utf-8');
    }
  } catch (err: any) {
    console.warn('[DeepSeekService] deepseek_data klasörü kontrol uyarısı:', err.message);
  }
}

/**
 * Parse a JSON file and extract DeepSeek items
 */
function parseJsonFile(filePath: string, fileName: string): DeepSeekItem[] {
  const items: DeepSeekItem[] = [];
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const parsed = JSON.parse(raw);
    const now = new Date().toISOString();

    const processObject = (obj: any, index: number) => {
      if (!obj || typeof obj !== 'object') return;

      const stem = obj.stem || obj.question || obj.soru || obj.soruKoku || '';
      const content = obj.content || obj.text || obj.ozet || obj.not || '';
      const title = obj.title || obj.baslik || obj.topic || (stem ? stem.slice(0, 60) + '...' : `DeepSeek Katkısı #${index + 1}`);
      const discipline = obj.discipline || obj.brans || obj.ders || 'Tıp';
      const committeeId = obj.committeeId || obj.kurulId || obj.kurul || 'donem3-kurul1';

      let itemType: DeepSeekItem['itemType'] = 'chunk';
      let fullContent = '';

      if (stem) {
        itemType = 'question';
        const opts = obj.options || obj.siklar || [];
        const optLines = Array.isArray(opts)
          ? opts.map((o: any) => typeof o === 'string' ? o : `${o.key || o.label || ''}) ${o.text || ''}`).join('\n')
          : '';
        const claim = obj.correctAnswer || obj.dogruCevap || obj.claimedAnswer || '';
        const expl = obj.explanation || obj.aciklama || '';

        fullContent = `[DEEPSEEK KATKILI TIP SORUSU]
Ders / Branş: ${discipline}
Kurul: ${committeeId}
Konu: ${title}
Soru Kökü:
${stem}

Seçenekler:
${optLines}

Doğru Cevap: ${claim}
${expl ? `\nDeepSeek Tıbbi Analizi & Açıklaması:\n${expl}` : ''}`.trim();
      } else if (content) {
        itemType = 'summary';
        fullContent = `[DEEPSEEK TIP ÖZETİ & DERS NOTU]
Ders: ${discipline}
Kurul: ${committeeId}
Başlık: ${title}
İçerik:
${content}`.trim();
      } else {
        fullContent = JSON.stringify(obj, null, 2);
      }

      const h = hashText(fullContent);
      items.push({
        id: obj.id || `deepseek-${h.slice(0, 10)}`,
        source: 'deepseek',
        contributor: 'DeepSeek AI',
        isContribution: true,
        attributionBadge: 'DeepSeek Katkısı',
        itemType,
        committeeId,
        discipline,
        topic: obj.topic || title,
        title,
        content: fullContent,
        rawPayload: obj,
        metadata: {
          sourceFile: fileName,
          fileFormat: 'json',
          importedAt: now,
          stem: stem || undefined,
          options: obj.options || undefined,
          correctAnswer: obj.correctAnswer || obj.dogruCevap || undefined,
          explanation: obj.explanation || obj.aciklama || undefined,
          tags: obj.tags || ['deepseek', 'tıp']
        },
        hash: h,
        createdAt: now,
        updatedAt: now
      });
    };

    if (Array.isArray(parsed)) {
      parsed.forEach((obj, idx) => processObject(obj, idx));
    } else if (typeof parsed === 'object') {
      if (Array.isArray(parsed.questions || parsed.sorular)) {
        (parsed.questions || parsed.sorular).forEach((q: any, idx: number) => processObject(q, idx));
      } else if (Array.isArray(parsed.chunks || parsed.parcalar)) {
        (parsed.chunks || parsed.parcalar).forEach((c: any, idx: number) => processObject(c, idx));
      } else {
        processObject(parsed, 0);
      }
    }
  } catch (err: any) {
    console.warn(`[DeepSeekService] JSON okuma hatası (${fileName}):`, err.message);
  }
  return items;
}

/**
 * Parse a JSONL file and extract DeepSeek items (one JSON per line)
 */
function parseJsonlFile(filePath: string, fileName: string): DeepSeekItem[] {
  const items: DeepSeekItem[] = [];
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const lines = raw.split('\n').map(l => l.trim()).filter(Boolean);
    const now = new Date().toISOString();

    for (let idx = 0; idx < lines.length; idx++) {
      try {
        const obj = JSON.parse(lines[idx]);
        if (!obj || typeof obj !== 'object') continue;

        const stem = obj.stem || obj.question || obj.soru || obj.soruKoku || '';
        const content = obj.content || obj.text || obj.ozet || obj.not || obj.explanation || '';
        const title = obj.topic || obj.title || obj.baslik || (stem ? stem.slice(0, 60) + '...' : `DeepSeek Soru #${idx + 1}`);
        const discipline = obj.discipline || obj.brans || obj.ders || 'Tıp Bilimleri';
        const committeeId = obj.committeeId || obj.kurulId || obj.kurul || 'donem3-kurul1';

        let itemType: DeepSeekItem['itemType'] = 'question';
        let fullContent = '';

        if (stem) {
          const opts = obj.options || obj.siklar || [];
          const optLines = Array.isArray(opts)
            ? opts.map((o: any) => typeof o === 'string' ? o : `${o.key || o.label || ''}) ${o.text || ''}`).join('\n')
            : (obj.optionsText || '');
          const claim = obj.correctAnswer || obj.dogruCevap || obj.claimedAnswer || '';
          const expl = obj.explanation || obj.aciklama || '';
          const evidence = obj.evidenceText ? `\nKanıt / Ders Notu Referansı:\n${obj.evidenceText}` : '';

          fullContent = `[DEEPSEEK DOĞRULANMIŞ TIP SORUSU]
Ders / Branş: ${discipline}
Kurul: ${committeeId}
Konu: ${title}
Soru Kökü:
${stem}

Seçenekler:
${optLines}

Doğru Cevap: ${claim}
${expl ? `\nDeepSeek Tıbbi Analizi & Çözümü:\n${expl}` : ''}${evidence}`.trim();
        } else {
          itemType = 'summary';
          fullContent = `[DEEPSEEK TIP ÖZETİ]
Ders: ${discipline}
Kurul: ${committeeId}
Başlık: ${title}
İçerik:
${content}`.trim();
        }

        const h = hashText(fullContent);
        items.push({
          id: obj.id || `deepseek-jsonl-${h.slice(0, 10)}`,
          source: 'deepseek',
          contributor: 'DeepSeek AI',
          isContribution: true,
          attributionBadge: 'DeepSeek Doğrulanmış Soru',
          itemType,
          committeeId,
          discipline,
          topic: obj.topic || title,
          title,
          content: fullContent,
          rawPayload: obj,
          metadata: {
            sourceFile: fileName,
            fileFormat: 'jsonl',
            importedAt: now,
            stem: stem || undefined,
            options: obj.options || undefined,
            correctAnswer: obj.correctAnswer || obj.claimedAnswer || undefined,
            explanation: obj.explanation || undefined,
            evidenceText: obj.evidenceText || undefined,
            lectureMatches: obj.lectureMatches || undefined,
            verification: obj.verification || undefined,
            embeddingText: obj.embeddingText || undefined,
            tags: ['deepseek', 'donem3', 'dogrulanmis_soru', discipline]
          },
          hash: h,
          createdAt: now,
          updatedAt: now
        });
      } catch (errLine: any) {
        // Skip malformed individual line
      }
    }
  } catch (err: any) {
    console.warn(`[DeepSeekService] JSONL okuma hatası (${fileName}):`, err.message);
  }
  return items;
}

/**
 * Parse a Markdown / Text file and extract DeepSeek items
 */
function parseMarkdownFile(filePath: string, fileName: string): DeepSeekItem[] {
  const items: DeepSeekItem[] = [];
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const now = new Date().toISOString();
    const cleanFileName = fileName.replace(/\.md|\.txt/g, '').replace(/_/g, ' ');

    // Guess discipline and committee from file name
    const lowerName = cleanFileName.toLowerCase();
    const discipline = lowerName.includes('patoloji')
      ? 'Tıbbi Patoloji'
      : lowerName.includes('farma')
      ? 'Tıbbi Farmakoloji'
      : lowerName.includes('mikro')
      ? 'Tıbbi Mikrobiyoloji'
      : lowerName.includes('genetik')
      ? 'Tıbbi Genetik'
      : lowerName.includes('halk')
      ? 'Halk Sağlığı'
      : 'Tıp Bilimleri';

    const committeeMatch = lowerName.match(/kurul\s*(\d)/);
    const committeeId = committeeMatch ? `donem3-kurul${committeeMatch[1]}` : 'donem3-kurul1';

    // Split markdown by sections (H1 # or H2 ##)
    const sections = raw.split(/\n(?=#{1,3}\s+)/);
    let secIdx = 1;

    for (const sec of sections) {
      const trimmed = sec.trim();
      if (trimmed.length < 40) continue;

      const headerMatch = trimmed.match(/^#{1,3}\s+(.+)/);
      const title = headerMatch ? headerMatch[1].trim() : `${cleanFileName} (Bölüm #${secIdx})`;

      const fullContent = `[DEEPSEEK AMFİ & DERS DERLEMESİ]
Ders: ${discipline}
Kurul: ${committeeId}
Konu: ${title}
Kaynak Dosya: ${fileName}
İçerik:
${trimmed}`.trim();

      const h = hashText(fullContent);
      items.push({
        id: `deepseek-md-${h.slice(0, 10)}`,
        source: 'deepseek',
        contributor: 'DeepSeek AI',
        isContribution: true,
        attributionBadge: 'DeepSeek Katkısı',
        itemType: 'summary',
        committeeId,
        discipline,
        topic: title,
        title,
        content: fullContent,
        metadata: {
          sourceFile: fileName,
          fileFormat: fileName.endsWith('.md') ? 'markdown' : 'text',
          importedAt: now,
          tags: ['deepseek', 'ders_ozeti', discipline]
        },
        hash: h,
        createdAt: now,
        updatedAt: now
      });
      secIdx++;
    }
  } catch (err: any) {
    console.warn(`[DeepSeekService] Markdown okuma hatası (${fileName}):`, err.message);
  }
  return items;
}

/**
 * Scan C:\Users\indui\Desktop\meds_database\deepseek_data, parse all items and update stores
 */
export async function scanAndIngestDeepSeekData(): Promise<DeepSeekSyncResult> {
  if (isScanning) {
    return {
      success: true,
      filesScanned: 0,
      itemsIngested: cachedDeepSeekItems.length,
      chunksCreated: cachedDeepSeekItems.length,
      fileList: [],
      lastSyncedAt: lastSyncTimestamp || new Date().toISOString(),
      message: 'Tarama zaten arka planda devam ediyor.'
    };
  }

  isScanning = true;
  ensureDeepSeekFolder();

  try {
    const files = fs.readdirSync(DEEPSEEK_DATA_DIR).filter(f => {
      const lower = f.toLowerCase();
      return (lower.endsWith('.json') || lower.endsWith('.jsonl') || lower.endsWith('.md') || lower.endsWith('.txt')) &&
             !lower.startsWith('readme');
    });

    console.log(`[DeepSeekService] 📂 ${files.length} adet DeepSeek veri dosyası bulundu.`);

    const allIngested: DeepSeekItem[] = [];

    for (const f of files) {
      const fullPath = path.join(DEEPSEEK_DATA_DIR, f);
      const lower = f.toLowerCase();
      if (lower.endsWith('.jsonl')) {
        const parsed = parseJsonlFile(fullPath, f);
        allIngested.push(...parsed);
      } else if (lower.endsWith('.json')) {
        const parsed = parseJsonFile(fullPath, f);
        allIngested.push(...parsed);
      } else {
        const parsed = parseMarkdownFile(fullPath, f);
        allIngested.push(...parsed);
      }
    }

    saveDeepSeekContributions(allIngested);
    lastSyncTimestamp = new Date().toISOString();

    console.log(`[DeepSeekService] ✅ ${allIngested.length} adet DeepSeek verisi başarıyla işlendi ve havuza eklendi.`);

    return {
      success: true,
      filesScanned: files.length,
      itemsIngested: allIngested.length,
      chunksCreated: allIngested.length,
      fileList: files,
      lastSyncedAt: lastSyncTimestamp,
      message: `${files.length} dosya tarandı, ${allIngested.length} adet DeepSeek katkısı hazırlandı.`
    };
  } catch (err: any) {
    console.error('[DeepSeekService] Tarama hatası:', err.message);
    return {
      success: false,
      filesScanned: 0,
      itemsIngested: 0,
      chunksCreated: 0,
      fileList: [],
      lastSyncedAt: new Date().toISOString(),
      message: 'Hata: ' + err.message
    };
  } finally {
    isScanning = false;
  }
}

/**
 * Real-time directory watcher on deepseek_data folder
 */
let watcherInitialized = false;
export function initDeepSeekWatcher(onUpdateCallback?: () => void): void {
  if (watcherInitialized) return;
  watcherInitialized = true;
  ensureDeepSeekFolder();

  // Initial load
  loadDeepSeekContributions();
  scanAndIngestDeepSeekData().then(() => {
    if (onUpdateCallback) onUpdateCallback();
  }).catch(() => {});

  let debounceTimer: NodeJS.Timeout | null = null;
  try {
    fs.watch(DEEPSEEK_DATA_DIR, (eventType, filename) => {
      if (!filename || filename.toLowerCase().startsWith('readme')) return;
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(async () => {
        console.log(`[DeepSeekService] 🔔 deepseek_data klasöründe yeni hareket tespit edildi (${filename})...`);
        await scanAndIngestDeepSeekData();
        if (onUpdateCallback) onUpdateCallback();
      }, 3000);
    });
    console.log('[DeepSeekService] 👁️ deepseek_data klasör izleyicisi (Watcher) aktif.');
  } catch (err: any) {
    console.warn('[DeepSeekService] Klasör izleyici başlatılamadı:', err.message);
  }
}
