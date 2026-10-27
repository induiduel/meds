import React, { useEffect, useMemo, useState } from 'react';
import { Check, Lock, Zap } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { satinAl, sayi, useBasarim, yenile, type KilitT } from '../../services/basarimIstemci';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/hucrem.css';

/**
 * v15 · Hücrem (tasarım sistemi v15 › M "Hücrem"). Yeni sayfa: /hucrem (Menü › Topluluk).
 * Çalışarak kazandığın ATP ile hücreni 28 evrim basamağında büyütürsün: ilkel çorbadan insana. Basamaklar
 * başarım tanımındaki `tur: "hucre"` kilitleridir (src/data/basarim/tanim.json); satın alma, ATP defteri ve eşitleme
 * mevcut başarım motorundan (POST /api/basarim/satin-al; sunucu "önceki basamak" şartını denetler). Her basamak bir
 * tıbbi bilgi açar. Çizim açılan basamak sayısına göre katman katman büyür (SVG, palet tokenları).
 */
export default function HucremV15() {
  const { tanim, durum, hata } = useBasarim();
  const [is, setIs] = useState(false);
  const [mesaj, setMesaj] = useState('');
  useEffect(() => { void yenile(); }, []);
  const basamaklar = useMemo(() => tanim.kilitler.filter((k) => k.tur === 'hucre' && k.etkin), [tanim]);
  const acik = durum?.kilit || {};
  const n = basamaklar.filter((b) => acik[b.id]).length;
  const sonraki = basamaklar.find((b) => !acik[b.id]);
  const simdiki = n ? basamaklar[n - 1] : null;
  const bakiye = durum?.atp.bakiye ?? 0;
  useV15Baslik({ baslik: 'Hücrem', alt: `${n}/${basamaklar.length} basamak · ${simdiki?.cag || 'Başlangıç'}` });

  const cag = useMemo(() => {
    const m = new Map<string, KilitT[]>();
    for (const b of basamaklar) { const c = b.cag || 'Diğer'; m.set(c, [...(m.get(c) || []), b]); }
    return [...m];
  }, [basamaklar]);

  const ac = async () => {
    if (!sonraki || is) return;
    setIs(true); setMesaj('');
    try { await satinAl(sonraki.id); setMesaj(`${sonraki.ad} açıldı!`); }
    catch (e: any) { setMesaj(e?.message || 'Açılamadı.'); }
    setIs(false);
  };

  if (!durum) {
    return (
      <div className="hc15">
        <section className="v15-card hc15-bos">
          <Hucre n={0} />
          <b>Hücreni büyütmek için giriş yap</b>
          <p>Çalıştıkça ATP kazanırsın; ATP ile hücren ilkel çorbadan insana 28 basamakta evrimleşir. {hata && <small>({hata})</small>}</p>
        </section>
      </div>
    );
  }

  return (
    <div className="hc15">
      <h1 className="sr-only">Hücrem</h1>
      <section className="v15-card hc15-sahne">
        <Hucre n={n} />
        <div className="hc15-durum">
          <span className="hc15-cag">{simdiki?.cag || 'Başlangıç'}</span>
          <b>{simdiki ? simdiki.ad : 'Henüz boş bir damla'}</b>
          <div className="v15-bar hc15-bar" aria-label={`${n} / ${basamaklar.length} basamak`}><span style={{ width: `${(n / Math.max(1, basamaklar.length)) * 100}%` }} /></div>
          <span className="hc15-atp"><Zap aria-hidden /> {sayi(bakiye)} mol ATP{durum.atp.kuyrukta ? ` · ${sayi(durum.atp.kuyrukta)} kuyrukta` : ''}</span>
        </div>
      </section>

      {sonraki ? (
        <section className="v15-card hc15-sonraki">
          <div>
            <span className="v15-cap">Sıradaki basamak · {basamaklar.indexOf(sonraki) + 1}</span>
            <b>{sonraki.ad}</b>
            <p>{sonraki.cag} çağı. Açınca bu basamağın tıbbi bilgisi ve hücrendeki yeni parçası görünür.</p>
          </div>
          <button type="button" className="hc15-ac" onClick={ac} disabled={is || bakiye < sonraki.fiyat}>
            <Zap aria-hidden /> {sayi(sonraki.fiyat)} mol ile aç
          </button>
          {bakiye < sonraki.fiyat && <p className="v15-cap hc15-eksik">{sayi(sonraki.fiyat - bakiye)} mol daha gerekli. ATP'yi günlük hedefler ve başarımlar verir.{' '}
            <a href={pathFor('basarimlar')} onClick={linkClick(() => navigateTo(pathFor('basarimlar')))}>Hedeflere bak</a></p>}
          {mesaj && <p className="hc15-mesaj" role="status">{mesaj}</p>}
        </section>
      ) : (
        <section className="v15-card hc15-sonraki is-bitti"><b>Evrim tamamlandı.</b><p>28 basamağın hepsini açtın. Hücrelerin uyumu artık sensin.</p>{mesaj && <p className="hc15-mesaj">{mesaj}</p>}</section>
      )}

      {cag.map(([ad, liste]) => (
        <section key={ad} className="hc15-cagbolum">
          <h2 className="v15-cap">{ad} · {liste.filter((b) => acik[b.id]).length}/{liste.length}</h2>
          <ol className="hc15-liste v15-card">
            {liste.map((b) => {
              const no = basamaklar.indexOf(b) + 1;
              const durumu = acik[b.id] ? 'acik' : b === sonraki ? 'sirada' : 'kilitli';
              return (
                <li key={b.id} className={`hc15-b is-${durumu}`}>
                  <span className="hc15-no" aria-hidden>{durumu === 'acik' ? <Check /> : durumu === 'kilitli' ? <Lock /> : no}</span>
                  <span className="hc15-bt">
                    <b>{no}. {b.ad}</b>
                    {durumu === 'acik' ? <span>{b.aciklama}</span> : <span>{durumu === 'sirada' ? `${sayi(b.fiyat)} mol ile açılır` : 'Önceki basamağı aç'}</span>}
                  </span>
                </li>
              );
            })}
          </ol>
        </section>
      ))}
    </div>
  );
}

