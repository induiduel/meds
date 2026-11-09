/** Taş Domino masası: zincir (yılan dizilim), iki uç yuvası, el şeridi, Çek / Pas / İpucu. Durumun tek kaynağı `oda`. */
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ArrowDownToLine, Lightbulb, SkipForward } from 'lucide-react';
import type { OdaGorunum, Tas } from '../../../services/masa/tipler';
import { masa } from '../../../services/masa/istemci';
import { uyar, type DominoGorunum, type DominoHamle, type DominoUc } from '../../../services/masa/motor/domino';
import { benOnde, oyuncuAdi, sesCal, titret, useTercih } from '../ortak';
import { TasGorsel, TAS_ORAN } from '../okey/Tas';
import '../../../styles/masa/okey.css';
import '../../../styles/masa/domino.css';

export default function DominoMasa({ oda }: { oda: OdaGorunum }) {
  const g = (oda.oyun as unknown as DominoGorunum | undefined)?.tur === 'domino' ? (oda.oyun as unknown as DominoGorunum) : null;
  if (!g) return <div className="om-kok om-kok--klasik dm-kok" />;
  return <Masa oda={oda} g={g} />;
}

/** Zincirin sığacağı en büyük taş genişliği ve satır başına taş (iki uç yuvası dahil) */
function zincirDuzen(n: number, W: number, H: number) {
  const adet = n + 2;
  for (let b = 50; b > 16; b -= 2) {
    const sutun = Math.max(3, Math.floor((W - 12) / (b + 4)));
    const satir = Math.ceil(adet / sutun);
    if (satir * (b * TAS_ORAN + 10) <= H) return { b, sutun };
  }
  return { b: 16, sutun: Math.max(3, Math.floor((W - 12) / 20)) };
}

type Oge = { tur: 'tas'; tas: Tas } | { tur: 'uc'; uc: DominoUc };

