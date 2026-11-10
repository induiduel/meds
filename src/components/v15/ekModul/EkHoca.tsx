import React, { useMemo, useState } from 'react';
import { Check, ChevronRight, Eye, RotateCcw, Shuffle, X } from 'lucide-react';
import type { EkModul, HocaSet, HocaSoru } from './ekVeri';

/**
 * Hocanın çalışma soruları (hoca_sorulari.json): boşluk doldurma (kart çevir + bildim/bilemedim), doğru–yanlış, çoktan seçmeli.
 * Metinler hocanın kendi yazımıyla durur; cevap anahtarı olmayan sette işaret MeDSor'undur ve ekranda bu söylenir.
 */
const kar = <T,>(a: T[]): T[] => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

export const HocaSetler: React.FC<{ m: EkModul; ac: (id: string) => void }> = ({ m, ac }) => (
  <ul className="ekm-hoca-setler" role="list">
    {(m.hoca?.setler || []).map((s) => (
      <li key={s.id}>
        <button type="button" className="v15-card" onClick={() => ac(s.id)}>
          <i>{s.sorular.length}</i>
          <span><b>{s.ad}</b><small>{s.aciklama}</small></span>
          <ChevronRight aria-hidden />
        </button>
      </li>
    ))}
  </ul>
);

export const HocaSetCoz: React.FC<{ set: HocaSet }> = ({ set }) => {
  const [karisik, setKarisik] = useState(false);
  const [tur, setTur] = useState(0);
  const sorular = useMemo(() => (karisik ? kar(set.sorular) : set.sorular), [set, karisik, tur]); // eslint-disable-line react-hooks/exhaustive-deps
  const [i, setI] = useState(0);
  const [yanit, setYanit] = useState<Record<number, string>>({});
  const [acik, setAcik] = useState(false);
  const q = sorular[i] as HocaSoru & Record<string, any>;
  const n = sorular.length;
  const dogruN = sorular.filter((s: any, k) => yanit[k] !== undefined && yanit[k] === (set.tur === 'bosluk' ? 'b' : String(s.dogru))).length;
  const cozulen = Object.keys(yanit).length;
  const bastan = (k = karisik) => { setKarisik(k); setTur((t) => t + 1); setI(0); setYanit({}); setAcik(false); };
  const ileri = () => { setAcik(false); setI((x) => Math.min(n - 1, x + 1)); };
  const isaretle = (v: string) => setYanit({ ...yanit, [i]: v });
  const y = yanit[i];
  const bitti = cozulen === n;
  // boşluk doldurma: boşluk sayısı cevaptaki virgüllü parça sayısına eşitse her boşluğa kendi parçası yazılır
  const parcalar = set.tur === 'bosluk' ? String(q.metin).split('____') : [];
  const bosN = parcalar.length - 1;
  const cevaplar = set.tur === 'bosluk' ? String(q.cevap).split(/\s*,\s*/) : [];
  const gor = acik || y !== undefined;
  const dolgu = (k: number) => (bosN === 1 ? q.cevap : cevaplar.length === bosN ? cevaplar[k] : '…');

  return (
    <div className="ekm ekm-soru ekm-hoca">
      <div className="ekm-soru-ust">
        <span><b>{i + 1}</b> / {n}</span>
        <div className="ekm-ilerle" aria-hidden><i style={{ width: `${(cozulen / n) * 100}%` }} /></div>
        <span className="ekm-zorluk">{dogruN} doğru</span>
        <button type="button" className={`ekm-kucuk is-oto${karisik ? ' is-on' : ''}`} onClick={() => bastan(!karisik)} aria-pressed={karisik}><Shuffle aria-hidden /> Karışık</button>
      </div>
      {set.anahtarsiz && <p className="ekm-not">Hocanın bu bölümde cevap anahtarı yok; doğru cevaplar hocanın diğer sorularındaki bilgilere göre işaretlendi.</p>}

      <article className="ekm-soru-kart v15-card">
        {set.tur === 'bosluk' && (
          <>
            <p className="ekm-kok ekm-bosluk">{parcalar.map((p, k) => (
              <React.Fragment key={k}>{p}{k < bosN && <span className={gor ? 'is-acik' : ''}>{gor ? dolgu(k) : '?'}</span>}</React.Fragment>
            ))}</p>
            {!acik && !y ? (
              <button type="button" className="v15-btn ekm-goster" onClick={() => setAcik(true)}><Eye aria-hidden /> Cevabı göster</button>
            ) : (
              <>
                <p className="ekm-cozum">Cevap: <b>{q.cevap}</b></p>
                {!y && (
                  <div className="ekm-dy-dugme is-buyuk">
                    <button type="button" onClick={() => { isaretle('b'); }}><Check aria-hidden /> Bildim</button>
                    <button type="button" onClick={() => { isaretle('x'); }}><X aria-hidden /> Bilemedim</button>
                  </div>
                )}
              </>
            )}
          </>
        )}
        {set.tur === 'dy' && (
          <>
            <p className="ekm-kok">{q.metin}</p>
            {y === undefined ? (
              <div className="ekm-dy-dugme is-buyuk">
                <button type="button" onClick={() => isaretle('true')}><Check aria-hidden /> Doğru</button>
                <button type="button" onClick={() => isaretle('false')}><X aria-hidden /> Yanlış</button>
              </div>
            ) : (
              <div className={`ekm-sonuc ${y === String(q.dogru) ? 'is-ok' : 'is-bad'}`}>
                <p><b>{y === String(q.dogru) ? 'Bildin.' : 'Bilemedin.'}</b> Hocanın cevabı: <b>{q.dogru ? 'Doğru' : 'Yanlış'}</b></p>
              </div>
            )}
          </>
        )}
        {set.tur === 'cs' && (
          <>
            <p className="ekm-kok">{q.kok}</p>
            <ul className="ekm-secenekler" role="list">
              {Object.keys(q.secenekler).map((h) => {
                const d = y !== undefined ? (h === q.dogru ? ' is-ok' : h === y ? ' is-bad' : ' is-sonuk') : '';
                return (
                  <li key={h}>
                    <button type="button" className={`ekm-secenek${d}`} disabled={y !== undefined} onClick={() => isaretle(h)}>
                      <i>{y !== undefined && h === q.dogru ? <Check aria-hidden /> : y !== undefined && h === y ? <X aria-hidden /> : h}</i><span>{q.secenekler[h]}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
            {y !== undefined && q.belirsiz && <p className="ekm-not">Bu sorunun cevabı tartışmaya açık; hocaya sormakta yarar var.</p>}
          </>
        )}
      </article>

      <nav className="ekm-soru-alt">
        <button type="button" className="v15-btn is-ghost" onClick={() => { setAcik(false); setI(Math.max(0, i - 1)); }} disabled={i === 0}>Önceki</button>
        {i < n - 1
          ? <button type="button" className="v15-btn" onClick={ileri}>Sonraki <ChevronRight aria-hidden /></button>
          : <button type="button" className="v15-btn" onClick={() => bastan()}><RotateCcw aria-hidden /> Baştan</button>}
      </nav>
      {bitti && <p className="ekm-puan v15-card"><b>{dogruN} / {n}</b><span>Set tamamlandı. Bilemediklerin için ilgili konunun dersine dön.</span></p>}
    </div>
  );
};
