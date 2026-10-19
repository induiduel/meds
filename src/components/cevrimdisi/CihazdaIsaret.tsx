/** Ders listelerinde "Cihazda" işareti: paket indirilmişse (güncellemesi olsa da) küçük bulut simgesi. Motor: services/cevrimdisi. */
import { CloudCheck } from 'lucide-react';
import { paketDurumu, useCevrimdisi } from '../../services/cevrimdisi/paketMotoru';

export default function CihazdaIsaret({ paket }: { paket: string }) {
  const S = useCevrimdisi();
  const d = paketDurumu(paket, S);
  if (d !== 'tamam' && d !== 'guncelleme' && d !== 'iniyor') return null;
  const metin = d === 'iniyor' ? 'İniyor' : 'Cihazda';
  return (
    <span className={`cv-cihazda${d === 'iniyor' ? ' is-iniyor' : ''}`} title={d === 'guncelleme' ? 'Cihazda (güncelleme var)' : `${metin} · internetsiz açılır`}>
      <CloudCheck aria-hidden="true" />
      <span>{metin}</span>
    </span>
  );
}
