import React, { useEffect, useMemo, useState } from 'react';
import { Check, ChevronRight, Eye, FileText, LayoutList, RotateCcw, Shuffle, X } from 'lucide-react';
import { hocaPdfKlip, type EkModul, type HocaSet, type HocaSoru } from './ekVeri';
import { useSira } from './ekOrtak';
import { EkSesliOynatici } from './EkSesliOynatici';
import { EkPdfHoca } from './EkPdfHoca';

const KIP_KEY = 'medsoru_ek_modul_hoca_kip';

/**
 * Hocanın çalışma soruları (hoca_sorulari.json): boşluk doldurma (kart çevir + bildim/bilemedim), doğru–yanlış, çoktan seçmeli.
 * Metinler hocanın kendi yazımıyla durur; cevap anahtarı olmayan sette işaret MeDSor'undur ve ekranda bu söylenir.
 */
const kar = <T,>(a: T[]): T[] => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

/** Bütün setler tek sayfada (sesli çözüm dahil): her soru kendi türünü ve asıl kimliğini taşır */
export const TUMU = 'tumu';
export const tumSet = (m: EkModul): HocaSet => ({
  id: TUMU, ad: 'Tüm sorular', tur: 'cs', aciklama: '',
  sorular: (m.hoca?.setler || []).flatMap((s) => s.sorular.map((q) => ({ ...q, tur: s.tur, k: `${s.id}-${q.no}` }))) as HocaSoru[],
});

