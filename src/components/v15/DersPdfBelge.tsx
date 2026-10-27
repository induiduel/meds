/** Ders PDF belgesi (saf render, hook/CSS yok): slayt boyutunda (720×540 pt) sayfalar; her adım = anlatım + hemen ardından özet.
 *  Stil: src/styles/v15/dersPdf.css (.dpdf). Tarayıcıda DersPdfEkranV15, Node'da scripts/ders_pdf.mjs kullanır. */
import React from 'react';
import type { DiPaket } from './dersIcerik';
import type { PdfAdim, PdfAkis } from './dersPdfAkis';

const kalin = (t: string): React.ReactNode[] => t.split(/\*\*(.+?)\*\*/g).map((p, i) => (i % 2 ? <strong key={i}>{p}</strong> : p));

/** Etiket: açıklama (+ `;` ile 3+ parça → alt madde) — DersIcerikV15.Madde ile aynı kural. */
function Madde({ t }: { t: string }) {
  const m = t.match(/^([^:]{2,40}):\s+(.+)$/);
  const et = m?.[1], g = m ? m[2] : t;
  const alt = g.split(/;\s+/);
  return (
    <li>
      {et && <b className="dpdf-et">{et}</b>}
      {alt.length >= 3 ? <ul className="dpdf-alt">{alt.map((a, i) => <li key={i}>{kalin(a)}</li>)}</ul> : kalin(g)}
    </li>
  );
}

/** Slayt anlatımı (markdown alt kümesi): paragraf, "- " madde, "> [!IMPORTANT|NOTE]" kutusu. */
function Anlatim({ md }: { md: string }) {
  const bloklar = md.trim().split(/\n{2,}/);
  return (
    <div className="dpdf-anlatim">
      {bloklar.map((b, i) => {
        const sat = b.split('\n');
        if (sat[0].startsWith('> ')) {
          const tur = /\[!(\w+)\]/.exec(sat[0])?.[1] || 'NOTE';
          const govde = sat.map((x) => x.replace(/^>\s?/, '')).filter((x) => x && !/^\[!\w+\]$/.test(x)).join(' ');
          return <aside key={i} className={`dpdf-kutu is-${tur.toLowerCase()}`}><b>{tur === 'IMPORTANT' ? 'Sınav spotu' : 'Not'}</b><span>{kalin(govde)}</span></aside>;
        }
        if (sat.every((x) => x.startsWith('- '))) return <ul key={i} className="dpdf-maddeler">{sat.map((x, j) => <Madde key={j} t={x.slice(2)} />)}</ul>;
        return <p key={i}>{kalin(sat.join(' '))}</p>;
      })}
    </div>
  );
}

const TON: Record<string, string> = { Etiyoloji: 'w', Fizyopatoloji: 'ai', Patogenez: 'ai', Morfoloji: 'a', 'Klinik bulgular': 'b', 'Ayırt edici bulgu': 'ok', Tanı: 'a', Görüntüleme: 'a', Tedavi: 'ok' };

function Hastalik({ h }: { h: DiPaket['hastaliklar'][number] }) {
  return (
    <section className="dpdf-hast">
      <header><span className="dpdf-harf">{h.ad[0]}</span><div><b>{h.ad}</b>{h.latin && <em>{h.latin}</em>}</div></header>
      <div className="dpdf-hast-g">
        {h.bolumler.map((b) => (
          <div key={b.b} className={`dpdf-bol is-${TON[b.b] || 'c'}`}><h4>{b.b}</h4><ul className="dpdf-maddeler">{b.m.map((x, i) => <Madde key={i} t={x.m} />)}</ul></div>
        ))}
      </div>
    </section>
  );
}

function Tablo({ t }: { t: DiPaket['tablolar'][number] }) {
  return (
    <section className={`dpdf-tablo${t.k ? ' is-k' : ''}`}>
      <h4>{t.k ? '⚖ ' : ''}{t.t}</h4>
      <table>
        <thead><tr>{t.h.map((x, i) => <th key={i}>{x}</th>)}</tr></thead>
        <tbody>{t.r.map((r, i) => <tr key={i}>{r.map((c, j) => (j === 0 ? <th key={j} scope="row">{c}</th> : <td key={j}>{c}</td>))}</tr>)}</tbody>
      </table>
    </section>
  );
}

function Liste({ l }: { l: DiPaket['listeler'][number] }) {
  const Etiket = l.sira === 'madde' ? 'ul' : 'ol';
  return (
    <section className="dpdf-liste">
      <h4>{l.t}</h4>
      <Etiket type={l.sira === 'alfa' ? 'a' : undefined} className={l.sira === 'madde' ? 'dpdf-maddeler' : 'dpdf-sira'} reversed={l.sira === 'azalan' || undefined}>
        {l.m.map((x, i) => <Madde key={i} t={x.m} />)}
      </Etiket>
    </section>
  );
}

