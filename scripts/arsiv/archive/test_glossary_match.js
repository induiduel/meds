const fs = require('fs');
const glossaryData = require('../src/data/medical_glossary.json');
const encyclopediaData = require('../src/data/medical_encyclopedia.json');

const STOP_WORDS = new Set(['ile', 've', 'bir', 'için', 'gibi', 'daha', 'çok', 'tip', 'her', 'bu', 'şu', 'veya', 'olan', 'göre']);
const patterns = [];
const map = new Map();

function addPattern(raw, item) {
  const clean = raw.trim();
  if (clean.length < 3) return;
  const lower = clean.toLowerCase();
  if (STOP_WORDS.has(lower)) return;
  patterns.push(clean);
  map.set(lower, item);
}

// Convert glossary into items
const items = [];
for (const [k, v] of Object.entries(glossaryData)) {
  if (typeof v === 'object' && v.term) {
    items.push(v);
  }
}

items.forEach((item) => {
  addPattern(item.term, item);
  const cleanTerm = item.term.replace(/\s*\([^)]*\)/g, '').trim();
  addPattern(cleanTerm, item);
  const parenMatch = item.term.match(/^(.+?)\s*\((.+?)\)$/);
  if (parenMatch) {
    addPattern(parenMatch[1], item);
    addPattern(parenMatch[2], item);
  }
  if (item.aliases) {
    item.aliases.forEach(a => addPattern(a, item));
  }
});

const unique = Array.from(new Set(patterns)).sort((a,b) => b.length - a.length);
console.log('Total patterns:', unique.length);

const escaped = unique.map((p) => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
try {
  const reg = new RegExp('(?<![\\p{L}\\p{N}])(' + escaped + ')(?![\\p{L}\\p{N}])', 'giu');
  console.log('Regex built successfully!');
  const testStr = 'Bu slaytta kazeöz nekroz, epiteloid histiyosit ve Langhans dev hücresi incelenmektedir. Bax ve Bak proteinleri apoptoz mekanizmasında rol oynar.';
  const matches = testStr.match(reg);
  console.log('Matches in testStr:', matches);
} catch (e) {
  console.error('Regex error:', e);
}
