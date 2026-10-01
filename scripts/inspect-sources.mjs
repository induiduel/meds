import fs from 'fs';

const pq = JSON.parse(fs.readFileSync('data/pastQuestions.json', 'utf8'));

const bySource = {};
pq.forEach(q => {
  const sf = q.sourceFile || 'unknown';
  if (!bySource[sf]) bySource[sf] = [];
  bySource[sf].push(q);
});

console.log('=== SOURCE BREAKDOWN ===');
for (const [sf, items] of Object.entries(bySource)) {
  const sample = items[0];
  const stem = (sample.rawQuestion && sample.rawQuestion.stem) || '';
  console.log(`[${items.length.toString().padStart(4)}] ${sf}`);
  console.log(`       Comm: ${sample.committeeId} | Disc: ${sample.discipline}`);
  console.log(`       Sample: ${stem.substring(0, 90).replace(/\s+/g, ' ')}...`);
}
