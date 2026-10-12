/**
 * Soru yazım yardımcısı işçisi: derlem modelini (≈2 MB JSON) ayrıştırma, dizin kurma, yazım
 * düzeltme ve cümle devamı hesapları ana iş parçacığının dışında çalışır; yazarken arayüz donmaz.
 * İstemci: src/services/composerClient.ts
 */
import { smartComposerService, loadComposerModel } from '../services/smartComposerService';

type Req =
  | { id: number; op: 'assist'; text: string; sources: string[] }
  | { id: number; op: 'spell'; text: string }
  | { id: number; op: 'warm' };

const ctx = self as unknown as {
  onmessage: ((e: MessageEvent<Req>) => void) | null;
  postMessage: (m: unknown) => void;
};

ctx.onmessage = async (e) => {
  const m = e.data;
  try {
    await loadComposerModel();
    if (m.op === 'assist') ctx.postMessage({ id: m.id, ok: true, result: smartComposerService.getAssist(m.text, m.sources) });
    else if (m.op === 'spell') ctx.postMessage({ id: m.id, ok: true, result: smartComposerService.getSpellingCorrection(m.text) });
    else ctx.postMessage({ id: m.id, ok: true, result: smartComposerService.hasModel() });
  } catch (err: any) {
    ctx.postMessage({ id: m.id, ok: false, error: String(err?.message || err) });
  }
};
