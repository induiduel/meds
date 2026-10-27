import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Activity, ArrowDown, ArrowRight, ArrowUpDown, ChevronLeft, ChevronRight, ArrowUp, Check, ChevronDown, CircleHelp, FlaskConical, Layers, ListChecks, Microscope,
  ListOrdered, Pill, Pin, RotateCw, Scale, Search, Sparkles, Stethoscope, Table2, X,
} from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { DI_BOLUMLER, dersIcerikGetir, dersSorulariGetir, type DiBolum, type DiPaket, type DiSoru, type DiTablo } from './dersIcerik';
import '../../styles/v15/dersIcerik.css';

/**
 * Ders içerik sayfaları (/dersler/ders/kurulN/<key>?b=terimler|hastaliklar|bilgiler|tablolar|sorular|kartlar), v15.
 * Okunaklılık kuralları (kullanıcı isteği 2026-10-27): her bilgi kendi kartında; başlık · kısa özet · maddeler sırası;
 * düz metin tablo yok — tablo türüne göre adım şeridi (Sıra/Adım), eşleşme kartları (2 sütun) ya da renkli karşılaştırma
 * matrisi (3+ sütun; telefonda satır kartı); Var/Yok, artar/azalır gibi değerler simgeyle; giriş animasyonu kademeli.
 * Veri biçimi: scripts/ders_icerik_uret.py (içerik işçisi bu biçimde üretir; bkz. docs/DERS_ICERIK_BICIMI.md).
 */
const norm = (s: string) => s.toLocaleLowerCase('tr');
/** **kalın** işaretli metni <b>'ye çevirir */
const Zengin = ({ t }: { t: string }) => <>{t.split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>))}</>;
/** "Etiket: açıklama" maddesi → kalın etiket; "a; b; c" (3+ parça) → iç içe alt maddeler */
function Madde({ t }: { t: string }) {
  const m = t.match(/^([^:]{2,40}):\s+(.+)$/);
  const govde = m ? m[2] : t;
  const parca = govde.split(/;\s+/);
  return (
    <li>
      {m && <b className="di15-et">{m[1]}</b>}
      {parca.length >= 3 ? <><Zengin t={parca[0]} /><ul className="di15-alt">{parca.slice(1).map((x, i) => <li key={i}><Zengin t={x} /></li>)}</ul></> : <Zengin t={govde} />}
    </li>
  );
}
/** Hücre değeri → simgeli rozet (Var/Yok, +/−, artar/azalır, evet/hayır) */
function Hucre({ v }: { v: string }) {
  const s = norm(v.trim());
  if (/^(var|evet|\+|pozitif|\(\+\))$/.test(s)) return <span className="di15-ik is-var"><Check aria-hidden />{v}</span>;
  if (/^(yok|hayır|-|−|negatif|\(-\))$/.test(s)) return <span className="di15-ik is-yok"><X aria-hidden />{v}</span>;
  if (/^(artar|artmış|yüksek|canlı|hiperaktif)/.test(s)) return <span className="di15-ik is-art"><ArrowUp aria-hidden />{v}</span>;
  if (/^(azalır|azalmış|düşük|kaybolur|yok olur|hipoaktif)/.test(s)) return <span className="di15-ik is-az"><ArrowDown aria-hidden />{v}</span>;
  return <>{v}</>;
}
const SIRA_RE = /^(sıra|adım|aşama|#|no)$/i;
const tabloTuru = (t: DiTablo): 'sira' | 'eslesme' | 'matris' =>
  SIRA_RE.test(t.h[0]?.trim() || '') || (t.r.length > 1 && t.r.every((r) => /^\d+[.)]?$/.test(r[0]?.trim() || ''))) ? 'sira' : t.h.length === 2 ? 'eslesme' : 'matris';
