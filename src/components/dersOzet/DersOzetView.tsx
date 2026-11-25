/**
 * Ders özeti (Kurul 2+): akılda kalması gerekenler, çıkmışlar, sesli özet (EMA, okunan madde işaretlenir) ve sesli soru çözümü.
 * Adres: /dersler/ders-ozeti[/kurul<N>[/<ders>]] (iç /ders-ozeti[/<ders>]?kurul=N). Veri: dersOzetVeri.ts.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { Check, ChevronLeft, ChevronRight, CircleCheck, Headphones, LayoutDashboard, ListChecks, Pause, Play, RotateCcw, Star } from 'lucide-react';
import { icKonum } from '../../siteHaritasi';
import { linkClick, navigateTo } from '../../router';
import { guvenliLazy } from '../../utils/guvenliLazy';
import { bayrak, useSiteAyar, yoneticiMi } from '../../services/siteAyar';
import { useV15Baslik } from '../v15/baslik';
import type { Brans } from '../spots/brans';
import { dk, ozDersYukle, ozDizinYukle, ozIlerlemeYaz, ozKurullar, TUR_AD, useOzIlerleme, type OzDers, type OzDizin } from './dersOzetVeri';
import { useOzetOynatici } from './oynatici';
import { isaretToggle, useOzetIsaret } from './dersOzetIsaret';
import { DersOzetYeni } from './DersOzetYeni';
import '../../styles/soru-cozucu.css';
import '../../styles/v15/cozucu.css';
import '../../styles/v15/dersOzet.css';

const SoruCozucu = guvenliLazy(() => import('../spots/cozucu/SoruCozucu'));

/**
 * Görünüm tercihi (cihazda): 'yeni' alternatif tam ekran çalışma ekranı, 'eski' klasik ekran.
 * Alternatif ekran `ders_ozet_yeni` özellik bayrağı yönetici tarafından açılmadan kimseye gösterilmez.
 */
const GORUNUM_KEY = 'medsoru_ders_ozet_gorunum_v1';
const gorunumOku = (): 'yeni' | 'eski' => { try { return localStorage.getItem(GORUNUM_KEY) === 'yeni' ? 'yeni' : 'eski'; } catch { return 'eski'; } };
const gorunumYaz = (v: 'yeni' | 'eski') => { try { localStorage.setItem(GORUNUM_KEY, v); } catch { /* yoksay */ } };
/** Alternatif ekran bu kullanıcıya açık mı: bayrak açık ya da yönetici */
const yeniEkranAcik = () => yoneticiMi() || bayrak('ders_ozet_yeni', false);

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
  const [gorunum, setGorunum] = useState<'yeni' | 'eski'>(gorunumOku);
  useSiteAyar(); // bayrak panelden açılınca ekran kendiliğinden yenilensin (yalnız yönetici)
  const yeniVar = yeniEkranAcik();
  useEffect(() => { ozDersYukle(ders).then(setD, () => setD(null)); }, [ders]);
  useV15Baslik(d ? { baslik: d.baslik, alt: `Ders özeti · ${d.brans || ''}`, geri: `/dersler/ders-ozeti/kurul${d.kurul}` } : { baslik: 'Ders özeti' });
  if (d === undefined) return <p className="dz-bos">Yükleniyor…</p>;
  if (!d) return <p className="dz-bos">Bu dersin özeti bulunamadı.</p>;
  const degistir = (v: 'yeni' | 'eski') => { gorunumYaz(v); setGorunum(v); };
  if (yeniVar && gorunum === 'yeni') return <DersOzetYeni ders={ders} d={d} onKlasik={() => degistir('eski')} />;
  return <Klasik ders={ders} d={d} yeniVar={yeniVar} onYeni={() => degistir('yeni')} />;
};

const Klasik: React.FC<{ ders: string; d: OzDers; yeniVar: boolean; onYeni: () => void }> = ({ ders, d, yeniVar, onYeni }) => {
  const [coz, setCoz] = useState<null | 'tum' | 'cikmis'>(null);
  const [cozKod, setCozKod] = useState<string | null>(null);
  const il = useOzIlerleme()[ders];
  const isaret = useOzetIsaret()[ders] || {};
  const [cikmisAc, setCikmisAc] = useState(false);
  const oy = useOzetOynatici(d, ders);
  const cikmisSay = useMemo(() => new Map((d.cikmis || []).map((c, i) => [c.id, i + 1])), [d]);

  const Oge: React.FC<{ id: string; children: React.ReactNode; className?: string }> = ({ id, children, className }) => (
    <li id={`dz-${id}`} className={`${className || ''}${oy.aktif === id ? ' dz-aktif' : ''}${isaret[id] ? ' dz-tik' : ''}`}>
      <button type="button" className="dz-tik-d" role="checkbox" aria-checked={!!isaret[id]} aria-label="Öğrendim olarak işaretle"
        onClick={(e) => { e.stopPropagation(); isaretToggle(ders, id); }}><Check size={12} aria-hidden /></button>
      <span className="dz-oge-i" onClick={() => oy.buradan(id)}>{children}</span>
    </li>
  );
  const rozet = (cs?: string[]) => cs?.length ? <span className="dz-cikmis" title="Bu bilgi çıkmış soruda soruldu">Çıkmış</span> : null;

  return (
    <div className="dz-sayfa dz-ders">
      {yeniVar && (
        <button type="button" className="dz-dugme dz-yeni-gec" onClick={onYeni}><LayoutDashboard size={16} aria-hidden /> Yeni çalışma ekranı (tam ekran)</button>
      )}
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
