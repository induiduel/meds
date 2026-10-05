import { useEffect, useSyncExternalStore } from 'react';

/**
 * Arayüz sürümü: v4 (minimal + kompakt okuma, varsayılan), v3 (minimal) ya da v2 (kompakt, yedek).
 * Tercih cihazda saklanır; ?ui=v2 / ?ui=v3 / ?ui=v4 adres parametresi de değiştirir.
 * Kök öğeye `ui-v3` (v3 ve v4) ve `ui-v4` sınıfları eklenir.
 */
export type UiVersion = 'v2' | 'v3' | 'v4';
const KEY = 'medsoru_ui_version';
const listeners = new Set<() => void>();

function read(): UiVersion {
  try {
    const q = new URLSearchParams(window.location.search).get('ui');
    if (q === 'v2' || q === 'v3' || q === 'v4') {
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
    if (v === 'v2' || v === 'v3' || v === 'v4') return v;
  } catch {
    /* ignore */
  }
  return 'v4';
}

let current: UiVersion = typeof window === 'undefined' ? 'v4' : read();

export function applyUiVersion(v: UiVersion = current) {
  // v4, v3'ün minimal Material katmanını devralır ve üstüne kompakt okuma düzenini ekler
  document.documentElement.classList.toggle('ui-v3', v === 'v3' || v === 'v4');
  document.documentElement.classList.toggle('ui-v4', v === 'v4');
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
  const next: Record<UiVersion, UiVersion> = { v4: 'v3', v3: 'v2', v2: 'v4' };
  return { ui: v, isV3: v === 'v3' || v === 'v4', isV4: v === 'v4', setUi: setUiVersion, toggleUi: () => setUiVersion(next[v]) };
}
