import fs from 'fs';
import path from 'path';
import type { Plugin } from 'vite';

/**
 * Sürüm damgası: derlemede guncelleme_notu.json'u okuyup istemciye __MEDS_SURUM__ / __MEDS_ONEM__ olarak gömer
 * ve dist/surum.json yazar. Sunucu /api/surum ile bu dosyayı verir; açık sekme kendi önem sayısından büyüğünü
 * görünce "Siteyi güncelle" diyaloğunu açar (src/components/system/UpdatePrompt.tsx).
 */
export function surumDosyasi(root: string): Plugin {
  const notYolu = path.join(root, 'guncelleme_notu.json');
  let not: { onem?: number; baslik?: string; maddeler?: string[] } = {};
  try { not = JSON.parse(fs.readFileSync(notYolu, 'utf8')); } catch { /* yoksa önem 0 */ }
  const surum = new Date().toISOString().replace(/[-:.TZ]/g, '').slice(0, 14);
  const onem = Number(not.onem) || 0;
  let outDir = path.join(root, 'dist');
  return {
    name: 'meds-surum-dosyasi',
    config: () => ({ define: { __MEDS_SURUM__: JSON.stringify(surum), __MEDS_ONEM__: String(onem) } }),
    configResolved(c) { outDir = path.resolve(c.root, c.build.outDir); },
    closeBundle() {
      const veri = { surum, onem, baslik: not.baslik || '', maddeler: Array.isArray(not.maddeler) ? not.maddeler : [] };
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, 'surum.json'), JSON.stringify(veri, null, 2));
    },
  };
}
