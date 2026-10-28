/**
 * Path-based routing for the app's top-level pages.
 *
 *   /            → soru ekle (home)
 *   /bugun       → Bugün: kaldığın yer, hızlı erişim, günün spotu, haftalık çalışma
 *   /ogren       → learn catalogue, /ogren/<deckId> opens a deck
 *   /sorular     → soru havuzu
 *   /cikmis      → çıkmış sorular
 *   /calis       → study hub, /test → focused test mode
 *   /siralama    → leaderboard (başarım puanı, dönem içinde)
 *   /basarimlar  → hedefler (günlük/haftalık/kurul), başarımlar, ATP ve kilitler (?s=)
 *   /yonetim     → admin panel (admins only)
 *   /ara/<sorgu> → tüm veri setlerinde arama sonuçları
 *   /manage      → yönetim konsolu (manage.nofrostlife.com.tr ile aynı ekran)
 *   /canliders   → Sesli ders (eski adı Canlı ders): sesli dersler (liste), /canliders/<key> metin + PDF ile dinleme
 *   /soru-cozucu → sesli soru çözücü (branş başlangıç ekranı; eski /spotlar?gorunum=cozucu buraya yönlenir)
 *   /cevrimdisi → çevrimdışı merkezi (ders paketlerini indir, güncelle, sil)
 *   /olasi-sorular → sınav sonrası öğrenci hatıralarından kurulan olası sorular (?kurul=N)
 *   /gecmis-kurullar → sınavı geçmiş kurulların içeriğine bağlantılar
 *   /kamp        → kurul kampları (?kurul=N), /kamp/<kurul>/<brans> tek kamp: sesli anlatım, kalıp kartları, deneme
 *   /alternatif-cozucu → patoloji alternatif sesli çözücü (kısa anlatım, otomatik geçiş)
 *   /en-onemliler → sınav için en önemliler (100 puan; eski /spotlar?gorunum=onem buraya yönlenir)
 *   /patoloji-check-up → Patoloji Hızlı Check Up: ders slaytlarından karşılaştırma tabloları + kısa notlar (?bolum=)
 *   /saglik      → Sağlık Bakanlığı: resmî veriler + ders bağları, /saglik/<bölüm> (asi, karabuk, yenidogan …)
 *
 * Old `#tab` links keep working: they are rewritten to the matching path on load.
 *
 * 2026-10-21: adres çubuğunda görünen adres iç içedir (/dersler/…, /sorular/…, /kamplar/kurul1/…); ROUTE_PATHS iç
 * (eski) adreslerdir. Çeviri tek yerde: siteHaritasi.ts (icYol / disYol). pathFor ve navigateTo görünen adres üretir,
 * parseLocation görünen adresi iç adrese çevirip okur. Kurallar: docs/SITE_HARITASI_KURALLARI.md
 */
import type React from 'react';
import { disYol, icYol, kanonik } from './siteHaritasi';

export type AppRoute =
  | 'quick_add'
  | 'son_prova'
  | 'cikmis_cozucu'
  | 'today'
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
  | 'spots'
  | 'sinav_plani'
  | 'sinav_takvimi'
  | 'ders_programi'
  | 'transcripts'
  | 'ai_chat'
  | 'admin'
  | 'manage'
  | 'search'
  | 'test_cikmis'
  | 'tester_ozet'
  | 'ornek_sorular'
  | 'kazanimlar'
  | 'oncelikli_dersler'
  | 'music'
  | 'datacore'
  | 'diseases'
  | 'health_ministry'
  | 'canli_ders'
  | 'settings'
  | 'stats'
  | 'sinav_calisma'
  | 'soru_cozucu'
  | 'alternatif_cozucu'
  | 'en_onemliler'
  | 'patoloji_checkup'
  | 'genetik_checkup'
  | 'kmb_asistan'
  | 'bitirdiklerim'
  | 'basarimlar'
  | 'cevrimdisi'
  | 'olasi_sorular'
  | 'soru_haritasi'
  | 'oyunlar'
  | 'notlarim'
  | 'video_ders'
  | 'pdf_olustur'
  | 'topluluk'
  | 'hucrem'
  | 'zihin_haritasi'
  | 'yanlislarim'
  | 'bildirimler'
  | 'gecmis_kurullar'
  | 'kamp'
  | 'guncellemeler'
  | 'hub_dersler'
  | 'hub_sorular'
  | 'hub_kamplar'
  | 'hub_kaynaklar'
  | 'ders_detay'
  | 'kisi'
  | 'arkadaslar'
  | 'program_ekle'
  | 'arka_plan'
  | 'dil_bolge'
  | 'ilk_adimlar'
  | 'yardim'
  | 'bulunamadi';

