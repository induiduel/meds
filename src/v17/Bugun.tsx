import { useEffect, useMemo, useState } from 'react';
import { linkClick, navigateTo, pathFor } from '../router';
import { cdKonumListesi, cdListeGetir, fmtSure, CD_KONUM_OLAY, type CdListeDers } from '../components/canliDers/canliDersStore';
import { Ikon } from '../components/v16/Ikon';
import type { Cihaz } from './Kabuk';

/**
 * v17 Bugün: kaldığın yer (son dinlenen ders), son derslerin sırası. Veri: ses deposunun "kaldığın yer" kayıtları +
 * ders listesi. Hiçbir şey dinlenmediyse boş durum Ders çalış'a yönlendirir.
 */
const SELAM = () => { const h = new Date().getHours(); return h < 6 ? 'İyi geceler' : h < 12 ? 'Günaydın' : h < 18 ? 'İyi günler' : 'İyi akşamlar'; };

export default function Bugun({ cihaz }: { cihaz: Cihaz }) {
  const [liste, setListe] = useState<CdListeDers[] | null>(null);
  const [konum, setKonum] = useState(() => cdKonumListesi());
  useEffect(() => {
    let ol = true;
    cdListeGetir().then((l) => { if (ol) setListe(l); }).catch(() => { if (ol) setListe([]); });
    const f = () => setKonum(cdKonumListesi());
    window.addEventListener(CD_KONUM_OLAY, f);
    return () => { ol = false; window.removeEventListener(CD_KONUM_OLAY, f); };
  }, []);
  const harita = useMemo(() => new Map((liste || []).map((d) => [d.key, d])), [liste]);
  const son = konum.map((k) => ({ k, d: harita.get(k.key) })).filter((x) => x.d).slice(0, 5) as { k: (typeof konum)[number]; d: CdListeDers }[];
  const ilk = son[0];
  const sure = (d: CdListeDers) => d.varsayilan?.sureSn || d.varyantlar?.[0]?.sureSn || 0;
  const tarih = new Date().toLocaleDateString('tr-TR', { weekday: 'long', day: 'numeric', month: 'long' });
  const pc = cihaz === 'pc';
  const git = (key: string) => linkClick(() => navigateTo(pathFor('canli_ders', key)));

  const ana = (
    <main>
      <p className="k7-ust" style={{ textTransform: 'none' }}>{tarih.charAt(0).toLocaleUpperCase('tr') + tarih.slice(1)}</p>
      <h1 className="k7-dev" style={{ fontSize: pc ? 52 : 34, paddingTop: 10 }}>{SELAM()}.</h1>
      {ilk ? (
        <a href={pathFor('canli_ders', ilk.d.key)} onClick={git(ilk.d.key)} className="k7-belir"
          style={{ display: 'grid', gridTemplateColumns: 'minmax(0,1fr) auto', gap: '8px 20px', alignItems: 'center', marginTop: pc ? 40 : 26, padding: '20px 0', borderTop: '1.5px solid var(--yazi)', borderBottom: '1px solid var(--cizgi)' }}>
          <span className="k7-ust" style={{ color: 'var(--vurgu)', gridColumn: '1 / -1' }}>Kaldığın yer</span>
          <span style={{ minWidth: 0 }}>
            <b className="k7-bas" style={{ display: 'block', fontSize: pc ? 30 : 22 }}>{ilk.d.baslik}</b>
            <span className="k7-not">{ilk.d.brans || 'Sesli ders'}{sure(ilk.d) ? `, ${fmtSure(Math.max(0, sure(ilk.d) - ilk.k.t))} kaldı` : ''}</span>
          </span>
          <span className="k7-cal" aria-hidden="true" style={{ width: pc ? 64 : 52, height: pc ? 64 : 52 }}><Ikon ad="oynat" /></span>
          {sure(ilk.d) > 0 && <span className="k7-il" style={{ gridColumn: '1 / -1', marginTop: 6 }}><i style={{ width: `${Math.min(100, (ilk.k.t / sure(ilk.d)) * 100)}%` }} /></span>}
        </a>
      ) : liste ? (
        <div style={{ marginTop: 26, padding: '20px 0', borderTop: '1.5px solid var(--yazi)', borderBottom: '1px solid var(--cizgi)' }}>
          <p className="k7-ara">Henüz bir ders dinlemedin.</p>
          <p className="k7-not" style={{ padding: '6px 0 14px' }}>Bir sesli ders aç; kaldığın yer burada görünür.</p>
          <a href="/dersler" className="k7-dg" onClick={linkClick(() => navigateTo('/dersler'))}>Derslere git</a>
        </div>
      ) : (
        <p className="k7-not" role="status" style={{ marginTop: 26 }}>Dersler yükleniyor…</p>
      )}
      {son.length > 1 && (
        <section>
          <h2 className="k7-ara" style={{ padding: '28px 0 6px' }}>Son dinlediklerin</h2>
          <ol>
            {son.slice(1).map(({ k, d }) => (
              <li key={d.key}>
                <a href={pathFor('canli_ders', d.key)} onClick={git(d.key)} className="k7-satir">
                  <span className="gov"><b>{d.baslik}</b><small>{d.brans || 'Sesli ders'}</small></span>
                  <span className="k7-not">{sure(d) ? `%${Math.min(100, Math.round((k.t / sure(d)) * 100))}` : ''}</span>
                </a>
              </li>
            ))}
          </ol>
        </section>
      )}
    </main>
  );
  return (
    <div className="k7-kaydir">
      <div style={{ maxWidth: pc ? 1120 : 720, margin: '0 auto', padding: pc ? '48px 40px 40px' : cihaz === 'tab' ? '32px 32px 40px' : '22px 20px 120px' }}>{ana}</div>
    </div>
  );
}
