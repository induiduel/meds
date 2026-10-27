import React, { useEffect, useRef, useState } from 'react';
import { Flame, RotateCcw, Star, Trophy, X } from 'lucide-react';

/**
 * v15 · Oyun görsel takımı (yalnız görünüm): üst şerit (ilerleme + tur/puan/seri), uçan "+N", tur sonu özet kartı ve
 * hafif CSS konfetisi. Ses yok, kütüphane yok; animasyonlar prefers-reduced-motion'da oyun.css'te kapanır.
 */

export function OyunUst({ ilerleme, sol, puan, puanEtiket = 'puan', seri = 0, carpan, ek, onCik, cikEtiket = 'Oyundan çık' }: {
  ilerleme: number; sol: React.ReactNode; puan: number; puanEtiket?: string; seri?: number; carpan?: number;
  ek?: React.ReactNode; onCik: () => void; cikEtiket?: string;
}) {
  const [ucan, setUcan] = useState<{ n: number; k: number } | null>(null);
  const once = useRef(puan);
  useEffect(() => {
    const fark = puan - once.current;
    once.current = puan;
    if (fark > 0) setUcan({ n: fark, k: Date.now() });
  }, [puan]);
  return (
    <div className="og15-ust">
      <div className="og15-ust-s">
        <span className="og15-cip">{sol}</span>
        <span className="og15-cip is-puan">
          <Star aria-hidden /> <b>{puan}</b> {puanEtiket}
          {ucan && <span key={ucan.k} className="og15-ucan" aria-hidden>+{ucan.n}</span>}
        </span>
        {carpan && carpan > 1 ? <span className="og15-cip is-carpan">×{carpan}</span> : null}
        {seri >= 2 && <span key={seri} className="og15-cip is-seri"><Flame aria-hidden /> {seri} seri</span>}
        {ek}
        <button type="button" className="og15-x" onClick={onCik} aria-label={cikEtiket}><X aria-hidden /></button>
      </div>
      <div className="og15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(ilerleme * 100)}>
        <span style={{ width: `${Math.max(0, Math.min(1, ilerleme)) * 100}%` }} />
      </div>
    </div>
  );
}

export function Konfeti() {
  return (
    <div className="og15-konfeti" aria-hidden>
      {Array.from({ length: 18 }, (_, i) => <i key={i} style={{ '--i': i } as React.CSSProperties} />)}
    </div>
  );
}

export function SonKart({ baslik, alt, dogru, yanlis, sureSn, enIyi, rekor, oran, onCik, onYeniden, children }: {
  baslik: React.ReactNode; alt?: React.ReactNode; dogru: number; yanlis: number; sureSn?: number; enIyi: number; rekor?: boolean;
  oran: number; onCik: () => void; onYeniden?: () => void; children?: React.ReactNode;
}) {
  const yildiz = oran >= 0.9 ? 3 : oran >= 0.6 ? 2 : oran > 0 ? 1 : 0;
  return (
    <section className="v15-card og15-son" lang="tr">
      {yildiz >= 2 && <Konfeti />}
      <Trophy aria-hidden className="og15-tac" />
      <div className="og15-yildiz" aria-label={`${yildiz} yıldız`}>
        {[0, 1, 2].map((i) => <Star key={i} aria-hidden className={i < yildiz ? 'is-dolu' : ''} style={{ '--i': i } as React.CSSProperties} />)}
      </div>
      <b className="og15-son-b">{baslik}</b>
      {rekor && <span className="og15-rekor">Yeni rekor!</span>}
      {alt && <p className="v15-cap og15-son-alt">{alt}</p>}
      <dl className="og15-oz">
        <div className="is-ok"><dt>Doğru</dt><dd>{dogru}</dd></div>
        <div className="is-bad"><dt>Yanlış</dt><dd>{yanlis}</dd></div>
        {sureSn !== undefined && <div><dt>Süre</dt><dd>{sureSn < 60 ? `${sureSn} sn` : `${Math.floor(sureSn / 60)} dk ${sureSn % 60} sn`}</dd></div>}
        <div className="is-warn"><dt>En iyi</dt><dd>{enIyi}</dd></div>
      </dl>
      {children}
      <div className="oy15-alt">
        <button type="button" className="oy15-cik" onClick={onCik}>Oyunlar</button>
        {onYeniden && <button type="button" className="v15-btn oy15-ana" onClick={onYeniden}><RotateCcw aria-hidden />Yeniden oyna</button>}
      </div>
    </section>
  );
}

/** Oyunun başlangıcından geçen saniye (özet kartı için) */
export function useGecenSure() {
  const bas = useRef(Date.now());
  return { sifirla: () => { bas.current = Date.now(); }, sn: () => Math.round((Date.now() - bas.current) / 1000) };
}
