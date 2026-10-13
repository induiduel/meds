import { useEffect, useRef } from 'react';
import { realtimeEventService } from '../services/realtimeEvents';

/**
 * Canlı SSE olayına abone ol (bileşen ömrü boyunca). `fn` her çizimde güncel kalır; olay seli ekranı
 * boğmasın diye `debounceMs` içinde gelenler tek çağrıya indirilir. Kaçan olay telafisi edilemediğinde
 * (`resync`) de çağrılır: ekran kendi verisini yeniden çeker.
 */
export function useLiveEvent(event: string, fn: (payload: any) => void, opts: { enabled?: boolean; debounceMs?: number } = {}) {
  const fnRef = useRef(fn);
  fnRef.current = fn;
  const { enabled = true, debounceMs = 250 } = opts;
  useEffect(() => {
    if (!enabled) return;
    let timer: ReturnType<typeof setTimeout> | null = null;
    let last: any = null;
    const fire = (p: any) => {
      last = p;
      if (timer) return;
      timer = setTimeout(() => {
        timer = null;
        fnRef.current(last);
      }, debounceMs);
    };
    const offs = [realtimeEventService.on(event, fire), realtimeEventService.on('resync', () => fire({ resync: true }))];
    return () => {
      offs.forEach((off) => off());
      if (timer) clearTimeout(timer);
    };
  }, [event, enabled, debounceMs]);
}
