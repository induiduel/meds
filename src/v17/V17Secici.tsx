import { useSyncExternalStore } from 'react';
import { v17Ayarla, v17Dinle, v17Istek } from './bayrak';

/** Ayarlar › Görünüm: yalnız yöneticiye görünen "v17 (deneme)" anahtarı (docs/V17_PLAN.md). */
export default function V17Secici() {
  const acik = useSyncExternalStore(v17Dinle, v17Istek, () => false);
  return (
    <label className="v16-anahtar">
      <span>
        <b>v17 tasarımı (deneme)</b>
        <small>Klinik editöryal: Bugün ve sesli ders yeni tasarımla açılır. Yalnız yöneticiye açık.</small>
      </span>
      <input type="checkbox" role="switch" aria-checked={acik} checked={acik} onChange={(e) => v17Ayarla(e.target.checked)} />
    </label>
  );
}