function Masa({ oda, g }: { oda: OdaGorunum; g: DominoGorunum }) {
  const tercih = useTercih();
  const ben = oda.ben;
  const tema = oda.ayar.tema === 'kitty' ? 'kitty' : 'klasik';
  const renkler = oda.ayar.renkler;
  const asistan = oda.ayar.asistan !== false;
  const kilit = oda.asama !== 'oyun' || oda.durdu || g.bitti;
  const siraBende = !kilit && g.sira === ben;
  const [secili, setSecili] = useState<number | null>(null);
  const [ipucu, setIpucu] = useState<{ tas: number; uc: DominoUc } | null>(null);
  const [sars, setSars] = useState<number | null>(null);
  const alanRef = useRef<HTMLDivElement | null>(null);
  const [alan, setAlan] = useState({ w: 600, h: 300 });

  useLayoutEffect(() => {
    const el = alanRef.current;
    if (!el) return;
    const olc = () => setAlan((a) => (a.w === el.clientWidth && a.h === el.clientHeight ? a : { w: el.clientWidth, h: el.clientHeight }));
    olc();
    const ro = new ResizeObserver(olc);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // sıra ya da el değişince seçim/ipucu sıfırlanır
  useEffect(() => { setSecili(null); setIpucu(null); }, [g.sira, g.zincir.length, g.elim.length]);

  const uygunTas = useMemo(() => new Set(g.secenekler.map((k) => k.tas)), [g.secenekler]);
  const tasUyar = useCallback((id: number, uc: DominoUc) => g.secenekler.some((k) => k.tas === id && k.uc === uc), [g.secenekler]);
  const elMap = useMemo(() => new Map(g.elim.map((t) => [t.id, t])), [g.elim]);

  const gonder = (h: DominoHamle) => { setIpucu(null); setSecili(null); masa.hamle(h as any); };
  const sarsit = (id: number) => { setSars(id); sesCal('hata'); titret([10, 40, 10]); window.setTimeout(() => setSars((s) => (s === id ? null : s)), 420); };

  const koy = (id: number, uc: DominoUc) => {
    if (!siraBende) return sarsit(id);
    // zorlu modda da yalnız kurala uyan bırakma kabul edilir (seçenek listesi sırası olana gelir)
    const t = elMap.get(id);
    if (!t || !tasUyar(id, uc) || !uyar(t, uc === 'bas' ? g.uclar.bas : g.uclar.son)) return sarsit(id);
    sesCal('tas');
    gonder({ t: 'koy', tas: id, uc });
  };

  /* ---------------- sürükle-bırak (işaretçi; DOM'a doğrudan dönüşüm, yeniden çizim yok) ---------------- */
  const sur = useRef<{ id: number; el: HTMLElement; x: number; y: number; oynadi: boolean } | null>(null);
  const basla = (e: React.PointerEvent<HTMLButtonElement>, id: number) => {
    if (kilit || e.button > 0) return;
    sur.current = { id, el: e.currentTarget, x: e.clientX, y: e.clientY, oynadi: false };
    e.currentTarget.setPointerCapture(e.pointerId);
  };
  const tasi = (e: React.PointerEvent) => {
    const s = sur.current;
    if (!s) return;
    const dx = e.clientX - s.x, dy = e.clientY - s.y;
    if (!s.oynadi && Math.hypot(dx, dy) < 8) return;
    s.oynadi = true;
    s.el.classList.add('dm-tas--surukle');
    s.el.style.transform = `translate(${dx}px, ${dy}px)`;
  };
  const birak = (e: React.PointerEvent) => {
    const s = sur.current;
    sur.current = null;
    if (!s) return;
    s.el.classList.remove('dm-tas--surukle');
    s.el.style.transform = '';
    if (!s.oynadi) { setSecili((x) => (x === s.id ? null : s.id)); return; }
    const hedef = (document.elementFromPoint(e.clientX, e.clientY) as HTMLElement | null)?.closest<HTMLElement>('[data-uc]');
    const uc = hedef?.dataset.uc as DominoUc | undefined;
    if (uc) koy(s.id, uc);
  };
  const iptal = () => { const s = sur.current; sur.current = null; if (s) { s.el.classList.remove('dm-tas--surukle'); s.el.style.transform = ''; } };

  /* ---------------- zincir dizilimi ---------------- */
  const { b, sutun } = zincirDuzen(g.zincir.length, alan.w, alan.h);
  const satirlar = useMemo(() => {
    const ogeler: Oge[] = [{ tur: 'uc', uc: 'bas' }, ...g.zincir.map((tas) => ({ tur: 'tas' as const, tas })), { tur: 'uc', uc: 'son' }];
    const out: Oge[][] = [];
    for (let i = 0; i < ogeler.length; i += sutun) out.push(ogeler.slice(i, i + sutun));
    return out;
  }, [g.zincir, sutun]);
  const elB = Math.max(30, Math.min(52, Math.floor((Math.min(alan.w, 720) - 16) / Math.max(7, Math.min(g.elim.length, 10)) - 6)));

  const ucYuva = (uc: DominoUc) => {
    const hedefMi = siraBende && (secili != null ? tasUyar(secili, uc) : asistan && g.secenekler.some((k) => k.uc === uc));
    const ip = ipucu?.uc === uc;
    return (
      <button key={uc} type="button" data-uc={uc} className={`dm-yuva${hedefMi ? ' is-hedef' : ''}${ip ? ' is-ipucu' : ''}`}
        style={{ width: b, height: b * TAS_ORAN }} aria-label={uc === 'bas' ? 'Baş ucu' : 'Son ucu'}
        onClick={() => { if (secili != null) koy(secili, uc); }} disabled={kilit} />
    );
  };

  const rakipler = benOnde(g.oyuncular, ben).filter((o) => o.id !== ben);
  const durum = g.bitti ? 'El bitti' : !siraBende ? `Sıra: ${oyuncuAdi(oda, g.sira)}` : g.tur_.ek ? 'Ek hamle! Bir taş daha koyabilirsin' : g.tur_.cekti ? 'Çektiğin taş uyuyor: koy ya da pas' : 'Sıra sende';

  return (
    <div className={`om-kok om-kok--${tema} dm-kok ${tercih.boyut === '3b' ? 'om-3b' : 'om-2b'}${kilit ? ' dm-kok--kilit' : ''}`}>
      <div className="dm-ust">
        {rakipler.map((o) => (
          <div key={o.id} className={`dm-rakip${g.sira === o.id ? ' is-sira' : ''}`}>
            <span className="dm-rakip-ad">{oyuncuAdi(oda, o.id)}</span>
            <span className="dm-rakip-say" aria-label={`${o.tasSayisi} taş`}>{o.tasSayisi}</span>
          </div>
        ))}
        <div className="dm-deste" aria-label={`Destede ${g.deste} taş`}>
          <TasGorsel tas={{ id: -1, s: 1, r: 0 }} renkler={renkler} tema={tema} boy={20} kapali />
          <b>{g.deste}</b>
        </div>
      </div>

      <div className="dm-alan" ref={alanRef}>
        <div className="dm-zincir" style={{ gap: 8 }}>
          {satirlar.map((satir, si) => (
            <div key={si} className={`dm-satir${si % 2 ? ' is-ters' : ''}`}>
              {satir.map((o) => o.tur === 'uc' ? ucYuva(o.uc) : (
                <TasGorsel key={o.tas.id} tas={o.tas} renkler={renkler} tema={tema} boy={b}
                  className={`dm-ztas${g.son?.tas === o.tas.id ? ' is-son' : ''}${o.tas === g.uclar.bas || o.tas === g.uclar.son ? ' is-uc' : ''}`} />
              ))}
            </div>
          ))}
        </div>
      </div>

      <div className="dm-alt">
        <div className={`dm-durum${siraBende ? ' is-ben' : ''}`} role="status">{durum}</div>
        <div className="dm-el" onPointerMove={tasi} onPointerUp={birak} onPointerCancel={iptal}>
          {g.elim.map((t) => {
            const vurgu = asistan && siraBende && uygunTas.has(t.id);
            return (
              <button key={t.id} type="button" className={`dm-tas${secili === t.id ? ' is-secili' : ''}${vurgu ? ' is-uygun' : ''}${ipucu?.tas === t.id ? ' is-ipucu' : ''}${sars === t.id ? ' is-sars' : ''}`}
                onPointerDown={(e) => basla(e, t.id)} disabled={kilit} aria-pressed={secili === t.id}>
                <TasGorsel tas={t} renkler={renkler} tema={tema} boy={elB} />
              </button>
            );
          })}
        </div>
        <div className="om-eylem-dugmeler dm-dugmeler">
          {asistan && (
            <button type="button" className="om-dugme" disabled={!siraBende || !g.secenekler.length}
              onClick={() => { const k = g.secenekler[0]; if (k) { setIpucu(k); setSecili(k.tas); } }}>
              <Lightbulb size={17} /> İpucu
            </button>
          )}
          <button type="button" className="om-dugme om-dugme--birincil" disabled={!g.cekOlur} onClick={() => { sesCal('cek'); gonder({ t: 'cek' }); }}>
            <ArrowDownToLine size={17} /> Çek
          </button>
          <button type="button" className="om-dugme" disabled={!g.pasOlur} onClick={() => gonder({ t: 'pas' })}>
            <SkipForward size={17} /> Pas
          </button>
        </div>
      </div>
    </div>
  );
}
