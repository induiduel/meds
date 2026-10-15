import { useEffect, useState } from 'react';
import type { AppRoute } from '../../router';
import { V12_PHONE_PAGES, type NavItem } from './navModel';

/**
 * Telefon gezinmesinin kişisel katmanı (v12 alt çubuk + "Tüm sayfalar"):
 *  - Alt çubuğun 3 yuvası (ortadaki "+ Soru ekle" sabit) öğrencinin seçtiği sayfalar olabilir → `medsoru_tabbar_v1` (profille eşitlenir).
 *  - Son açılan sayfalar → `medsoru_nav_recent_v1` (yalnız bu cihaz).
 *  - Sayfa arama: ad, kısa ad ve açıklama; Türkçe harfler ve büyük/küçük harf yok sayılır.
 */
const SLOTS_KEY = 'medsoru_tabbar_v1';
const RECENT_KEY = 'medsoru_nav_recent_v1';
const SLOTS_EVENT = 'medsoru:tabbar';

export const DEFAULT_TAB_SLOTS: AppRoute[] = ['today', 'learn', 'past_exams'];

const PAGE_IDS = new Set<AppRoute>(V12_PHONE_PAGES.map((it) => it.id));

const read = <T>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};
const write = (key: string, v: unknown) => {
  try {
    localStorage.setItem(key, JSON.stringify(v));
  } catch {
    /* depolama kapalı */
  }
};

const readSlots = (): AppRoute[] => {
  const v = read<unknown>(SLOTS_KEY, null);
  if (!Array.isArray(v) || v.length !== 3) return DEFAULT_TAB_SLOTS;
  const ids = v.filter((x): x is AppRoute => typeof x === 'string' && PAGE_IDS.has(x as AppRoute));
  return ids.length === 3 && new Set(ids).size === 3 ? ids : DEFAULT_TAB_SLOTS;
};

export const setTabSlots = (slots: AppRoute[] | null) => {
  if (slots) write(SLOTS_KEY, slots);
  else {
    try {
      localStorage.removeItem(SLOTS_KEY);
    } catch {
      /* yok */
    }
  }
  window.dispatchEvent(new Event(SLOTS_EVENT));
};

/** Alt çubuğun 3 seçilebilir yuvası (soldan: 1, 2, 4. sıra) */
export const useTabSlots = (): AppRoute[] => {
  const [slots, setSlots] = useState(readSlots);
  useEffect(() => {
    const on = () => setSlots(readSlots());
    const onStorage = (e: StorageEvent) => {
      if (e.key === null || e.key === SLOTS_KEY) on();
    };
    window.addEventListener(SLOTS_EVENT, on);
    window.addEventListener('storage', onStorage);
    return () => {
      window.removeEventListener(SLOTS_EVENT, on);
      window.removeEventListener('storage', onStorage);
    };
  }, []);
  return slots;
};

/** Açılan sayfayı son kullanılanlara yazar; listeyi (en yeni önce) döndürür */
export const useRecentPages = (active: AppRoute): AppRoute[] => {
  const [list, setList] = useState<AppRoute[]>(() => read<AppRoute[]>(RECENT_KEY, []).filter((id) => PAGE_IDS.has(id)));
  useEffect(() => {
    if (!PAGE_IDS.has(active)) return;
    setList((prev) => {
      if (prev[0] === active) return prev;
      const next = [active, ...prev.filter((id) => id !== active)].slice(0, 8);
      write(RECENT_KEY, next);
      return next;
    });
  }, [active]);
  return list;
};

const fold = (s: string) =>
  s
    .toLocaleLowerCase('tr-TR')
    .replace(/ı/g, 'i')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '');

/** Sayfa arama: önce adı sorguyla başlayanlar, sonra adında geçenler, sonra açıklamasında geçenler */
export const matchPages = (q: string, pages: NavItem[]): NavItem[] => {
  const words = fold(q).split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  const scored: { it: NavItem; s: number }[] = [];
  for (const it of pages) {
    const name = fold(`${it.label} ${it.short || ''}`);
    const all = `${name} ${fold(it.hint)}`;
    if (!words.every((w) => all.includes(w))) continue;
    const s = name.split(/\s+/).some((p) => p.startsWith(words[0])) ? 0 : words.every((w) => name.includes(w)) ? 1 : 2;
    scored.push({ it, s });
  }
  return scored.sort((a, b) => a.s - b.s).map((x) => x.it);
};
