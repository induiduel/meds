/**
 * Özel günler: karşılama ekranındaki günün cümlesini o güne özel cümle değiştirir ve o gün kalp yağmuru olur.
 * Tarihleri buraya ekle (ay 1–12). Doğum günü ve yıl dönümü için satırları doldurman yeterli.
 */
export type OzelGun = { ay: number; gun: number; cumle: string; selam?: string };

export const OZEL_GUNLER: OzelGun[] = [
  { ay: 2, gun: 14, cumle: 'Sevgililer günün kutlu olsun. İyi ki seninleyim.', selam: 'Sevgililer gününde' },
  // { ay: 0, gun: 0, cumle: 'Doğum günün kutlu olsun Arzu.', selam: 'Bugün senin günün' },
  // { ay: 0, gun: 0, cumle: 'Bugün bizim günümüz. İyi ki.', selam: 'Yıl dönümümüzde' },
];

export function bugunOzelGun(d = new Date()): OzelGun | null {
  return OZEL_GUNLER.find((g) => g.ay === d.getMonth() + 1 && g.gun === d.getDate() && g.gun > 0) || null;
}
