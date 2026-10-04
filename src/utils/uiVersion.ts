import { useEffect, useSyncExternalStore } from 'react';

/**
 * Arayüz sürümü: v3 (minimal, varsayılan) ya da v2 (kompakt, yedek).
 * Tercih cihazda saklanır; ?ui=v2 / ?ui=v3 adres parametresi de değiştirir.
 * Kök öğeye `ui-v3` sınıfı eklenir; v3 stilleri yalnızca bu sınıf altında çalışır.
 */
export type UiVersion = 'v2' | 'v3';
const KEY = 'medsoru_ui_version';
const listeners = new Set<() => void>();

function read(): UiVersion {
  try {
    const q = new URLSearchParams(window.location.search).get('ui');
    if (q === 'v2' || q === 'v3') {
      localStorage.setItem(KEY, q);
      return q;
    }
    const v = localStorage.getItem(KEY);
    if (v === 'v2' || v === 'v3') return v;
  } catch {
    /* ignore */
  }
  return 'v3';
}

let current: UiVersion = typeof window === 'undefined' ? 'v3' : read();

export function applyUiVersion(v: UiVersion = current) {
  document.documentElement.classList.toggle('ui-v3', v === 'v3');
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
  return { ui: v, isV3: v === 'v3', setUi: setUiVersion, toggleUi: () => setUiVersion(v === 'v3' ? 'v2' : 'v3') };
}
