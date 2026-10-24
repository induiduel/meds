/** KMB sahne eylemleri: cümle ilerledikçe birikir; sayaçlar aynı eylem yeniden gelince animasyonu baştan oynatır */
import type { SahneDurum } from './sahneler';

export type Eylem = { t: 'vurgula' | 'ciz' | 'renk' | 'goster' | 'gizle' | 'etiket'; id: string; renk?: string };

export function uygula(durum: SahneDurum, eylemler: Eylem[] = []): SahneDurum {
  const d = { ...durum };
  for (const e of eylemler) {
    const o = { ...(d[e.id] || {}) };
    if (e.t === 'vurgula') o.vurgu = (o.vurgu || 0) + 1;
    else if (e.t === 'ciz') { o.ciz = (o.ciz || 0) + 1; o.gor = true; }
    else if (e.t === 'renk') o.renk = e.renk;
    else if (e.t === 'goster') o.gor = true;
    else if (e.t === 'gizle') { o.gor = false; o.etiket = false; }
    else if (e.t === 'etiket') o.etiket = true;
    d[e.id] = o;
  }
  return d;
}
