/**
 * Ders özeti (Kurul 2+): akılda kalması gerekenler, çıkmışlar, sesli özet (EMA, okunan madde işaretlenir) ve sesli soru çözümü.
 * Adres: /dersler/ders-ozeti[/kurul<N>[/<ders>]] (iç /ders-ozeti[/<ders>]?kurul=N). Veri: dersOzetVeri.ts.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Check, ChevronLeft, ChevronRight, CircleCheck, Headphones, ListChecks, Pause, Play, RotateCcw, Star } from 'lucide-react';
import { icKonum } from '../../siteHaritasi';
import { linkClick, navigateTo } from '../../router';
import { guvenliLazy } from '../../utils/guvenliLazy';
import { useV15Baslik } from '../v15/baslik';
import type { Brans } from '../spots/brans';
import { dk, klipAdres, klipSirasi, ogeKlibi, ozDersYukle, ozDizinYukle, ozIlerlemeYaz, ozKurullar, TUR_AD, useOzIlerleme, type OzDers, type OzDizin } from './dersOzetVeri';
import '../../styles/soru-cozucu.css';
import '../../styles/v15/cozucu.css';
import '../../styles/v15/dersOzet.css';

const SoruCozucu = guvenliLazy(() => import('../spots/cozucu/SoruCozucu'));
const HIZLAR = [1, 1.25, 1.5, 1.75];
const HIZ_KEY = 'medsoru_ders_ozet_hiz_v1';
const hizOku = () => { try { const v = Number(localStorage.getItem(HIZ_KEY)); return HIZLAR.includes(v) ? v : 1; } catch { return 1; } };

const Bag: React.FC<React.AnchorHTMLAttributes<HTMLAnchorElement> & { to: string }> = ({ to, children, ...p }) => (
  <a href={to} onClick={linkClick(() => navigateTo(to))} {...p}>{children}</a>
);
const kalin = (m: string) => m.split(/\*\*(.+?)\*\*/g).map((p, i) => (i % 2 ? <strong key={i}>{p}</strong> : <React.Fragment key={i}>{p}</React.Fragment>));