export const HocaSetler: React.FC<{ m: EkModul; ac: (id: string) => void }> = ({ m, ac }) => (
  <ul className="ekm-hoca-setler" role="list">
    <li>
      <button type="button" className="v15-card" onClick={() => ac(TUMU)}>
        <i>{(m.hoca?.setler || []).reduce((t, s) => t + s.sorular.length, 0)}</i>
        <span><b>Tüm sorular tek sayfada</b><small>Bütün setler sırayla; sesli çözümle baştan sona dinleyebilirsin</small></span>
        <ChevronRight aria-hidden />
      </button>
    </li>
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

const BOS = { klip: {}, ozet: { id: '', ad: '' } } as unknown as EkModul;

/** Sesli çözüm: her soru iki klip — h-<set>-<no> (soru okunur) + hc-<set>-<no> (cevap ve açıklama); sıra = [h1, hc1, h2, hc2 …].
 *  Ortak ses öğesi (ekOrtak) sayesinde hız ayarı, kilit ekranı ve arka planda çalma ders oynatıcısıyla aynıdır. */
export const HocaSetCoz: React.FC<{ set: HocaSet; m?: EkModul }> = ({ set, m }) => {
  const [karisik, setKarisik] = useState(false);
  const [tur, setTur] = useState(0);
  const sorular = useMemo(() => (karisik ? kar(set.sorular) : set.sorular), [set, karisik, tur]); // eslint-disable-line react-hooks/exhaustive-deps
  const [i, setI] = useState(0);
  const [yanit, setYanit] = useState<Record<number, string>>({});
  const [acik, setAcik] = useState(false);
  const q = sorular[i] as HocaSoru & Record<string, any>;
  const n = sorular.length;
  const dogruN = sorular.filter((s: any, k) => yanit[k] !== undefined && yanit[k] === ((s.tur || set.tur) === 'bosluk' ? 'b' : String(s.dogru))).length;
  const cozulen = Object.keys(yanit).length;
  const bastan = (k = karisik) => { sira.durdur(); setKarisik(k); setTur((t) => t + 1); setI(0); setYanit({}); setAcik(false); };
  const ileri = () => { setAcik(false); setI((x) => Math.min(n - 1, x + 1)); };
  const isaretle = (v: string) => setYanit({ ...yanit, [i]: v });
  const y = yanit[i];
  const bitti = cozulen === n;
  // boşluk doldurma: boşluk sayısı cevaptaki virgüllü parça sayısına eşitse her boşluğa kendi parçası yazılır
  const qt = (q.tur || set.tur) as HocaSet['tur']; // tüm sorular sayfasında tür soruya göre
  const parcalar = qt === 'bosluk' ? String(q.metin).split('____') : [];
  const bosN = parcalar.length - 1;
  const cevaplar = qt === 'bosluk' ? String(q.cevap).split(/\s*,\s*/) : [];
  const gor = acik || y !== undefined;
  const dolgu = (k: number) => (bosN === 1 ? q.cevap : cevaplar.length === bosN ? cevaplar[k] : '…');
  const kim = (s: HocaSoru) => s.k || `${set.id}-${s.no}`;
  const klipler = useMemo(() => sorular.flatMap((s) => [`h-${kim(s)}`, `hc-${kim(s)}`]), [sorular]); // eslint-disable-line react-hooks/exhaustive-deps
  const sira = useSira(m || BOS, klipler, undefined, (k) => `${set.ad} · Soru ${Math.floor(k / 2) + 1}`);
  // çalan klip soruyu sürükler: soru okunurken soru açılır, çözüm klibinde cevap gösterilir
  useEffect(() => {
    if (sira.i < 0) return;
    setI(Math.floor(sira.i / 2));
    setAcik(sira.i % 2 === 1);
  }, [sira.i]);
  const git = (x: number) => { setAcik(false); setI(x); if (sira.i >= 0) sira.cal(x * 2); };
  const cozumGor = gor || (qt !== 'bosluk' && y !== undefined);
  // "PDF ile": çözümlü kitapçık sesle eş zamanlı (sesli dersteki gibi), yanında etkileşimli soru kartı
  const pdfVar = useMemo(() => !!m && klipler.some((k) => hocaPdfKlip(m, k)), [m, klipler]);
  const [kipSec, setKipSec] = useState<'pdf' | 'kart'>(() => { try { return localStorage.getItem(KIP_KEY) === 'kart' ? 'kart' : 'pdf'; } catch { return 'pdf'; } });
  const kip = pdfVar ? kipSec : 'kart';
  const kipDegis = (k: 'pdf' | 'kart') => { setKipSec(k); try { localStorage.setItem(KIP_KEY, k); } catch { /* yok */ } };

  return (
    <div className={`ekm ekm-soru ekm-hoca${kip === 'pdf' ? ' ekm-pdfkip' : ''}`}>
      <div className="ekm-soru-ust">
        <span><b>{i + 1}</b> / {n}</span>
        <div className="ekm-ilerle" aria-hidden><i style={{ width: `${(cozulen / n) * 100}%` }} /></div>
        <span className="ekm-zorluk">{dogruN} doğru</span>
        <button type="button" className={`ekm-kucuk is-oto${karisik ? ' is-on' : ''}`} onClick={() => bastan(!karisik)} aria-pressed={karisik}><Shuffle aria-hidden /> Karışık</button>
      </div>
      {m && <EkSesliOynatici m={m} sira={sira} klipler={klipler} grup={2} birim="Soru" ad={(p, k) => `Soru ${p + 1} · ${k % 2 ? 'çözüm' : 'soru okunuyor'}`} />}
      {pdfVar && (
        <div className="ekm-kip" role="group" aria-label="Çözüm görünümü">
          <button type="button" className={kip === 'pdf' ? 'is-on' : ''} aria-pressed={kip === 'pdf'} onClick={() => kipDegis('pdf')}><FileText aria-hidden /> PDF ile</button>
          <button type="button" className={kip === 'kart' ? 'is-on' : ''} aria-pressed={kip === 'kart'} onClick={() => kipDegis('kart')}><LayoutList aria-hidden /> Yalnız soru</button>
        </div>
      )}
      {set.anahtarsiz && <p className="ekm-not">Hocanın bu bölümde cevap anahtarı yok; doğru cevaplar hocanın diğer sorularındaki bilgilere göre işaretlendi.</p>}

      <div className={kip === 'pdf' ? 'ekm-pdf-bolme ekm-hoca-bolme' : 'ekm-hoca-tek'}>
      {kip === 'pdf' && m && <EkPdfHoca m={m} klipler={klipler} soru={i} sira={sira} />}
      <div className="ekm-hoca-yan">
      <article className="ekm-soru-kart v15-card">
        {qt === 'bosluk' && (
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
        {qt === 'dy' && (
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
        {qt === 'cs' && (
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
            {acik && y === undefined && <p className="ekm-cozum">Doğru cevap: <b>{q.dogru}) {q.secenekler[q.dogru]}</b></p>}
          </>
        )}
        {qt === 'dy' && acik && y === undefined && <p className="ekm-cozum">Hocanın cevabı: <b>{q.dogru ? 'Doğru' : 'Yanlış'}</b></p>}
        {q.cozum && cozumGor && <p className="ekm-cozum ekm-hoca-cozum">{q.cozum}</p>}
        {q.hata && cozumGor && (
          <div className="ekm-hata" role="note">
            <p><b>Bu soruda hata var.</b> {q.hata.hata}</p>
            <p><b>Doğrusu:</b> {q.hata.dogrusu}</p>
            <p><b>Neden hatalı:</b> {q.hata.neden}</p>
            <p><b>Neden yine de böyle yazıldı:</b> {q.hata.yazilma}</p>
          </div>
        )}
      </article>

      <nav className="ekm-soru-alt">
        <button type="button" className="v15-btn is-ghost" onClick={() => git(Math.max(0, i - 1))} disabled={i === 0}>Önceki</button>
        {i < n - 1
          ? <button type="button" className="v15-btn" onClick={() => (sira.i >= 0 ? git(i + 1) : ileri())}>Sonraki <ChevronRight aria-hidden /></button>
          : <button type="button" className="v15-btn" onClick={() => bastan()}><RotateCcw aria-hidden /> Baştan</button>}
      </nav>
      </div>
      </div>
      {bitti && <p className="ekm-puan v15-card"><b>{dogruN} / {n}</b><span>Set tamamlandı. Bilemediklerin için ilgili konunun dersine dön.</span></p>}
    </div>
  );
};