/** Hastalık bölüm adına göre ton + simge */
const BOLUM_TON: [RegExp, string, React.ElementType][] = [
  [/etiyo|neden|risk/i, 'w', FlaskConical], [/klinik|bulgu|belirti/i, 'b', Stethoscope], [/tanı|muayene|test/i, 'a', Microscope],
  [/tedavi|yönetim/i, 'ok', Pill], [/patoge|mekaniz|fizyo/i, 'ai', Activity],
];
const bolumTon = (b: string) => BOLUM_TON.find(([r]) => r.test(b)) || [null, 'c', ListChecks] as const;
type Sira = 'varsayilan' | 'az' | 'za' | 'slayt' | 'slayt-azalan' | 'puan';
const SIRA_AD: Record<Sira, string> = { varsayilan: 'Varsayılan sıra', az: 'Alfabetik (A → Z)', za: 'Alfabetik (Z → A)', slayt: 'Slayt: önce → sonra', 'slayt-azalan': 'Slayt: sonra → önce', puan: 'Sınav önemi (yüksek → düşük)' };
/** "5", "5-6", [7, 9] → ilk slayt numarası (yoksa sona) */
const slaytNo = (s: unknown): number => {
  const m = String(Array.isArray(s) ? s[0] ?? '' : s ?? '').match(/\d+/);
  return m ? parseInt(m[0], 10) : Number.MAX_SAFE_INTEGER;
};
function sirala<T>(l: T[], d: Sira, ad: (x: T) => string, sl?: (x: T) => unknown, pu?: (x: T) => number): T[] {
  if (d === 'varsayilan') return l;
  const k = [...l];
  if (d === 'az') k.sort((a, b) => ad(a).localeCompare(ad(b), 'tr'));
  else if (d === 'za') k.sort((a, b) => ad(b).localeCompare(ad(a), 'tr'));
  else if (d === 'slayt' && sl) k.sort((a, b) => slaytNo(sl(a)) - slaytNo(sl(b)) || ad(a).localeCompare(ad(b), 'tr'));
  else if (d === 'slayt-azalan' && sl) k.sort((a, b) => { const x = slaytNo(sl(a)), y = slaytNo(sl(b)); return (x === y ? 0 : x === Number.MAX_SAFE_INTEGER ? 1 : y === Number.MAX_SAFE_INTEGER ? -1 : y - x) || ad(a).localeCompare(ad(b), 'tr'); });
  else if (d === 'puan' && pu) k.sort((a, b) => pu(b) - pu(a));
  return k;
}
const puanTon = (p: number) => (p >= 90 ? 'is-cok' : p >= 70 ? 'is-orta' : 'is-az');

/** Yatay çip şeridi: fare tekerleği, sürükleme, ok düğmeleri; aktif çip görünür kalır */
function useSerit(bagimlilik: unknown) {
  const ref = useRef<HTMLElement | null>(null);
  const [kenar, setKenar] = useState({ sol: false, sag: false });
  const guncelle = () => {
    const e = ref.current; if (!e) return;
    setKenar({ sol: e.scrollLeft > 4, sag: e.scrollLeft + e.clientWidth < e.scrollWidth - 4 });
  };
  useEffect(() => {
    const e = ref.current; if (!e) return;
    e.querySelector<HTMLElement>('.is-on')?.scrollIntoView({ block: 'nearest', inline: 'center' });
    guncelle();
    const tekerlek = (ev: WheelEvent) => {
      if (e.scrollWidth <= e.clientWidth || Math.abs(ev.deltaX) > Math.abs(ev.deltaY)) return;
      ev.preventDefault(); e.scrollLeft += ev.deltaY;
    };
    let x0 = 0, l0 = 0, basili = false, surukle = false;
    const bas = (ev: PointerEvent) => { if (ev.pointerType !== 'mouse') return; basili = true; surukle = false; x0 = ev.clientX; l0 = e.scrollLeft; };
    const hareket = (ev: PointerEvent) => { if (!basili) return; if (Math.abs(ev.clientX - x0) > 5) surukle = true; if (surukle) e.scrollLeft = l0 - (ev.clientX - x0); };
    const birak = () => { basili = false; };
    const tikla = (ev: MouseEvent) => { if (surukle) { ev.preventDefault(); ev.stopPropagation(); surukle = false; } };
    e.addEventListener('wheel', tekerlek, { passive: false });
    e.addEventListener('pointerdown', bas); window.addEventListener('pointermove', hareket); window.addEventListener('pointerup', birak);
    e.addEventListener('click', tikla, true); e.addEventListener('scroll', guncelle, { passive: true });
    window.addEventListener('resize', guncelle);
    return () => {
      e.removeEventListener('wheel', tekerlek); e.removeEventListener('pointerdown', bas);
      window.removeEventListener('pointermove', hareket); window.removeEventListener('pointerup', birak);
      e.removeEventListener('click', tikla, true); e.removeEventListener('scroll', guncelle); window.removeEventListener('resize', guncelle);
    };
  }, [bagimlilik]);
  const kaydir = (y: number) => ref.current?.scrollBy({ left: y * Math.max(160, (ref.current?.clientWidth || 0) * 0.6), behavior: 'smooth' });
  return { ref, kenar, kaydir };
}

