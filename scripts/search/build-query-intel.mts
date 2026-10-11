/**
 * Sorgu zekâsı paketini derler: data/search/query-intel.{json,bin}
 *   npx tsx scripts/search/build-query-intel.mts [--force]
 * Sunucu açılışta bunu düşük öncelikli alt süreç olarak çağırır (imza aynıysa hemen çıkar).
 */
import path from 'path';
import { fileURLToPath } from 'url';
import { buildQueryIntelPack } from '../../src/services/queryIntel/build.ts';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const force = process.argv.includes('--force');
const res = buildQueryIntelPack({ projectRoot: root, force, log: (m) => console.log(m) });
console.log(JSON.stringify({ ok: true, skipped: res.skipped, stats: res.stats }));
if (!process.argv.includes('--no-graph')) {
  const { buildDiseaseGraph } = await import('../../src/services/knowledge/diseaseGraphBuild.ts');
  const g = buildDiseaseGraph({ projectRoot: root, force, log: (m: string) => console.log(m) });
  console.log(JSON.stringify({ ok: true, graph: g.skipped ? 'atlandı' : 'yazıldı', stats: g.stats }));
}
