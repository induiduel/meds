/**
 * src/data/interactive_learning_decks.json (≈14 MB) tek parça olarak tarayıcıya gönderilince
 * öğrenme sayfası açılırken donuyordu. Bu eklenti derleme/geliştirme başlarken veriyi böler:
 *   src/data/decks/catalog.json      → liste için hafif bilgiler (slaytsız + sayılar)
 *   src/data/decks/items/<id>.json   → bir destenin tam içeriği (yalnızca açılınca yüklenir)
 * Kaynak dosya değişmedikçe yeniden yazılmaz. Çıktı .gitignore'dadır.
 */
import fs from 'fs';
import path from 'path';
import type { Plugin } from 'vite';

export const safeDeckFile = (id: string) => id.replace(/[^a-zA-Z0-9_-]+/g, '_');

export function splitLearningDecks(root: string): Plugin {
  const src = path.resolve(root, 'src/data/interactive_learning_decks.json');
  const outDir = path.resolve(root, 'src/data/decks');
  const itemsDir = path.join(outDir, 'items');
  const catalogFile = path.join(outDir, 'catalog.json');

  const run = () => {
    if (!fs.existsSync(src)) return;
    const srcTime = fs.statSync(src).mtimeMs;
    if (fs.existsSync(catalogFile)) {
      try {
        const cat = JSON.parse(fs.readFileSync(catalogFile, 'utf8'));
        const pub = cat.filter((x: any) => x.isNew || String(x.version || '').startsWith('2') || (x.slideCount && x.slideCount >= 50));
        if (cat.length >= 100 && pub.length >= 29 && fs.statSync(catalogFile).mtimeMs >= srcTime) return;
      } catch {}
    }
    const decks: any[] = JSON.parse(fs.readFileSync(src, 'utf8'));
    fs.rmSync(itemsDir, { recursive: true, force: true });
    fs.mkdirSync(itemsDir, { recursive: true });
    const catalog = [];
    for (const d of decks) {
      if (!d || !d.id || !Array.isArray(d.slides) || d.slides.length === 0) continue;
      fs.writeFileSync(path.join(itemsDir, `${safeDeckFile(d.id)}.json`), JSON.stringify(d));
      const { slides, ...meta } = d;
      const questionCount =
        meta.questionCount ||
        (Array.isArray(d.questions) ? d.questions.length : 0) ||
        slides.reduce((n: number, s: any) => n + (s.relatedQuestions?.length || s.questions?.length || 0), 0);
      const cardCount =
        meta.cardCount ||
        meta.flashcardCount ||
        (Array.isArray(d.flashcards) ? d.flashcards.length : 0) ||
        slides.reduce((n: number, s: any) => n + (s.flashcards?.length || 0), 0);

      catalog.push({
        ...meta,
        slideCount: slides.length,
        questionCount,
        cardCount,
        firstSlideNumber: slides[0]?.slideNumber ?? 1,
      });
    }
    fs.writeFileSync(catalogFile, JSON.stringify(catalog, null, 2));
    console.log(`[decks] ${catalog.length} deste bölündü (Yayınlanan: ${catalog.filter((x: any) => x.isNew || String(x.version || '').startsWith('2') || x.slideCount >= 50).length}) → src/data/decks/`);
  };

  return {
    name: 'medsor-split-learning-decks',
    config() { run(); },
    configureServer(server) {
      server.watcher.add(src);
      server.watcher.on('change', (file) => { if (path.resolve(file) === src) run(); });
    },
  };
}
