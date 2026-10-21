/**
 * İzleme hızı kaydırıcısı (Bitirdiklerim + Sınav planı): dersleri kaç × dinlediğini girer, kalan süre bu hızla hesaplanır.
 * Değer calismaTakip.izlemeHizi (profil kv, cihazlar arası). Boşsa kalan ders süresi 1×, plan ölçülen hızla. Stil: styles/takip.css (.ih-*).
 */
import React from 'react';
import { Gauge, RotateCcw } from 'lucide-react';
import { izlemeHiziYaz, sureYaz, useIzlemeHizi } from '../../services/calismaTakip';

const MIN = 1, MAX = 2.5, ADIM = 0.25;
const DURAKLAR = [1, 1.25, 1.5, 1.75, 2, 2.5];
const xYaz = (v: number) => `${v.toLocaleString('tr-TR', { maximumFractionDigits: 2 })}×`;
const konum = (v: number) => ((v - MIN) / (MAX - MIN)) * 100;

export default function IzlemeHizi({ kisa }: { kisa?: boolean }) {
  const secili = useIzlemeHizi();
  const v = secili ?? 1.5;
  const yuzde = konum(v);
  return (
    <div className={`ih${secili == null ? ' is-bos' : ''}`}>
      <div className="ih-ust">
        <span className="ih-ic" aria-hidden><Gauge /></span>
        <div className="ih-baslik">
          <b>Dersleri kaç × hızda izliyorsun?</b>
          <small>
            {secili == null
              ? 'Henüz seçmedin; kalan ders süresi 1× gösteriliyor. Kaydırarak ya da bir hıza dokunarak seç.'
              : `1 saatlik ders sana ~${sureYaz(3600 / v)} sürüyor; kalan ders süresi ve plan buna göre.`}
          </small>
        </div>
        <output className="ih-deger" aria-live="polite">{secili == null ? '—' : xYaz(v)}</output>
      </div>

      <div className="ih-ray" style={{ ['--ih-p' as string]: `${yuzde}%` }}>
        <input
          type="range" min={MIN} max={MAX} step={ADIM} value={v}
          aria-label="İzleme hızı" aria-valuetext={xYaz(v)}
          onChange={(e) => izlemeHiziYaz(Number(e.target.value))}
          onPointerDown={() => { if (secili == null) izlemeHiziYaz(v); }}
        />
        <div className="ih-duraklar">
          {DURAKLAR.map((d) => (
            <button key={d} type="button" style={{ left: `${konum(d)}%` }} className={secili === d ? 'is-on' : ''}
              onClick={() => izlemeHiziYaz(d)} aria-label={`${xYaz(d)} seç`}>{xYaz(d)}</button>
          ))}
        </div>
      </div>

      {!kisa && secili != null && (
        <button type="button" className="ih-sifirla" onClick={() => izlemeHiziYaz(null)}>
          <RotateCcw aria-hidden /> Seçimi kaldır
        </button>
      )}
    </div>
  );
}
