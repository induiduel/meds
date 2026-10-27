import { BookOpen, CircleHelp, Flag, House, Library } from 'lucide-react';
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
