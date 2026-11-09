import { BookOpen, CircleHelp, Flag, Gamepad2, House, Library, MessagesSquare, ShieldCheck, Stethoscope, UserRound } from 'lucide-react';
import type React from 'react';
import type { AppRoute } from '../../router';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { NAV_ITEMS, NAV_TREE, type NavItem } from '../shell/navModel';
import { menudeGorunur, siteAyarAbone } from '../../services/siteAyar';

/**
 * v15 gezinmesi (tasarım sistemi v15 › Kabuk): "ne yapmak istiyorum?" sorusunun dört işi + önde Bugün.
 * Bölümün alt sayfaları merkez modelinden (merkezModel.MERKEZ_ARACLARI) gelir; merkezde olmayan ama NAV_TREE'de aynı
 * gruptaki sayfalar sona eklenir. Böylece kenar menüsü, ray, alt sekme ve merkez sayfaları aynı listeyi gösterir.
 */
export interface V15Section {
  id: 'bugun' | 'dersler' | 'sorular' | 'kamplar' | 'kaynaklar' | 'eglence';
  label: string;
  /** Alt sekme ve rayda kısa ad */
  short: string;
  icon: React.ElementType;
  /** Bölüm düğmesinin açtığı sayfa (merkez) */
  hub: AppRoute;
  items: NavItem[];
}

/** Eğlence bölgesi: gizlenmemiş oyunlar (Taş Masası: okey modları + Uno, Hücrem). Soru çöz listesinde tekrar görünmez. */
const OYUNLAR: AppRoute[] = ['oyunlar', 'hucrem'];

const NAV_GROUP: Record<Exclude<V15Section['id'], 'bugun' | 'eglence'>, string> = {
  dersler: 'Ders çalış',
  sorular: 'Soru çöz',
  kamplar: 'Sınava hazırlan',
  kaynaklar: 'Başvuru',
};

const itemsOf = (id: Exclude<V15Section['id'], 'bugun'>): NavItem[] => {
  if (id === 'eglence') return OYUNLAR.filter((r) => menudeGorunur(r)).map((r) => NAV_ITEMS[r]).filter(Boolean);
  const seen = new Set<AppRoute>(OYUNLAR);
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
  { id: 'dersler', label: 'Ders çalış', short: 'Ders', icon: BookOpen, hub: 'hub_dersler', items: [] },
  { id: 'sorular', label: 'Soru çöz', short: 'Soru', icon: CircleHelp, hub: 'hub_sorular', items: [] },
  { id: 'kamplar', label: 'Sınava hazırlan', short: 'Sınav', icon: Flag, hub: 'hub_kamplar', items: [] },
  { id: 'kaynaklar', label: 'Başvuru', short: 'Başvuru', icon: Library, hub: 'hub_kaynaklar', items: [] },
  { id: 'eglence', label: 'Eğlence', short: 'Eğlence', icon: Gamepad2, hub: 'oyunlar', items: [] },
];
/** Bölüm listeleri çalışma anında (site ayarı değişince) yerinde yenilenir; merkezModel/navModel aboneleri önce çalışır */
function bolumSuz() {
  for (const s of V15_SECTIONS) if (s.id !== 'bugun') s.items.splice(0, s.items.length, ...itemsOf(s.id));
}
bolumSuz();
siteAyarAbone(bolumSuz);

/** Menüde ayrı satırı olmayan alt sayfalar (ders ayrıntısı Ders çalış bölümündedir) */
const ALT_SAYFA: Partial<Record<AppRoute, V15Section['id']>> = { ders_detay: 'dersler', program_ekle: 'dersler' };

/** Sayfanın bölümü (merkez sayfası da kendi bölümüne aittir); kişisel sayfalarda undefined */
export const sectionOf = (r: AppRoute): V15Section | undefined =>
  V15_SECTIONS.find((s) => s.hub === r) || V15_SECTIONS.find((s) => ALT_SAYFA[r] === s.id || s.items.some((it) => it.id === r));

