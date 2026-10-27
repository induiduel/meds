/**
 * Başlangıç görevleri (tasarım AB11 baslangicGorev): tamamlanma durumu yalnız mevcut gerçek kayıtlardan hesaplanır —
 * profil (profilKurulum), çalışma takibi (calismaTakip), soru ilerlemesi (studyStore), favoriler, bildirim izni,
 * arkadaşlık (/api/arkadas), kişisel program. Kartın kapatılması profil anahtarında (medsoru_ilk_adimlar_v1) tutulur.
 */
import { useEffect, useState, useSyncExternalStore } from 'react';
import type { AppRoute } from '../router';
import { useProfil } from './profilKurulum';
import { useTakip } from './calismaTakip';
import { getProgress } from './studyStore';
import { useFavoriler } from './favoriStore';
import { useKisiselProgram } from './kisiselProgram';
import { safeJsonFetch } from './api';
import { userNotificationService } from './userNotificationService';

export interface IlkAdim { id: string; ad: string; ac: string; tamam: boolean; git: AppRoute | 'profil' | 'bildirim' }

let arkadasVar: boolean | null = null;
let arkadasP: Promise<boolean> | null = null;
const arkadasYukle = () => {
  if (!arkadasP) {
    arkadasP = safeJsonFetch<{ arkadaslar: unknown[]; giden: unknown[] }>('/api/arkadas')
      .then((r) => (arkadasVar = !!r.ok && !!r.data && ((r.data.arkadaslar?.length || 0) + (r.data.giden?.length || 0)) > 0))
      .catch(() => false);
  }
  return arkadasP;
};

const bildirimAcik = () => { try { return userNotificationService.isPushEnabled(); } catch { return false; } };

export function useIlkAdimlar(): IlkAdim[] {
  const profil = useProfil();
  const takip = useTakip();
  const fav = useFavoriler();
  const kp = useKisiselProgram();
  const [ark, setArk] = useState<boolean | null>(arkadasVar);
  useEffect(() => { let c = true; void arkadasYukle().then((v) => c && setArk(v)); return () => { c = false; }; }, []);
  const kayitlar = Object.entries(takip.k || {});
  const sesli = kayitlar.some(([k, v]) => k.startsWith('sesli:') && (v.sn >= 60 || v.durum === 'bitti'));
  const soru = Object.keys(getProgress()).length + kayitlar.reduce((n, [, v]) => n + (v.soru || 0), 0);
  return [
    { id: 'profil', ad: 'Profilini kur', ac: 'Üniversite, sınıf, kurul ve günlük hedef', tamam: !!profil.tamam, git: 'profil' },
    { id: 'sesli', ad: 'İlk sesli dersini dinle', ac: 'En az bir dakika', tamam: sesli, git: 'canli_ders' },
    { id: 'soru', ad: '10 soru çöz', ac: soru >= 10 ? 'Tamam' : `${Math.min(soru, 10)} / 10`, tamam: soru >= 10, git: 'soru_cozucu' },
    { id: 'favori', ad: 'Bir bilgiyi favorilere ekle', ac: 'Ders sayfasındaki terim ya da bilgi kartında yıldıza dokun', tamam: fav.length > 0, git: 'hub_dersler' },
    { id: 'bildirim', ad: 'Bildirimleri aç', ac: 'Yeni ders ve sınav hatırlatmaları', tamam: bildirimAcik(), git: 'bildirim' },
    { id: 'arkadas', ad: 'Bir arkadaş ekle', ac: 'Birlikte çalışın, soru çözmeye davet edin', tamam: !!ark, git: 'arkadaslar' },
    { id: 'program', ad: 'Programına kendi etkinliğini ekle', ac: 'Lab, telafi ya da grup çalışması', tamam: kp.length > 0, git: 'program_ekle' },
  ];
}

const KEY = 'medsoru_ilk_adimlar_v1';
const OLAY = 'medsor:ilk-adimlar';
const kapaliOku = () => { try { return !!JSON.parse(localStorage.getItem(KEY) || '{}')?.kapali; } catch { return false; } };
export const ilkAdimlarKapat = (kapali: boolean) => {
  try { localStorage.setItem(KEY, JSON.stringify(kapali ? { kapali: new Date().toISOString() } : {})); } catch { /* dolu */ }
  window.dispatchEvent(new Event(OLAY));
};
const abone = (f: () => void) => {
  window.addEventListener(OLAY, f); window.addEventListener('storage', f); window.addEventListener('medsoru:user-data-applied', f);
  return () => { window.removeEventListener(OLAY, f); window.removeEventListener('storage', f); window.removeEventListener('medsoru:user-data-applied', f); };
};
export const useIlkAdimlarKapali = () => useSyncExternalStore(abone, kapaliOku, kapaliOku);
