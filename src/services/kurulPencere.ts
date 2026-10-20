/**
 * Kurul takvimi üzerine ekran yardımcıları (kurulTakvimi.ts kuralına dokunmaz, yalnız onu kullanır).
 *  - Geliştirme günü: yerelde `?gun=2026-10-27` ile ekranlar o güne göre denenir (canlıda yok sayılır).
 *  - Sınav penceresi: son sınav günü ve sonraki 7 gün — olası sorular ve numaralı giriş öne çıkar.
 */
import { KURULLAR, aktifKurul, arsivKurullar, bugun, sinavaKalanGun, sonSinavKurul, type KurulBilgi } from './kurulTakvimi';

const yerelMi = () => {
  try { return /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname) || location.hostname.endsWith('.localhost'); } catch { return false; }
};

/** Bugün; yerelde ?gun=YYYY-AA-GG verilmişse o gün (yalnız deneme). */
export function ekranGunu(): string {
  if (yerelMi()) {
    try {
      const g = new URLSearchParams(location.search).get('gun');
      if (g && /^\d{4}-\d{2}-\d{2}$/.test(g)) return g;
    } catch { /* yok */ }
  }
  return bugun();
}

export const gunFarki = (a: string, b: string) => Math.round((Date.parse(b) - Date.parse(a)) / 86400000);

const AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
/** "2026-10-23" → "23 Ekim" (yıl farklıysa "23 Ekim 2027") */
export function tarihYaz(iso: string, gun: string = bugun()): string {
  const [y, m, d] = iso.split('-').map(Number);
  if (!y || !m || !d) return iso;
  return `${d} ${AYLAR[m - 1]}${String(y) !== gun.slice(0, 4) ? ` ${y}` : ''}`;
}

export interface SinavPenceresi { kurul: KurulBilgi; gecenGun: number }
/** Son sınav bugün ya da en çok 7 gün önceyse o kurul; değilse null. */
export function sinavPenceresi(gun: string = ekranGunu()): SinavPenceresi | null {
  const k = sonSinavKurul(gun);
  if (!k) return null;
  const g = gunFarki(k.sinav, gun);
  return g >= 0 && g <= 7 ? { kurul: k, gecenGun: g } : null;
}

export interface TakvimDurumu {
  gun: string;
  aktif: KurulBilgi;
  kalan: number;
  arsiv: KurulBilgi[];
  son: KurulBilgi | null;
  pencere: SinavPenceresi | null;
}
export function takvimDurumu(gun: string = ekranGunu()): TakvimDurumu {
  return { gun, aktif: aktifKurul(gun), kalan: sinavaKalanGun(gun), arsiv: arsivKurullar(gun), son: sonSinavKurul(gun), pencere: sinavPenceresi(gun) };
}

export { KURULLAR };
export type { KurulBilgi };

/** "ÜROGENİTAL VE OBSTETRİK KURULU" → "Ürogenital ve Obstetrik Kurulu" */
export function kurulAdi(k: KurulBilgi): string {
  return k.ad.toLocaleLowerCase('tr-TR').split(/\s+/).map((w) => (w === 've' ? w : w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1))).join(' ');
}

/** Bağlantıya ?gun= deneme parametresini taşır (yalnız yerelde etkili). */
export function gunluBag(url: string): string {
  try {
    const g = new URLSearchParams(location.search).get('gun');
    if (!g || !yerelMi()) return url;
    return url + (url.includes('?') ? '&' : '?') + 'gun=' + encodeURIComponent(g);
  } catch { return url; }
}

const BULUNMA = ["'ta", "'ta", "'ta", "'da", "'ta", "'da", "'da", "'ta", "'de", "'de", "'da", "'ta"];
/** "2026-10-23" → "23 Ekim'de" (ayın bulunma eki; yıl yazılmaz) */
export function tarihteYaz(iso: string): string {
  const [, m, d] = iso.split('-').map(Number);
  if (!m || !d) return iso;
  return `${d} ${AYLAR[m - 1]}${BULUNMA[m - 1]}`;
}
