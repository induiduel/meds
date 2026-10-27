import React, { useState } from 'react';
import { useAppFullscreen } from '../../utils/fullscreen';
import { ekranUyanikAcik, ekranUyanikYaz } from '../../services/ekranUyanik';

/**
 * v15 · Tam ekran ve kısayollar (tasarım O10 tamEkranAyar). Profil › Ayarlar › Tam ekran ve kısayollar.
 * Uygulama tam ekranı (Fullscreen API / PWA), sesli derste ekran kararmasın (Wake Lock) ve klavye kısayolları listesi.
 * Yalnız gerçekten çalışan seçenekler var; tasarımdaki "kendiliğinden tam ekran" ve "yatayda yan yana" altyapı yok.
 */
const KISAYOL: [string, string][] = [
  ['Tam ekran', 'F'],
  ['Oynat / duraklat (sesli ders)', 'Boşluk'],
  ['10 sn geri / ileri', '← →'],
  ['Önceki / sonraki bölüm', '↑ ↓'],
  ['Şık seç (soru)', 'A–E'],
  ['PDF\'te ara', 'Ctrl + F'],
  ['Arama', 'Ctrl + K'],
  ['Kapat / çık', 'Esc'],
];

export default function TamEkranAyarV15() {
  const [tam, tamDegis] = useAppFullscreen();
  const [uyanik, setUyanik] = useState(ekranUyanikAcik);
  const destek = typeof navigator !== 'undefined' && 'wakeLock' in navigator;
  return (
    <div className="kre-cols te15">
      <section className="v15-card kre-kart">
        <label className="kre-sat">
          <span>Uygulamayı tam ekran aç</span>
          <button type="button" role="switch" aria-checked={tam} className={`kre-tgl${tam ? ' is-on' : ''}`} onClick={() => tamDegis()}><i /></button>
        </label>
        <p className="kre-not">Tarayıcı çubuğu ve sistem çubukları gizlenir. Ana ekrana eklediğin uygulamada zaten tam ekran açılır.</p>
        <label className="kre-sat">
          <span>Sesli derste ekran kararmasın</span>
          <button type="button" role="switch" aria-checked={uyanik} disabled={!destek} className={`kre-tgl${uyanik ? ' is-on' : ''}`} onClick={() => { setUyanik(!uyanik); ekranUyanikYaz(!uyanik); }}><i /></button>
        </label>
        {!destek && <p className="kre-not">Bu tarayıcı ekranı açık tutmayı desteklemiyor.</p>}
      </section>
      <section className="v15-card kre-kart">
        <b>Kısayollar</b>
        <ul className="te15-kl">
          {KISAYOL.map(([ad, tus]) => <li key={ad}><span>{ad}</span><kbd>{tus}</kbd></li>)}
        </ul>
      </section>
    </div>
  );
}