/* ---------------------------------------------------------------------------
 * Bütün sayfalar menüsü (telefon/tablet "Menü" ızgarası ve masaüstü kenar çubuğu aynı listeyi kullanır).
 * Yeni sayfa NAV_TREE'ye (shell/navModel) eklenince burada kendiliğinden görünür; Kişisel'e yalnız aşağıdaki liste.
 * ------------------------------------------------------------------------- */
export interface MenuGrubu { id: string; label: string; icon: React.ElementType; hub?: AppRoute; items: NavItem[]; alt?: string }
/** Tasarım A03: Eğlence (oyunlar) dört işin yanında ayrı bölüm */
// H147: Başarımlar ve Güncelleme günlüğü hesap sayfalarıyla birlikte Kişisel'de (Oyunlar/Başvuru altında aranmıyordu)
// H305: Arka plan işleri Çevrimdışı ve indirmeler'e katıldı; menüde tek giriş
const KISISEL: AppRoute[] = ['bitirdiklerim', 'basarimlar', 'guncellemeler', 'study', 'notlarim', 'bildirimler', 'stats', 'pdf_olustur', 'cevrimdisi', 'music', 'ilk_adimlar', 'settings', 'dil_bolge', 'yardim'];

const YONETIM = { id: 'manage', label: 'Yönetim', short: 'Yönetim', hint: 'Yönetim konsolu', icon: ShieldCheck, tint: '#64748B' } as NavItem;

export function menuGruplari(isAdmin: boolean): MenuGrubu[] {
  const seen = new Set<AppRoute>(['today']);
  const al = (ids: (NavItem | undefined)[]) => ids.filter((it): it is NavItem => !!it && !seen.has(it.id) && (seen.add(it.id), true));
  const grup = (label: string) => NAV_TREE.find((g) => g.label === label)?.items || [];
  const sec = (id: V15Section['id']) => V15_SECTIONS.find((s) => s.id === id)!;
  const oyun = al(OYUNLAR.filter((r) => menudeGorunur(r)).map((r) => NAV_ITEMS[r]));
  const out: MenuGrubu[] = [
    { id: 'dersler', label: 'Ders çalış', icon: BookOpen, hub: 'hub_dersler', items: al(sec('dersler').items) },
    { id: 'sorular', label: 'Soru çöz', icon: CircleHelp, hub: 'hub_sorular', items: al(sec('sorular').items) },
    { id: 'kamplar', label: 'Sınava hazırlan', icon: Flag, hub: 'hub_kamplar', items: al(sec('kamplar').items) },
    { id: 'checkup', label: 'Check Up', icon: Stethoscope, items: al(grup('Check Up')) },
    { id: 'kaynaklar', label: 'Başvuru', icon: Library, hub: 'hub_kaynaklar', items: al(sec('kaynaklar').items) },
    { id: 'eglence', label: 'Eğlence', icon: Gamepad2, items: oyun },
    { id: 'topluluk', label: 'Topluluk', icon: MessagesSquare, items: al(grup('Topluluk')) },
    { id: 'kisisel', label: 'Kişisel', icon: UserRound, items: al([...KISISEL.filter((r) => menudeGorunur(r)).map((r) => NAV_ITEMS[r]), ...(isAdmin ? [YONETIM] : [])]) },
  ];
  // Bölüm başlığının altındaki açıklama: ilk birkaç sayfanın kısa adı (tasarım: "Sesli dersler, Öğren, Spotlar…")
  return out.filter((g) => g.items.length).map((g) => ({ ...g, alt: g.items.slice(0, 4).map((it) => it.short || it.label).join(', ') + (g.items.length > 4 ? '…' : '') }));
}
/** Sayfanın menü grubu (kenar çubuğunda hangi grup açık başlasın) */
export const menuGrubuOf = (r: AppRoute, gruplar: MenuGrubu[]) => gruplar.find((g) => g.hub === r || g.items.some((it) => it.id === r))?.id;