export function Ozet({ a }: { a: Omit<PdfAdim, 'slayt'> }) {
  const bas = (ad: string, n: number) => <h3 className="dpdf-bas">{ad}<small>{n}</small></h3>;
  return (
    <div className="dpdf-ozet">
      {a.terimler.length > 0 && <>{bas('Terimler', a.terimler.length)}<div className="dpdf-terimler">{a.terimler.map((t, i) => <div key={i} className="dpdf-terim"><b>{t.t}</b>{t.e.length > 0 && <small>{t.e.join(' · ')}</small>}<p>{t.a}</p></div>)}</div></>}
      {a.kisaltmalar.length > 0 && <>{bas('Kısaltmalar', a.kisaltmalar.length)}<div className="dpdf-kisa">{a.kisaltmalar.map((k, i) => <div key={i}><span>{k.k}</span>{k.acilim}</div>)}</div></>}
      {a.hastaliklar.length > 0 && <>{bas('Hastalıklar ve kavramlar', a.hastaliklar.length)}{a.hastaliklar.map((h) => <Hastalik key={h.id} h={h} />)}</>}
      {a.listeler.length > 0 && <>{bas('Sıralamalar', a.listeler.length)}{a.listeler.map((l, i) => <Liste key={i} l={l} />)}</>}
      {a.tablolar.length > 0 && <>{bas('Tablolar ve karşılaştırmalar', a.tablolar.length)}{a.tablolar.map((t, i) => <Tablo key={i} t={t} />)}</>}
      {(a.onemli.length > 0 || a.spotlar.length > 0 || a.bilgiler.length > 0) && (
        <>{bas('Sınav spotları', a.onemli.length + a.spotlar.length + a.bilgiler.length)}
          <ul className="dpdf-spot">
            {a.onemli.map((o, i) => <li key={`o${i}`} className="is-onem"><b>{o.b}</b> {kalin(o.m)}</li>)}
            {a.spotlar.map((s, i) => <li key={`s${i}`}>{kalin(s.m)}</li>)}
            {a.bilgiler.map((s, i) => <li key={`b${i}`}>{s.b && <b>{s.b}: </b>}{kalin(s.m)}</li>)}
          </ul></>
      )}
      {a.kartlar.length > 0 && <>{bas('Hatırlatma kartları', a.kartlar.length)}<div className="dpdf-kartlar">{a.kartlar.map((k, i) => <div key={i}><b>{k.o}</b><span>{k.a}</span></div>)}</div></>}
    </div>
  );
}
const ozetVar = (a: Omit<PdfAdim, 'slayt'>) => [a.terimler, a.kisaltmalar, a.hastaliklar, a.listeler, a.tablolar, a.bilgiler, a.onemli, a.spotlar, a.kartlar].some((x) => x.length);

export default function DersPdfBelge({ akis, kod }: { akis: PdfAkis; kod?: string }) {
  return (
    <div className="dpdf">
      <section className="dpdf-kapak">
        <small>{kod || 'Ders notu'}</small>
        <h1>{akis.baslik}</h1>
        <p>{akis.adimlar.length} adım · anlatım ve her adımın hemen ardından özeti</p>
      </section>
      {akis.adimlar.map(({ slayt, ...ozet }) => {
        const md = slayt.synthesisNarrative || slayt.content || '';
        return (
          <article key={slayt.slideNumber} className={`dpdf-adim${slayt.isCheckpoint ? ' is-tekrar' : ''}`} data-adim={slayt.slideNumber}>
            <header className="dpdf-ust">
              <span className="dpdf-no">{slayt.isCheckpoint ? 'Tekrar' : slayt.slideNumber}</span>
              <div><h2>{slayt.title.replace(/^\[TEKRAR SAYFASI - ([^\]]+)\]\s*/i, '$1 · ')}</h2>{slayt.subtitle && <p>{slayt.subtitle}</p>}</div>
            </header>
            <Anlatim md={md} />
            {ozetVar(ozet) && <><div className="dpdf-ayrac">Bu adımın özeti</div><Ozet a={ozet} /></>}
          </article>
        );
      })}
      {akis.ek && <article className="dpdf-adim"><header className="dpdf-ust"><span className="dpdf-no">Ek</span><div><h2>Ek özetler</h2><p>Belirli bir adıma bağlanamayan kayıtlar</p></div></header><Ozet a={akis.ek} /></article>}
      {akis.quiz.length > 0 && (
        <article className="dpdf-adim">
          <header className="dpdf-ust"><span className="dpdf-no">?</span><div><h2>Kendini sına</h2><p>Mini sorular, adım sırasıyla; doğru şık işaretli</p></div></header>
          <ol className="dpdf-quiz">
            {akis.quiz.map(({ adim, q }, i) => (
              <li key={i}><b>{q.q}</b><small>Adım {adim || '—'}</small>
                <ul>{q.o.map((o) => <li key={o.k} className={o.d ? 'is-dogru' : ''}><span>{o.k}</span>{o.t}{o.d && o.a ? <em>{o.a}</em> : null}</li>)}</ul>
              </li>
            ))}
          </ol>
        </article>
      )}
    </div>
  );
}