const TABLO_TUR_AD: Record<string, string> = { karsilastirma: 'Karşılaştırma', sira: 'Sıralama', eslesme: 'Eşleştirme', matris: 'Tablo' };
const tabloKategori = (t: DiTablo) => (t.k ? 'karsilastirma' : tabloTuru(t));

export default function DersIcerikV15({ dersKey, bolum }: { dersKey: string; bolum: DiBolum }) {
  const [p, setP] = useState<DiPaket | null>(null);
  const [kaz, setKaz] = useState<{ no: number; metin: string; sorular: DiSoru[] }[]>([]);
  const [ara, setAra] = useState('');
  const [alt, setAlt] = useState<string>('');
  const [sira, setSira] = useState<Sira>('varsayilan');
  const [tur, setTur] = useState('');
  const serit = useSerit(`${bolum}-${p ? 1 : 0}`);
  useEffect(() => {
    dersIcerikGetir(dersKey).then(setP);
    dersSorulariGetir(dersKey).then(setKaz);
  }, [dersKey]);
  useEffect(() => { setAra(''); setAlt(''); setSira('varsayilan'); setTur(''); }, [bolum]);
  useEffect(() => { setSira('varsayilan'); }, [alt]);
  const q = norm(ara.trim());
  const ok = (...s: (string | undefined)[]) => !q || s.some((x) => x && norm(x).includes(q));
  const sorular = useMemo(() => kaz.flatMap((k) => k.sorular), [kaz]);
  if (!p) return <p className="di15-bos v15-card">Yükleniyor…</p>;

  const sayi: Record<DiBolum, number> = { terimler: p.terimler.length + p.kisaltmalar.length, hastaliklar: p.hastaliklar.length, bilgiler: p.onemli.length + p.bilgiler.length + p.spotlar.length, listeler: p.listeler.length, quiz: p.quiz.length, tablolar: p.tablolar.length, sorular: sorular.length, kartlar: p.kartlar.length };
  const url = (b: DiBolum) => `${pathFor('ders_detay', dersKey)}?b=${b}`;
  const AltSekme = ({ l }: { l: [string, string, number][] }) => {
    const sec = alt || l.find((x) => x[2])?.[0] || l[0][0];
    return (
      <div className="v15-seg di15-alts" role="tablist">
        {l.filter((x) => x[2]).map(([id, ad, n]) => <button key={id} type="button" role="tab" aria-selected={sec === id} aria-current={sec === id ? 'page' : undefined} onClick={() => setAlt(id)}>{ad}<small>{n}</small></button>)}
      </div>
    );
  };
  const altSec = (ilk: string) => alt || ilk;

  return (
    <div className="di15">
      <div className="di15-seritkap">
      {serit.kenar.sol && <button type="button" className="di15-ser-ok is-sol" onClick={() => serit.kaydir(-1)} aria-label="Sola kaydır"><ChevronLeft aria-hidden /></button>}
      <nav className="di15-tabs" aria-label="Ders içerikleri" ref={serit.ref as React.RefObject<HTMLElement>}>
        {DI_BOLUMLER.filter((b) => sayi[b.id]).map((b) => (
          <a key={b.id} href={url(b.id)} className={b.id === bolum ? 'is-on' : ''} aria-current={b.id === bolum ? 'page' : undefined} onClick={linkClick(() => navigateTo(url(b.id)))}>
            {b.ad} <span>{sayi[b.id]}</span>
          </a>
        ))}
      </nav>
      {serit.kenar.sag && <button type="button" className="di15-ser-ok is-sag" onClick={() => serit.kaydir(1)} aria-label="Sağa kaydır"><ChevronRight aria-hidden /></button>}
      </div>
      <label className="di15-ara"><Search aria-hidden /><input value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Bu sayfada ara" aria-label="Bu sayfada ara" /></label>

      {(() => {
        const sec = alt;
        const slaytli = bolum === 'hastaliklar' || bolum === 'tablolar' || bolum === 'listeler' || (bolum === 'terimler' && sec !== 'kisa') || (bolum === 'bilgiler' && sec !== 'spot');
        const puanli = bolum === 'bilgiler' && (sec === 'onemli' || (!sec && p.onemli.length > 0));
        const secenek: Sira[] = bolum === 'kartlar' || bolum === 'quiz' || bolum === 'sorular' ? [] : ['varsayilan', 'az', 'za', ...(slaytli ? (['slayt', 'slayt-azalan'] as Sira[]) : []), ...(puanli ? (['puan'] as Sira[]) : [])];
        if (secenek.length < 2) return null;
        return (
          <label className="di15-sirala"><ArrowUpDown aria-hidden /><span>Sırala</span>
            <select value={secenek.includes(sira) ? sira : 'varsayilan'} onChange={(e) => setSira(e.target.value as Sira)} aria-label="Sıralama">
              {secenek.map((o) => <option key={o} value={o}>{SIRA_AD[o]}</option>)}
            </select>
          </label>
        );
      })()}

      {(bolum === 'tablolar' || bolum === 'listeler') && (() => {
        const kayit: string[] = bolum === 'tablolar' ? p.tablolar.map(tabloKategori) : p.listeler.map((l) => l.sira);
        const adlar: Record<string, string> = bolum === 'tablolar' ? TABLO_TUR_AD : { numara: 'Sayılı', alfa: 'Harfli', azalan: 'Büyükten küçüğe', madde: 'Sırasız' };
        const turler = Object.keys(adlar).filter((k) => kayit.includes(k));
        if (turler.length < 2) return null;
        return (
          <div className="v15-seg di15-alts di15-filtre" role="tablist" aria-label="Türe göre süz">
            <button type="button" role="tab" aria-selected={!tur} onClick={() => setTur('')}>Tümü<small>{kayit.length}</small></button>
            {turler.map((k) => <button key={k} type="button" role="tab" aria-selected={tur === k} onClick={() => setTur(tur === k ? '' : k)}>{adlar[k]}<small>{kayit.filter((x) => x === k).length}</small></button>)}
          </div>
        );
      })()}

      {bolum === 'terimler' && (() => {
        const sec = altSec(p.terimler.length ? 'terim' : 'kisa');
        return (
          <>
            <AltSekme l={[['terim', 'Terimler', p.terimler.length], ['kisa', 'Kısaltmalar', p.kisaltmalar.length]]} />
            {sec === 'terim' ? (
              <ul className="di15-izgara di15-anim" role="list">
                {sirala(p.terimler.filter((x) => ok(x.t, x.a, ...x.e)), sira, (x) => x.t, (x) => x.s).map((x, i) => (
                  <li key={x.t} className="v15-card di15-terim" style={{ '--i': i } as React.CSSProperties}>
                    <div className="di15-terim-u"><span className="di15-harf" aria-hidden>{x.t.charAt(0)}</span><b>{x.t}</b></div>
                    {x.e.length > 0 && <div className="di15-cipler">{x.e.map((e) => <span key={e}>{e}</span>)}</div>}
                    <p>{x.a}</p>
                    {x.s && <small className="di15-slayt">Slayt s.{x.s}</small>}
                  </li>
                ))}
              </ul>
            ) : (
              <ul className="di15-kisa di15-anim" role="list">
                {sirala(p.kisaltmalar.filter((x) => ok(x.k, x.acilim)), sira, (x) => x.k).map((x, i) => (
                  <li key={x.k} className="v15-card" style={{ '--i': i } as React.CSSProperties}><span className="di15-kisa-k">{x.k}</span><span>{x.acilim}</span></li>
                ))}
              </ul>
            )}
          </>
        );
      })()}

      {bolum === 'hastaliklar' && (
        <div className="di15-yigin di15-anim">
          {sirala(p.hastaliklar.filter((h) => ok(h.ad, h.latin, ...h.bolumler.flatMap((b) => b.m.map((x) => x.m)))), sira, (h) => h.ad, (h) => h.s).map((h, i) => <HastalikKart key={h.id} h={h} i={i} acik={i === 0} />)}
        </div>
      )}

      {bolum === 'bilgiler' && (() => {
        const sec = altSec(p.onemli.length ? 'onemli' : p.spotlar.length ? 'spot' : 'slayt');
        return (
          <>
            <AltSekme l={[['onemli', 'Önemli noktalar', p.onemli.length], ['spot', 'Sınav spotları', p.spotlar.length], ['slayt', 'Slayttan', p.bilgiler.length]]} />
            {sec === 'onemli' && (
              <div className="di15-yigin di15-anim">
                {sirala(p.onemli.filter((x) => ok(x.b, x.m, ...x.alt)), sira, (x) => x.b, (x) => x.s, (x) => x.p).map((x, i) => (
                  <article key={i} className="v15-card di15-onem" style={{ '--i': i } as React.CSSProperties}>
                    <header>
                      <span className={`di15-puan ${puanTon(x.p)}`} title="Sınav önemi (100 üzerinden)"><b>{x.p}</b><small>puan</small></span>
                      <h3>{x.b}</h3>
                    </header>
                    <p className="di15-ozet"><Zengin t={x.m} /></p>
                    {x.alt.length > 0 && <ul className="di15-maddeler">{x.alt.map((a, j) => <Madde key={j} t={a} />)}</ul>}
                    {x.n && <p className="di15-neden"><Sparkles aria-hidden /><span>{x.n}</span></p>}
                    {x.s?.length > 0 && <small className="di15-slayt">Slayt s.{x.s.join(', ')}</small>}
                  </article>
                ))}
              </div>
            )}
            {sec === 'spot' && (
              <ul className="di15-yigin di15-anim" role="list">
                {p.spotlar.filter((x) => ok(x.m)).map((x, i) => (
                  <li key={i} className="v15-card di15-spot" style={{ '--i': i } as React.CSSProperties}>
                    <Pin aria-hidden />
                    <div><p><Zengin t={x.m.replace(/^📌\s*\[SINAV SPOTU\]\s*/, '')} /></p><small>{x.bolum} · adım {x.n}</small></div>
                  </li>
                ))}
              </ul>
            )}
            {sec === 'slayt' && (
              <ul className="di15-izgara di15-anim" role="list">
                {sirala(p.bilgiler.filter((x) => ok(x.b, x.m)), sira, (x) => x.b, (x) => x.s).map((x, i) => (
                  <li key={i} className="v15-card di15-bilgi" style={{ '--i': i } as React.CSSProperties}><b>{x.b}</b><p><Zengin t={x.m} /></p>{x.s && <small className="di15-slayt">Slayt s.{x.s}</small>}</li>
                ))}
              </ul>
            )}
          </>
        );
      })()}

      {bolum === 'listeler' && (
        <div className="di15-yigin">
          {sirala(p.listeler.filter((l) => (!tur || l.sira === tur) && ok(l.t, ...l.m.map((x) => x.m))), sira, (l) => l.t, (l) => l.n).map((l, i) => (
            <section key={i} className="v15-card di15-tb is-sira">
              <header className="di15-tb-u">
                <span className="di15-tb-ik" aria-hidden><ListOrdered /></span>
                <div><h3>{l.t}</h3><small>{{ numara: 'Sıralı (1, 2, 3)', alfa: 'Sıralı (a, b, c)', azalan: 'Büyükten küçüğe', madde: 'Sırasız liste' }[l.sira]} · adım {l.n}</small></div>
              </header>
              {React.createElement(l.sira === 'madde' ? 'ul' : 'ol', { className: `di15-maddeler${l.sira === 'madde' ? '' : ' di15-num is-' + l.sira}`, type: l.sira === 'alfa' ? 'a' : undefined },
                l.m.map((x, j) => <Madde key={j} t={x.m} />))}
              {l.a && <p className="di15-ac is-d">{l.a}</p>}
            </section>
          ))}
        </div>
      )}

      {bolum === 'quiz' && (
        <div className="di15-yigin">
          {p.quiz.filter((x) => ok(x.q, ...x.o.map((o) => o.t))).map((x, i) => (
            <Soru key={i} no={i + 1} s={{ id: `q${i}`, kazanim: 0, zorluk: '', soru: x.q, secenekler: Object.fromEntries(x.o.map((o) => [o.k, o.t])), dogru: x.o.find((o) => o.d)?.k || '', aciklama: x.o.find((o) => o.d)?.a || '' }} />
          ))}
        </div>
      )}

      {bolum === 'tablolar' && (
        <div className="di15-yigin">
          {sirala(p.tablolar.filter((t) => (!tur || tabloKategori(t) === tur) && ok(t.t, ...t.r.flat())), sira, (t) => t.t, (t) => t.n).map((t, i) => <TabloKart key={i} t={t} />)}
        </div>
      )}

      {bolum === 'sorular' && kaz.map((k) => {
        const l = k.sorular.filter((s) => ok(s.soru, ...Object.values(s.secenekler)));
        return l.length > 0 && (
          <section key={k.no} className="di15-kaz">
            <h2 className="di15-kaz-h"><span>K{k.no}</span>{k.metin}</h2>
            <div className="di15-yigin">{l.map((s, j) => <Soru key={s.id} s={s} no={j + 1} />)}</div>
          </section>
        );
      })}

      {bolum === 'kartlar' && (
        <ul className="di15-kartlar" role="list">
          {p.kartlar.filter((x) => ok(x.o, x.a)).map((x, i) => <CevirKart key={i} o={x.o} a={x.a} c={x.c} />)}
        </ul>
      )}
    </div>
  );
}

