import React, { useEffect, useMemo, useState } from 'react';
import { Search } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { DI_BOLUMLER, dersIcerikGetir, dersSorulariGetir, type DiBolum, type DiPaket, type DiSoru } from './dersIcerik';
import '../../styles/v15/dersIcerik.css';

/** Ders içerik sayfaları: /dersler/ders/kurulN/<key>?b=terimler|hastaliklar|bilgiler|tablolar|sorular|kartlar */
const norm = (s: string) => s.toLocaleLowerCase('tr');

export default function DersIcerikV15({ dersKey, bolum }: { dersKey: string; bolum: DiBolum }) {
  const [p, setP] = useState<DiPaket | null>(null);
  const [kaz, setKaz] = useState<{ no: number; metin: string; sorular: DiSoru[] }[]>([]);
  const [ara, setAra] = useState('');
  useEffect(() => {
    dersIcerikGetir(dersKey).then(setP);
    dersSorulariGetir(dersKey).then(setKaz);
  }, [dersKey]);
  useEffect(() => setAra(''), [bolum]);
  const q = norm(ara.trim());
  const ok = (...s: (string | undefined)[]) => !q || s.some((x) => x && norm(x).includes(q));
  const sorular = useMemo(() => kaz.flatMap((k) => k.sorular), [kaz]);
  if (!p) return <p className="di15-bos v15-card">Yükleniyor…</p>;

  const sayi: Record<DiBolum, number> = { terimler: p.terimler.length + p.kisaltmalar.length, hastaliklar: p.hastaliklar.length, bilgiler: p.onemli.length + p.bilgiler.length + p.spotlar.length, tablolar: p.tablolar.length, sorular: sorular.length, kartlar: p.kartlar.length };
  const url = (b: DiBolum) => `${pathFor('ders_detay', dersKey)}?b=${b}`;

  return (
    <div className="di15">
      <nav className="di15-tabs" aria-label="Ders içerikleri">
        {DI_BOLUMLER.filter((b) => sayi[b.id]).map((b) => (
          <a key={b.id} href={url(b.id)} className={b.id === bolum ? 'is-on' : ''} aria-current={b.id === bolum ? 'page' : undefined} onClick={linkClick(() => navigateTo(url(b.id)))}>
            {b.ad} <span>{sayi[b.id]}</span>
          </a>
        ))}
      </nav>
      <label className="di15-ara v15-card"><Search aria-hidden /><input value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Bu sayfada ara" /></label>

      {bolum === 'terimler' && (
        <>
          <ul className="di15-list v15-card" role="list">
            {p.terimler.filter((x) => ok(x.t, x.a, ...x.e)).map((x) => (
              <li key={x.t}><b>{x.t}</b>{x.e.length > 0 && <em> · {x.e.join(', ')}</em>}<p>{x.a}</p>{x.s && <small>Slayt s.{x.s}</small>}</li>
            ))}
          </ul>
          {p.kisaltmalar.length > 0 && (
            <>
              <h2 className="v15-h2">Kısaltmalar</h2>
              <ul className="di15-list v15-card" role="list">
                {p.kisaltmalar.filter((x) => ok(x.k, x.acilim)).map((x) => <li key={x.k}><b>{x.k}</b><p>{x.acilim}</p></li>)}
              </ul>
            </>
          )}
        </>
      )}

      {bolum === 'hastaliklar' && p.hastaliklar.filter((h) => ok(h.ad, h.latin, ...h.bolumler.flatMap((b) => b.m))).map((h) => (
        <details key={h.id} className="di15-kart v15-card">
          <summary><b>{h.ad}</b>{h.latin && <em> · {h.latin}</em>}<small>{h.kat}</small></summary>
          {h.bolumler.map((b) => (
            <section key={b.b}><h3>{b.b}</h3><ul>{b.m.map((m, i) => <li key={i}>{m}</li>)}</ul></section>
          ))}
          {h.s.length > 0 && <small>Slayt s.{h.s.join(', ')}</small>}
        </details>
      ))}

      {bolum === 'bilgiler' && (
        <>
          <h2 className="v15-h2">Önemli noktalar</h2>
          <ul className="di15-list v15-card" role="list">
            {p.onemli.filter((x) => ok(x.b, x.m, ...x.alt)).map((x, i) => (
              <li key={i}><b>{x.b}</b> <span className={`di15-puan p${Math.min(9, Math.floor(x.p / 10))}`}>{x.p}</span>
                <p>{x.m.replace(/\*\*/g, '')}</p>
                {x.alt.length > 0 && <ul>{x.alt.map((a, j) => <li key={j}>{a}</li>)}</ul>}
                {x.n && <small>{x.n}</small>}</li>
            ))}
          </ul>
          <h2 className="v15-h2">Sınav spotları</h2>
          <ul className="di15-list v15-card" role="list">
            {p.spotlar.filter((x) => ok(x.m)).map((x, i) => <li key={i}><p>{x.m.replace(/^📌\s*\[SINAV SPOTU\]\s*/, '')}</p><small>{x.bolum} · adım {x.n}</small></li>)}
          </ul>
          <h2 className="v15-h2">Slayttan çıkan bilgiler</h2>
          <ul className="di15-list v15-card" role="list">
            {p.bilgiler.filter((x) => ok(x.b, x.m)).map((x, i) => <li key={i}><b>{x.b}</b><p>{x.m}</p>{x.s && <small>Slayt s.{x.s}</small>}</li>)}
          </ul>
        </>
      )}

      {bolum === 'tablolar' && p.tablolar.filter((t) => ok(t.t, ...t.r.flat())).map((t, i) => (
        <section key={i} className="di15-tablo v15-card">
          <h3>{t.t}</h3>
          <div className="di15-kay"><table><thead><tr>{t.h.map((h) => <th key={h}>{h}</th>)}</tr></thead>
            <tbody>{t.r.map((r, j) => <tr key={j}>{r.map((c, k) => <td key={k}>{c}</td>)}</tr>)}</tbody></table></div>
          <small>{t.k ? 'Karşılaştırma' : 'Tablo'} · adım {t.n}</small>
        </section>
      ))}

      {bolum === 'sorular' && kaz.map((k) => {
        const l = k.sorular.filter((s) => ok(s.soru, ...Object.values(s.secenekler)));
        return l.length > 0 && (
          <section key={k.no}>
            <h2 className="v15-h2">{k.metin}</h2>
            {l.map((s) => <Soru key={s.id} s={s} />)}
          </section>
        );
      })}

      {bolum === 'kartlar' && <ul className="di15-list v15-card" role="list">
        {p.kartlar.filter((x) => ok(x.o, x.a)).map((x, i) => <KartSatiri key={i} o={x.o} a={x.a} c={x.c} />)}
      </ul>}
    </div>
  );
}

function KartSatiri({ o, a, c }: { o: string; a: string; c: string }) {
  const [ac, setAc] = useState(false);
  return <li><button className="di15-kb" onClick={() => setAc(!ac)} aria-expanded={ac}><b>{o}</b><small>{c}</small></button>{ac && <p>{a}</p>}</li>;
}

function Soru({ s }: { s: DiSoru }) {
  const [sec, setSec] = useState<string | null>(null);
  return (
    <div className="di15-soru v15-card">
      <p><b>{s.soru}</b></p>
      {Object.entries(s.secenekler).map(([k, v]) => (
        <button key={k} disabled={!!sec} onClick={() => setSec(k)} className={sec ? (k === s.dogru ? 'is-d' : k === sec ? 'is-y' : '') : ''}>{k}) {v}</button>
      ))}
      {sec && <p className="di15-ac">{sec === s.dogru ? 'Doğru. ' : `Doğru cevap ${s.dogru}. `}{s.aciklama}</p>}
    </div>
  );
}
