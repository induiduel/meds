import { useEffect } from 'react';
import { navigateTo, pathFor, type AppRoute } from '../../router';
import { V15_SECTIONS, sectionOf, type V15Section } from './navV15';

/**
 * v15 gezinme belleği (standart uygulama davranışı):
 *  - Uygulama içi geçmiş yığını (oturum boyunca): üst bardaki Geri önce bir önceki sayfaya döner; geçmiş yoksa
 *    sayfanın bölüm merkezine (merkezde ise Bugün'e) gider. Böylece tarayıcının geri tuşuna gerek kalmaz.
 *  - Bölüm başına son adres: alt sekmeye dokununca o sekmede kaldığın sayfa açılır; etkin sekmeye yeniden dokunmak
 *    sekmenin başına (merkez) döndürür.
 * Kayıt sessionStorage'da; erişilemezse bellek içi çalışır.
 */
const YIGIN_KEY = 'medsoru_v15_gecmis';
const SON_KEY = 'medsoru_v15_sekme_son';
const oku = <T,>(k: string, f: T): T => { try { const r = sessionStorage.getItem(k); return r ? (JSON.parse(r) as T) : f; } catch { return f; } };
const yaz = (k: string, v: unknown) => { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch { /* özel pencere */ } };

let yigin: string[] = oku<string[]>(YIGIN_KEY, []);
let son: Record<string, string> = oku<Record<string, string>>(SON_KEY, {});
const suan = () => location.pathname + location.search;

/** Kişisel sayfalar ve Başvuru: alt çubukta "Menü" sekmesine aittir */
export const MENU_SAYFALARI: AppRoute[] = ['topluluk', 'settings', 'stats', 'basarimlar', 'bitirdiklerim', 'study', 'notlarim', 'pdf_olustur', 'manage'];
export type SekmeId = Exclude<V15Section['id'], 'kaynaklar'> | 'menu';
export const sekmeOf = (r: AppRoute): SekmeId | undefined => {
  if (MENU_SAYFALARI.includes(r)) return 'menu';
  const s = sectionOf(r);
  return s ? (s.id === 'kaynaklar' ? 'menu' : s.id) : undefined;
};

/** Her rota değişiminde çağrılır (TopBarV15) */
export function useGezinmeKaydi(active: AppRoute) {
  useEffect(() => {
    const y = suan();
    if (yigin[yigin.length - 1] !== y) {
      if (yigin[yigin.length - 2] === y) yigin.pop(); // tarayıcı/uygulama geri: yığından düş
      else yigin.push(y);
      if (yigin.length > 60) yigin = yigin.slice(-60);
      yaz(YIGIN_KEY, yigin);
    }
    const sk = sekmeOf(active);
    if (sk && sk !== 'menu') { son = { ...son, [sk]: y }; yaz(SON_KEY, son); }
  });
}

/** Merkez ve Bugün kök sayfadır (geri düğmesi gerekmez) */
export const kokMu = (r: AppRoute) => r === 'today' || V15_SECTIONS.some((s) => s.hub === r);

/** Üst bar Geri: önce uygulama içi geçmiş, yoksa bölüm merkezi */
export function geriGit(active: AppRoute) {
  if (yigin.length > 1) { history.back(); return; }
  const s = sectionOf(active);
  navigateTo(pathFor(s && s.hub !== active ? s.hub : 'today'));
}

/** Alt sekmeye dokunma: başka sekmeden gelince kaldığın sayfa, aynı sekmede merkeze dönüş */
export function sekmeyeGit(s: V15Section, active: AppRoute, onGo: (r: AppRoute) => void) {
  const burada = sekmeOf(active) === s.id;
  const hedef = son[s.id];
  if (!burada && hedef && hedef !== pathFor(s.hub)) navigateTo(hedef);
  else onGo(s.hub);
}