function HastalikKart({ h, i, acik }: { h: DiPaket['hastaliklar'][number]; i: number; acik: boolean }) {
  const [ac, setAc] = useState(acik);
  return (
    <article className={`v15-card di15-hast${ac ? ' is-acik' : ''}`} style={{ '--i': i } as React.CSSProperties}>
      <button type="button" className="di15-hast-u" onClick={() => setAc(!ac)} aria-expanded={ac}>
        <span className="di15-harf is-b" aria-hidden>{h.ad.charAt(0)}</span>
        <span className="di15-hast-t"><b>{h.ad}</b>{h.latin && <em>{h.latin}</em>}<small>{h.kat.split('/').map((x) => x.trim()).join(' › ')}</small></span>
        <ChevronDown className="di15-ok" aria-hidden />
      </button>
      {ac && (
        <div className="di15-hast-g">
          {h.bolumler.map((b) => {
            const [, ton, Ik] = bolumTon(b.b);
            return (
              <section key={b.b} className={`di15-bol is-${ton}`}>
                <h4><Ik aria-hidden />{b.b}</h4>
                <ul className="di15-maddeler">{b.m.map((m, j) => <Madde key={j} t={m.m} />)}</ul>
              </section>
            );
          })}
          {h.s.length > 0 && <small className="di15-slayt">Slayt s.{h.s.join(', ')}</small>}
        </div>
      )}
    </article>
  );
}

