import fs from 'fs';
import path from 'path';

const LOCAL_CHUNKS_FILE = path.resolve('data/local_rag_chunks.json');
console.log('Loading local_rag_chunks.json...');
const tLoad = Date.now();
const raw = fs.readFileSync(LOCAL_CHUNKS_FILE, 'utf-8');
const chunks = JSON.parse(raw);
console.log(`Loaded ${chunks.length} chunks in ${Date.now() - tLoad}ms`);

const TURKISH_STOPWORDS = new Set([
  've', 'ile', 'veya', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bunun',
  'buna', 'şekilde', 'olarak', 'üzere', 'bir', 'bu', 'şu', 'o', 'her', 'tüm', 'bütün',
  'sayfa', 'slayt', 'bölüm', 'ders', 'notu', 'konu', 'ünite', 'tablo', 'şekil', 'görsel',
  'hangisidir', 'aşağıdakilerden', 'hangisi', 'nedir', 'aşağıdaki', 'vardır', 'yoktur',
  'doğrudur', 'yanlıştır', 'göre', 'ilgili', 'ilişkin', 'arasında', 'yer', 'alır',
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are', 'was'
]);

function cleanTextForTokens(text) {
  return text
    .toLowerCase()
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'’“”…\[\]<>|\\+]/g, ' ')
    .split(/\s+/)
    .map(w => w.trim())
    .filter(w => w.length >= 3 && !TURKISH_STOPWORDS.has(w));
}

const chunkMap = new Map();
for (const c of chunks) chunkMap.set(c.id, c);

// Inverted index with TF: token -> Map<chunkId, tf>
const invertedIndex = new Map();
const docLengths = new Map();
let totalDocLen = 0;

console.log('Building BM25 index...');
const tIdx = Date.now();
for (let i = 0; i < chunks.length; i++) {
  const chunk = chunks[i];
  // Weight title and discipline higher by repeating in scanned text
  const textToScan = `${chunk.title} ${chunk.title} ${chunk.discipline || ''} ${chunk.content}`;
  const tokens = cleanTextForTokens(textToScan);
  docLengths.set(chunk.id, tokens.length);
  totalDocLen += tokens.length;

  const freqMap = new Map();
  for (const t of tokens) {
    freqMap.set(t, (freqMap.get(t) || 0) + 1);
  }

  for (const [t, freq] of freqMap.entries()) {
    let posting = invertedIndex.get(t);
    if (!posting) {
      posting = new Map();
      invertedIndex.set(t, posting);
    }
    posting.set(chunk.id, freq);
  }
}

const avgDocLength = totalDocLen / (chunks.length || 1);
console.log(`Indexed in ${Date.now() - tIdx}ms. Unique tokens: ${invertedIndex.size}, avgDocLength: ${Math.round(avgDocLength)}`);

// BM25 Search function
function searchBM25(queryText, options = {}) {
  const limit = options.limit || 5;
  const cleanTokens = cleanTextForTokens(queryText);
  if (cleanTokens.length === 0) return [];

  const N = chunks.length || 1;
  const k1 = 1.2;
  const b = 0.75;
  const avgdl = avgDocLength;

  const tokenInfo = [];
  for (const t of cleanTokens) {
    const postings = invertedIndex.get(t);
    if (postings && postings.size > 0) {
      const df = postings.size;
      const idf = Math.log(1 + (N - df + 0.5) / (df + 0.5));
      tokenInfo.push({ token: t, idf, postings });
    }
  }

  if (tokenInfo.length === 0) return [];

  // Sort by IDF descending: most discriminating terms first
  tokenInfo.sort((x, y) => y.idf - x.idf);
  // Optimization: Prune query tokens to top 6 most informative terms (highest IDF)
  const tokensToScore = tokenInfo.slice(0, 6);

  const candidateScores = new Map();
  const matchedTokensCount = new Map();

  for (const { token, idf, postings } of tokensToScore) {
    for (const [chunkId, tf] of postings.entries()) {
      const docLen = docLengths.get(chunkId) || avgdl;
      const tfNorm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (docLen / avgdl)));
      const termScore = idf * tfNorm;

      candidateScores.set(chunkId, (candidateScores.get(chunkId) || 0) + termScore);
      matchedTokensCount.set(chunkId, (matchedTokensCount.get(chunkId) || 0) + 1);
    }
  }

  // Pre-built Map for O(1) instant chunk retrieval
  const scoredResults = [];
  const normalizedQuery = queryText.toLowerCase().replace(/[^a-z0-9ğüşıöç]/gi, ' ').trim();

  for (const [id, bmScore] of candidateScores.entries()) {
    const chunk = chunkMap.get(id);
    if (!chunk) continue;

    if (options.committeeId && chunk.committeeId && chunk.committeeId !== options.committeeId) {
      continue;
    }
    if (options.discipline && chunk.discipline && !chunk.discipline.toLowerCase().includes(options.discipline.toLowerCase())) {
      continue;
    }

    let finalScore = bmScore;

    // Term coordination boost (chunks matching multiple query terms)
    const matchCount = matchedTokensCount.get(id) || 1;
    finalScore *= (1 + 0.25 * (matchCount - 1));

    // Exact phrase match bonus
    const lowerContent = chunk.content.toLowerCase();
    if (lowerContent.includes(normalizedQuery)) {
      finalScore += 25;
    }

    // High yield document types bonus
    if (chunk.documentType === 'deepseek_contribution') {
      finalScore += 20;
    } else if (chunk.documentType === 'past_question') {
      finalScore += 12;
    } else if (chunk.documentType === 'ai_refinement' || chunk.documentType === 'summary') {
      finalScore += 8;
    }

    scoredResults.push({ chunk, score: finalScore });
  }

  scoredResults.sort((a, b) => b.score - a.score);
  return scoredResults.slice(0, limit);
}

// Test cases
const testQueries = [
  'Papiller tiroid karsinomunun sitolojik/histopatolojik tanı kriterleri, Orphan Annie gözü nükleusları, psammom cisimcikleri',
  'Asetaminofen (parasetamol) intoksikasyonunda hepatotoksisiteden sorumlu reaktif toksik metabolit hangisidir ve antidot olarak N-asetilsistein (NAC)',
  'Yenidoğan, çocuk ve erişkinlerde akut pürülan bakteriyel menenjitin en sık etkenleri nelerdir ve tipik BOS incelemesinde basınç, protein, glukoz',
  'beta blokerler astım kontrendikasyonu propranolol bronkospazm metoprolol kardiyoselektif'
];

for (let i = 0; i < testQueries.length; i++) {
  const q = testQueries[i];
  const t0 = Date.now();
  const res = searchBM25(q, { limit: 3 });
  const dur = Date.now() - t0;
  console.log(`\n======================================================`);
  console.log(`[Test ${i + 1}] Query: "${q.slice(0, 70)}..."`);
  console.log(`Duration: ${dur} ms | Results: ${res.length}`);
  res.forEach((r, idx) => {
    console.log(`  ${idx + 1}. [${r.chunk.documentType}] "${r.chunk.title}" (Discipline: ${r.chunk.discipline}) | Score: ${r.score.toFixed(1)}`);
    console.log(`     Excerpt: ${r.chunk.content.slice(0, 140).replace(/\n/g, ' ')}...`);
  });
}
