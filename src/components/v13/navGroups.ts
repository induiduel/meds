import { Archive, ClipboardCheck, GraduationCap, Library, Sun, UserRound } from 'lucide-react';
import type React from 'react';
import type { AppRoute } from '../../router';
import { NAV_ITEMS, NAV_TREE, type NavItem } from '../shell/navModel';

/**
 * v13 "Ada" gezinmesi: iki düzey. Omurga = öğrencinin niyeti (6 öbek), panel = öbeğin sayfaları.
 * Sayfalar navModel.NAV_TREE'den gelir (tek kaynak); burada yalnız öbeklere bölünür. Her sayfa en çok 2 dokunuşta.
 */
export interface V13Group {
  id: 'bugun' | 'ders' | 'sinav' | 'coz' | 'basvuru' | 'sen';
  label: string;
  /** Alt adada / omurgada kısa ad */
  short: string;
  icon: React.ElementType;
  items: NavItem[];
}

const byLabel = (l: string) => NAV_TREE.find((g) => g.label === l)?.items || [];

export const V13_GROUPS: V13Group[] = [
  { id: 'bugun', label: 'Bugün', short: 'Bugün', icon: Sun, items: [NAV_ITEMS.today] },
  { id: 'ders', label: 'Ders çalış', short: 'Ders', icon: GraduationCap, items: byLabel('Ders çalış') },
  { id: 'sinav', label: 'Sınava hazırlan', short: 'Sınav', icon: ClipboardCheck, items: byLabel('Sınava hazırlan') },
  { id: 'coz', label: 'Soru çöz', short: 'Çöz', icon: Archive, items: byLabel('Soru çöz') },
  { id: 'basvuru', label: 'Başvuru', short: 'Başvur', icon: Library, items: byLabel('Başvuru') },
  { id: 'sen', label: 'Sen ve topluluk', short: 'Sen', icon: UserRound, items: [...byLabel('Kişisel'), ...byLabel('Topluluk')] },
];

export const groupOf = (r: AppRoute): V13Group | undefined => V13_GROUPS.find((g) => g.items.some((it) => it.id === r));

/** Öbekte en son açılan sayfa (alt adada öbek düğmesi oraya götürür) */
const LAST_KEY = 'medsoru_v13_last';
export const readLast = (): Partial<Record<V13Group['id'], AppRoute>> => {
  try {
    return JSON.parse(localStorage.getItem(LAST_KEY) || '{}') || {};
  } catch {
    return {};
  }
};
export const rememberLast = (r: AppRoute) => {
  const g = groupOf(r);
  if (!g) return;
  try {
    localStorage.setItem(LAST_KEY, JSON.stringify({ ...readLast(), [g.id]: r }));
  } catch {
    /* gizli pencere */
  }
};
export const lastIn = (g: V13Group): AppRoute => {
  const r = readLast()[g.id];
  return r && g.items.some((it) => it.id === r) ? r : g.items[0].id;
};
