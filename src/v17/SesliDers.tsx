import React, { Suspense, useEffect, useMemo, useState } from 'react';
import { guvenliLazy } from '../utils/guvenliLazy';
import { linkClick, navigateTo } from '../router';
import {
  cdAralik, cdAtla, cdDetayBagla, cdDetayGetir, cdHizDongu, cdOynat, cdParagrafa, cdParagrafSinirlari, cdToggle,
  fmtSure, useCd, type CdDetay,
} from '../components/canliDers/canliDersStore';
import { Ikon } from '../components/v16/Ikon';
import { Kabuk, type Cihaz } from './Kabuk';
import '../styles/canli-ders.css';

/**
 * v17 sesli ders (docs/V17_PLAN.md). Kabuk, başlık, bölüm şeridi, okuma metni ve oynatıcı yeni yazıldı; ses ve
 * PDF çekirdeği (metin takibi, canlı çizim, terim/çıkmış katmanı — AGENTS kural 17/18) mevcut CdPdfBolme'den gelir.
 */
const CdPdfBolme = guvenliLazy(() => import('../components/canliDers/CanliDersDers').then((m) => ({ default: m.CdPdfBolme })));

type Gorunum = 'ikisi' | 'metin' | 'slayt';
const GORUNUM_KEY = 'medsor_v17_sesli_gorunum';

/** Cümle başlangıç saniyeleri: paragraf başı + sesin ölçülü cümle zamanları */
function cumleBaslari(d: CdDetay | null, vid: string | null, i: number): number[] {
  const r = cdAralik(i);
  if (!r) return [];
  const v = d?.varyantlar.find((x) => x.id === vid);
  return [r[0], ...((v?.cumleZaman?.[String(i)] || []).filter((x) => x > r[0] && x < r[1]))];
}

function Oynatici({ detay, cihaz }: { detay: CdDetay; cihaz: Cihaz }) {
  const playing = useCd((s) => s.playing);
  const t = useCd((s) => s.t);
  const dur = useCd((s) => s.dur);
  const rate = useCd((s) => s.rate);
  const aktif = useCd((s) => s.aktif);
  const cumle = useCd((s) => s.cumle);
  const vid = useCd((s) => s.vid);
  const bekliyor = useCd((s) => s.bekliyor);
  const bizim = useCd((s) => s.key === detay.key);
  const paragraflar = useMemo(() => detay.bolumler.flatMap((b) => b.paragraflar), [detay]);
  const cumleGit = (yon: 1 | -1) => {
    const pi = paragraflar.findIndex((p) => p.i === aktif);
    if (pi < 0) return;
    const bas = cumleBaslari(detay, vid, aktif);
    const c = Math.max(0, cumle);
    if (yon > 0) {
      if (c + 1 < bas.length) cdAtla(bas[c + 1]);
      else if (pi + 1 < paragraflar.length) cdParagrafa(paragraflar[pi + 1].i, false);
    } else if (c > 0) cdAtla(bas[c - 1]);
    else if (pi > 0) { const onceki = cumleBaslari(detay, vid, paragraflar[pi - 1].i); if (onceki.length) cdAtla(onceki[onceki.length - 1]); }
  };
  const cal = () => { if (!bizim) cdOynat(detay); else cdToggle(); };
  const oran = dur > 0 ? Math.min(100, (t / dur) * 100) : 0;
  const hiz = String(rate).replace('.', ',');
  const cubuk = (
    <label className="k7-cubuk" aria-label="Ders konumu">
      <span className="k7-il"><i style={{ width: `${oran}%` }} /></span>
      <input type="range" min={0} max={Math.max(1, Math.round(dur))} value={Math.round(t)} onChange={(e) => cdAtla(Number(e.target.value))}
        aria-valuetext={`${fmtSure(t)} / ${fmtSure(dur)}`} />
    </label>
  );
  const dugmeler = (
    <>
      <button type="button" className="k7-ik" onClick={() => cumleGit(-1)} aria-label="Önceki cümle"><Ikon ad="onceki" /></button>
      <button type="button" className="k7-cal" onClick={cal} aria-label={playing && bizim ? 'Duraklat' : 'Oynat'} aria-busy={bekliyor}>
        <Ikon ad={playing && bizim ? 'duraklat' : 'oynat'} />
      </button>
      <button type="button" className="k7-ik" onClick={() => cumleGit(1)} aria-label="Sonraki cümle"><Ikon ad="sonraki" /></button>
    </>
  );
  if (cihaz === 'tel') {
    return (
      <footer style={{ flex: 'none', background: 'color-mix(in srgb, var(--zemin) 94%, transparent)', backdropFilter: 'blur(12px)', boxShadow: '0 -1px 0 var(--cizgi)', padding: '2px 14px max(14px, env(safe-area-inset-bottom))' }}>
        {cubuk}
        <div className="k7-oyn" style={{ justifyContent: 'space-between' }}>
          <button type="button" className="k7-dg2" onClick={cdHizDongu} aria-label={`Oynatma hızı ${hiz}`} style={{ minWidth: 62 }}>{hiz}×</button>
          {dugmeler}
          <span className="k7-no" style={{ minWidth: 62, textAlign: 'right', fontSize: 14 }}>{fmtSure(t)}</span>
        </div>
      </footer>
    );
  }
  return (
    <div className="k7-oyn" style={{ flex: 1, minWidth: 0 }}>
      {dugmeler}
      <span className="k7-no" style={{ fontSize: 14 }}>{fmtSure(t)}</span>
      {cubuk}
      <span className="k7-no" style={{ fontSize: 14 }}>{fmtSure(dur)}</span>
      <button type="button" className="k7-dg2" onClick={cdHizDongu} aria-label={`Oynatma hızı ${hiz}`}>{hiz}×</button>
    </div>
  );
}