export const ROUTE_PATHS: Record<AppRoute, string> = {
  quick_add: '/',
  today: '/bugun',
  learn: '/ogren',
  glossary: '/sozluk',
  flashcards: '/kartlar',
  questions: '/havuz',
  past_exams: '/cikmis',
  study: '/calis',
  practice: '/test',
  test_cikmis: '/test/cikmis',
  tester_ozet: '/tester/ozet',
  ornek_sorular: '/ornek-sorular',
  kazanimlar: '/kazanimlar',
  oncelikli_dersler: '/oncelikli-dersler',
  datacore: '/veri',
  leaderboard: '/siralama',
  music: '/muzik',
  notes: '/notlar',
  summaries: '/ozetler',
  spots: '/spotlar',
  sinav_plani: '/sinav-plani',
  sinav_takvimi: '/takvim',
  ders_programi: '/program',
  transcripts: '/ses-kayitlari',
  ai_chat: '/asistan',
  matrix: '/harita',
  booklet: '/kitapcik',
  admin: '/yonetim',
  manage: '/manage',
  search: '/ara',
  diseases: '/hastaliklar',
  health_ministry: '/saglik',
  canli_ders: '/canliders',
  settings: '/ayarlar',
  stats: '/istatistik',
  sinav_calisma: '/sinav-calisma',
  soru_cozucu: '/soru-cozucu',
  alternatif_cozucu: '/alternatif-cozucu',
  en_onemliler: '/en-onemliler',
  patoloji_checkup: '/patoloji-check-up',
  genetik_checkup: '/genetik-check-up',
  kmb_asistan: '/kmb',
  son_prova: '/son-prova',
  cikmis_cozucu: '/cikmis-cozucu',
  bitirdiklerim: '/bitirdiklerim',
  basarimlar: '/basarimlar',
  cevrimdisi: '/cevrimdisi',
  olasi_sorular: '/olasi-sorular',
  soru_haritasi: '/soru-haritasi',
  oyunlar: '/oyunlar',
  notlarim: '/notlarim',
  video_ders: '/video-ders',
  pdf_olustur: '/pdf-olustur',
  topluluk: '/topluluk',
  hucrem: '/hucrem',
  zihin_haritasi: '/zihin-haritasi',
  yanlislarim: '/yanlislarim',
  bildirimler: '/bildirimler',
  gecmis_kurullar: '/gecmis-kurullar',
  kamp: '/kamp',
  guncellemeler: '/guncellemeler',
  // merkez sayfaları: görünen /dersler · /sorular · /kamplar · /kaynaklar (siteHaritasi çevirir)
  hub_dersler: '/ders-merkezi',
  hub_sorular: '/soru-merkezi',
  hub_kamplar: '/kamp-merkezi',
  hub_kaynaklar: '/kaynak-merkezi',
  // v15 ders ayrıntısı: görünen /dersler/ders/kurulN/<dersKey>
  ders_detay: '/ders',
  kisi: '/kisi',
  arkadaslar: '/arkadaslar',
  // görünen /dersler/program/ekle (siteHaritasi çevirir)
  program_ekle: '/program-ekle',
  arka_plan: '/arka-plan', // H302: yalnız eski adres; siteHaritasi /cevrimdisi#isler'e yönlendirir, BY_SEGMENT'te tekil kalsın
  dil_bolge: '/dil-bolge',
  ilk_adimlar: '/ilk-adimlar',
  yardim: '/yardim',
  // AB16: bilinmeyen adres — parseLocation yalnız eşleşmeyen yolda döndürür
  bulunamadi: '/bulunamadi',
};