function TabloKart({ t }: { t: DiTablo }) {
  const tur = tabloTuru(t);
  return (
    <section className={`v15-card di15-tb is-${tur}${t.k ? ' is-kars' : ''}`}>
      <header className="di15-tb-u">
        <span className="di15-tb-ik" aria-hidden>{t.k ? <Scale aria-label="Karşılaştırma" /> : tur === 'sira' ? <ListChecks /> : tur === 'eslesme' ? <Layers /> : <Table2 />}</span>
        <div><h3>{t.t}</h3><small>{t.k ? 'Karşılaştırma' : tur === 'sira' ? 'Sıralama' : tur === 'eslesme' ? 'Eşleştirme' : 'Tablo'} · adım {t.n}</small></div>
      </header>
      {tur === 'sira' && (
        <ol className="di15-adim di15-anim">
          {t.r.map((r, j) => (
            <li key={j} style={{ '--i': j } as React.CSSProperties}>
              <span className="di15-adim-n">{r[0]}</span>
              <div><b>{r[1]}</b>{r.slice(2).map((c, k) => <small key={k}><em>{t.h[k + 2]}:</em> {c}</small>)}</div>
            </li>
          ))}
        </ol>
      )}
      {tur === 'eslesme' && (
        <>
          <div className="di15-es-bas" aria-hidden><span>{t.h[0]}</span><ArrowRight /><span>{t.h[1]}</span></div>
          <ul className="di15-es di15-anim" role="list">
            {t.r.map((r, j) => (
              <li key={j} style={{ '--i': j } as React.CSSProperties}>
                <span className={`di15-es-a${r[0].length <= 8 ? ' is-kisa' : ''}`}>{r[0]}</span>
                <ArrowRight className="di15-es-ok" aria-hidden />
                <span className="di15-es-b"><Hucre v={r[1]} /></span>
              </li>
            ))}
          </ul>
        </>
      )}
      {tur === 'matris' && (
        <>
          <div className="di15-mat-kap">
            <table className="di15-mat">
              <thead><tr>{t.h.map((h, k) => <th key={h} className={k ? `is-r${k % 5}` : ''}>{h}</th>)}</tr></thead>
              <tbody className="di15-anim">{t.r.map((r, j) => (
                <tr key={j} style={{ '--i': j } as React.CSSProperties}>{r.map((c, k) => (k === 0 ? <th key={k} scope="row">{c}</th> : <td key={k} className={t.k && k === 1 && t.h.length >= 3 ? `is-taraf is-t${t.r.map((x) => x[1]).filter((v, i2, l) => l.indexOf(v) === i2).indexOf(r[1]) % 4}` : undefined}><Hucre v={c} /></td>))}</tr>
              ))}</tbody>
            </table>
          </div>
          {!t.k && (
          <ul className="di15-mat-kart di15-anim" role="list">
            {t.r.map((r, j) => (
              <li key={j} style={{ '--i': j } as React.CSSProperties}>
                <b>{r[0]}</b>
                {t.k && t.h.length >= 3 ? (
                  <div className="di15-kars">
                    <span className={`di15-kars-ch is-r${(1 + t.r.map((x) => x[1]).filter((v, a, l) => l.indexOf(v) === a).indexOf(r[1])) % 5}`}>{r[1]}</span>
                    {r.slice(2).map((c, k) => <p key={k}>{c}</p>)}
                  </div>
                ) : (
                <dl>{r.slice(1).map((c, k) => <div key={k} className={`is-r${(k + 1) % 5}`}><dt>{t.h[k + 1]}</dt><dd><Hucre v={c} /></dd></div>)}</dl>
                )}
              </li>
            ))}
          </ul>
          )}
        </>
      )}
    </section>
  );
}

