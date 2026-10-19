/**
 * İstemci Tarafı WhatsApp Tercihleri Deposu
 * (medsoru_whatsapp_prefs_v1)
 *
 * Öğrencinin günlük WhatsApp tekrar bildirim tercihlerini (aktif/pasif, telefon,
 * saat, içerik seçimleri) saklar, profil KV'si üzerinden sunucuya eşitler.
 */

import { useEffect, useState } from 'react';
import { toast } from '../components/ui/Toast';

export interface WhatsAppPrefs {
  enabled: boolean;
  phone: string; // örn. "0532 123 45 67" veya "905321234567"
  hour: number; // 0..23 (varsayılan: 21 -> 21:00)
  includeStarredParagraphs: boolean; // Yıldızlı / beğenilen paragraflar
  includeFavoriteCards: boolean; // Favori ezber kartları
  includeFavoriteQuestions: boolean; // Favori çıkmış sorular
  paragraphCount: number; // Günde kaç paragraf (1..3)
  cardCount: number; // Günde kaç kart (1..3)
  lastSentDate?: string; // YYYY-MM-DD
  lastStatus?: {
    at: string;
    success: boolean;
    message?: string;
  };
}

export const WHATSAPP_PREFS_KEY = 'medsoru_whatsapp_prefs_v1';
const EVENT_NAME = 'medsor:whatsapp_prefs_degisti';

export const DEFAULT_WHATSAPP_PREFS: WhatsAppPrefs = {
  enabled: false,
  phone: '',
  hour: 21,
  includeStarredParagraphs: true,
  includeFavoriteCards: true,
  includeFavoriteQuestions: false,
  paragraphCount: 1,
  cardCount: 1,
};

function emitChange() {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent(EVENT_NAME));
  }
}

export function getWhatsAppPrefs(): WhatsAppPrefs {
  if (typeof window === 'undefined') return { ...DEFAULT_WHATSAPP_PREFS };
  try {
    const raw = localStorage.getItem(WHATSAPP_PREFS_KEY);
    if (!raw) return { ...DEFAULT_WHATSAPP_PREFS };
    const parsed = JSON.parse(raw);
    return {
      ...DEFAULT_WHATSAPP_PREFS,
      ...(parsed && typeof parsed === 'object' ? parsed : {}),
    };
  } catch {
    return { ...DEFAULT_WHATSAPP_PREFS };
  }
}

export function saveWhatsAppPrefs(updates: Partial<WhatsAppPrefs>): WhatsAppPrefs {
  const current = getWhatsAppPrefs();
  const next: WhatsAppPrefs = {
    ...current,
    ...updates,
  };

  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(WHATSAPP_PREFS_KEY, JSON.stringify(next));
      emitChange();
    } catch (e) {
      console.error('WhatsApp tercihleri kaydedilemedi', e);
    }
  }

  return next;
}

/** Gerçek zamanlı WhatsApp tercihlerini dinleyen hook */
export function useWhatsAppPrefs(): [WhatsAppPrefs, (updates: Partial<WhatsAppPrefs>) => void] {
  const [prefs, setPrefs] = useState<WhatsAppPrefs>(getWhatsAppPrefs);

  useEffect(() => {
    const handler = () => setPrefs(getWhatsAppPrefs());
    window.addEventListener(EVENT_NAME, handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener(EVENT_NAME, handler);
      window.removeEventListener('storage', handler);
    };
  }, []);

  const update = (updates: Partial<WhatsAppPrefs>) => {
    const next = saveWhatsAppPrefs(updates);
    setPrefs(next);
  };

  return [prefs, update];
}

export interface WhatsAppServerStatus {
  configured: boolean;
  phoneNumberIdMasked: string | null;
  templateConfigured: boolean;
  templateName: string | null;
  apiVersion: string;
}

/** Sunucudaki WhatsApp API yapılandırma durumunu kontrol eder */
export async function fetchWhatsAppStatus(): Promise<WhatsAppServerStatus> {
  try {
    const res = await fetch('/api/whatsapp/status');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    return {
      configured: false,
      phoneNumberIdMasked: null,
      templateConfigured: false,
      templateName: null,
      apiVersion: 'v21.0',
    };
  }
}

/** Test mesajı gönderir */
export async function sendTestWhatsAppMessage(phone: string): Promise<{ success: boolean; message: string }> {
  try {
    const res = await fetch('/api/whatsapp/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data?.error || `Mesaj gönderilemedi (${res.status})`);
    }

    return {
      success: true,
      message: data.message || 'Test mesajı WhatsApp numaranıza iletildi.',
    };
  } catch (err: any) {
    return {
      success: false,
      message: err?.message || 'Ağ hatası veya geçersiz numara.',
    };
  }
}

/** Günün tekrarını şimdi gönder */
export async function triggerDailyDigestNow(
  phone: string,
  prefs: WhatsAppPrefs
): Promise<{ success: boolean; message: string }> {
  try {
    // İstemcideki mevcut yıldızlı paragrafları ve favori kartları gönderim gövdesine ekle
    let yildizliRaw: any = null;
    try {
      yildizliRaw = localStorage.getItem('medsoru_yildizli_paragraflar_v1');
    } catch {}

    const res = await fetch('/api/whatsapp/send-digest-now', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone,
        prefs,
        kv: {
          medsoru_yildizli_paragraflar_v1: yildizliRaw ? { v: yildizliRaw, at: new Date().toISOString() } : undefined,
        },
      }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data?.error || `Günün tekrarı gönderilemedi (${res.status})`);
    }

    return {
      success: true,
      message: data.message || 'Günün tekrarı WhatsApp numaranıza iletildi.',
    };
  } catch (err: any) {
    return {
      success: false,
      message: err?.message || 'Gönderim sırasında hata oluştu.',
    };
  }
}
