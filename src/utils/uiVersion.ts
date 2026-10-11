/**
 * Arayüz tek sürümdür (v8). Eski sürüm seçimi (v2 klasik, v3, v4) 2026-10-11'de kaldırıldı.
 * Kök öğeye `ui-v3 ui-v4 ui-v7` sınıfları eklenir: mevcut CSS katmanları (index.css v3/v4, health.css v7) bunlara bağlıdır.
 * Eski cihaz tercihi (`medsoru_ui_version`, göç bayrakları) bir kez temizlenir.
 */
export function applyUiVersion() {
  document.documentElement.classList.add('ui-v3', 'ui-v4', 'ui-v7');
  try {
    for (const k of ['medsoru_ui_version', 'medsoru_ui_v4_migrated', 'medsoru_ui_v7_migrated']) localStorage.removeItem(k);
  } catch {
    /* ignore */
  }
}
