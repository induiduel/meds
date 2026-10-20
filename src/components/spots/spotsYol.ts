/**
 * Soru çözücü (/soru-cozucu) ve En önemliler (/en-onemliler) adresleri. Eskiden ikisi de /spotlar?gorunum=… idi;
 * eski bağlantılar ExamSpotsView'da yeni adrese yönlenir. Parametreler: brans, ders (kod), coz (1|yanlis|cikmis), asistan, m.
 */
import { navigateTo, pathFor } from '../../router';
import { kanonik } from '../../siteHaritasi';
import type { Brans } from './brans';

type P = Partial<Record<'brans' | 'ders' | 'coz' | 'asistan' | 'm', string | null | undefined>>;

const yap = (yol: string, p: P) => {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(p)) if (v) sp.set(k, v);
  const q = sp.toString();
  // görünen adres: /sorular/soru-cozucu/kurul1/<branş>?ders=… (siteHaritasi)
  return kanonik(q ? `${yol}?${q}` : yol);
};

export const cozucuYolu = (p: P & { brans?: Brans | null } = {}) => yap(pathFor('soru_cozucu'), p);
export const onemYolu = (p: P & { brans?: Brans | null } = {}) => yap(pathFor('en_onemliler'), p);

export const cozucuyaGit = (p: Parameters<typeof cozucuYolu>[0] = {}) => navigateTo(cozucuYolu(p));
export const onemeGit = (p: Parameters<typeof onemYolu>[0] = {}) => navigateTo(onemYolu(p));