function konum(): { kurul: number; ders?: string } {
  const k = icKonum();
  const ders = /^\/ders-ozeti\/([^/?#]+)/.exec(k.pathname)?.[1];
  const q = Number(new URLSearchParams(k.search).get('kurul'));
  const kurul = ders ? Number(/^k(\d)/.exec(ders)?.[1]) : q || ozKurullar()[0] || 2;
  return { kurul, ders: ders ? decodeURIComponent(ders) : undefined };
}

const DersOzetView: React.FC = () => {
  const [yer, setYer] = useState(konum);
  useEffect(() => {
    const f = () => setYer(konum());
    window.addEventListener('popstate', f);
    window.addEventListener('meds:navigate', f as EventListener);
    return () => { window.removeEventListener('popstate', f); window.removeEventListener('meds:navigate', f as EventListener); };
  }, []);
  return yer.ders ? <DersOzet key={yer.ders} ders={yer.ders} /> : <Liste kurul={yer.kurul} />;
};
export default DersOzetView;

const Liste: React.FC<{ kurul: number }> = ({ kurul }) => {
  const [dz, setDz] = useState<OzDizin | null | undefined>(undefined);
  useEffect(() => { setDz(undefined); ozDizinYukle(kurul).then(setDz, () => setDz(null)); }, [kurul]);
  useV15Baslik({ baslik: 'Ders özeti', alt: `Kurul ${kurul} · akılda kalması gerekenler` });
  const il = useOzIlerleme();
  const biten = (dz?.dersler || []).filter((d) => il[d.ders]?.bitti).length;
  const gruplar = useMemo(() => {
    const m = new Map<string, OzDizin['dersler']>();
    for (const d of dz?.dersler || []) m.set(d.brans || 'Diğer', [...(m.get(d.brans || 'Diğer') || []), d]);
    return [...m.entries()];
  }, [dz]);
  return (
    <div className="dz-sayfa">
      <p className="dz-tanit">Her dersin sınavda sorulan ve sorulabilecek bilgileri kısa maddelerle: çıkmışlar, spot bilgiler, ayırıcı noktalar. Sesli dinleyebilir, sonra dersin sorularını sesli çözümle çözebilirsin.</p>
      {ozKurullar().length > 1 && (
        <div className="dz-kurullar">{ozKurullar().map((k) => <Bag key={k} to={`/dersler/ders-ozeti/kurul${k}`} className={k === kurul ? 'on' : ''}>Kurul {k}</Bag>)}</div>
      )}
      {!!dz?.dersler.length && <p className="dz-sayac"><CircleCheck size={16} aria-hidden /> {biten}/{dz.dersler.length} ders bitti</p>}
      {dz === undefined && <p className="dz-bos">Yükleniyor…</p>}
      {dz !== undefined && !dz?.dersler.length && <p className="dz-bos">Bu kurul için henüz ders özeti yok.</p>}
      {gruplar.map(([b, ds]) => (
        <section key={b} className="dz-grup">
          <h2>{b}</h2>
          <ul>
            {ds.map((d) => (
              <li key={d.ders}>
                <Bag to={`/dersler/ders-ozeti/kurul${kurul}/${d.ders}`} className={`dz-kart${il[d.ders]?.bitti ? ' dz-bitti' : ''}`}>
                  {il[d.ders]?.bitti ? <Check size={18} aria-label="Bitti" /> : <ListChecks size={18} aria-hidden />}
                  <span className="dz-kart-ad">{d.baslik}</span>
                  <span className="dz-kart-alt">{d.madde} madde · {d.cikmis} çıkmış{d.ses ? ` · ${dk(d.sure)} sesli` : ''}{d.soru ? ` · ${d.soru} soru` : ''}{!il[d.ders]?.bitti && il[d.ders]?.klip ? ' · yarıda' : ''}</span>
                </Bag>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
};

const DersOzet: React.FC<{ ders: string }> = ({ ders }) => {
  const [d, setD] = useState<OzDers | null | undefined>(undefined);
  const [coz, setCoz] = useState<null | 'tum' | 'cikmis'>(null);
  const [cozKod, setCozKod] = useState<string | null>(null);
  const il = useOzIlerleme()[ders];
  const [cikmisAc, setCikmisAc] = useState(false);
  useEffect(() => { ozDersYukle(ders).then(setD, () => setD(null)); }, [ders]);
  useV15Baslik(d ? { baslik: d.baslik, alt: `Ders özeti · ${d.brans || ''}`, geri: `/dersler/ders-ozeti/kurul${d.kurul}` } : { baslik: 'Ders özeti' });
  const oy = useOynatici(d || null, ders);
  const cikmisSay = useMemo(() => new Map((d?.cikmis || []).map((c, i) => [c.id, i + 1])), [d]);
  if (d === undefined) return <p className="dz-bos">Yükleniyor…</p>;
  if (!d) return <p className="dz-bos">Bu dersin özeti bulunamadı.</p>;

  const Oge: React.FC<{ id: string; children: React.ReactNode; className?: string }> = ({ id, children, className }) => (
    <li id={`dz-${id}`} className={`${className || ''}${oy.aktif === id ? ' dz-aktif' : ''}`} onClick={() => oy.buradan(id)}>{children}</li>
  );
  const rozet = (cs?: string[]) => cs?.length ? <span className="dz-cikmis" title="Bu bilgi çıkmış soruda soruldu">Çıkmış</span> : null;

  return (
    <div className="dz-sayfa dz-ders">
      <p className="dz-giris" id="dz-giris">{kalin(d.giris)}</p>
      <div className="dz-araclar">
        {d.ses && (
          <button type="button" className="dz-dugme dz-birincil" onClick={oy.calYaDur}>
            {oy.caliyor ? <Pause size={16} aria-hidden /> : <Headphones size={16} aria-hidden />} {oy.caliyor ? 'Duraklat' : oy.basladi || il?.klip ? 'Kaldığın yerden dinle' : `Sesli dinle · ${dk(d.sure)}`}
          </button>
        )}
        {d.cozucu && (
          <>
            <button type="button" className="dz-dugme" onClick={() => { oy.dur(); setCozKod(d.cozucu!.kod); setCoz('tum'); }}><Play size={16} aria-hidden /> Sesli soru çöz · {d.cozucu.soru}</button>
            {d.cozucu.cikmis > 0 && <button type="button" className="dz-dugme" onClick={() => { oy.dur(); setCozKod(d.cozucu!.kod); setCoz('cikmis'); }}>Yalnız çıkmışlar · {d.cozucu.cikmis}</button>}
          </>
        )}
      </div>

      <nav className="dz-icindekiler" aria-label="Bölümler">
        {d.bolumler.map((b) => <a key={b.id} href={`#dz-b-${b.id}`} onClick={(e) => { e.preventDefault(); document.getElementById(`dz-b-${b.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>{b.baslik}</a>)}
        <a href="#dz-akilda" onClick={(e) => { e.preventDefault(); document.getElementById('dz-akilda')?.scrollIntoView({ behavior: 'smooth' }); }}>Akılda kalması gerekenler</a>
      </nav>

      {d.bolumler.map((b) => (
        <section key={b.id} id={`dz-b-${b.id}`} className="dz-bolum">
          <h2>{b.baslik}</h2>
          <ul>
            {b.maddeler.map((m) => (
              <Oge key={m.id} id={m.id} className={`dz-madde dz-${m.tur}`}>
                {TUR_AD[m.tur] && <span className="dz-tur">{TUR_AD[m.tur]}</span>}
                <span className="dz-metin">{kalin(m.metin)}</span>
                {rozet(m.cikmis)}
                <span className="dz-sayfa-no" title="Slayt sayfası">s. {m.s.join(', ')}</span>
              </Oge>
            ))}
          </ul>
        </section>
      ))}

      <section id="dz-akilda" className="dz-bolum dz-akilda">
        <h2><Star size={18} aria-hidden /> Akılda kalması gerekenler</h2>
        <ol>
          {d.akilda.map((a, i) => (
            <Oge key={i} id={`akilda-${i + 1}`} className="dz-madde">
              <span className="dz-metin">{kalin(a.metin)}</span>{rozet(a.cikmis)}
            </Oge>
          ))}
        </ol>
      </section>

      <div className="dz-bitir">
        {il?.bitti ? (
          <button type="button" className="dz-dugme" onClick={() => ozIlerlemeYaz(ders, null)}><RotateCcw size={16} aria-hidden /> Bitti işaretini kaldır</button>
        ) : (
          <button type="button" className="dz-dugme dz-birincil" onClick={() => ozIlerlemeYaz(ders, { bitti: new Date().toISOString() })}><Check size={16} aria-hidden /> Bu özeti bitirdim</button>
        )}
        {d.cozucu && <button type="button" className="dz-dugme" onClick={() => { oy.dur(); setCozKod(d.cozucu!.kod); setCoz('tum'); }}><Play size={16} aria-hidden /> Şimdi soruları çöz</button>}
      </div>

      {d.cikmis.length > 0 && (
        <section className="dz-bolum dz-cikmislar">
          <button type="button" className="dz-ac" onClick={() => setCikmisAc((x) => !x)} aria-expanded={cikmisAc}>
            Bu dersin çıkmış soruları ({d.cikmis.length}) {cikmisAc ? '−' : '+'}
          </button>
          {cikmisAc && (
            <ol>
              {d.cikmis.map((c) => (
                <li key={c.id} value={cikmisSay.get(c.id)}>
                  <p className="dz-kok">{c.kok}</p>
                  <p className="dz-cevap"><strong>Cevap:</strong> {c.cevap}{c.yil ? <span className="dz-yil"> · {c.yil}</span> : null}</p>
                </li>
              ))}
            </ol>
          )}
        </section>
      )}

      {d.ses && oy.basladi && (
        <div className="dz-oynatici" role="region" aria-label="Sesli özet">
          <button type="button" onClick={oy.onceki} aria-label="Önceki bölüm"><ChevronLeft size={20} /></button>
          <button type="button" className="dz-oy-ana" onClick={oy.calYaDur} aria-label={oy.caliyor ? 'Duraklat' : 'Oynat'}>{oy.caliyor ? <Pause size={22} /> : <Play size={22} />}</button>
          <button type="button" onClick={oy.sonraki} aria-label="Sonraki bölüm"><ChevronRight size={20} /></button>
          <span className="dz-oy-ad">{oy.klipAdi}</span>
          <button type="button" className="dz-oy-hiz" onClick={oy.hizDegis} aria-label="Okuma hızı">{oy.hiz}×</button>
          <div className="dz-oy-cubuk" style={{ ['--p' as string]: `${Math.round(oy.ilerleme * 100)}%` }} />
        </div>
      )}

      {coz && d.cozucu && (
        <React.Suspense fallback={null}>
          <SoruCozucu key={cozKod || d.cozucu.kod} brans={d.cozucu.brans as Brans} kod={cozKod || d.cozucu.kod} mod={coz === 'cikmis' ? 'cikmis' : undefined}
            onClose={() => setCoz(null)} onDersDegis={(k) => { if (!d.cozucu?.kodlar || d.cozucu.kodlar.includes(k)) setCozKod(k); else setCoz(null); }} />
        </React.Suspense>
      )}
    </div>
  );
};

/** Klipleri sırayla çalar; çalan öğeyi (madde) işaretler ve görünür tutar; maddeye dokununca oradan başlar. */
function useOynatici(d: OzDers | null, ders: string) {
  const ses = useRef<HTMLAudioElement | null>(null);
  const [klip, setKlip] = useState<string | null>(null);
  const [caliyor, setCaliyor] = useState(false);
  const [aktif, setAktif] = useState<string | null>(null);
  const [ilerleme, setIlerleme] = useState(0);
  const [hiz, setHiz] = useState(hizOku);
  const sira = useMemo(() => (d ? klipSirasi(d) : []), [d]);
  const toplam = d?.sure || 1;

  useEffect(() => () => { ses.current?.pause(); }, []);
  const yukle = (k: string, bas = 0) => {
    if (!d) return;
    let a = ses.current;
    if (!a) {
      a = new Audio();
      ses.current = a;
      a.addEventListener('play', () => setCaliyor(true));
      a.addEventListener('pause', () => setCaliyor(false));
    }
    a.onended = () => {
      const i = sira.indexOf(k);
      if (i >= 0 && i + 1 < sira.length) yukle(sira[i + 1]);
      else { setCaliyor(false); setAktif(null); ozIlerlemeYaz(ders, { klip: undefined, t: undefined, bitti: new Date().toISOString() }); }
    };
    let sonYaz = 0;
    a.ontimeupdate = () => {
      const t = a!.currentTime;
      const x = d.ses?.klipler[k];
      if (!x) return;
      const once = sira.slice(0, sira.indexOf(k)).reduce((s, q) => s + (d.ses?.klipler[q]?.sure || 0), 0);
      setIlerleme((once + t) / toplam);
      if (Date.now() - sonYaz > 5000) { sonYaz = Date.now(); ozIlerlemeYaz(ders, { klip: k, t: Math.max(0, t - 2) }); }
      const oge = Object.entries(x.oge).find(([, [b, s]]) => t >= b - 0.05 && t < s + 0.4)?.[0];
      const id = oge === 'baslik' ? null : oge;
      if (id) setAktif((o) => {
        if (o !== id) document.getElementById(`dz-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return id;
      });
    };
    a.src = klipAdres(d, k);
    a.playbackRate = hiz;
    a.currentTime = bas;
    setKlip(k);
    a.play().catch(() => setCaliyor(false));
  };
  const calYaDur = () => {
    const a = ses.current;
    if (!klip || !a) {
      const il = (() => { try { return JSON.parse(localStorage.getItem('medsoru_ders_ozet_v1') || '{}')[ders]; } catch { return null; } })();
      return il?.klip && sira.includes(il.klip) ? yukle(il.klip, il.t || 0) : yukle(sira[0]);
    }
    if (a.paused) a.play().catch(() => undefined); else a.pause();
  };
  const atla = (y: number) => { const i = sira.indexOf(klip || ''); const j = Math.min(sira.length - 1, Math.max(0, i + y)); if (sira[j]) yukle(sira[j]); };
  const buradan = (oge: string) => {
    if (!d?.ses || !klip) return; // yalnız dinleme başladıysa dokununca atlar (okurken yanlışlıkla ses açılmasın)
    const k = ogeKlibi(d, oge);
    if (k) yukle(k, d.ses.klipler[k].oge[oge][0]);
  };
  const hizDegis = () => {
    const h = HIZLAR[(HIZLAR.indexOf(hiz) + 1) % HIZLAR.length];
    setHiz(h);
    try { localStorage.setItem(HIZ_KEY, String(h)); } catch { /* yoksay */ }
    if (ses.current) ses.current.playbackRate = h;
  };
  const klipAdi = !d || !klip ? '' : klip === 'g' ? 'Giriş' : klip === 'a' ? 'Akılda kalması gerekenler' : d.bolumler[Number(klip.slice(2)) - 1]?.baslik || '';
  return {
    caliyor, aktif, ilerleme, hiz, klipAdi, basladi: !!klip,
    calYaDur, buradan, hizDegis, onceki: () => atla(-1), sonraki: () => atla(1), dur: () => ses.current?.pause(),
  };
}
