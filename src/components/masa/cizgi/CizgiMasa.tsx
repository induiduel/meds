/**
 * Çizgi Yarışı masası: dikey kareli şerit (bakanın sahası altta), kalem çizgileri, son 4 tur vurgusu, gerileme izi,
 * zar (kapışmada iki zar), yön düğmeleri ve "hepsini ilerle". Kurallar motor/cizgi.ts.
 */
import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { ArrowLeft, ArrowRight, ArrowUp, ChevronsUp, Dices, Hourglass } from 'lucide-react';
import type { CizgiGorunum, Hucre, OdaGorunum } from '../../../services/masa/tipler';
import { masa } from '../../../services/masa/istemci';
import { azHareket, sesCal, titret } from '../ortak';
import { OyuncuSerit, benOyuncuMu, rakipId } from '../tahta/ortak';
import '../../../styles/masa/tahta.css';

const RENK = { ben: '#e4572e', rakip: '#2563eb' };

export default function CizgiMasa({ oda }: { oda: OdaGorunum }) {
  const c = oda.oyun?.tur === 'cizgi' ? (oda.oyun as CizgiGorunum) : null;
  if (!c) return null;
  return <Pist oda={oda} c={c} />;
}

function Zar({ deger, kazandi, kaybetti, k }: { deger: number; kazandi?: boolean; kaybetti?: boolean; k: string }) {
  const az = azHareket();
  const noktalar: Record<number, [number, number][]> = {
    1: [[50, 50]], 2: [[28, 28], [72, 72]], 3: [[28, 28], [50, 50], [72, 72]], 4: [[28, 28], [72, 28], [28, 72], [72, 72]],
    5: [[28, 28], [72, 28], [50, 50], [28, 72], [72, 72]], 6: [[28, 26], [72, 26], [28, 50], [72, 50], [28, 74], [72, 74]],
  };
  return (
    <motion.svg key={k} className={`tm-zar${kazandi ? ' is-kazan' : ''}${kaybetti ? ' is-kayip' : ''}`} viewBox="0 0 100 100" aria-label={`Zar ${deger}`}
      initial={az ? false : { rotate: -200, scale: 0.4, y: -30 }} animate={{ rotate: 0, scale: 1, y: 0 }} transition={{ type: 'spring', stiffness: 260, damping: 16 }}>
      <rect x="6" y="6" width="88" height="88" rx="20" />
      {(noktalar[deger] || []).map(([x, y], i) => <circle key={i} cx={x} cy={y} r="8.5" />)}
    </motion.svg>
  );
}

