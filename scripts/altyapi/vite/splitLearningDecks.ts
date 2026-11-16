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

/*
 * Parçalı deste kaynağı (VERI_MODELI Faz 3 adım 3; biçim `scripts/deste_deposu.py`). Yalnız MEDS_DESTE_PARCALI=1 +
 * MEDS_DESTE_PARCA_DIZIN verilmiş ve `_sira.json` varsa: desteler parçalardan (sıra dosyasındaki sırayla) okunur,
 * tazelik damgası `_sira.json`'dur (her parça yazımında en son yeniden yazılır). Aksi hâlde monolit — eski yol birebir.
 */
function parcaliKaynak(): { damga: string; oku: () => any[] } | null {
  const dz = process.env.MEDS_DESTE_PARCALI === '1' && process.env.MEDS_DESTE_PARCA_DIZIN ? path.resolve(process.env.MEDS_DESTE_PARCA_DIZIN) : null;
  const sira = dz ? path.join(dz, '_sira.json') : '';
  if (!dz || !fs.existsSync(sira)) return null;
  return {
    damga: sira,
    oku: () => {
      const s = JSON.parse(fs.readFileSync(sira, 'utf8'));
      if (s?.bicim !== 1) throw new Error(`desteler/_sira.json biçimi ${s?.bicim} desteklenmiyor`);
      return (s.desteler || []).map((g: any) => JSON.parse(fs.readFileSync(path.join(dz, g.dosya), 'utf8')));
    },
  };
}

const deckGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';

