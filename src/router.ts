/**
 * Path-based routing for the app's top-level pages.
 *
 *   /            → soru ekle (home)
 *   /ogren       → learn catalogue, /ogren/<deckId> opens a deck
 *   /sorular     → soru havuzu
 *   /cikmis      → çıkmış sorular
 *   /calis       → study hub, /test → focused test mode
 *   /siralama    → leaderboard
 *   /yonetim     → admin panel (admins only)
 *   /manage      → yönetim konsolu (manage.nofrostlife.com.tr ile aynı ekran)
 *
 * Old `#tab` links keep working: they are rewritten to the matching path on load.
 */
import type React from 'react';

export type AppRoute =
  | 'quick_add'
  | 'learn'
  | 'glossary'
  | 'flashcards'
  | 'questions'
  | 'past_exams'
  | 'matrix'
  | 'leaderboard'
  | 'notes'
  | 'practice'
  | 'booklet'
  | 'study'
  | 'summaries'
  | 'transcripts'
  | 'admin'
  | 'manage';

export const ROUTE_PATHS: Record<AppRoute, string> = {
  quick_add: '/',
  learn: '/ogren',
  glossary: '/sozluk',
  flashcards: '/kartlar',
  questions: '/sorular',
  past_exams: '/cikmis',
  study: '/calis',
  practice: '/test',
  leaderboard: '/siralama',
  notes: '/notlar',
  summaries: '/ozetler',
  transcripts: '/ses-kayitlari',
  matrix: '/harita',
  booklet: '/kitapcik',
  admin: '/yonetim',
  manage: '/manage',
};

export const ROUTE_TITLES: Record<AppRoute, string> = {
  quick_add: 'Soru ekle',
  learn: 'Öğren',
  glossary: 'Sözlük & Ansiklopedi',
  flashcards: 'Ezber kartları',
  questions: 'Soru havuzu',
  past_exams: 'Çıkmış sorular',
  study: 'Çalış',
  practice: 'Test çöz',
  leaderboard: 'Sıralama',
  notes: 'Ders notları',
  summaries: 'Ders özetleri',
  transcripts: 'Ses kayıtları',
  matrix: 'Soru haritası',
  booklet: 'A4 kitapçık',
  admin: 'Yönetim',
  manage: 'Yönetim Konsolu',
};

const BY_SEGMENT: Record<string, AppRoute> = Object.fromEntries(
  (Object.entries(ROUTE_PATHS) as [AppRoute, string][])
    .filter(([, p]) => p !== '/')
    .map(([r, p]) => [p.slice(1), r])
);

// Legacy aliases (old hash ids, English slugs) so shared links never 404 into the home page silently.
const ALIASES: Record<string, AppRoute> = {
  quick_add: 'quick_add',
  learn: 'learn',
  glossary: 'glossary',
  sozluk: 'glossary',
  ansiklopedi: 'glossary',
  dictionary: 'glossary',
  flashcards: 'flashcards',
  'ezber-kartlari': 'flashcards',
  questions: 'questions',
  havuz: 'questions',
  past_exams: 'past_exams',
  'cikmis-sorular': 'past_exams',
  matrix: 'matrix',
  leaderboard: 'leaderboard',
  notes: 'notes',
  practice: 'practice',
  'test-coz': 'practice',
  booklet: 'booklet',
  study: 'study',
  summaries: 'summaries',
  transcripts: 'transcripts',
  admin: 'admin',
  manage: 'manage',
  yonetim: 'admin',
};

export interface ParsedRoute {
  route: AppRoute;
  /** Second path segment, e.g. the deck id in /ogren/<deckId>. */
  param?: string;
}

/** Strips a deployment prefix such as /meds so the same build works under a sub-path. */
const stripBase = (pathname: string) => pathname.replace(/^\/meds(?=\/|$)/, '') || '/';

export const parseLocation = (loc: Pick<Location, 'pathname' | 'hash'> = window.location): ParsedRoute => {
  const hash = decodeURIComponent(loc.hash.replace(/^#\/?/, ''));
  const segs = stripBase(loc.pathname).split('/').filter(Boolean).map(decodeURIComponent);
  if (segs.length > 0) {
    const route = BY_SEGMENT[segs[0]] || ALIASES[segs[0]];
    if (route) return { route, param: segs[1] };
  }
  // Legacy #tab links (only on the root path)
  if (hash && (ALIASES[hash] || BY_SEGMENT[hash])) return { route: ALIASES[hash] || BY_SEGMENT[hash] };
  return { route: 'quick_add' };
};

export const pathFor = (route: AppRoute, param?: string) =>
  ROUTE_PATHS[route] + (param ? `/${encodeURIComponent(param)}` : '');

/** Push (or replace) the address bar without reloading; no-op if already there. */
export const writeLocation = (route: AppRoute, param?: string, replace = false) => {
  try {
    const next = pathFor(route, param);
    const current = window.location.pathname + window.location.hash;
    if (current === next) return;
    window.history[replace ? 'replaceState' : 'pushState']({ route, param }, '', next);
  } catch {
    /* sandboxed iframes may block history writes */
  }
};

/** Click handler for <a href> nav links: plain clicks route in-app, modified clicks open a new tab. */
export const linkClick = (go: () => void) => (e: React.MouseEvent) => {
  if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  e.preventDefault();
  go();
};
