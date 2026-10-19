/**
 * Yıldızlı Paragraflar Deposu (medsoru_yildizli_paragraflar_v1)
 *
 * Öğrencinin Sesli Ders (Canlı Ders), Sesli Sınav Asistanı ve Soru Çözücü ekranlarında
 * yıldızladığı paragrafları / cümleleri saklar, profille eşitler ve deeplink ile doğrudan
 * alıntılanan yere geri yönlendirir.
 */
import { useEffect, useState } from 'react';
import { logActivity } from './activityLog';
import { toast } from '../components/ui/Toast';

export type ParagrafKaynak = 'canli_ders' | 'asistan' | 'soru_cozucu';

export interface YildizliParagraf {
  id: string; // örn. cd_pat01_p12 veya as_e02_e02-05_c1
  kaynak: ParagrafKaynak;
  kaynakAd: string; // 'Sesli ders' | 'Sınav asistanı' | 'Soru çözücü'
  baslik: string; // Ders veya konu başlığı
  altBaslik?: string; // Bölüm veya nokta başlığı
  metin: string; // Paragrafın tam metni
  deeplink: string; // Tıklandığında doğrudan noktaya/paragrafa giden yol
  tarih: number; // Date.now()
  meta?: {
    dersKey?: string;
    brans?: string;
    dersKod?: string;
    noktaId?: string;
    paragrafIndex?: number;
    soruNo?: number;
  };
}

export const YILDIZLI_PARAGRAFLAR_KEY = 'medsoru_yildizli_paragraflar_v1';
const EVENT_NAME = 'medsor:yildizli_paragraflar_degisti';

function emitChange() {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent(EVENT_NAME));
  }
}

export function getYildizliParagraflar(): YildizliParagraf[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(YILDIZLI_PARAGRAFLAR_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveYildizliParagraflar(list: YildizliParagraf[]) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(YILDIZLI_PARAGRAFLAR_KEY, JSON.stringify(list));
    emitChange();
  } catch (e) {
    console.error('Yıldızlı paragraflar kaydedilemedi', e);
  }
}

export function yildizliMi(id: string): boolean {
  const list = getYildizliParagraflar();
  return list.some((x) => x.id === id);
}

export function yildizEkle(item: Omit<YildizliParagraf, 'tarih'>): void {
  const list = getYildizliParagraflar();
  const filtered = list.filter((x) => x.id !== item.id);
  const yeni: YildizliParagraf = { ...item, tarih: Date.now() };
  saveYildizliParagraflar([yeni, ...filtered]);
  logActivity('kaydet', `Bir paragrafı tekrar listene ekledin: ${item.baslik.slice(0, 50)}`);
  toast.success('Tekrar listesine eklendi', 'Yıldızlı paragraflarımdan istediğin zaman tekrar edebilirsin.');
}

export function yildizCikar(id: string): void {
  const list = getYildizliParagraflar();
  const item = list.find((x) => x.id === id);
  const filtered = list.filter((x) => x.id !== id);
  saveYildizliParagraflar(filtered);
  toast.info('Listeden çıkarıldı', item ? item.baslik.slice(0, 40) : undefined);
}

export function yildizToggle(item: Omit<YildizliParagraf, 'tarih'>): boolean {
  if (yildizliMi(item.id)) {
    yildizCikar(item.id);
    return false;
  } else {
    yildizEkle(item);
    return true;
  }
}

export function yildizTemizle(): void {
  saveYildizliParagraflar([]);
  toast.info('Yıldızlı paragraflar temizlendi');
}

/** Gerçek zamanlı yıldızlı paragraflar listesi hook'u */
export function useYildizliParagraflar(): YildizliParagraf[] {
  const [list, setList] = useState<YildizliParagraf[]>(getYildizliParagraflar);

  useEffect(() => {
    const handler = () => setList(getYildizliParagraflar());
    window.addEventListener(EVENT_NAME, handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener(EVENT_NAME, handler);
      window.removeEventListener('storage', handler);
    };
  }, []);

  return list;
}

/** Belirli bir paragrafın yıldızlı olup olmadığını dinleyen hook */
export function useYildizliMi(id: string): boolean {
  const [ekli, setEkli] = useState<boolean>(() => yildizliMi(id));

  useEffect(() => {
    const handler = () => setEkli(yildizliMi(id));
    window.addEventListener(EVENT_NAME, handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener(EVENT_NAME, handler);
      window.removeEventListener('storage', handler);
    };
  }, [id]);

  return ekli;
}

/** Toplam yıldızlı paragraf sayısını dinleyen hook */
export function useYildizliSayisi(): number {
  const [count, setCount] = useState<number>(() => getYildizliParagraflar().length);

  useEffect(() => {
    const handler = () => setCount(getYildizliParagraflar().length);
    window.addEventListener(EVENT_NAME, handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener(EVENT_NAME, handler);
      window.removeEventListener('storage', handler);
    };
  }, []);

  return count;
}
