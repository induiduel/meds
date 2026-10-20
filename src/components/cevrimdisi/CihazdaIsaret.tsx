/**
 * Ders listelerindeki çevrimdışı işareti: paket cihazdaysa "Cihazda" (sessiz indirildiyse "Cihazda · sessiz"), inmiyorsa küçük
 * "İndir" düğmesi — böylece ders, merkeze gitmeden listeden tek dokunuşla cihaza alınır (ses/PDF ayardaki varsayılana göre).
 * Motor: services/cevrimdisi.
 */
import React from 'react';
import { CloudCheck, CloudDownload } from 'lucide-react';
import { kuyrugaEkle, paketDurumu, useCevrimdisi } from '../../services/cevrimdisi/paketMotoru';

export default function CihazdaIsaret({ paket, indir = true }: { paket: string; indir?: boolean }) {
  const S = useCevrimdisi();
  const d = paketDurumu(paket, S);
  if (d === 'yok' || d === 'hata') {
    // Paket listesi bilinmiyorsa (merkez hiç açılmadı) ya da internet yoksa düğme gösterilmez
    if (!indir || !navigator.onLine || !S.hazir || (S.katalog.length && !S.katalog.some((p) => p.id === paket))) return null;
    const dur = (e: React.SyntheticEvent) => { e.preventDefault(); e.stopPropagation(); };
    return (
      <button type="button" className="cv-cihazda-indir" title="İnternetsiz kullanmak için cihaza indir"
        aria-label="Bu dersi çevrimdışı kullanmak için indir"
        onClick={(e) => { dur(e); kuyrugaEkle([paket]); }} onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') e.stopPropagation(); }}>
        <CloudDownload aria-hidden="true" /><span>{d === 'hata' ? 'Yeniden' : 'İndir'}</span>
      </button>
    );
  }
  if (d !== 'tamam' && d !== 'guncelleme' && d !== 'iniyor' && d !== 'kuyrukta') return null;
  const k = S.kayitlar[paket];
  const sessiz = k?.secim && !k.secim.ses && S.katalog.find((p) => p.id === paket)?.ek?.ses;
  const metin = d === 'iniyor' ? 'İniyor' : d === 'kuyrukta' ? 'Sırada' : sessiz ? 'Cihazda · sessiz' : 'Cihazda';
  return (
    <span className={`cv-cihazda${d === 'iniyor' || d === 'kuyrukta' ? ' is-iniyor' : ''}`}
      title={d === 'guncelleme' ? 'Cihazda (güncelleme var)' : sessiz ? 'Cihazda, sesler indirilmedi · internetsiz açılır' : `${metin} · internetsiz açılır`}>
      <CloudCheck aria-hidden="true" />
      <span>{metin}</span>
    </span>
  );
}
