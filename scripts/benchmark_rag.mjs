import dotenv from 'dotenv';
dotenv.config();

import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q';
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function check() {
  console.log('--- Checking Supabase rag_chunks count ---');
  const t0 = Date.now();
  const { count, error } = await supabase.from('rag_chunks').select('*', { count: 'exact', head: true });
  console.log('Query time:', Date.now() - t0, 'ms');
  console.log('Count:', count, 'Error:', error?.message);

  const { initLocalRagEngine, searchLocalRag } = await import('../src/services/localRagEngine.ts');
  console.log('\n--- Initializing localRagEngine ---');
  const tInit = Date.now();
  initLocalRagEngine();
  console.log('Init time:', Date.now() - tInit, 'ms');

  const queries = [
    'tiroid nodülleri ve papiller karsinom',
    'asetaminofen toksisitesi NAPQI n-asetilsistein',
    'akut bakteriyel menenjit BOS bulguları',
    'beta blokerler astım kontrendikasyonu propranolol'
  ];

  for (const q of queries) {
    const t0 = Date.now();
    const results = await searchLocalRag(q, { limit: 5 });
    const dur = Date.now() - t0;
    console.log(`\nQuery: "${q}" -> ${results.length} results in ${dur}ms`);
    if (results.length > 0) {
      console.log(`  Top hit: [${results[0].documentType}] ${results[0].title} (Score: ${results[0].matchScore.toFixed(1)})`);
    }
  }
}

check().catch(console.error);
