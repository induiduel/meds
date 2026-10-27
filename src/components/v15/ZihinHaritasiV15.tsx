import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, ChevronRight, Flame, Headphones } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { cdDetayGetir, type CdDetay } from '../canliDers/canliDersStore';
import { useDersListesi, dersKurulu, dersAdi } from './dersVeri';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/zihin.css';

/**
 * v15 · Zihin haritası (tasarım sistemi v15 › J03–J06 / W05–W10). Yeni sayfa: /zihin-haritasi?ders=<key> ↔
 * /dersler/zihin-haritasi. Merkez = ders; dallar = sesli dersin bölümleri; yapraklar = bölümün anahtar terimleri
 * (anlatım metnindeki `vurgu` türü "t" aralıkları, sık geçen ve önemli olanlar önde). Çıkmış soru eşlemesi olan bölüm
 * alev rozeti taşır (`cikmisKonum` paragrafı). Uydurma yok: veri dersin kendi metninden. Geniş ekranda dairesel
 * harita, dar ekranda açılır ağaç; ikisinde de dala dokununca terimler açılır, bölümden sesli derse geçilir.
 */
interface Dal { baslik: string; i0: number; terimler: string[]; aciklama: Record<string, string>; cikmis: number }

function haritaKur(d: CdDetay): Dal[] {
  const cikmisP = new Map<number, number>();
  for (const c of (d as any).cikmisKonum || []) if (typeof c?.p === 'number') cikmisP.set(c.p, (cikmisP.get(c.p) || 0) + 1);
  const terimKat = (d as any).terim as Record<string, Record<string, { t?: { t: string; a?: string }[] }>> | undefined;
  return d.bolumler.map((b) => {
    const say = new Map<string, number>();
    const aciklama: Record<string, string> = {};
    let cikmis = 0;
    const slayt = new Set<string>();
    for (const p of b.paragraflar) {
      cikmis += cikmisP.get(p.i) || 0;
      // paragrafın eşlendiği slayttaki terim katmanı (terim + 1–2 cümle açıklama)
      const e = d.pdf?.paragraflar?.[p.i];
      if (e) {
        const sk = `${e.dosya}/${e.sayfa}`;
        if (!slayt.has(sk)) {
          slayt.add(sk);
          for (const x of terimKat?.[String(e.dosya)]?.[String(e.sayfa)]?.t || []) {
            if (!x?.t || x.t.length > 40) continue;
            say.set(x.t, (say.get(x.t) || 0) + 2);
            if (x.a) aciklama[x.t] = x.a;
          }
        }
      }
      for (const [bas, son, tur, onem] of d.vurgu?.[String(p.i)] || []) {
        if (tur !== 't') continue;
        const t = p.metin.slice(bas, son).replace(/[.,;:()]+$/g, '').trim();
        if (t.length < 3 || t.length > 40) continue;
        const k = t.charAt(0).toLocaleUpperCase('tr-TR') + t.slice(1);
        say.set(k, (say.get(k) || 0) + 1 + (onem || 0));
      }
    }
    const terimler = [...say].sort((a, b2) => b2[1] - a[1]).map(([t]) => t).slice(0, 6);
    return { baslik: b.baslik || 'Bölüm', i0: b.paragraflar[0]?.i ?? 0, terimler, aciklama, cikmis };
  });
}
const kisalt = (s: string, n: number) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