export function splitLearningDecks(root: string): Plugin {
  const src = path.resolve(root, 'src/data/interactive_learning_decks.json');
  const outDir = path.resolve(root, 'src/data/decks');
  const itemsDir = path.join(outDir, 'items');
  const catalogFile = path.join(outDir, 'catalog.json');
  const flashcardsFile = path.join(outDir, 'flashcards.json');
  const kzDir = path.resolve(root, 'src/data/kazanimlar');
  const kzLiteDir = path.join(kzDir, 'lite');
  const kzQuestionsDir = path.join(kzDir, 'questions');

  /** Kazanım lite biçim sürümü: 2 = ekranın kullanmadığı anlatım alanları budandı (kurul başına parça ≤ ~0,4 MB). */
  const LITE_SURUM = 2;
  const splitKazanimlar = () => {
    if (!fs.existsSync(kzDir)) return;
    fs.mkdirSync(kzLiteDir, { recursive: true });
    fs.mkdirSync(kzQuestionsDir, { recursive: true });
    for (let k = 1; k <= 6; k++) {
      const kFile = path.join(kzDir, `k${k}.json`);
      if (!fs.existsSync(kFile)) continue;
      const liteFile = path.join(kzLiteDir, `k${k}.json`);
      // Soru havuzu konu (ders/lesson) başına bölünür: questions/k<N>/d<i>-k<j>.json + questions/k<N>/_dizin.json
      // (kazanım kimliği → dosya). Eski tek dosya questions/k<N>.json (K1'de ≈31 MB tek parça) artık üretilmez;
      // tek tüketicisi KazanimlarView'dı. Eski dosya silinmez, yalnız güncellenmez (glob onu artık kapsamaz).
      const qDir = path.join(kzQuestionsDir, `k${k}`);
      const qFile = path.join(qDir, '_dizin.json');
      const srcMtime = fs.statSync(kFile).mtimeMs;
      if (fs.existsSync(liteFile) && fs.existsSync(qFile)) {
        try {
          // LITE_SURUM: lite biçimi değişince (alan budaması) eski dosya mtime'a bakılmadan yeniden üretilir
          const guncel = fs.readFileSync(liteFile, 'utf8').includes(`"liteSurum":${LITE_SURUM}`);
          if (guncel && fs.statSync(liteFile).mtimeMs >= srcMtime && fs.statSync(qFile).mtimeMs >= srcMtime) continue;
        } catch {}
      }
      try {
        const raw = JSON.parse(fs.readFileSync(kFile, 'utf8'));
        const parcalar: Record<string, Record<string, { cikmisSorular?: any[]; ornekSorular?: any[] }>> = {};
        const dizin: Record<string, string> = {};
        const lite = {
          ...raw,
          liteSurum: LITE_SURUM,
          dersler: (raw.dersler || []).map((d: any, di: number) => ({
            ...d,
            konular: (d.konular || []).map((konu: any, ki: number) => ({
              ...konu,
              kazanimlar: (konu.kazanimlar || []).map((kz: any) => {
                const cList = Array.isArray(kz.cikmisSorular) ? kz.cikmisSorular : [];
                const oList = Array.isArray(kz.ornekSorular) ? kz.ornekSorular : [];
                if (kz.id && (cList.length > 0 || oList.length > 0)) {
                  const dosya = `d${di}-k${ki}`;
                  dizin[kz.id] = dosya;
                  (parcalar[dosya] ||= {})[kz.id] = {
                    ...(cList.length > 0 ? { cikmisSorular: cList } : {}),
                    ...(oList.length > 0 ? { ornekSorular: oList } : {}),
                  };
                }
                // Ekran (KazanimlarView) ve saglik/baglantilari_kur.py yalnız aşağıdaki alanları okur. Anlatım alanları
                // (anlatim_ses, ozet_konu_anlatimi, bilinmesi_gerekenler, kisa_anlatim[_ses]) K1 lite'ın ≈%80'iydi
                // (3,1 MB); ekranda gösterilmediği için lite'a taşınmaz → kurul parçası ≤ ~0,4 MB.
                return {
                  id: kz.id,
                  metin: kz.metin,
                  slaytlar: Array.isArray(kz.slaytlar) ? kz.slaytlar : [],
                  sozlukTerimleri: Array.isArray(kz.sozlukTerimleri) ? kz.sozlukTerimleri : [],
                  ozetler: Array.isArray(kz.ozetler) ? kz.ozetler : [],
                  totalCikmisCount: cList.length,
                  totalOrnekCount: kz.totalOrnekCount ?? oList.length,
                  firstOrnekKazanimNo: oList[0]?.kazanimNo,
                  cikmisSorular: [],
                  ornekSorular: [],
                };
              }),
            })),
          })),
        };
        fs.writeFileSync(liteFile, JSON.stringify(lite));
        fs.rmSync(qDir, { recursive: true, force: true }); // yalnız türetilen klasör: bayat parça kalmasın
        fs.mkdirSync(qDir, { recursive: true });
        for (const [dosya, harita] of Object.entries(parcalar)) fs.writeFileSync(path.join(qDir, `${dosya}.json`), JSON.stringify(harita));
        fs.writeFileSync(qFile, JSON.stringify(dizin)); // en son: varlığı bölmenin tamamlandığını gösterir
      } catch (e) {
        console.warn(`[kazanimlar] k${k}.json bölünemedi:`, e);
      }
    }
  };

  const run = () => {
    splitKazanimlar();
    const parcali = parcaliKaynak();
    const damga = parcali ? parcali.damga : src;
    if (!fs.existsSync(damga)) return;
    const srcTime = fs.statSync(damga).mtimeMs;
    const decks: any[] = parcali ? parcali.oku() : JSON.parse(fs.readFileSync(src, 'utf8'));
    const valid = decks.filter((d) => d && d.id && Array.isArray(d.slides) && d.slides.length > 0);
    // Katalog kaynaktan yeniyse VE parça sayısı tutuyorsa bölmeyi atla; aksi halde yeniden üret
    // (yalnız mtime'a bakmak, parçalar silinmiş/eksikken tüm destelerin açılmamasına yol açıyordu).
    if (fs.existsSync(catalogFile) && fs.existsSync(flashcardsFile)) {
      try {
        if (fs.statSync(catalogFile).mtimeMs >= srcTime && fs.statSync(flashcardsFile).mtimeMs >= srcTime) {
          let itemCount = 0;
          try {
            itemCount = fs.existsSync(itemsDir) ? fs.readdirSync(itemsDir).filter((f) => f.endsWith('.json')).length : 0;
          } catch {}
          // Eski biçimli katalog (Test çöz sayaçları yok) yeniden üretilir
          const fresh = fs.readFileSync(catalogFile, 'utf8').includes('"testCounts"');
          if (fresh && itemCount === valid.length && valid.length > 0) return;
        }
      } catch {}
    }
    fs.rmSync(itemsDir, { recursive: true, force: true });
    fs.mkdirSync(itemsDir, { recursive: true });
    const catalog = [];
    const extractedCards: any[] = [];
    for (const d of decks) {
      if (!d || !d.id || !Array.isArray(d.slides) || d.slides.length === 0) continue;
      fs.writeFileSync(path.join(itemsDir, `${safeDeckFile(d.id)}.json`), JSON.stringify(d));
      const { slides, questions, steps, flashcards, ...meta } = d;
      const questionCount =
        meta.questionCount ||
        (Array.isArray(questions) ? questions.length : 0) ||
        slides.reduce((n: number, s: any) => n + (s.relatedQuestions?.length || s.questions?.length || 0), 0);
      const cardCount =
        meta.cardCount ||
        meta.flashcardCount ||
        (Array.isArray(flashcards) ? flashcards.length : 0) ||
        slides.reduce((n: number, s: any) => n + (s.flashcards?.length || 0), 0);

      // Sürüm seçimi (V1/V2) için öğrenciye gösterilen ölçüler
      let interactiveCount = 0;
      let wordCount = 0;
      // Test çöz sayaçları (services/testBank.ts ile aynı geçerlilik koşulları)
      const testCounts = { mini: 0, vaka: 0, tuzak: 0, bosluk: 0 };
      const grp = d.shortTitle || d.title;
      const dGrp = deckGroup(d.discipline);
      for (const s of slides) {
        const els = s.interactiveElements || s.elements || (s.interactiveElement ? [s.interactiveElement] : []);
        interactiveCount += Array.isArray(els) ? els.length : 0;
        for (const e of Array.isArray(els) ? els : []) {
          if (e?.type === 'micro_quiz') {
            const o = (e.microQuizOptions || e.options || []).filter((x: any) => String(x?.text ?? '').trim());
            if (String(e.question || e.sentence || '').trim() && o.length >= 2 && o.some((x: any) => x.isCorrect)) testCounts.mini++;
          } else if (e?.type === 'branching_logic') {
            const o = (e.options || []).filter((x: any) => String(x?.text ?? '').trim());
            if (String(e.scenario || e.question || '').trim() && o.length >= 2 && o.some((x: any) => x.isCorrect)) testCounts.vaka++;
          } else if (e?.type === 'spot_the_lie') {
            const it = (e.items || e.statements || []).filter((x: any) => String(x?.text ?? '').trim());
            if (it.length >= 3 && it.length <= 5 && it.filter((x: any) => x.isLie).length === 1) testCounts.tuzak++;
          } else if (e?.type === 'cloze_masking') {
            const m = String(e.maskedTerm || '').trim();
            if (m && String(e.sentence || '').toLocaleLowerCase('tr').includes(m.toLocaleLowerCase('tr'))) testCounts.bosluk++;
          }
        }
        wordCount += String(s.synthesisNarrative || s.content || '').split(/\s+/).filter(Boolean).length;
        if (Array.isArray(s.flashcards)) {
          s.flashcards.forEach((c: any, i: number) => {
            const front = c?.front || c?.question;
            const back = c?.back || c?.answer;
            if (!front || !back) return;
            extractedCards.push({
              id: `d:${d.id}:${s.slideNumber}:${c.id || i}`,
              group: grp,
              front,
              back,
              sub: `${dGrp} · slayt ${s.slideNumber}`,
              ...(c.hint ? { pearl: c.hint } : {}),
            });
          });
        }
      }
      catalog.push({
        ...meta,
        slideCount: slides.length,
        interactiveCount,
        testCounts,
        wordCount,
        sizeKb: Math.round(Buffer.byteLength(JSON.stringify(d)) / 1024),
        questionCount,
        cardCount,
        firstSlideNumber: slides[0]?.slideNumber ?? 1,
      });
    }
    fs.writeFileSync(catalogFile, JSON.stringify(catalog, null, 2));
    fs.writeFileSync(flashcardsFile, JSON.stringify(extractedCards));
    console.log(`[decks] ${catalog.length} deste bölündü (${extractedCards.length} kart ayrıştırıldı) → src/data/decks/`);
  };

  return {
    name: 'medsor-split-learning-decks',
    config() { run(); },
    configureServer(server) {
      const izle = parcaliKaynak()?.damga || src;
      server.watcher.add(izle);
      server.watcher.on('change', (file) => { if (path.resolve(file) === izle) run(); });
    },
  };
}