export const ROUTE_TITLES: Record<AppRoute, string> = {
  quick_add: 'Soru ekle',
  today: 'Bugün',
  learn: 'Etkileşimli dersler',
  glossary: 'Sözlük',
  diseases: 'Hastalıklar',
  health_ministry: 'Sağlık Bakanlığı',
  canli_ders: 'Sesli ders',
  flashcards: 'Ezber kartları',
  questions: 'Soru havuzu',
  past_exams: 'Çıkmış sorular',
  study: 'Listelerim ve notlar',
  practice: 'Deneme sınavı',
  test_cikmis: 'Test Edilen Çıkmış Sorular (Faz 14 İnceleme)',
  tester_ozet: '2026-2027 Ders Notları Test Laboratuvarı',
  ornek_sorular: 'Örnek sorular',
  kazanimlar: 'Kazanımlar',
  oncelikli_dersler: 'Öncelikli dersler',
  datacore: 'Veri Merkezi (Core v2)',
  leaderboard: 'Sıralama',
  music: 'Müzik',
  notes: 'Ders notları',
  summaries: 'Ders özetleri',
  spots: 'Sınav spotları',
  sinav_plani: 'Sınav planı',
  sinav_takvimi: 'Sınav takvimi',
  ders_programi: 'Ders programı',
  transcripts: 'Ses kayıtları',
  ai_chat: 'Asistan',
  matrix: 'Soru haritası',
  booklet: 'A4 kitapçık',
  admin: 'Yönetim',
  manage: 'Yönetim Konsolu',
  search: 'Arama',
  settings: 'Profil ve ayarlar',
  stats: 'İstatistiklerim',
  sinav_calisma: 'Sınav çalışması',
  soru_cozucu: 'Soru çözücü',
  alternatif_cozucu: 'Alternatif çözücü',
  en_onemliler: 'En önemliler',
  patoloji_checkup: 'Patoloji Hızlı Check Up',
  genetik_checkup: 'TBG Sınav Kampı',
  kmb_asistan: 'KMB görsel asistan',
  son_prova: 'Son Prova',
  cikmis_cozucu: 'Çıkmış çözücü',
  bitirdiklerim: 'Bitirdiklerim',
  basarimlar: 'Başarımlar',
  cevrimdisi: 'Çevrimdışı',
  olasi_sorular: 'Olası sorular',
  soru_haritasi: 'Soru haritası',
  oyunlar: 'Oyunlar',
  notlarim: 'Notlarım',
  video_ders: 'Video ders',
  pdf_olustur: 'PDF oluştur',
  topluluk: 'Topluluk',
  hucrem: 'Hücrem',
  zihin_haritasi: 'Zihin haritası',
  yanlislarim: 'Yanlışlarım',
  bildirimler: 'Bildirimler',
  gecmis_kurullar: 'Geçmiş kurullar',
  kamp: 'Kurul kampı',
  guncellemeler: 'Güncelleme günlüğü',
  hub_dersler: 'Ders çalış',
  hub_sorular: 'Soru çöz',
  hub_kamplar: 'Sınava hazırlan',
  hub_kaynaklar: 'Başvuru',
  ders_detay: 'Ders',
  kisi: 'Profil',
  arkadaslar: 'Arkadaşlar',
  program_ekle: 'Programa ekle',
  arka_plan: 'Arka plan işleri',
  dil_bolge: 'Dil ve bölge',
  ilk_adimlar: 'İlk adımlar',
  yardim: 'Yardım',
  bulunamadi: 'Sayfa bulunamadı',
};

const BY_SEGMENT: Record<string, AppRoute> = Object.fromEntries(
  (Object.entries(ROUTE_PATHS) as [AppRoute, string][])
    .filter(([, p]) => p !== '/' && !p.slice(1).includes('/'))
    .map(([r, p]) => [p.slice(1), r])
);