function CevirKart({ o, a, c }: { o: string; a: string; c: string }) {
  const [ac, setAc] = useState(false);
  return (
    <li>
      <button type="button" className={`di15-cevir${ac ? ' is-ac' : ''}`} onClick={() => setAc(!ac)} aria-pressed={ac} aria-label={ac ? `Cevap: ${a}` : `Soru: ${o}. Cevabı görmek için dokun`}>
        <span className="di15-cevir-y is-on"><small>{c}</small><b>{o}</b><em><RotateCw aria-hidden /> Cevabı gör</em></span>
        <span className="di15-cevir-y is-arka"><small>Cevap</small><b>{a}</b><em><RotateCw aria-hidden /> Soruya dön</em></span>
      </button>
    </li>
  );
}

function Soru({ s, no }: { s: DiSoru; no: number }) {
  const [sec, setSec] = useState<string | null>(null);
  return (
    <article className="v15-card di15-soru">
      <header><span className="di15-soru-n">{no}</span><span className={`di15-zor is-${norm(s.zorluk || '')}`}>{s.zorluk}</span></header>
      <p className="di15-soru-k">{s.soru}</p>
      <div className="di15-sik">
        {Object.entries(s.secenekler).map(([k, v]) => (
          <button key={k} type="button" disabled={!!sec} onClick={() => setSec(k)} className={sec ? (k === s.dogru ? 'is-d' : k === sec ? 'is-y' : 'is-s') : ''}>
            <span className="di15-sik-h">{k}</span><span>{v}</span>{sec && k === s.dogru && <Check aria-hidden />}{sec === k && k !== s.dogru && <X aria-hidden />}
          </button>
        ))}
      </div>
      {sec && <p className={`di15-ac ${sec === s.dogru ? 'is-d' : 'is-y'}`}><b>{sec === s.dogru ? 'Doğru.' : `Doğru cevap ${s.dogru}.`}</b> {s.aciklama}</p>}
      {!sec && <p className="di15-ipucu"><CircleHelp aria-hidden /> Bir şık seç; açıklama altta açılır.</p>}
    </article>
  );
}

