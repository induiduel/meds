/**
 * Yazım yardımcısı işçisinin (src/workers/composerWorker.ts) istemcisi.
 *  - Her işlem türünde en çok 1 istek işçide bekler; hızlı yazımda aradaki istekler atlanır
 *    (yalnız en son metin hesaplanır, kuyruk birikmez). Atlanan istek `null` ile döner.
 *  - Worker kurulamazsa (eski tarayıcı) aynı motor ana iş parçacığında çalışır.
 */
import type { AssistResult } from './smartComposerService';

type Op = 'assist' | 'spell';
type SpellResult = { text: string; changes: { from: string; to: string }[] } | null;
type Pending = { payload: any; resolve: (v: any) => void };

let worker: Worker | null = null;
let broken = false;
let seq = 0;
const waiting = new Map<number, (m: any) => void>();
const busy: Record<Op, boolean> = { assist: false, spell: false };
const queued: Partial<Record<Op, Pending>> = {};

function getWorker(): Worker | null {
  if (worker || broken || typeof Worker === 'undefined') return worker;
  try {
    worker = new Worker(new URL('../workers/composerWorker.ts', import.meta.url), { type: 'module' });
    worker.onmessage = (e: MessageEvent<{ id: number }>) => {
      const cb = waiting.get(e.data.id);
      if (cb) { waiting.delete(e.data.id); cb(e.data); }
    };
    worker.onerror = () => {
      // işçi çöktü: bekleyenleri boş yanıtla kapat, sonraki istekler ana iş parçacığında çalışır
      broken = true;
      worker?.terminate();
      worker = null;
      for (const cb of waiting.values()) cb({ ok: false });
      waiting.clear();
    };
  } catch {
    broken = true;
    worker = null;
  }
  return worker;
}

async function runLocal(op: Op, payload: any): Promise<any> {
  const { smartComposerService, loadComposerModel } = await import('./smartComposerService');
  await loadComposerModel();
  return op === 'assist'
    ? smartComposerService.getAssist(payload.text, payload.sources)
    : smartComposerService.getSpellingCorrection(payload.text);
}

function send(op: Op, payload: any, resolve: (v: any) => void): void {
  const w = getWorker();
  busy[op] = true;
  const done = (v: any) => {
    resolve(v);
    busy[op] = false;
    const next = queued[op];
    if (next) { delete queued[op]; send(op, next.payload, next.resolve); }
  };
  if (!w) { runLocal(op, payload).then(done, () => done(null)); return; }
  const id = ++seq;
  waiting.set(id, (m) => done(m.ok ? m.result : null));
  w.postMessage({ id, op, ...payload });
}

function request<T>(op: Op, payload: any): Promise<T | null> {
  return new Promise((resolve) => {
    if (!busy[op]) { send(op, payload, resolve); return; }
    // işçi meşgul: bekleyen eski isteği düşür, yerine en yenisini koy
    queued[op]?.resolve(null);
    queued[op] = { payload, resolve };
  });
}

export const composerClient = {
  /** Hayalet metin, kelime önerileri ve "Düzelt" (yazım + noktalama) */
  assist: (text: string, sources: string[] = []) => request<AssistResult>('assist', { text, sources }),
  /** Yalnız yazım düzeltmesi (seçenek kutuları, serbest metin) */
  spell: (text: string) => request<SpellResult>('spell', { text }),
  /** Modeli önceden yükler (kutuya odaklanınca) */
  warm: () => { const w = getWorker(); if (w) w.postMessage({ id: ++seq, op: 'warm' }); },
};