/** Bölüm şeridi: her bölüm kendi süresi oranında; dinlenen kısım dolar, dokununca bölüme gider */
function BolumSeridi({ detay, etiketli = true }: { detay: CdDetay; etiketli?: boolean }) {
  const aktif = useCd((s) => s.aktif);
  const bizim = useCd((s) => s.key === detay.key);
  const parcalar = detay.bolumler.map((b) => b.paragraflar.map((p) => p.i)).filter((x) => x.length);
  const agirlik = parcalar.map((ids) => {
    const a = cdAralik(ids[0]), z = cdAralik(ids[ids.length - 1]);
    return a && z ? Math.max(1, z[1] - a[0]) : ids.length;
  });
  return (
    <div className="k7-bseri" role="list" aria-label="Bölümler">
      {parcalar.map((ids, k) => {
        const bas = ids[0], son = ids[ids.length - 1];
        const dolu = !bizim || aktif < bas ? 0 : aktif > son ? 1 : (ids.indexOf(aktif) + 0.5) / ids.length;
        const simdi = bizim && aktif >= bas && aktif <= son;
        return (
          <button key={k} type="button" role="listitem" className={simdi ? 'is-simdi' : ''} style={{ flex: `${agirlik[k]} 1 0` }}
            onClick={() => cdParagrafa(bas)} aria-current={simdi ? 'step' : undefined} title={detay.bolumler[k]?.baslik}>
            <i><b style={{ width: `${dolu * 100}%` }} /></i>
            {etiketli && <em>{detay.bolumler[k]?.baslik || `Bölüm ${k + 1}`}</em>}
          </button>
        );
      })}
    </div>
  );
}

/** Okuma metni: geçmiş, okunan (eozin alt vurgu), gelecek; cümleye dokununca oraya gider */
function Metin({ detay, buyuk }: { detay: CdDetay; buyuk?: boolean }) {
  const aktif = useCd((s) => s.aktif);
  const cumle = useCd((s) => s.cumle);
  const vid = useCd((s) => s.vid);
  const bizim = useCd((s) => s.key === detay.key);
  useEffect(() => {
    if (!bizim || aktif < 0) return;
    const el = document.querySelector<HTMLElement>(`.k7-okuma [data-p="${aktif}"] .simdi`) || document.querySelector<HTMLElement>(`.k7-okuma [data-p="${aktif}"]`);
    el?.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  }, [aktif, cumle, bizim]);
  return (
    <article className="k7-okuma" style={{ fontSize: buyuk ? 19 : 18, maxWidth: '64ch' }}>
      {detay.bolumler.map((b, bi) => (
        <section key={bi}>
          {b.baslik && <h3>{b.baslik}</h3>}
          {b.paragraflar.map((p) => {
            const sin = cdParagrafSinirlari(p.i, p.metin);
            const parcalar: string[] = [];
            let a = 0;
            for (const e of sin) { parcalar.push(p.metin.slice(a, e)); a = e; }
            if (a < p.metin.length) parcalar.push(p.metin.slice(a));
            const durum = !bizim || p.i > aktif ? 'gelecek' : p.i < aktif ? 'gecti' : '';
            return (
              <p key={p.i} data-p={p.i}>
                {parcalar.map((m, c) => {
                  const cls = durum || (c < cumle ? 'gecti' : c === cumle ? 'simdi' : 'gelecek');
                  return (
                    <span key={c} data-c={c} className={cls} onClick={() => {
                      if (!bizim) { cdOynat(detay); return; }
                      const bas = cumleBaslari(detay, vid, p.i);
                      if (bas[c] != null) cdAtla(bas[c]); else cdParagrafa(p.i);
                    }}>{m}</span>
                  );
                })}
              </p>
            );
          })}
        </section>
      ))}
    </article>
  );
}

