// RAG yerel parçalarını ayrı süreçte yeniden üretir (sunucu içi /api/rag/reindex 2 GB yığında çöker).
// Çalıştır: systemctl --user stop meds-web; NODE_OPTIONS=--max-old-space-size=3800 npx tsx scripts/rag-yeniden-parcala.mts
// Ardından vektörler: .venv-ocr/bin/python scripts/advanced_ai/rag_vektor_hatti.py [--oracle]
import { runAutoChunking, saveLocalChunksToFile } from '../src/services/localRagEngine.ts';

const r = await runAutoChunking({ syncToCloud: false });
await saveLocalChunksToFile(true);
console.log(JSON.stringify(r));
process.exit(0);