function Pist({ oda, c }: { oda: OdaGorunum; c: CizgiGorunum }) {
  const ben = oda.ben, rakip = rakipId(oda), oyuncu = benOyuncuMu(oda);
  const benimC = c.cizgiler[ben] || [], rakipC = c.cizgiler[rakip] || [];
  // Bakan 1. oyuncuysa (r=0'dan başlar) satırlar yukarı doğru artar; 2. oyuncuysa tahta 180° döner
  const alttan = (c.cizgiler[ben]?.[0]?.r ?? 0) === 0 || !oyuncu;
  const L = c.uzunluk, G = c.genislik;
  const ekran = (h: Hucre) => ({ x: alttan ? h.s : G - 1 - h.s, y: alttan ? L - 1 - h.r : h.r });
  const etkin = oyuncu && oda.asama === 'oyun' && !oda.durdu && !c.bitti;
  const siraBende = etkin && c.sira === ben;
  const [otoKos, setOtoKos] = useState(() => { try { return localStorage.getItem('medsoru_cizgi_otokos') !== '0'; } catch { return true; } });
  const otoYaz = (v: boolean) => { setOtoKos(v); try { localStorage.setItem('medsoru_cizgi_otokos', v ? '1' : '0'); } catch { /* yok */ } };

  // Otomatik koş: zar gelince tek seçenek düz ilerlemekse adımların hepsi tek hamlede harcanır (zar görünsün diye kısa bekleme)
  useEffect(() => {
    if (!otoKos || !siraBende || c.zar == null || c.kalan <= 0) return;
    if (c.yonler.length !== 1 || c.yonler[0] !== 'duz') return;
    const t = setTimeout(() => masa.hamle({ t: 'kos' }), 380);
    return () => clearTimeout(t);
  }, [otoKos, c, siraBende]);

  // Kısa kutlama yazısı: büyük zar, kapışma sonucu, yan geçiş
  const [flas, setFlas] = useState<{ k: number; metin: string; iyi: boolean } | null>(null);
  useEffect(() => { if (!flas) return; const t = setTimeout(() => setFlas(null), 1300); return () => clearTimeout(t); }, [flas]);

  const son = c.gecmis[c.gecmis.length - 1];
  const sonK = useRef(c.gecmis.length + ':' + (son?.tur ?? 0));
  const sonOzel = useRef(`${son?.tur ?? 0}:${son?.ozel?.length ?? 0}`);
  useEffect(() => {
    const k = c.gecmis.length + ':' + (son?.tur ?? 0) + ':' + (son?.zar ?? 0) + ':' + (son?.ozel?.length ?? 0) + (c.zar == null ? 'b' : 'a');
    if (k !== sonK.current && son) {
      sesCal(son.kapisma ? (son.kapisma.kazanan === ben ? 'kazan' : 'ceza') : 'tas');
      const benim = son.o === ben;
      const OZEL_AD = { ileri: '+3 adım!', yan: '+1 yan hakkı', zar: 'Yeniden zar!', tuzak: 'Tuzak! 2 geri' } as const;
      const ozelK = `${son.tur}:${son.ozel?.length ?? 0}`, ozelYeni = !!son.ozel?.length && ozelK !== sonOzel.current;
      sonOzel.current = ozelK;
      if (son.ozel?.length && !ozelYeni) { /* bu kare zaten duyuruldu */ } else if (ozelYeni && son.ozel) {
        const t = son.ozel[son.ozel.length - 1], iyi = t !== 'tuzak';
        setFlas({ k: Date.now(), metin: `${benim ? '' : 'Rakip: '}${OZEL_AD[t]}`, iyi: benim ? iyi : !iyi });
        sesCal(t === 'tuzak' ? 'ceza' : 'kazan');
      } else if (son.kapisma) {
        const kaz = son.kapisma.kazanan;
        setFlas({ k: Date.now(), metin: kaz == null ? 'Kapışma: eşit!' : kaz === ben ? `Kapışmayı kazandın +${Math.abs(son.fark)}` : `Kapışmayı kaybettin −${Math.abs(son.fark)}`, iyi: kaz === ben });
        if (kaz && kaz !== ben) titret(40);
      } else if (c.zar != null) { /* tur sürüyor */ } else if (son.zar === 6 && son.fark >= 6) setFlas({ k: Date.now(), metin: benim ? 'Altı! Tam yol' : 'Rakip altı attı', iyi: benim });
      else if (son.fark === 0 && son.eklenen.length === 0) setFlas({ k: Date.now(), metin: benim ? 'Yol kapalı, tur yandı' : 'Rakip sıkıştı', iyi: !benim });
    }
    sonK.current = k;
  }, [son, c.zar]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (c.zar != null && c.sira === ben) { sesCal('cek'); titret(10); } }, [c.zar]); // eslint-disable-line react-hooks/exhaustive-deps

  // Hücre boyu: genişliğe sığdır; uzun pistte kaydırılır, kendi başıma odaklanır
  const kapRef = useRef<HTMLDivElement>(null);
  const [gen, setGen] = useState(320);
  useLayoutEffect(() => {
    const el = kapRef.current; if (!el) return;
    const olc = () => setGen(el.clientWidth);
    olc(); const ro = new ResizeObserver(olc); ro.observe(el); return () => ro.disconnect();
  }, []);
  const H = Math.max(18, Math.min(64, Math.floor((Math.min(gen, 480) - 16) / G)));
  const bas = benimC[benimC.length - 1];
  useEffect(() => {
    const el = kapRef.current; if (!el || !bas) return;
    const y = ekran(bas).y * H;
    el.scrollTo({ top: Math.max(0, y - el.clientHeight * 0.55), behavior: azHareket() ? 'auto' : 'smooth' });
  }, [bas?.r, bas?.s, H]); // eslint-disable-line react-hooks/exhaustive-deps

  // Son 4 tur: hücre → yaş (0 en yeni) — vurgu soluklaşır
  const yas = useMemo(() => {
    const m = new Map<string, number>();
    c.gecmis.forEach((a, k) => a.eklenen.forEach((h) => m.set(`${a.o}:${h.s},${h.r}`, c.gecmis.length - 1 - k)));
    return m;
  }, [c.gecmis]);
  const silinen = c.gecmis.slice(-2).flatMap((a, k, arr) => (a.silinen.length ? [{ a, eski: arr.length - 1 - k }] : []));

  const yol = (hs: Hucre[]) => hs.map((h, i) => { const p = ekran(h); return `${i ? 'L' : 'M'}${(p.x + 0.5) * H} ${(p.y + 0.5) * H}`; }).join(' ');
  const parca = (o: string, renk: string, hs: Hucre[]) => hs.slice(1).map((h, i) => {
    const a = ekran(hs[i]), b = ekran(h), y = yas.get(`${o}:${h.s},${h.r}`);
    if (y == null) return null;
    return <line key={`${o}${i}`} x1={(a.x + 0.5) * H} y1={(a.y + 0.5) * H} x2={(b.x + 0.5) * H} y2={(b.y + 0.5) * H} stroke={renk} strokeWidth={H * 0.36} strokeLinecap="round" opacity={[0.95, 0.6, 0.38, 0.22][y] ?? 0} className="tm-cz-iz" />;
  });

  // Ekran yönüne göre sol/sağ düğmeleri (döndürülmüş tahtada motorun "sol"u ekranda sağdır)
  const solYon = alttan ? 'sol' : 'sag', sagYon = alttan ? 'sag' : 'sol';
  const kapismaSon = son?.kapisma;
  const benimYan = c.yanHak[ben] ?? 0, rakipYan = c.yanHak[rakip] ?? 0;
  const ilerleme = (hs: Hucre[]) => (hs.length ? Math.abs(hs[hs.length - 1].r - hs[0].r) : 0);

  return (
    <div className="tm-kok tm-cz">
      <OyuncuSerit oda={oda} id={rakip} isaret={<><i className="tm-cz-renk" style={{ background: RENK.rakip }} />Yan hakkı {rakipYan}</>}
        sag={<small className="tm-cz-ilerleme">{ilerleme(rakipC) + 1}/{L}</small>} />

      <div className="tm-cz-yaris" aria-hidden="true">
        <span className="tm-cz-yaris-iz" />
        <span className="tm-cz-yaris-orta" />
        <motion.i className="tm-cz-yaris-ben" style={{ background: RENK.ben }} animate={{ left: `${(ilerleme(benimC) / Math.max(1, L - 1)) * 100}%` }} transition={{ type: 'spring', stiffness: 160, damping: 20 }} />
        <motion.i className="tm-cz-yaris-rakip" style={{ background: RENK.rakip }} animate={{ left: `${(1 - ilerleme(rakipC) / Math.max(1, L - 1)) * 100}%` }} transition={{ type: 'spring', stiffness: 160, damping: 20 }} />
      </div>

      <AnimatePresence>{flas && (
          <motion.div key={flas.k} className={`tm-cz-flas${flas.iyi ? ' is-iyi' : ' is-kotu'}`} role="status"
            initial={{ opacity: 0, x: '-50%', y: 16, scale: 0.8 }} animate={{ opacity: 1, x: '-50%', y: 0, scale: 1 }} exit={{ opacity: 0, x: '-50%', y: -18 }} transition={{ duration: 0.25 }}>{flas.metin}</motion.div>
      )}</AnimatePresence>
      <div className="tm-cz-pist" ref={kapRef}>
        <svg width={G * H} height={L * H} viewBox={`0 0 ${G * H} ${L * H}`} className="tm-cz-svg" role="img" aria-label={`Çizgi Yarışı pisti, ${L} satır ${G} sütun`}>
          <defs>
            <pattern id="tm-cz-kare" width={H} height={H} patternUnits="userSpaceOnUse"><path d={`M${H} 0H0V${H}`} fill="none" stroke="#7aa3c9" strokeOpacity=".35" strokeWidth="1" /></pattern>
          </defs>
          <rect width={G * H} height={L * H} fill="#fdfaf2" />
          {/* kaleler: üst rakibin kalesi (benim hedefim), alt benim kalem */}
          <rect x="0" y="0" width={G * H} height={H} className="tm-cz-kale is-hedef" />
          <rect x="0" y={(L - 1) * H} width={G * H} height={H} className="tm-cz-kale is-ben" />
          <rect width={G * H} height={L * H} fill="url(#tm-cz-kare)" />
          <line x1="0" x2={G * H} y1={(L / 2) * H} y2={(L / 2) * H} className="tm-cz-orta" />
          {Array.from({ length: Math.floor(L / 8) }, (_, k) => (k + 1) * 8).filter((r) => r < L).map((r) => (
            <text key={r} x="3" y={(L - r) * H - 3} className="tm-cz-satir">{alttan ? r : L - r}</text>
          ))}
          {/* eğlenceli mod özel kareleri */}
          {(c.ozel || []).map((x) => { const p = ekran(x); return (
            <g key={`o${x.s},${x.r}`} className={`tm-cz-ozel is-${x.t}`}>
              <rect x={p.x * H + 2} y={p.y * H + 2} width={H - 4} height={H - 4} rx={H * 0.2} />
              <text x={(p.x + 0.5) * H} y={(p.y + 0.5) * H} fontSize={H * 0.55} textAnchor="middle" dominantBaseline="central">{({ ileri: '⏩', yan: '↔', zar: '🎲', tuzak: '💥' } as const)[x.t]}</text>
            </g>
          ); })}
          {/* gerileme izi: silinen kısım kesik çizgi, 1–2 tur görünür */}
          {silinen.map(({ a, eski }) => (
            <path key={`s${a.tur}`} d={yol(a.silinen)} stroke={a.o === ben ? RENK.ben : RENK.rakip} strokeWidth={H * 0.22} strokeDasharray={`${H * 0.25} ${H * 0.3}`} strokeLinecap="round" fill="none" opacity={eski ? 0.25 : 0.55} />
          ))}
          {[{ o: rakip, hs: rakipC, renk: RENK.rakip }, { o: ben, hs: benimC, renk: RENK.ben }].map(({ o, hs, renk }) => (
            <g key={o}>
              <path d={yol(hs)} stroke={renk} strokeWidth={H * 0.3} strokeLinecap="round" strokeLinejoin="round" fill="none" opacity=".8" />
              {parca(o, renk, hs)}
              {hs.length > 0 && (() => { const p = ekran(hs[hs.length - 1]); return <motion.circle cx={(p.x + 0.5) * H} cy={(p.y + 0.5) * H} r={H * 0.32} fill="#fff" stroke={renk} strokeWidth={H * 0.12} animate={{ cx: (p.x + 0.5) * H, cy: (p.y + 0.5) * H }} transition={{ duration: 0.12 }} />; })()}
            </g>
          ))}
        </svg>
      </div>

      <div className="tm-cz-zarlar" aria-live="polite">
        <AnimatePresence mode="popLayout">
          {kapismaSon && son ? (
            <motion.div key={`k${son.tur}`} className="tm-cz-kapisma" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <Zar k={`a${son.tur}`} deger={son.zar} kazandi={kapismaSon.kazanan === son.o} kaybetti={!!kapismaSon.kazanan && kapismaSon.kazanan !== son.o} />
              <b>Kapışma</b>
              <Zar k={`b${son.tur}`} deger={kapismaSon.rakipZar} kazandi={!!kapismaSon.kazanan && kapismaSon.kazanan !== son.o} kaybetti={kapismaSon.kazanan === son.o} />
              <span className={`tm-cz-fark${kapismaSon.kazanan === ben ? ' is-iyi' : kapismaSon.kazanan ? ' is-kotu' : ''}`}>
                {kapismaSon.kazanan == null ? 'Eşit' : kapismaSon.kazanan === ben ? `+${Math.abs(son.fark)}` : `−${Math.abs(son.fark)}`}
              </span>
            </motion.div>
          ) : c.zar != null ? (
            <motion.div key={`z${c.zar}-${c.gecmis.length}`} className="tm-cz-kapisma"><Zar k={`z${c.zar}-${c.gecmis.length}`} deger={c.zar} /><span>{c.sira === ben ? `${c.kalan} adım kaldı` : 'Rakip ilerliyor'}</span></motion.div>
          ) : son ? (
            <motion.div key={`s${son.tur}`} className="tm-cz-kapisma is-soluk"><Zar k={`s${son.tur}`} deger={son.zar} /><span>{son.o === ben ? 'Senin son zarın' : 'Rakibin son zarı'}: {son.fark > 0 ? `+${son.fark}` : son.fark}</span></motion.div>
          ) : null}
        </AnimatePresence>
      </div>
      {c.kapisma && !c.bitti && <p className="tm-not is-uyari" role="status">Çizgiler yüz yüze: sıradaki zar atınca iki zar birden atılır, büyük atan farkı kadar ilerler, küçük atan geriler.</p>}

      <OyuncuSerit oda={oda} id={ben} alt isaret={<><i className="tm-cz-renk" style={{ background: RENK.ben }} />Yan hakkı {benimYan}</>}
        sag={<small className="tm-cz-ilerleme">{ilerleme(benimC) + 1}/{L}</small>} />

      {oyuncu && (
        <div className="tm-eylem">
          {c.zar == null ? (
            <button type="button" className="mk-dugme is-ana is-buyuk" disabled={!siraBende} onClick={() => { masa.hamle({ t: 'zar' }); titret(12); }}><Dices size={20} /> {c.kapisma ? 'Kapışma zarı at' : 'Zar at'}</button>
          ) : (
            <>
              <button type="button" className="mk-dugme is-acik" disabled={!siraBende || !c.yonler.includes(solYon)} onClick={() => masa.hamle({ t: 'ilerle', yon: solYon })} aria-label="Sola geç"><ArrowLeft size={20} /></button>
              <button type="button" className="mk-dugme is-ana" disabled={!siraBende || !c.yonler.includes('duz')} onClick={() => masa.hamle({ t: 'ilerle', yon: 'duz' })}><ArrowUp size={20} /> İlerle</button>
              <button type="button" className="mk-dugme is-acik" disabled={!siraBende || !c.yonler.includes(sagYon)} onClick={() => masa.hamle({ t: 'ilerle', yon: sagYon })} aria-label="Sağa geç"><ArrowRight size={20} /></button>
              <button type="button" className="mk-dugme is-acik" disabled={!siraBende || !c.yonler.includes('duz') || c.kalan < 2} onClick={() => masa.hamle({ t: 'kos' })}><ChevronsUp size={18} /> Hepsi</button>
              <button type="button" className="mk-dugme is-soluk" disabled={!siraBende} onClick={() => masa.hamle({ t: 'bekle' })} aria-label="Kalan adımları yak"><Hourglass size={18} /></button>
            </>
          )}
        </div>
      )}
      {siraBende && c.zar != null && !c.yonler.length && <p className="tm-not">Yolun kapalı ve yana geçemiyorsun: kalan adımlar yanar.</p>}
      {siraBende && c.zar != null && c.yonler.some((y) => y !== 'duz') && <p className="tm-not is-uyari" role="status">Önün kapalı: sola ya da sağa geç (yan hakkın {benimYan}).</p>}
      {oyuncu && (
        <label className="tm-cz-oto"><input type="checkbox" checked={otoKos} onChange={(e) => otoYaz(e.target.checked)} /> Otomatik ilerle <small>(seçim gerekince durur)</small></label>
      )}
    </div>
  );
}