// Legacy aliases (old hash ids, English slugs) so shared links never 404 into the home page silently.
export const ALIASES: Record<string, AppRoute> = {
  quick_add: 'quick_add',
  today: 'today',
  bugun: 'today',
  'bugün': 'today',
  learn: 'learn',
  spotlar: 'spots',
  'sinav-plani': 'sinav_plani',
  takvim: 'sinav_takvimi',
  program: 'ders_programi',
  'ders-programi': 'ders_programi',
  spots: 'spots',
  'sinav-spotlari': 'spots',
  glossary: 'glossary',
  sozluk: 'glossary',
  ansiklopedi: 'glossary',
  dictionary: 'glossary',
  flashcards: 'flashcards',
  'ezber-kartlari': 'flashcards',
  questions: 'questions',
  sorular: 'questions',
  havuz: 'questions',
  ornek_sorular: 'ornek_sorular',
  'ornek-sorular': 'ornek_sorular',
  kazanimlar: 'kazanimlar',
  'oncelikli-dersler': 'oncelikli_dersler',
  oncelikli: 'oncelikli_dersler',
  'kolay-dersler': 'oncelikli_dersler',
  kazanim: 'kazanimlar',
  mufredat: 'kazanimlar',
  curriculum: 'kazanimlar',
  past_exams: 'past_exams',
  'past-exams': 'past_exams',
  cikmis: 'past_exams',
  'cikmis-sorular': 'past_exams',
  matrix: 'matrix',
  leaderboard: 'leaderboard',
  music: 'music',
  muzik: 'music',
  settings: 'settings',
  ayarlar: 'settings',
  profil: 'settings',
  profile: 'settings',
  'müzik': 'music',
  notes: 'notes',
  practice: 'practice',
  'test-coz': 'practice',
  booklet: 'booklet',
  study: 'study',
  summaries: 'summaries',
  transcripts: 'transcripts',
  ai_chat: 'ai_chat',
  asistan: 'ai_chat',
  chat: 'ai_chat',
  sohbet: 'ai_chat',
  admin: 'admin',
  manage: 'manage',
  yonetim: 'admin',
  search: 'search',
  arama: 'search',
  diseases: 'diseases',
  hastaliklar: 'diseases',
  'tibbi-hastaliklar': 'diseases',
  atlas: 'diseases',
  'saglik-bakanligi': 'health_ministry',
  bakanlik: 'health_ministry',
  'halk-sagligi': 'health_ministry',
  karabuk: 'health_ministry',
  'asi-takvimi': 'health_ministry',
  canli_ders: 'canli_ders',
  'canli-ders': 'canli_ders',
  'canlı-ders': 'canli_ders',
  'canlıders': 'canli_ders',
  'sesli-ders': 'canli_ders',
  'sinav-calisma': 'sinav_calisma',
  sinav_calisma: 'sinav_calisma',
  sinav: 'sinav_calisma',
  'sinav-hazirlik': 'sinav_calisma',
  'soru-kampi': 'sinav_calisma',
  soru_cozucu: 'soru_cozucu',
  cozucu: 'soru_cozucu',
  'sesli-cozucu': 'soru_cozucu',
  alternatif_cozucu: 'alternatif_cozucu',
  'alternatif-cozucu': 'alternatif_cozucu',
  alt_cozucu: 'alternatif_cozucu',
  'alt-cozucu': 'alternatif_cozucu',
  alternatif: 'alternatif_cozucu',
  en_onemliler: 'en_onemliler',
  onemliler: 'en_onemliler',
  'onem-listesi': 'en_onemliler',
  patoloji_checkup: 'patoloji_checkup',
  'check-up': 'patoloji_checkup',
  checkup: 'patoloji_checkup',
  'patoloji-checkup': 'patoloji_checkup',
  genetik_checkup: 'genetik_checkup',
  son_prova: 'son_prova',
  cikmis_cozucu: 'cikmis_cozucu',
  'cikmis-cozucu': 'cikmis_cozucu',
  'son-prova': 'son_prova',
  sonprova: 'son_prova',
  prova: 'son_prova',
  'sinav-provasi': 'son_prova',
  'genetik-checkup': 'genetik_checkup',
  'genetik-check-up': 'genetik_checkup',
  genetik: 'genetik_checkup',
  tbg: 'genetik_checkup',
  'genetik-kampi': 'genetik_checkup',
  kmb: 'kmb_asistan',
  kmb_asistan: 'kmb_asistan',
  bitirdiklerim: 'bitirdiklerim',
  basarimlar: 'basarimlar',
  basarim: 'basarimlar',
  hedefler: 'basarimlar',
  atp: 'basarimlar',
  bitirdiklerimiz: 'bitirdiklerim',
  ilerlemem: 'bitirdiklerim',
  'kontrol-listesi': 'bitirdiklerim',
  cevrimdisi: 'cevrimdisi',
  offline: 'cevrimdisi',
  indirilenler: 'cevrimdisi',
  'cevrimdisi-mod': 'cevrimdisi',
  olasi_sorular: 'olasi_sorular',
  'soru-haritasi': 'soru_haritasi',
  oyunlar: 'oyunlar',
  oyun: 'oyunlar',
  notlarim: 'notlarim',
  'video-ders': 'video_ders',
  videolar: 'video_ders',
  'pdf-olustur': 'pdf_olustur',
  topluluk: 'topluluk',
  kisi: 'kisi',
  arkadaslar: 'arkadaslar',
  arkadas: 'arkadaslar',
  'arka-plan-isleri': 'cevrimdisi', // H302: arka plan işleri /cevrimdisi'ye katıldı
  'dil-ve-bolge': 'dil_bolge',
  'ilk-adim': 'ilk_adimlar',
  yardim: 'yardim',
  'yardim-merkezi': 'yardim',
  sss: 'yardim',
  hucrem: 'hucrem',
  'zihin-haritasi': 'zihin_haritasi',
  yanlislarim: 'yanlislarim',
  bildirimler: 'bildirimler',
  'hücrem': 'hucrem',
  'notlarım': 'notlarim',
  olasi: 'olasi_sorular',
  'olasi-soru': 'olasi_sorular',
  gecmis_kurullar: 'gecmis_kurullar',
  'gecmis-kurul': 'gecmis_kurullar',
  arsiv: 'gecmis_kurullar',
  'kurul-arsivi': 'gecmis_kurullar',
  'sinav-kampi': 'kamp',
  guncellemeler: 'guncellemeler',
  guncelleme: 'guncellemeler',
  surumler: 'guncellemeler',
  degisiklikler: 'guncellemeler',
  changelog: 'guncellemeler',
};

