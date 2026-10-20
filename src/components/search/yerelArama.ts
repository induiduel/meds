/**
 * İnternetsiz arama yedeği: sunucu araması (/api/search/all) yanıt vermezse cihazdaki verilerde aranır —
 * çıkmış sorular (pastQuestionsCache, IndexedDB), havuz soruları (offlineDatabaseService), sözlük (GLOSSARY) ve
 * etkileşimli ders başlıkları (DECK_CATALOG). Sonuçlar sunucu biçimindedir (SearchHit; içerik localRagEngine
 * kalıbıyla yazılır), HitView aynı kartları çizer. Puanlama basit: terimlerin tümü geçmeli, başlıkta geçen öne çıkar.
 */
import type { SearchDocType, SearchHit, SearchResponse } from './searchShared';

const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

interface Belge { hit: SearchHit; metin: string; baslik: string }
let belgeler: Promise<Belge[]> | null = null;
let kurulma = 0;

async function kur(): Promise<Belge[]> {
  const out: Belge[] = [];
  const ekle = (hit: SearchHit) => out.push({ hit, metin: katla(`${hit.title}\n${hit.content}`), baslik: katla(hit.title) });
  const soruIcerik = (q: any) => {
    const r = q.reconstruction;
    const stem = String(r?.stem || q.rawStem || q.topic || '').trim();
    const sec = (r?.options?.length ? r.options : q.options || []).map((o: any) => `${o.key}) ${o.text}`).join('\n');
    const cevap = r?.correctAnswer || q.claimedAnswer || '';
    return `Ders / Branş: ${q.discipline || 'Tıp'}\nKurul: ${q.committeeId || ''}\nSınav Yılı: ${q.examYear || 'Geçmiş Sınav'}\nKonu: ${q.topic || ''}\nSoru Kökü:\n${stem}\n\nSeçenekler:\n${sec}\n${cevap ? `\nDoğru / Kabul Edilen Cevap: ${cevap}\n` : ''}${r?.explanation ? `\nAçıklama: ${r.explanation}` : ''}`;
  };
  const soru = (q: any, tur: SearchDocType) => ekle({
    id: `yerel-${tur}-${q.id}`, documentId: q.id, documentType: tur, committeeId: q.committeeId, discipline: q.discipline,
    title: `${q.discipline || 'Tıp'} - ${q.topic || (tur === 'past_question' ? 'Çıkmış Soru' : 'Havuz sorusu')}${q.examYear ? ` (${q.examYear})` : ''}`,
    pageNumber: q.questionNumber, snippet: '', content: soruIcerik(q), score: 0,
  });
  const [{ pastQuestionsCache }, { offlineDatabaseService }, { GLOSSARY }, { loadDeckCatalog }] = await Promise.all([
    import('../../services/pastQuestionsCache'), import('../../services/offlineDatabaseService'),
    import('../../data/glossary'), import('../../data/deckStore'),
  ]);
  const [cikmis, havuz, desteler] = await Promise.all([
    pastQuestionsCache.getCachedQuestions().catch(() => []),
    offlineDatabaseService.getQuestions().catch(() => []),
    loadDeckCatalog().catch(() => []),
  ]);
  const gorulen = new Set<string>();
  for (const q of cikmis) { gorulen.add(q.id); soru(q, 'past_question'); }
  for (const q of havuz) if (!gorulen.has(q.id)) soru(q, q.isPastExam ? 'past_question' : 'active_question');
  for (const g of GLOSSARY) ekle({
    id: `yerel-gloss-${g.term}`, documentId: g.term, documentType: 'glossary_term', discipline: g.discipline, title: `Sözlük: ${g.term}`,
    snippet: '', score: 0,
    content: `[SÖZLÜK TERİMİ]\nTerim: ${g.term}\nKategori: ${g.category}\nTanım: ${g.definition}${g.clinicalPearls ? `\nKlinik İnci: ${g.clinicalPearls}` : ''}${g.aliases?.length ? `\nEşanlamlı: ${g.aliases.join(', ')}` : ''}`,
  });
  for (const d of desteler) ekle({
    id: `yerel-deck-${d.id}`, documentId: String(d.id), documentType: 'deck_slide', discipline: d.discipline, title: `${d.title}`,
    pageNumber: d.firstSlideNumber, snippet: '', score: 0,
    content: `[İNTERAKTİF DERS SLAYTI]\nDeste: ${d.title}\nDers: ${d.discipline || ''}\n\n${d.overview || ''}\n${(d.highYieldPearls || []).join('\n')}`,
  });
  return out;
}

export async function yerelArama(
  q: string,
  opts: { types?: SearchDocType[]; offset?: number; limit?: number; committeeId?: string } = {},
): Promise<SearchResponse | null> {
  const terimler = katla(q).split(/\s+/).filter((t) => t.length > 1);
  if (!terimler.length) return null;
  // Veri cihazda değişebilir (eşitleme, yeni paket): 2 dakikadan eskiyse yeniden kurulur
  if (!belgeler || Date.now() - kurulma > 120_000) { kurulma = Date.now(); belgeler = kur().catch(() => []); }
  const hepsi = await belgeler;
  const uygun = hepsi.filter((b) => (!opts.types?.length || opts.types.includes(b.hit.documentType))
    && (!opts.committeeId || !b.hit.committeeId || b.hit.committeeId === opts.committeeId)
    && terimler.every((t) => b.metin.includes(t)));
  const puanli = uygun.map((b) => ({ b, p: terimler.reduce((a, t) => a + (b.baslik.includes(t) ? 3 : 0) + Math.min(3, b.metin.split(t).length - 1), 0) }))
    .sort((x, y) => y.p - x.p);
  const byType: SearchResponse['byType'] = {};
  for (const { b } of puanli) byType[b.hit.documentType] = (byType[b.hit.documentType] || 0) + 1;
  const off = opts.offset || 0;
  const lim = opts.limit || 5;
  const results = puanli.slice(off, off + lim).map(({ b, p }) => {
    const ham = b.hit.content.replace(/\s+/g, ' ');
    const i = katla(ham).indexOf(terimler[0]);
    const snippet = ham.slice(Math.max(0, i - 80), Math.max(0, i - 80) + 240);
    return { ...b.hit, score: p, snippet };
  });
  return { query: q, total: puanli.length, capped: false, byType, results };
}
