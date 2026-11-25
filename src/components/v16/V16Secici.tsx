import { useSyncExternalStore } from 'react';
import { v16Ayarla, v16Dinle, v16Istek } from '../../utils/v16';

/** Ayarlar › Görünüm: yalnız yöneticiye görünen "v16 (deneme)" anahtarı (docs/V16_PLAN.md). */
export default function V16Secici() {
  const acik = useSyncExternalStore(v16Dinle, v16Istek, () => false);
  return (
    <label className="v16-anahtar">
      <span>
        <b>v16 tasarımı (deneme)</b>
        <small>Yalnız yöneticiye açık. Öğrenciler v15'i görmeye devam eder.</small>
      </span>
      <input type="checkbox" role="switch" aria-checked={acik} checked={acik} onChange={(e) => v16Ayarla(e.target.checked)} />
    </label>
  );
}