export interface ParsedRoute {
  route: AppRoute;
  /** Second path segment, e.g. the deck id in /ogren/<deckId>. */
  param?: string;
}

/** Strips a deployment prefix such as /meds so the same build works under a sub-path. */
const stripBase = (pathname: string) => pathname.replace(/^\/meds(?=\/|$)/, '') || '/';

export const parseLocation = (gorunen: Pick<Location, 'pathname' | 'hash' | 'search'> = typeof window !== 'undefined' ? window.location : { pathname: '/', hash: '', search: '' }): ParsedRoute => {
  const loc = icAdres(gorunen);
  const hash = decodeURIComponent(loc.hash.replace(/^#\/?/, ''));
  const cleanPath = stripBase(loc.pathname);

  // Exact multi-segment route matching
  if (cleanPath === '/test/cikmis' || cleanPath.startsWith('/test/cikmis/')) {
    const extra = cleanPath.replace(/^\/test\/cikmis\/?/, '');
    return { route: 'test_cikmis', param: extra || undefined };
  }
  if (cleanPath === '/tester/ozet' || cleanPath.startsWith('/tester/ozet/')) {
    const extra = cleanPath.replace(/^\/tester\/ozet\/?/, '');
    return { route: 'tester_ozet', param: extra || undefined };
  }

  // /cikmis/<questionId> doğrudan soru rota desteği
  if (cleanPath.startsWith('/cikmis/')) {
    const extra = cleanPath.replace(/^\/cikmis\/?/, '');
    return { route: 'past_exams', param: extra || undefined };
  }

  // ?questionId=... URL sorgu parametresi desteği
  if (loc.search) {
    try {
      const sp = new URLSearchParams(loc.search);
      const qId = sp.get('questionId');
      if (qId) return { route: 'past_exams', param: qId };
    } catch {}
  }

  const segs = cleanPath.split('/').filter(Boolean).map(decodeURIComponent);
  if (segs.length > 0) {
    const route = BY_SEGMENT[segs[0]] || ALIASES[segs[0]];
    if (route) return { route, param: segs[1] };
    // AB16: tanınmayan yol sessizce ana sayfaya düşmez; siteHaritasi çevirisi ve takma adlar yukarıda denendi
    return { route: 'bulunamadi' };
  }
  // Legacy #tab links (only on the root path)
  if (hash === 'tester/ozet' || hash === 'tester_ozet') return { route: 'tester_ozet' };
  if (hash === 'test/cikmis' || hash === 'test_cikmis') return { route: 'test_cikmis' };
  if (hash && (ALIASES[hash] || BY_SEGMENT[hash])) return { route: ALIASES[hash] || BY_SEGMENT[hash] };
  return { route: 'quick_add' };
};

/** Görünen adresi iç adrese çevirir (siteHaritasi.icYol); hash korunur */
function icAdres(l: Pick<Location, 'pathname' | 'hash' | 'search'>): Pick<Location, 'pathname' | 'hash' | 'search'> {
  try {
    const u = new URL(icYol(l.pathname + l.search), 'https://x.invalid');
    return { pathname: u.pathname, search: u.search, hash: l.hash };
  } catch {
    return l;
  }
}

/** Bir sayfanın iç (eski) adresi — yalnız çeviri katmanı ve sınamalar için */
export const icPathFor = (route: AppRoute, param?: string) =>
  ROUTE_PATHS[route] + (param ? `/${encodeURIComponent(param)}` : '');

/** Bir sayfanın adres çubuğunda görünen adresi */
export const pathFor = (route: AppRoute, param?: string) => disYol(icPathFor(route, param));

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

/**
 * A page's deep-link target id: the path parameter (/sozluk/<id>) or the legacy query keys
 * share links used (?id=, ?term=, ?noteId=, ?ornekId= …). Undefined when the URL has none.
 */
export const deepLinkIdFor = (route: AppRoute, param?: string): string | undefined => {
  if (param) return param;
  if (typeof window === 'undefined') return undefined;
  const sp = new URLSearchParams(window.location.search);
  const keys: Partial<Record<AppRoute, string[]>> = {
    glossary: ['id', 'term'],
    diseases: ['id'],
    summaries: ['noteId', 'summaryId', 'id'],
    ornek_sorular: ['ornekId'],
    flashcards: ['id'],
    notes: ['id'],
  };
  for (const k of keys[route] || []) {
    const v = sp.get(k);
    if (v) return v;
  }
  return undefined;
};

/**
 * In-app navigation to any path (with query/hash): pushes the URL and lets the App's popstate
 * handler rebuild the page state from it, so a link behaves the same clicked in-app or opened fresh.
 */
export const navigateTo = (url: string) => {
  try {
    const u = new URL(url, window.location.origin);
    const next = kanonik(u.pathname + u.search + u.hash);
    if (window.location.pathname + window.location.search + window.location.hash !== next) {
      window.history.pushState({}, '', next);
      (window as unknown as { __icGezinti?: boolean }).__icGezinti = true;
    }
    window.dispatchEvent(new PopStateEvent('popstate'));
    window.scrollTo({ top: 0 });
  } catch {
    window.location.assign(url);
  }
};
