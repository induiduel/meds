/**
 * Kişisel sınavlar ve pratik hatırlatma tercihi (tasarım D06 "Sınavlarım"). Kurul sınavları takvimden gelir
 * (kurulTakvimi); öğrencinin eklediği pratik/KMB/ara sınavlar burada (`medsoru_sinavlarim_v1`, hesaba eşitlenir).
 * Hatırlatma açıkken Bildirimler, kurul ve kişisel sınavdan 5/3/1 gün önce soru çözme hatırlatması gösterir.
 */
export interface KisiselSinav { id: string; ad: string; gun: string; tur: 'Komite' | 'Pratik' | 'Ara sınav' | 'Diğer' }
export const SINAVLARIM_KEY = 'medsoru_sinavlarim_v1';
export const HATIRLAT_KEY = 'medsoru_sinav_hatirlat_v1';
export const kisiselOku = (): KisiselSinav[] => { try { const l = JSON.parse(localStorage.getItem(SINAVLARIM_KEY) || '[]'); return Array.isArray(l) ? l : []; } catch { return []; } };
export const kisiselYaz = (l: KisiselSinav[]) => { try { localStorage.setItem(SINAVLARIM_KEY, JSON.stringify(l.slice(0, 50))); } catch { /* dolu */ } };
export const hatirlatOku = () => { try { return localStorage.getItem(HATIRLAT_KEY) !== '0'; } catch { return true; } };
export const hatirlatYaz = (v: boolean) => { try { localStorage.setItem(HATIRLAT_KEY, v ? '1' : '0'); } catch { /* yok */ } };
