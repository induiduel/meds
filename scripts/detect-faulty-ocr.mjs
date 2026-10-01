import fs from 'fs';

const pq = JSON.parse(fs.readFileSync('data/pastQuestions.json', 'utf8'));

const badQuestions = [];

pq.forEach(q => {
  const stem = (q.rawQuestion && q.rawQuestion.stem) || '';
  const options = (q.rawQuestion && q.rawQuestion.options) || [];
  const fullText = stem + ' ' + options.map(o => o.text || '').join(' ');
  const reasons = [];

  // Check 1: Web scraper URL / portal junk
  if (stem.includes('karabuk.edu.tr') || stem.includes('Anal z/') || stem.includes('Ders / Ünite /Konu') || stem.includes('Sıra No Ders')) {
    reasons.push('Portal header / URL scrape');
  }

  // Check 2: Exam meta instructions (not a question)
  if (stem.includes('Bu sınav toplam') && stem.includes('sorudan oluşmaktadır')) {
    reasons.push('Exam meta instructions');
  }

  // Check 3: Raw answer key text
  if (/^[A-E\s]{6,}$/.test(stem.trim()) || stem.trim() === 'C B C D D D' || stem.startsWith('Cevap Anahtarı') || stem.includes('Sıra No Cevap Doğru Sıra No Cevap Doğru')) {
    reasons.push('Raw answer key dump');
  }

  // Check 4: Extremely short or missing stem
  if (stem.trim().length < 15 && options.length <= 1) {
    reasons.push('Missing/extremely short stem');
  }

  // Check 5: Massive option text (>800 chars in a single option indicates multiple concatenated questions/table dump)
  if (options.some(o => (o.text || '').length > 800)) {
    reasons.push('Mashed table dump in options (>800 chars)');
  }

  // Check 6: Multiple Sıra No / Cevap table headers in stem
  const siraNoCount = (stem.match(/Sıra No/gi) || []).length;
  if (siraNoCount >= 3) {
    reasons.push('Repeated table column dump in stem');
  }

  // Check 7: High ratio of null bytes or gibberish characters
  const nullBytes = (fullText.match(/\u0000/g) || []).length;
  if (nullBytes > 0) {
    reasons.push('Null bytes in text');
  }

  // Check 8: Gibberish sequences
  if (/\b(?:SzRARM|mpsziz|pfBğösr|vndgu7|krv9|xkp\w+|pBğösr)\b/i.test(fullText)) {
    reasons.push('Garbled OCR gibberish');
  }

  // Check 9: Excessive symbols or broken OCR artifact lines
  // e.g. text consisting mostly of punctuation / symbols or broken numbers
  const alphaCount = (stem.match(/[a-zA-ZğüşıöçĞÜŞİÖÇ]/g) || []).length;
  if (stem.length > 20 && alphaCount / stem.length < 0.35) {
    reasons.push('Very low alphabetic ratio (<35%)');
  }

  // Check 10: Fewer than 3 words in stem or empty stem
  const words = stem.trim().split(/\s+/).filter(w => w.length > 1);
  if (words.length < 3) {
    reasons.push('Stem has fewer than 3 words: "' + stem.trim() + '"');
  }

  // Check 11: Completely empty options AND short stem
  if (options.length === 0 && stem.length < 50) {
    reasons.push('No options and short stem');
  }

  // Check 12: Broken OCR patterns with lots of standalone single characters
  // e.g., "ö l ü m   s a y ı s ı" or "a b c d e f"
  const singleLetterWords = words.filter(w => w.length === 1 && !['a', 'b', 'c', 'd', 'e', 'I', 'V', 'X'].includes(w));
  if (words.length > 5 && singleLetterWords.length / words.length > 0.4) {
    reasons.push('Fragmented single-letter OCR noise');
  }

  if (reasons.length > 0) {
    badQuestions.push({
      id: q.id,
      source: q.sourceFile,
      reasons,
      stem: stem.substring(0, 100).replace(/\s+/g, ' ')
    });
  }
});

console.log(`Total faulty OCR / corrupted questions found: ${badQuestions.length}`);
console.log('Breakdown by reason:');
const reasonCounts = {};
badQuestions.forEach(b => {
  b.reasons.forEach(r => {
    const key = r.split(':')[0];
    reasonCounts[key] = (reasonCounts[key] || 0) + 1;
  });
});
console.log(reasonCounts);
console.log('\nSample faulty questions (first 30):');
badQuestions.slice(0, 30).forEach((b, i) => {
  console.log(`[${(i+1).toString().padStart(2)}] [${b.source}] (${b.reasons.join('; ')}) -> ${b.stem}`);
});

