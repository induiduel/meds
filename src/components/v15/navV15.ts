import { BookOpen, CircleHelp, Flag, House, Library, MessagesSquare, ShieldCheck, Stethoscope, UserRound } from 'lucide-react';
import type React from 'react';
import type { AppRoute } from '../../router';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { NAV_ITEMS, NAV_TREE, type NavItem } from '../shell/navModel';

/**
 * v15 gezinmesi (tasarım sistemi v15 › Kabuk): "ne yapmak istiyorum?" sorusunun dört işi + önde Bugün.
 * Bölümün alt sayfaları merkez modelinden (merkezModel.MERKEZ_ARACLARI) gelir; merkezde olmayan ama NAV_TREE'de aynı
 * gruptaki sayfalar sona eklenir. Böylece kenar menüsü, ray, alt sekme ve merkez sayfaları aynı listeyi gösterir.
 */
export interface V15Section {
  id: 'bugun' | 'dersler' | 'sorular' | 'kamplar' | 'kaynaklar';
  label: string;
  /** Alt sekme ve rayda kısa ad */
  short: string;
  icon: React.ElementType;
  /** Bölüm düğmesinin açtığı sayfa (merkez) */
  hub: AppRoute;
  items: NavItem[];
}

const NAV_GROUP: Record<Exclude<V15Section['id'], 'bugun'>, string> = {
  dersler: 'Ders çalış',
  sorular: 'Soru çöz',
  kamplar: 'Sınava hazırlan',
  kaynaklar: 'Başvuru',
};

const itemsOf = (id: Exclude<V15Section['id'], 'bugun'>): NavItem[] => {
  const seen = new Set<AppRoute>();
  const out: NavItem[] = [];
  const add = (it?: NavItem) => {
    if (!it || seen.has(it.id)) return;
    seen.add(it.id);
    out.push(it);
  };
  MERKEZ_ARACLARI[id].forEach((a) => add(NAV_ITEMS[a.id]));
  (NAV_TREE.find((g) => g.label === NAV_GROUP[id])?.items || []).forEach(add);
  return out;
};

export const V15_SECTIONS: V15Section[] = [
  { id: 'bugun', label: 'Bugün', short: 'Bugün', icon: House, hub: 'today', items: [] },
  { id: 'dersler', label: 'Ders çalış', short: 'Ders', icon: BookOpen, hub: 'hub_dersler', items: itemsOf('dersler') },
  { id: 'sorular', label: 'Soru çöz', short: 'Soru', icon: CircleHelp, hub: 'hub_sorular', items: itemsOf('sorular') },
  { id: 'kamplar', label: 'Sınava hazırlan', short: 'Sınav', icon: Flag, hub: 'hub_kamplar', items: itemsOf('kamplar') },
  { id: 'kaynaklar', label: 'Başvuru', short: 'Başvuru', icon: Library, hub: 'hub_kaynaklar', items: itemsOf('kaynaklar') },
];

/** Menüde ayrı satırı olmayan alt sayfalar (ders ayrıntısı Ders çalış bölümündedir) */
const ALT_SAYFA: Partial<Record<AppRoute, V15Section['id']>> = { ders_detay: 'dersler' };

/** Sayfanın bölümü (merkez sayfası da kendi bölümüne aittir); kişisel sayfalarda undefined */
export const sectionOf = (r: AppRoute): V15Section | undefined =>
  V15_SECTIONS.find((s) => s.hub === r || ALT_SAYFA[r] === s.id || s.items.some((it) => it.id === r));

/* ---------------------------------------------------------------------------
 * Bütün sayfalar menüsü (telefon/tablet "Menü" ızgarası ve masaüstü kenar çubuğu aynı listeyi kullanır).
 * Yeni sayfa NAV_TREE'ye (shell/navModel) eklenince burada kendiliğinden görünür; Kişisel'e yalnız aşağıdaki liste.
 * ------------------------------------------------------------------------- */
export interface MenuGrubu { id: string; label: string; icon: React.ElementType; hub?: AppRoute; items: NavItem[] }
const KISISEL: AppRoute[] = ['bitirdiklerim', 'study', 'notlarim', 'stats', 'pdf_olustur', 'cevrimdisi', 'music', 'settings'];

const YONETIM = { id: 'manage', label: 'Yönetim', short: 'Yönetim', hint: 'Yönetim konsolu', icon: ShieldCheck, tint: '#64748B' } as NavItem;

export function menuGruplari(isAdmin: boolean): MenuGrubu[] {
  const seen = new Set<AppRoute>(['today']);
  const al = (ids: (NavItem | undefined)[]) => ids.filter((it): it is NavItem => !!it && !seen.has(it.id) && (seen.add(it.id), true));
  const grup = (label: string) => NAV_TREE.find((g) => g.label === label)?.items || [];
  const sec = (id: V15Section['id']) => V15_SECTIONS.find((s) => s.id === id)!;
  const out: MenuGrubu[] = [
    { id: 'dersler', label: 'Ders çalış', icon: BookOpen, hub: 'hub_dersler', items: al(sec('dersler').items) },
    { id: 'sorular', label: 'Soru çöz', icon: CircleHelp, hub: 'hub_sorular', items: al(sec('sorular').items) },
    { id: 'kamplar', label: 'Sınava hazırlan', icon: Flag, hub: 'hub_kamplar', items: al(sec('kamplar').items) },
    { id: 'checkup', label: 'Check Up', icon: Stethoscope, items: al(grup('Check Up')) },
    { id: 'kaynaklar', label: 'Başvuru', icon: Library, hub: 'hub_kaynaklar', items: al(sec('kaynaklar').items) },
    { id: 'topluluk', label: 'Topluluk', icon: MessagesSquare, items: al(grup('Topluluk')) },
    { id: 'kisisel', label: 'Kişisel', icon: UserRound, items: al([...KISISEL.map((r) => NAV_ITEMS[r]), ...(isAdmin ? [YONETIM] : [])]) },
  ];
  return out.filter((g) => g.items.length);
}
/** Sayfanın menü grubu (kenar çubuğunda hangi grup açık başlasın) */
export const menuGrubuOf = (r: AppRoute, gruplar: MenuGrubu[]) => gruplar.find((g) => g.hub === r || g.items.some((it) => it.id === r))?.id;
