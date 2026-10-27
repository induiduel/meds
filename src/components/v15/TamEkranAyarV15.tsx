import React, { useState } from 'react';
import { useAppFullscreen } from '../../utils/fullscreen';
import { ekranUyanikAcik, ekranUyanikYaz } from '../../services/ekranUyanik';
import { useDersEkranTercih } from '../../services/dersEkranTercih';
import '../../styles/v15/ek15.css';

/**
 * v15 · Tam ekran ve kısayollar (tasarım O10 tamEkranAyar). Profil › Ayarlar › Tam ekran ve kısayollar.
 * Uygulama tam ekranı (Fullscreen API / PWA), sesli derste ekran kararmasın (Wake Lock) ve klavye kısayolları listesi.
 * "Ders açılınca kendiliğinden tam ekran" ve "Yatayda yan yana" sesli ders ekranına bağlıdır (services/dersEkranTercih.ts, cihazda).
 */
/**
 * AB10: yalnız kodda gerçekten çalışan kısayollar (kaynak: shell/shellHooks.useSearchShortcut, canliDers/CanliDersDock,
 * CanliDersDers tam ekran, v15/PracticeV15, summary/SummaryReader). Kronometrenin klavye kısayolu yok → grup konmadı.
 * Yeni kısayol bağlanınca buraya eklenir; çalışmayan kısayol listelenmez.
 */
const GRUPLAR: [string, [string, string][]][] = [
  ['Genel', [
    ['Arama', 'Ctrl + K  ya da  /'],
    ['Yardım merkezi', '?'],
    ['Özet okurken metinde ara', 'Ctrl + F'],
    ['Pencereyi kapat / tam ekrandan çık', 'Esc'],
  ]],
  ['Sesli ders', [
    ['Oynat / duraklat', 'Boşluk'],
    ['10 sn geri / ileri', '← →'],
    ['Hızı düşür / artır', '[  ]'],
    ['Önceki / sonraki bölüm (zaman çubuğu seçiliyken)', 'Shift + ← →'],
    ['Yazıyı büyüt / küçült (tam ekranda)', '+  −'],
  ]],
  ['Soru', [
    ['Şık seç', 'A–E'],
    ['Cevapla', 'Enter'],
  ]],
];

export default function TamEkranAyarV15() {
  const [tam, tamDegis] = useAppFullscreen();
  const [uyanik, setUyanik] = useState(ekranUyanikAcik);
  const [otoTam, setOtoTam] = useDersEkranTercih('otoTam');
  const [yatayYan, setYatayYan] = useDersEkranTercih('yatayYan');
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
        <label className="kre-sat">
          <span>Ders açılınca kendiliğinden tam ekran</span>
          <button type="button" role="switch" aria-checked={otoTam} className={`kre-tgl${otoTam ? ' is-on' : ''}`} onClick={() => setOtoTam(!otoTam)}><i /></button>
        </label>
        <p className="kre-not">Tarayıcılar tam ekranı yalnız bir dokunuşla izin verir: sesli ders açıldıktan sonraki ilk dokunuşunda tam ekrana geçer.</p>
        <label className="kre-sat">
          <span>Yatayda yan yana</span>
          <button type="button" role="switch" aria-checked={yatayYan} className={`kre-tgl${yatayYan ? ' is-on' : ''}`} onClick={() => setYatayYan(!yatayYan)}><i /></button>
        </label>
        <p className="kre-not">Telefonu ya da tableti yatay tuttuğunda sesli derste slayt ve metin yan yana görünür.</p>
      </section>
      <section className="v15-card kre-kart">
        <b>Kısayollar</b>
        {GRUPLAR.map(([grup, liste]) => (
          <div key={grup} className="ky15-g">
            <h3 className="v15-cap">{grup}</h3>
            <ul className="te15-kl">
              {liste.map(([ad, tus]) => <li key={ad}><span>{ad}</span><kbd>{tus}</kbd></li>)}
            </ul>
          </div>
        ))}
        <p className="kre-not">Kısayollar fiziksel klavyede çalışır; yazı alanındayken devre dışıdır.</p>
      </section>
    </div>
  );
}
