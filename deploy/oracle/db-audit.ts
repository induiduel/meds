/**
 * db-audit.ts — Oracle local Supabase denetimi (meds-server konteyneri içinden çalışır).
 * Çalıştırma (Oracle): docker cp db-audit.ts meds-server:/tmp/ &&
 *   docker exec -w /app meds-server npx tsx /tmp/db-audit.ts
 * Her tablo: okuma + sayım. RPC'ler: gerçek vektörle self-test. questions: yaz-sil döngüsü.
 */
import { createClient } from '@supabase/supabase-js';

const url = (process.env.LOCAL_SUPABASE_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');
const key = process.env.LOCAL_SUPABASE_KEY || process.env.SUPABASE_SECRET_KEY || '';
if (!key) {
  console.error('FAIL: anahtar yok (LOCAL_SUPABASE_KEY)');
  process.exit(2);
}
const sb = createClient(url, key);

async function main(): Promise<number> {
let pass = 0;
let fail = 0;
const ok = (name: string, cond: boolean, extra = '') => {
  if (cond) { pass++; console.log(`PASS ${name}${extra ? ' — ' + extra : ''}`); }
  else { fail++; console.log(`FAIL ${name}${extra ? ' — ' + extra : ''}`); }
};

// 1. Tablolar: sayım + 1 satır okuma
const tables: Array<[string, string]> = [
  ['questions', 'id'],
  ['past_questions', 'id'],
  ['past_question_reports', 'id'],
  ['lecture_notes', 'id'],
  ['users', 'uid'],
  ['rag_chunks', 'id'],
];
for (const [t, col] of tables) {
  try {
    const c = await sb.from(t).select(col, { count: 'exact', head: true });
    const r = await sb.from(t).select('*').limit(1);
    // past_question_reports boş olabilir (raporlar JSON kolonunda); şema varsa PASS.
    const needRow = t !== 'past_question_reports';
    ok(`tablo:${t}`, !c.error && !r.error && (!needRow || (r.data?.length || 0) > 0),
      `count=${c.count ?? '?'} err=${c.error?.message || r.error?.message || 'yok'}`);
  } catch (e: any) {
    ok(`tablo:${t}`, false, String(e?.message || e).slice(0, 120));
  }
}

// 2. RPC: bge-m3 (gerçek vektörle self-test)
try {
  const row = await sb.from('rag_chunks').select('id,embedding_bge_m3').not('embedding_bge_m3', 'is', null).limit(1).single();
  if (row.error || !row.data) throw new Error('bge vektörlü satır yok: ' + (row.error?.message || ''));
  const rpc: any = await (sb as any).rpc('match_rag_chunks_bge_m3', { query_embedding: row.data.embedding_bge_m3, match_count: 3 });
  const top = rpc.data?.[0];
  ok('rpc:match_rag_chunks_bge_m3', !rpc.error && top?.id === row.data.id,
    `top=${top?.id === row.data.id ? 'self' : top?.id} sim=${top?.similarity}`);
} catch (e: any) {
  ok('rpc:match_rag_chunks_bge_m3', false, String(e?.message || e).slice(0, 120));
}

// 3. RPC: e5 (gerçek vektörle self-test)
try {
  const row = await sb.from('rag_chunks').select('id,embedding_e5').not('embedding_e5', 'is', null).limit(1).single();
  if (row.error || !row.data) throw new Error('e5 vektörlü satır yok: ' + (row.error?.message || ''));
  const rpc: any = await (sb as any).rpc('match_rag_chunks_e5', { query_embedding: row.data.embedding_e5, match_count: 3 });
  const top = rpc.data?.[0];
  ok('rpc:match_rag_chunks_e5', !rpc.error && top?.id === row.data.id,
    `top=${top?.id === row.data.id ? 'self' : top?.id}`);
} catch (e: any) {
  ok('rpc:match_rag_chunks_e5', false, String(e?.message || e).slice(0, 120));
}

// 4. Yaz-sil döngüsü (questions, sahte id — iz bırakmaz)
const probeId = 'audit-probe-oracle';
try {
  const w = await sb.from('questions').upsert([{ id: probeId, committee_id: 'donem3-kurul1', question_number: -1, status: 'gathering', tags: [], fragments: [], options: [], data: { probe: true } }], { onConflict: 'id' });
  const d = await sb.from('questions').delete().eq('id', probeId);
  const v = await sb.from('questions').select('id').eq('id', probeId);
  ok('yaz-sil:questions', !w.error && !d.error && !v.error && (v.data?.length || 0) === 0,
    `w=${w.error?.message || 'ok'} d=${d.error?.message || 'ok'}`);
} catch (e: any) {
  ok('yaz-sil:questions', false, String(e?.message || e).slice(0, 120));
}

console.log(`\nSONUÇ: ${pass} PASS, ${fail} FAIL`);
  return fail ? 1 : 0;
}

main().then((code) => process.exit(code ?? 0)).catch((e) => { console.error('FATAL', String(e).slice(0, 200)); process.exit(2); });
