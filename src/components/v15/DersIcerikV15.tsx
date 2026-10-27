import React, { useEffect, useMemo, useState } from 'react';
import {
  Activity, ArrowDown, ArrowRight, ArrowUp, Check, ChevronDown, CircleHelp, FlaskConical, Layers, ListChecks, Microscope,
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
const puanTon = (p: number) => (p >= 90 ? 'is-cok' : p >= 70 ? 'is-orta' : 'is-az');

export default function DersIcerikV15({ dersKey, bolum }: { dersKey: string; bolum: DiBolum }) {
  const [p, setP] = useState<DiPaket | null>(null);
  const [kaz, setKaz] = useState<{ no: number; metin: string; sorular: DiSoru[] }[]>([]);
  const [ara, setAra] = useState('');
  const [alt, setAlt] = useState<string>('');
  useEffect(() => {
    dersIcerikGetir(dersKey).then(setP);
    dersSorulariGetir(dersKey).then(setKaz);
  }, [dersKey]);
  useEffect(() => { setAra(''); setAlt(''); }, [bolum]);
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
      <nav className="di15-tabs" aria-label="Ders içerikleri">
        {DI_BOLUMLER.filter((b) => sayi[b.id]).map((b) => (
          <a key={b.id} href={url(b.id)} className={b.id === bolum ? 'is-on' : ''} aria-current={b.id === bolum ? 'page' : undefined} onClick={linkClick(() => navigateTo(url(b.id)))}>
            {b.ad} <span>{sayi[b.id]}</span>
          </a>
        ))}
      </nav>
      <label className="di15-ara"><Search aria-hidden /><input value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Bu sayfada ara" aria-label="Bu sayfada ara" /></label>

      {bolum === 'terimler' && (() => {
        const sec = altSec(p.terimler.length ? 'terim' : 'kisa');
        return (
          <>
            <AltSekme l={[['terim', 'Terimler', p.terimler.length], ['kisa', 'Kısaltmalar', p.kisaltmalar.length]]} />
            {sec === 'terim' ? (
              <ul className="di15-izgara di15-anim" role="list">
                {p.terimler.filter((x) => ok(x.t, x.a, ...x.e)).map((x, i) => (
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
                {p.kisaltmalar.filter((x) => ok(x.k, x.acilim)).map((x, i) => (
                  <li key={x.k} className="v15-card" style={{ '--i': i } as React.CSSProperties}><span className="di15-kisa-k">{x.k}</span><span>{x.acilim}</span></li>
                ))}
              </ul>
            )}
          </>
        );
      })()}

      {bolum === 'hastaliklar' && (
        <div className="di15-yigin di15-anim">
          {p.hastaliklar.filter((h) => ok(h.ad, h.latin, ...h.bolumler.flatMap((b) => b.m.map((x) => x.m)))).map((h, i) => <HastalikKart key={h.id} h={h} i={i} acik={i === 0} />)}
        </div>
      )}

      {bolum === 'bilgiler' && (() => {
        const sec = altSec(p.onemli.length ? 'onemli' : p.spotlar.length ? 'spot' : 'slayt');
        return (
          <>
            <AltSekme l={[['onemli', 'Önemli noktalar', p.onemli.length], ['spot', 'Sınav spotları', p.spotlar.length], ['slayt', 'Slayttan', p.bilgiler.length]]} />
            {sec === 'onemli' && (
              <div className="di15-yigin di15-anim">
                {p.onemli.filter((x) => ok(x.b, x.m, ...x.alt)).map((x, i) => (
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
                {p.bilgiler.filter((x) => ok(x.b, x.m)).map((x, i) => (
                  <li key={i} className="v15-card di15-bilgi" style={{ '--i': i } as React.CSSProperties}><b>{x.b}</b><p><Zengin t={x.m} /></p>{x.s && <small className="di15-slayt">Slayt s.{x.s}</small>}</li>
                ))}
              </ul>
            )}
          </>
        );
      })()}

      {bolum === 'listeler' && (
        <div className="di15-yigin">
          {p.listeler.filter((l) => ok(l.t, ...l.m.map((x) => x.m))).map((l, i) => (
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
          {p.tablolar.filter((t) => ok(t.t, ...t.r.flat())).map((t, i) => <TabloKart key={i} t={t} />)}
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
    <section className={`v15-card di15-tb is-${tur}`}>
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
                <tr key={j} style={{ '--i': j } as React.CSSProperties}>{r.map((c, k) => (k === 0 ? <th key={k} scope="row">{c}</th> : <td key={k}><Hucre v={c} /></td>))}</tr>
              ))}</tbody>
            </table>
          </div>
          {/* telefonda satır kartları */}
          <ul className="di15-mat-kart di15-anim" role="list">
            {t.r.map((r, j) => (
              <li key={j} style={{ '--i': j } as React.CSSProperties}>
                <b>{r[0]}</b>
                <dl>{r.slice(1).map((c, k) => <div key={k} className={`is-r${(k + 1) % 5}`}><dt>{t.h[k + 1]}</dt><dd><Hucre v={c} /></dd></div>)}</dl>
              </li>
            ))}
          </ul>
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

