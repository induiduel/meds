import React from 'react';
import { adminIstek, bildir, useAdminSorgu } from '../../kit';

/** Yönetim › Site sayfalarının ortak parçaları (site_ayar.json; sunucu yonetim16/siteAyar.ts) */
export type SayfaDurumu = 'acik' | 'gizli' | 'kapali' | 'yalniz-yonetici';
export type Duyuru = { acik: boolean; metin: string; ton: 'bilgi' | 'uyari' | 'hata'; baglanti?: string; baslangic?: string; bitis?: string; kurul?: number[]; kapatilabilir?: boolean };
export type SiteAyarTam = {
  surum: number; guncellendi: string; guncelleyen?: string;
  sayfalar: Record<string, SayfaDurumu>; menu: Record<string, boolean>; bayraklar: Record<string, boolean>;
  gorunurluk: Record<string, string>; duyuru: Duyuru | null; bakim: { acik: boolean; sure?: string; mesaj?: string };
};

export function useSiteAyarAdmin() {
  const s = useAdminSorgu<SiteAyarTam>('/api/admin/site-ayar', { canliOlay: ['site_ayar_changed'] });
  const veri = s.veri ? { ...s.veri, sayfalar: s.veri.sayfalar || {}, menu: s.veri.menu || {}, bayraklar: s.veri.bayraklar || {} } : null;
  return { ...s, veri };
}

/** Kısmi yazım (haritada null = anahtarı sil → derleme varsayılanı). Başarıda yeni tam ayarı döner. */
export async function siteAyarYaz(parca: Partial<Record<keyof SiteAyarTam, unknown>>, basari?: string): Promise<SiteAyarTam | null> {
  try {
    const r = await adminIstek<SiteAyarTam>('/api/admin/site-ayar', { yontem: 'PUT', govde: parca });
    if (basari) bildir(basari, 'iyi');
    return r;
  } catch (e: any) {
    bildir(e?.message || 'Kaydedilemedi', 'kotu');
    return null;
  }
}

export const Anahtar: React.FC<{ acik: boolean; degistir: (v: boolean) => void; etiket: string; mesgul?: boolean }> = ({ acik, degistir, etiket, mesgul }) => (
  <button type="button" role="switch" aria-checked={acik} aria-label={etiket} title={etiket} disabled={mesgul} className={`m16-anahtar${acik ? ' on' : ''}`} onClick={() => degistir(!acik)}><i /></button>
);

/** ISO ↔ <input type="datetime-local"> */
export const yerelTarih = (iso?: string) => {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
};
export const isoTarih = (yerel: string) => (yerel ? new Date(yerel).toISOString() : undefined);
