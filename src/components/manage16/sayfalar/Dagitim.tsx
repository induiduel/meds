import React from 'react';
import { SayfaBasligi, IstatistikIzgara, IstatistikKart, Hata, Yukleniyor, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

/** Sistem › Dağıtım bilgisi — canlı commit, dist/surum.json, dist/dagitim.json, guncelleme_notu.json (onem). Salt okunur; dağıtım dagit.sh ile yapılır. */
export default function Dagitim(_p: SayfaProps) {
  const s = useAdminSorgu<any>('/api/admin/sistem/dagitim');
  const v = s.veri;
  return (
    <>
      <SayfaBasligi baslik="Dağıtım bilgisi" aciklama={v ? `Hedef sunucu: ${v.sunucu}. Dağıtımın tek yolu: bash meds/deploy/oracle/dagit.sh (kural 15).` : 'Sürüm ve commit'}
        eylemler={<button type="button" className="m16-btn" onClick={() => void s.yenile()}>Yenile</button>} />
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      {!v && !s.hata && <Yukleniyor satir={3} />}
      {v && (
        <>
          <IstatistikIzgara>
            <IstatistikKart etiket="Derleme sürümü (surum.json)" deger={v.surum?.onem ?? '—'} alt={v.surum?.surum || 'dist/surum.json yok'} />
            <IstatistikKart etiket="Güncelleme notu onem" deger={v.not?.onem ?? '—'} alt={v.not?.baslik} ton={v.not && v.surum && v.not.onem !== v.surum.onem ? 'uyari' : 'notr'} />
            <IstatistikKart etiket="Dağıtılan commit" deger={(v.dagitim?.commit || '—').slice(0, 10)} alt={v.dagitim?.at ? zamanMetni(v.dagitim.at) : 'dist/dagitim.json yok'} />
            <IstatistikKart etiket="Çalışma ağacı" deger={v.git ? (v.git.commit || '').slice(0, 10) : 'git yok'} alt={v.git ? `${v.git.dal} · ${v.git.kirliDosya} değişmiş dosya` : 'Bu sunucuda depo yok'} ton={v.git?.kirliDosya ? 'uyari' : 'notr'} />
          </IstatistikIzgara>
          <div className="m16-ts-izgara">
            {v.not && (
              <section className="m16-kart">
                <h2>Son güncelleme notu</h2>
                <p><strong>{v.not.baslik}</strong></p>
                <ul>{(v.not.maddeler || []).map((m: string, i: number) => <li key={i}>{m}</li>)}</ul>
              </section>
            )}
            {v.git?.son?.length > 0 && (
              <section className="m16-kart">
                <h2>Son commitler</h2>
                <ul className="m16-liste">{v.git.son.map((c: any) => <li key={c.h}><code>{c.h}</code><span className="m16-kisalt" title={c.mesaj}>{c.mesaj}</span><time>{zamanMetni(c.at)}</time></li>)}</ul>
              </section>
            )}
            <section className="m16-kart"><h2>Ham dosyalar</h2><pre className="m16-ts-log">{JSON.stringify({ surum: v.surum, dagitim: v.dagitim }, null, 2)}</pre></section>
          </div>
        </>
      )}
    </>
  );
}
