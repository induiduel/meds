import { useEffect, useSyncExternalStore } from 'react';

/**
 * Arayüz sürümü: v7 (Apple Sağlık, varsayılan), v4 (klinik kitapçık), v3 (minimal) ya da v2 (yedek).
 * Tercih cihazda saklanır; ?ui=v2 / v3 / v4 / v7 adres parametresi de değiştirir.
 * Kök öğeye `ui-v3` (v3, v4, v7), `ui-v4` (v4, v7) ve `ui-v7` sınıfları eklenir; v7 kuralları styles/health.css'tedir.
 */
export type UiVersion = 'v2' | 'v3' | 'v4' | 'v7';
const KEY = 'medsoru_ui_version';
const listeners = new Set<() => void>();

function read(): UiVersion {
  try {
    const q = new URLSearchParams(window.location.search).get('ui');
    if (q === 'v2' || q === 'v3' || q === 'v4' || q === 'v7') {
      localStorage.setItem(KEY, q);
      return q;
    }
    const v = localStorage.getItem(KEY);
    // v4 çıktığında, varsayılan olarak v3'te kalmış cihazlar bir kez v4'e taşınır; v2 seçenler korunur
    if (v === 'v3' && !localStorage.getItem('medsoru_ui_v4_migrated')) {
      localStorage.setItem('medsoru_ui_v4_migrated', '1');
      localStorage.setItem(KEY, 'v4');
      return 'v4';
    }
    // v7 çıktığında v3/v4'teki cihazlar bir kez v7'ye taşınır; v2 seçenler korunur
    if ((v === 'v3' || v === 'v4') && !localStorage.getItem('medsoru_ui_v7_migrated')) {
      localStorage.setItem('medsoru_ui_v7_migrated', '1');
      localStorage.setItem(KEY, 'v7');
      return 'v7';
    }
    if (v === 'v2' || v === 'v3' || v === 'v4' || v === 'v7') return v;
  } catch {
    /* ignore */
  }
  return 'v7';
}

let current: UiVersion = typeof window === 'undefined' ? 'v7' : read();

export function applyUiVersion(v: UiVersion = current) {
  // v4, v3'ün minimal Material katmanını devralır ve üstüne kompakt okuma düzenini ekler
  document.documentElement.classList.toggle('ui-v3', v === 'v3' || v === 'v4' || v === 'v7');
  document.documentElement.classList.toggle('ui-v4', v === 'v4' || v === 'v7');
  document.documentElement.classList.toggle('ui-v7', v === 'v7');
}

export function setUiVersion(v: UiVersion) {
  current = v;
  try {
    localStorage.setItem(KEY, v);
  } catch {
    /* ignore */
  }
  applyUiVersion(v);
  listeners.forEach((l) => l());
}

export function useUiVersion() {
  const v = useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    () => current,
    () => current
  );
  useEffect(() => applyUiVersion(v), [v]);
  const next: Record<UiVersion, UiVersion> = { v7: 'v4', v4: 'v3', v3: 'v2', v2: 'v7' };
  return { ui: v, isV3: v === 'v3' || v === 'v4' || v === 'v7', isV4: v === 'v4' || v === 'v7', isV7: v === 'v7', setUi: setUiVersion, toggleUi: () => setUiVersion(next[v]) };
}
