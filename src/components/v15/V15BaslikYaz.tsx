import { useAppearance } from '../../utils/appearance';
import { useV15Baslik } from './baslik';

/** JSX içinden üst bar başlığı yazar (yalnız v15'te); hiçbir şey çizmez. Kancası olmayan eski sayfa başlıkları için. */
export default function V15BaslikYaz({ baslik, alt }: { baslik: string; alt?: string }) {
  useV15Baslik(useAppearance().v15 ? { baslik, alt } : null);
  return null;
}