/** Basamak sayısına göre katman katman büyüyen hücre çizimi */
function Hucre({ n }: { n: number }) {
  const g = (min: number) => n >= min;
  const cok = g(22);
  return (
    <svg className="hc15-svg" viewBox="0 0 240 200" role="img" aria-label={`Hücre: ${n} basamak açık`}>
      <defs>
        <radialGradient id="hc15-sit" cx="45%" cy="40%" r="65%"><stop offset="0" stopColor="var(--color-white)" /><stop offset="1" stopColor="var(--color-accent-soft)" /></radialGradient>
      </defs>
      {/* su damlası / ilkel çorba */}
      <ellipse cx="120" cy="100" rx={g(1) ? 104 : 70} ry={g(1) ? 86 : 56} className="hc15-su" />
      {g(2) && [30, 70, 180, 205, 60, 150].map((x, i) => <circle key={i} cx={x} cy={30 + ((i * 47) % 140)} r="3" className="hc15-mol" />)}
      {cok && <circle cx="58" cy="62" r="34" className="hc15-zar is-yan" />}
      {cok && <circle cx="186" cy="146" r="28" className="hc15-zar is-yan" />}
      {g(9) && <ellipse cx="120" cy="100" rx="78" ry="64" className="hc15-duvar" />}
      {g(10) && <path d="M196 104 q14 -8 22 4 t22 2" className="hc15-kamci" />}
      {g(5) ? <ellipse cx="120" cy="100" rx="72" ry="58" className="hc15-zar" fill="url(#hc15-sit)" /> : g(3) && <circle cx="120" cy="100" r="22" className="hc15-zar is-proto" />}
      {g(4) && !g(7) && <path d="M100 100 q10 -14 20 0 t20 0" className="hc15-rna" />}
      {g(20) && <g className="hc15-iskelet">{[[60, 80, 180, 120], [70, 130, 170, 70], [120, 44, 120, 156]].map(([a, b, c, d], i) => <line key={i} x1={a} y1={b} x2={c} y2={d} />)}</g>}
      {g(16) && <path d="M70 120 q10 -10 20 0 t20 0 t20 0" className="hc15-er" />}
      {g(17) && <g className="hc15-golgi">{[0, 6, 12].map((d) => <path key={d} d={`M150 ${66 + d} q12 -8 24 0`} />)}</g>}
      {g(15) ? <g><circle cx="118" cy="96" r="22" className="hc15-cekirdek" /><circle cx="122" cy="92" r="6" className="hc15-cekirdekcik" /></g>
        : g(7) && <path d="M98 100 c8 -12 16 12 24 0 s16 12 24 0" className="hc15-dna" />}
      {g(8) && [[84, 70], [150, 120], [96, 132], [140, 64], [160, 98]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r="2.6" className="hc15-ribozom" />)}
      {g(11) && [[80, 108], [158, 134]].map(([x, y], i) => <ellipse key={i} cx={x} cy={y} rx="9" ry="5" className="hc15-kloro" />)}
      {g(18) && [[86, 84, -20], [152, 108, 25], [104, 136, 10]].map(([x, y, r], i) => <ellipse key={i} cx={x} cy={y} rx="11" ry="6" transform={`rotate(${r} ${x} ${y})`} className="hc15-mito" />)}
      {g(19) && [[138, 140], [72, 96]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r="4.5" className="hc15-lizo" />)}
      {g(25) && <path d="M28 150 l18 -10 l10 14 l14 -6" className="hc15-sinir" />}
      {g(28) && <text x="120" y="190" textAnchor="middle" className="hc15-insan">37 trilyon hücre</text>}
    </svg>
  );
}
