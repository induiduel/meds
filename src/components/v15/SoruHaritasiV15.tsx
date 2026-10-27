import React, { useEffect, useMemo, useState } from 'react';
import { linkClick, navigateTo } from '../../router';
import { KURUL_NOLAR, kurulKaydet, varsayilanKurul } from '../kurul/KurulSecici';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/harita.css';

/**
 * v15 · Soru haritası (tasarım sistemi v15.4 › b2harita): kurul × ders × sınav yılı çıkmış soru sayıları ısı tablosu.
 * Yeni sayfa: /soru-haritasi ↔ /sorular/soru-haritasi. Veri src/data/soru_haritasi.json (scripts/v15/soru_haritasi.py,
 * pastQuestions.json'dan yalnız sayım). Hücreye dokunmak çıkmışları o ders ve yılla süzülü açar (?ders=&yil=&kurul=).
 * Tablo kendi kartında yatay kayar; ders sütunu yapışkan.
 */
interface Harita { uretildi: string; yillar: string[]; kurullar: Record<string, Record<string, Record<string, number>>> }
const kisaYil = (y: string) => (/^\d{4}-\d{4}$/.test(y) ? `${y.slice(2, 4)}-${y.slice(7)}` : '?');
const tr = (n: number) => n.toLocaleString('tr-TR');

export default function SoruHaritasiV15() {
  const [veri, setVeri] = useState<Harita | null>(null);
  const [kurul, setKurul] = useState<number>(() => {
    try { const n = Number(new URLSearchParams(location.search).get('kurul')); return n >= 1 && n <= 6 ? n : varsayilanKurul(); } catch { return varsayilanKurul(); }
  });
  useEffect(() => {
    let c = true;
    import('../../data/soru_haritasi.json').then((m) => c && setVeri((m.default ?? m) as unknown as Harita));
    return () => { c = false; };
  }, []);

  const tablo = veri?.kurullar[String(kurul)] || {};
  const yillar = useMemo(() => (veri ? veri.yillar.filter((y) => Object.values(tablo).some((r) => r[y])) : []), [veri, tablo]);
  const satirlar = Object.entries(tablo).map(([d, r]) => ({ d, r, top: Object.values(r).reduce((a, b) => a + b, 0) }));
  const enCok = Math.max(1, ...satirlar.flatMap((s) => yillar.map((y) => s.r[y] || 0)));
  const toplam = satirlar.reduce((a, s) => a + s.top, 0);
  useV15Baslik({ baslik: 'Soru haritası', alt: veri ? `Kurul ${kurul} · ${tr(toplam)} çıkmış soru` : `Kurul ${kurul}` });

  const hucreYol = (d: string, y?: string) => {
    const p = new URLSearchParams({ kurul: String(kurul), ders: d });
    if (y && y !== 'Yılı belirsiz') p.set('yil', y);
    return `/sorular/cikmis?${p}`;
  };

  return (
    <div className="hr15">
      <h1 className="sr-only">Soru haritası</h1>
      <div className="o15-cipler v15-hscroll hr15-k" role="toolbar" aria-label="Kurul">
        {KURUL_NOLAR.map((k) => (
          <button key={k} type="button" className={`o15-cip${k === kurul ? ' is-on' : ''}`} aria-pressed={k === kurul}
            onClick={() => { kurulKaydet(k); setKurul(k); }}>Kurul {k}</button>
        ))}
      </div>
      <p className="v15-cap hr15-ac">Her hücre o yılın sınavında o dersten çıkan soru sayısı; koyulaştıkça çok. Hücreye dokun, o soruları aç.</p>
      {!veri ? (
        <span className="v15-skel b15-skel" aria-hidden />
      ) : !satirlar.length ? (
        <p className="b15-bos v15-card">Kurul {kurul} için çıkmış soru yok.</p>
      ) : (
        <div className="hr15-kap v15-card">
          <table className="hr15-t">
            <thead>
              <tr>
                <th scope="col" className="hr15-d">Ders</th>
                {yillar.map((y) => <th key={y} scope="col" title={y}>{kisaYil(y)}</th>)}
                <th scope="col">Top.</th>
              </tr>
            </thead>
            <tbody>
              {satirlar.map((s) => (
                <tr key={s.d}>
                  <th scope="row" className="hr15-d">{s.d}</th>
                  {yillar.map((y) => {
                    const n = s.r[y] || 0;
                    const yog = Math.round(12 + (n / enCok) ** 0.6 * 78);
                    return (
                      <td key={y}>
                        {n ? (
                          <a href={hucreYol(s.d, y)} onClick={linkClick(() => navigateTo(hucreYol(s.d, y)))} className={`hr15-h${yog > 55 ? ' is-koyu' : ''}`}
                            style={{ '--y': `${yog}%` } as React.CSSProperties}
                            aria-label={`${s.d}, ${y}: ${n} soru`}>{n}</a>
                        ) : <span className="hr15-bos" aria-hidden>·</span>}
                      </td>
                    );
                  })}
                  <td><a href={hucreYol(s.d)} onClick={linkClick(() => navigateTo(hucreYol(s.d)))} className="hr15-top">{tr(s.top)}</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {veri && <p className="v15-cap hr15-ac">Güncelleme: {new Date(`${veri.uretildi}T12:00:00`).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' })}. "?" sütunu yılı belli olmayan sorular.</p>}
    </div>
  );
}