const Yukleniyor = () => <p className="k7-not" role="status" style={{ padding: 24 }}>Ders hazırlanıyor…</p>;

export default function SesliDers({ dersKey, cihaz }: { dersKey: string; cihaz: Cihaz }) {
  const [detay, setDetay] = useState<CdDetay | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [gorunum, setGorunumHam] = useState<Gorunum>(() => { try { const v = localStorage.getItem(GORUNUM_KEY); return v === 'metin' || v === 'slayt' ? v : 'ikisi'; } catch { return 'ikisi'; } });
  const setGorunum = (g: Gorunum) => { setGorunumHam(g); try { localStorage.setItem(GORUNUM_KEY, g); } catch { /* yok */ } };
  const [rayAcik, setRayAcik] = useState(true);
  const [tam, setTam] = useState(false);
  const baskaCaliyor = useCd((s) => !!s.key && s.key !== dersKey && s.playing);
  const canli = useCd((s) => s.key === dersKey);

  useEffect(() => {
    let ol = true;
    setDetay(null); setHata(null);
    cdDetayGetir(dersKey).then((d) => { if (!ol) return; setDetay(d); cdDetayBagla(d); }).catch(() => { if (ol) setHata('Ders açılamadı. Bağlantını kontrol edip yeniden dene.'); });
    return () => { ol = false; };
  }, [dersKey]);

  if (hata) return <Kabuk cihaz={cihaz} aktif="ders"><div style={{ padding: 24 }}><p className="k7-ara">{hata}</p><button type="button" className="k7-dg" style={{ marginTop: 14 }} onClick={() => location.reload()}>Yeniden dene</button></div></Kabuk>;
  if (!detay) return <Kabuk cihaz={cihaz} aktif="ders"><Yukleniyor /></Kabuk>;

  const pdfVar = !!detay.pdf;
  const slaytGoster = pdfVar && gorunum !== 'metin';
  const metinGoster = gorunum !== 'slayt' || !pdfVar;
  const geri = linkClick(() => { if (history.length > 1) history.back(); else navigateTo('/dersler'); });
  const ust = `${detay.brans || 'Sesli ders'}${detay.kurul ? `, Kurul ${detay.kurul}` : ''}`;
  const sekmeler = pdfVar && (
    <div role="group" aria-label="Görünüm" style={{ display: 'flex', padding: 3, borderRadius: 999, background: 'var(--alan)', flex: 'none' }}>
      {([['ikisi', 'Slayt ve metin'], ['metin', 'Metin'], ['slayt', 'Slayt']] as [Gorunum, string][]).map(([g, ad]) => (
        <button key={g} type="button" aria-pressed={gorunum === g} onClick={() => setGorunum(g)}
          style={{ height: 32, padding: '0 12px', borderRadius: 999, font: '600 13px/1 var(--sans)', whiteSpace: 'nowrap', background: gorunum === g ? 'var(--yuzey)' : 'transparent', color: gorunum === g ? 'var(--yazi)' : 'var(--yazi-3)', boxShadow: gorunum === g ? 'var(--golge)' : 'none' }}>{ad}</button>
      ))}
    </div>
  );
  const baskaUyari = baskaCaliyor && (
    <div role="status" className="k7-belir" style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 14px', margin: '8px 0 0', borderRadius: 12, background: 'var(--vurgu-acik)', color: 'var(--yazi)', font: '500 14px/1.35 var(--sans)' }}>
      <span style={{ flex: 1, minWidth: 0 }}>Başka bir ders çalıyor.</span>
      <button type="button" className="k7-dg2" onClick={() => cdOynat(detay)}>Bu dersi başlat</button>
    </div>
  );
  const pdf = slaytGoster && (
    <Suspense fallback={<Yukleniyor />}>
      <div className="k7-pdf" style={{ minHeight: 0, minWidth: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
        <CdPdfBolme detay={detay} canli={canli} sigdir={cihaz !== 'tel'} />
      </div>
    </Suspense>
  );

  if (cihaz === 'tel') {
    return (
      <Kabuk cihaz="tel" aktif="ders" tam>
        <header style={{ padding: '6px 8px 0', flex: 'none' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <a href="/dersler" className="k7-ik" aria-label="Geri" onClick={geri}><Ikon ad="geri" /></a>
            <span className="k7-ust" style={{ flex: 1, minWidth: 0, textAlign: 'center', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{ust}</span>
            <span style={{ width: 44 }} />
          </div>
          <div style={{ padding: '2px 12px 0' }}>
            <h1 className="k7-bas" style={{ fontSize: 22 }}>{detay.baslik}</h1>
            <div style={{ padding: '8px 0 6px' }}><BolumSeridi detay={detay} etiketli={false} /></div>
            {sekmeler && <div style={{ paddingBottom: 6, overflowX: 'auto' }}>{sekmeler}</div>}
            {baskaUyari}
          </div>
        </header>
        {pdf && <div style={{ flex: metinGoster ? '0 0 42%' : 1, minHeight: 0, padding: '4px 12px 0', display: 'flex', flexDirection: 'column' }}>{pdf}</div>}
        {metinGoster && <div className="k7-kaydir" style={{ padding: '6px 20px 24px' }}><Metin detay={detay} /></div>}
        {!metinGoster && <div style={{ flex: 'none' }} />}
        <Oynatici detay={detay} cihaz="tel" />
      </Kabuk>
    );
  }

  const govde = (
    <div style={{ flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: slaytGoster && metinGoster ? `minmax(0, ${cihaz === 'pc' ? 1.35 : 1.2}fr) minmax(0, 1fr)` : 'minmax(0, 1fr)', gap: cihaz === 'pc' ? 40 : 28, padding: cihaz === 'pc' ? '20px 40px 0' : '8px 28px 0' }}>
      {pdf && <div style={{ minHeight: 0, display: 'flex', flexDirection: 'column', paddingBottom: 16 }}>{pdf}</div>}
      {metinGoster && <div className="k7-kaydir" style={{ padding: '4px 6px 24px', justifySelf: slaytGoster ? 'stretch' : 'center', width: '100%', maxWidth: slaytGoster ? undefined : 760 }}><Metin detay={detay} buyuk={cihaz === 'pc'} /></div>}
    </div>
  );
  const basBandi = (
    <section style={{ flex: 'none', padding: cihaz === 'pc' ? '18px 40px 12px' : '16px 28px 10px', boxShadow: '0 1px 0 var(--cizgi)', display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 12, minWidth: 0, flexWrap: 'wrap' }}>
        {cihaz === 'tab' && !tam && (
          <button type="button" className="k7-ik is-cer" onClick={() => setRayAcik((r) => !r)} aria-expanded={rayAcik} aria-label={rayAcik ? 'Menüyü gizle' : 'Menüyü göster'} title={rayAcik ? 'Menüyü gizle' : 'Menüyü göster'} style={{ alignSelf: 'center' }}><Ikon ad="izgara" /></button>
        )}
        <div style={{ flex: '1 1 320px', minWidth: 0 }}>
          <p className="k7-ust">{ust}</p>
          <h1 className={cihaz === 'pc' ? 'k7-dev' : 'k7-bas'} style={{ fontSize: cihaz === 'pc' ? 34 : 26, paddingTop: 4 }}>{detay.baslik}</h1>
        </div>
        {sekmeler}
        <button type="button" className="k7-ik is-cer" onClick={() => setTam((v) => !v)} aria-pressed={tam} aria-label={tam ? 'Tam ekrandan çık' : 'Tam ekran'} title={tam ? 'Tam ekrandan çık' : 'Tam ekran'}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{tam ? <path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}</svg>
        </button>
      </div>
      {cihaz === 'pc' && <Oynatici detay={detay} cihaz="pc" />}
      <BolumSeridi detay={detay} />
      {baskaUyari}
    </section>
  );
  return (
    <Kabuk cihaz={cihaz} aktif="ders" rayAcik={rayAcik} tam={tam}>
      {basBandi}
      {govde}
      {cihaz === 'tab' && <footer style={{ flex: 'none', padding: '10px 28px 16px', boxShadow: '0 -1px 0 var(--cizgi)' }}><Oynatici detay={detay} cihaz="tab" /></footer>}
    </Kabuk>
  );
}
