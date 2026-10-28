/**
 * Kullanıcılar grubu (v16) — sayfalar arası ortak küçük yardımcılar. Sayfa değildir; sayfalar bunu statik içe aktarabilir.
 */
import React from 'react';
import { Rozet, type Ton } from '../kit';

export const sureMetni = (sn?: number | null) => {
  const s = Math.max(0, Math.round(Number(sn) || 0));
  if (s < 60) return `${s} sn`;
  const dk = Math.round(s / 60);
  if (dk < 60) return `${dk} dk`;
  const sa = Math.floor(dk / 60);
  return `${sa} sa ${dk % 60 ? `${dk % 60} dk` : ''}`.trim();
};

export const ROL_ETIKET: Record<string, string> = { admin: 'Yönetici', moderator: 'Moderatör', student: 'Öğrenci', guest: 'Misafir' };
export const ROL_TON: Record<string, Ton> = { admin: 'vurgu', moderator: 'bilgi', student: 'notr', guest: 'notr' };
export const RolRozeti: React.FC<{ rol?: string | null }> = ({ rol }) => <Rozet ton={ROL_TON[rol || 'student'] || 'notr'}>{ROL_ETIKET[rol || 'student'] || rol}</Rozet>;

export const ETKINLIK_ETIKET: Record<string, string> = { cevrimici: 'Çevrimiçi', bugun: 'Son 24 saat', hafta: 'Son 7 gün', ay: 'Son 30 gün', pasif: '30 günden eski' };

export const OLAY_ETIKET: Record<string, string> = {
  comment: 'Yorum', report: 'Bildirim', question: 'Soru', fragment: 'Katkı', option: 'Şık', like: 'Beğeni', note: 'Not', vote: 'Oy',
  login: 'Giriş', page: 'Sayfa', study: 'Çalışma',
};
export const olayEtiket = (k: string) => OLAY_ETIKET[k] || k;

export const tarihMetni = (iso?: string | null) => (iso ? new Date(iso).toLocaleString('tr-TR', { dateStyle: 'short', timeStyle: 'short' }) : '—');

/** Kişi anahtarını adres parçasına çevirir (u:abc → u%3Aabc) */
export const kisiYolu = (key: string, sekme?: string) => `kisi/${encodeURIComponent(key)}${sekme ? `/${sekme}` : ''}`;

/** Satır içi kişi bağlantısı (panel içi gezinme) */
export const KisiBag: React.FC<{ anahtar?: string | null; git: (y: string) => void; children: React.ReactNode }> = ({ anahtar, git, children }) =>
  anahtar ? (
    <a href={`/manage/${kisiYolu(anahtar)}`} onClick={(e) => { if (e.metaKey || e.ctrlKey) return; e.preventDefault(); e.stopPropagation(); git(kisiYolu(anahtar)); }}>{children}</a>
  ) : <>{children}</>;