export default function ZihinHaritasiV15() {
  const [key, setKey0] = useState(() => new URLSearchParams(location.search).get('ders') || '');
  const setKey = (k: string) => { setKey0(k); try { const u = new URL(location.href); u.searchParams.set('ders', k); history.replaceState(history.state, '', u); } catch { /* yok */ } };
  const { dersler } = useDersListesi();
  const [detay, setDetay] = useState<CdDetay | null>(null);
  const [hata, setHata] = useState('');
  const [acik, setAcik] = useState<number | null>(null);
  const [kurul, setKurul] = useState<number | null>(null);

  useEffect(() => {
    if (!key && dersler?.length) setKey(dersler[0].key);
  }, [dersler, key]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!key) return;
    let c = true; setDetay(null); setHata(''); setAcik(null);
    cdDetayGetir(key).then((d) => c && setDetay(d), (e) => c && setHata(e?.message || 'Ders alınamadı.'));
    return () => { c = false; };
  }, [key]);
  const ozet = dersler?.find((d) => d.key === key);
  useEffect(() => { if (ozet && kurul == null) setKurul(dersKurulu(ozet)); }, [ozet, kurul]);
  const dallar = useMemo(() => (detay ? haritaKur(detay) : []), [detay]);
  const baslik = detay?.baslik || ozet?.baslik || 'Ders';
  useV15Baslik({ baslik: 'Zihin haritası', alt: detay ? `${baslik} · ${dallar.length} bölüm` : 'Ders seç' });

  const kurullar = useMemo(() => [...new Set((dersler || []).map(dersKurulu))].sort(), [dersler]);
  const secenek = (dersler || []).filter((d) => kurul == null || dersKurulu(d) === kurul);
  const sesliYol = (i: number) => `${pathFor('canli_ders', key)}?p=${i}`;

  return (
    <div className="zh15">
      <h1 className="sr-only">Zihin haritası</h1>
      <div className="zh15-sec">
        <select value={kurul ?? ''} onChange={(e) => setKurul(Number(e.target.value))} aria-label="Kurul">
          {kurullar.map((k) => <option key={k} value={k}>Kurul {k}</option>)}
        </select>
        <select value={key} onChange={(e) => setKey(e.target.value)} aria-label="Ders">
          {secenek.map((d) => <option key={d.key} value={d.key}>{dersAdi(d)}</option>)}
        </select>
      </div>

      {hata ? <p className="b15-bos v15-card">{hata}</p> : !detay ? <span className="v15-skel b15-skel" aria-hidden /> : (
        <>
          {/* geniş ekran: dairesel harita */}
          <div className="zh15-daire v15-card" aria-hidden={false}>
            <Daire baslik={baslik} dallar={dallar} acik={acik} sec={setAcik} />
          </div>
          {/* dar ekran ve ayrıntı: ağaç */}
          <ol className="zh15-agac" aria-label={`${baslik} bölümleri`}>
            {dallar.map((d, i) => (
              <li key={i} className={`zh15-dal${acik === i ? ' is-acik' : ''}`} style={{ '--t': (i * 360) / Math.max(1, dallar.length) } as React.CSSProperties}>
                <button type="button" className="zh15-dal-b" aria-expanded={acik === i} onClick={() => setAcik(acik === i ? null : i)}>
                  <span className="zh15-no">{i + 1}</span>
                  <b>{d.baslik}</b>
                  {d.cikmis > 0 && <span className="zh15-cikmis" title={`${d.cikmis} çıkmış soru bu bölümde`}><Flame aria-hidden />{d.cikmis}</span>}
                  {acik === i ? <ChevronDown aria-hidden /> : <ChevronRight aria-hidden />}
                </button>
                {acik === i && (
                  <div className="zh15-yaprak">
                    {d.terimler.length ? <ul>{d.terimler.map((t) => <li key={t} title={d.aciklama[t]}><b>{t}</b>{d.aciklama[t] && <span>{d.aciklama[t]}</span>}</li>)}</ul> : <p className="v15-cap">Bu bölümde işaretli anahtar terim yok.</p>}
                    <a href={sesliYol(d.i0)} onClick={linkClick(() => navigateTo(sesliYol(d.i0)))} className="zh15-dinle"><Headphones aria-hidden />Bu bölümü dinle</a>
                  </div>
                )}
              </li>
            ))}
          </ol>
          <p className="v15-cap zh15-ac">Dallar dersin bölümleri, yapraklar anlatımda öne çıkan anahtar terimler. Alev: o bölümden çıkmış soru eşleşmesi var.</p>
        </>
      )}
    </div>
  );
}

/** Dairesel harita (SVG): merkez ders, çevrede bölümler; seçili bölümün terimleri dışa doğru açılır */
function Daire({ baslik, dallar, acik, sec }: { baslik: string; dallar: Dal[]; acik: number | null; sec: (i: number | null) => void }) {
  const W = 980, H = 700, cx = W / 2, cy = H / 2, R = 220;
  const n = Math.max(1, dallar.length);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="zh15-svg" role="img" aria-label={`${baslik} zihin haritası`}>
      {dallar.map((d, i) => {
        const a = (i / n) * Math.PI * 2 - Math.PI / 2;
        // kutuplara yakın dallar sırayla dışa itilir: üst/alt uçlarda etiketler üst üste binmesin
        const kutup = Math.abs(Math.sin(a)) > 0.8 ? (i % 2 ? 46 : 0) : 0;
        const x = cx + Math.cos(a) * (R + kutup * 0.6), y = cy + Math.sin(a) * (R * 0.95 + kutup);
        const sag = Math.cos(a) >= 0;
        const on = acik === i;
        return (
          <g key={i} className={`zh15-n${on ? ' is-on' : ''}${acik != null && !on ? ' is-sonuk' : ''}`} style={{ '--t': (i * 360) / n } as React.CSSProperties}
            onClick={() => sec(on ? null : i)} role="button" tabIndex={0} onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sec(on ? null : i); } }}>
            <path d={`M${cx} ${cy} Q ${(cx + x) / 2} ${cy} ${x} ${y}`} className="zh15-bag" />
            <circle cx={x} cy={y} r={on ? 9 : 7} className="zh15-nokta" />
            <text x={x + (sag ? 14 : -14)} y={y + 4} textAnchor={sag ? 'start' : 'end'} className="zh15-et">{kisalt(d.baslik, 30)}{d.cikmis ? ' 🔥' : ''}</text>
            {on && d.terimler.map((t, k) => {
              const ty = y - ((d.terimler.length - 1) * 22) / 2 + k * 22 + 22;
              const tx = x + (sag ? 34 : -34);
              return (
                <g key={t}>
                  <path d={`M${x} ${y} C ${x + (sag ? 20 : -20)} ${y} ${tx - (sag ? 10 : -10)} ${ty} ${tx} ${ty}`} className="zh15-bag is-ince" />
                  <text x={tx + (sag ? 6 : -6)} y={ty + 4} textAnchor={sag ? 'start' : 'end'} className="zh15-terim">{kisalt(t, 28)}</text>
                </g>
              );
            })}
          </g>
        );
      })}
      <g className="zh15-merkez">
        <rect x={cx - 120} y={cy - 30} width={240} height={60} rx={18} />
        <text x={cx} y={cy + 5} textAnchor="middle">{kisalt(baslik, 30)}</text>
      </g>
    </svg>
  );
}
