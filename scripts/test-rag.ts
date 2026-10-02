import dotenv from 'dotenv';
dotenv.config();

import { searchRagChunks, executeRagQuery } from '../src/services/ragService.ts';

async function test() {
  const apiKey = process.env.GEMINI_API_KEY || '';
  console.log('Testing RAG search...');
  const searchResults = await searchRagChunks('tiroid nodülleri ve papiller karsinom', apiKey, { limit: 2 });
  console.log('Arama Sonucu Adedi:', searchResults.length);
  if (searchResults.length > 0) {
    console.log('En İyi Eşleşme:', searchResults[0].title, '| Branş:', searchResults[0].discipline);
  }

  console.log('\nTesting executeRagQuery (mode: reduction)...');
  const ragAns = await executeRagQuery({
    query: 'Papiller tiroid karsinomu yüksek verimli hap bilgiler ve çıkmış soru ipuçları',
    mode: 'reduction',
    limit: 2
  }, apiKey, 'gemini-3.1-flash-lite');

  console.log('\n--- ÜRETİLEN HAP BİLGİ YANITI ---\n');
  console.log(ragAns.answer.slice(0, 400) + '...\n');
  console.log('Kullanılan Model:', ragAns.usedModel);
  console.log('Referans Kaynak Sayısı:', ragAns.sourcesCount);
  console.log('\n✅ TEST BAŞARIYLA TAMAMLANDI!');
}

test().catch(err => {
  console.error('Test hatası:', err);
});
