import { scanAndIngestDeepSeekData, loadDeepSeekContributions } from '../src/services/deepseekDataService.ts';

async function main() {
  console.log('DeepSeek verileri taranıyor ve havuza aktarılıyor...');
  const result = await scanAndIngestDeepSeekData();
  console.log('Sonuç:', result);
  const items = loadDeepSeekContributions();
  console.log(`Toplam DeepSeek katkısı: ${items.length}`);
  const byType: Record<string, number> = {};
  for (const it of items) {
    byType[it.itemType] = (byType[it.itemType] || 0) + 1;
  }
  console.log('Türe göre dağılım:', byType);
}

main().catch(err => {
  console.error('Hata:', err);
  process.exit(1);
});
