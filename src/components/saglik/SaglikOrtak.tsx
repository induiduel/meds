import React, { createContext, useCallback, useContext, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowRight, BookOpenCheck, Check, ChevronDown, ChevronLeft, ChevronRight, Crosshair, ExternalLink, GraduationCap,
  Presentation, RotateCcw, Shuffle, Table2, Target, X,
} from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import {
  bolumSorulari, sayi, type BaglantiCapa, type BolumBaglanti, type BolumId, type Kaynak, type SeriNokta, type SinavSorusu,
} from './saglikVeri';

/* ===============================================================================================================
 * Kaynak atfı: bölüm kendi kaynak listesini numaralar; <Atif id> o numarayı üst simge olarak gösterir.
 * =============================================================================================================== */

interface AtifBaglam { sira: Map<string, number>; kaynaklar: Record<string, Kaynak> }
const AtifCtx = createContext<AtifBaglam>({ sira: new Map(), kaynaklar: {} });

export const AtifSaglayici: React.FC<{ ids: string[]; kaynaklar: Record<string, Kaynak>; children: React.ReactNode }> = ({ ids, kaynaklar, children }) => {
  const deger = useMemo(() => {
    const sira = new Map<string, number>();
    ids.filter((id) => kaynaklar[id]).forEach((id, i) => sira.set(id, i + 1));
    return { sira, kaynaklar };
  }, [ids, kaynaklar]);
  return <AtifCtx.Provider value={deger}>{children}</AtifCtx.Provider>;
};

/** Kaynak numarası (üst simge). Tıklayınca sayfa sonundaki kaynakçaya iner. */
export const Atif: React.FC<{ id?: string; konum?: string }> = ({ id, konum }) => {
  const { sira, kaynaklar } = useContext(AtifCtx);
  if (!id) return null;
  const n = sira.get(id);
  const k = kaynaklar[id];
  if (!n || !k) return null;
  const baslik = `${k.kurum} — ${k.belge}${k.yil ? ` (${k.yil})` : ''}${konum ? ` · ${konum}` : ''}`;
  return (
    <a className="sbk-atif" href={`#sbk-kaynak-${n}`} title={baslik} aria-label={`Kaynak ${n}: ${baslik}`}>
      {n}
    </a>
  );
};

/** Çok kaynaklı serilerde ek kaynaklar tek "+N" rozetinde (numaraları ipucunda; tam liste kaynakçada) */
export const EkAtif: React.FC<{ ids: string[] }> = ({ ids }) => {
  const { sira, kaynaklar } = useContext(AtifCtx);
  const gecerli = ids.filter((id) => sira.has(id) && kaynaklar[id]);
  if (!gecerli.length) return null;
  if (gecerli.length === 1) return <Atif id={gecerli[0]} />;
  const baslik = gecerli.map((id) => `[${sira.get(id)}] ${kaynaklar[id].belge}${kaynaklar[id].yil ? ` (${kaynaklar[id].yil})` : ''}`).join('\n');
  return <a className="sbk-atif" href={`#sbk-kaynak-${sira.get(gecerli[0])}`} title={baslik} aria-label={`${gecerli.length} ek kaynak`}>+{gecerli.length}</a>;
};

export const Kaynakca: React.FC<{ dogrulanamayan?: string[] }> = ({ dogrulanamayan }) => {
  const { sira, kaynaklar } = useContext(AtifCtx);
  const liste = [...sira.entries()].sort((a, b) => a[1] - b[1]);
  if (!liste.length) return null;
  const temiz = (dogrulanamayan || []).map((x) => x.replace(/\s*\((?:[a-z]+[-_][\w-]+(?:[;,]\s*)?)+\)/gi, ''));
  return (
    <section className="sbk-kaynakca" aria-labelledby="sbk-kaynakca-h">
      <h2 id="sbk-kaynakca-h">Kaynaklar</h2>
      <p className="sbk-muted">Bu sayfadaki her sayı aşağıdaki resmî kaynaklardan alınmıştır. Değerler kaynağın yayımladığı yıla aittir.</p>
      <ol>
        {liste.map(([id, n]) => {
          const k = kaynaklar[id];
          return (
            <li key={id} id={`sbk-kaynak-${n}`}>
              <span className="sbk-kaynakca-n">{n}</span>
              <span>
                <b>{k.kurum}</b> — {k.belge}{k.yil ? ` (${k.yil})` : ''}.{' '}
                <a href={k.url} target="_blank" rel="noopener noreferrer">{alanAdi(k.url)} <ExternalLink aria-hidden /></a>
                {k.erisim && <span className="sbk-muted"> · erişim {tarihTR(k.erisim)}</span>}
              </span>
            </li>
          );
        })}
      </ol>
      {temiz.length > 0 && (
        <details className="sbk-dogrulanamayan">
          <summary>Resmî kaynakta teyit edilemediği için sayı yazılmayan konular ({temiz.length})</summary>
          <ul>{temiz.map((x, i) => <li key={i}>{x}</li>)}</ul>
        </details>
      )}
    </section>
  );
};

const alanAdi = (u: string) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return u; } };
export const tarihTR = (s: string) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s);
  return m ? `${m[3]}.${m[2]}.${m[1]}` : s;
};

/* ===============================================================================================================
 * Metin: **kalın**, ==vurgu==, "- " maddeler ve satır sonları (ders notu ve açıklamalardaki biçim)
 * =============================================================================================================== */

const satirIci = (s: string): React.ReactNode[] =>
  s.split(/(\*\*[^*]+\*\*|==[^=]+==)/g).map((p, i) => {
    if (p.startsWith('**') && p.endsWith('**')) return <strong key={i}>{p.slice(2, -2)}</strong>;
    if (p.startsWith('==') && p.endsWith('==')) return <mark key={i}>{p.slice(2, -2)}</mark>;
    return <React.Fragment key={i}>{p}</React.Fragment>;
  });

export const MiniMetin: React.FC<{ metin: string; className?: string }> = ({ metin, className }) => {
  const bloklar: React.ReactNode[] = [];
  let liste: string[] = [];
  const bosalt = () => {
    if (liste.length) bloklar.push(<ul key={`u${bloklar.length}`}>{liste.map((m, i) => <li key={i}>{satirIci(m)}</li>)}</ul>);
    liste = [];
  };
  for (const ham of metin.split('\n')) {
    const s = ham.trim();
    if (!s) { bosalt(); continue; }
    const m = /^(?:[-•*]|\d+[.)])\s+(.*)$/.exec(s);
    if (m) { liste.push(m[1]); continue; }
    bosalt();
    bloklar.push(<p key={`p${bloklar.length}`}>{satirIci(s.replace(/^#+\s*/, ''))}</p>);
  }
  bosalt();
  return <div className={`sbk-metin ${className || ''}`}>{bloklar}</div>;
};

/* ===============================================================================================================
 * İç bağlantı (uygulama içi gezinme) ve "Derste" çapaları
 * =============================================================================================================== */

export const IcBag: React.FC<{ to: string; className?: string; children: React.ReactNode; title?: string }> = ({ to, className, children, title }) => (
  <a href={to} className={className} title={title} onClick={linkClick(() => navigateTo(to))}>{children}</a>
);

export const desteYolu = (id: string, slayt?: number) => `${pathFor('learn')}/${encodeURIComponent(id)}${slayt ? `?slide=${slayt}` : ''}`;

/** Veri bloğunun dersteki karşılığı: "Derste · Ana Çocuk Sağlığı İzlemi · Slayt 26" */
export const DersteCapa: React.FC<{ capalar?: BaglantiCapa[] }> = ({ capalar }) => {
  if (!capalar?.length) return null;
  return (
    <div className="sbk-capa" role="list" aria-label="Bu konunun işlendiği ders slaytları">
      <span className="sbk-capa-l"><Presentation aria-hidden /> Derste</span>
      {capalar.slice(0, 2).map((c) => (
        <IcBag key={`${c.deste}-${c.slayt}`} to={desteYolu(c.deste, c.slayt)} className="sbk-capa-a" title={c.baslik}>
          <span role="listitem">{c.kisa} · <b>Slayt {c.slayt}</b></span>
        </IcBag>
      ))}
    </div>
  );
};

/* ===============================================================================================================
 * Yapı taşları: Blok (kart), Kpi (gösterge kutusu), Rozet
 * =============================================================================================================== */

export const Blok: React.FC<{
  baslik: React.ReactNode; ikon?: React.ElementType; alt?: React.ReactNode; capalar?: BaglantiCapa[];
  arac?: React.ReactNode; genis?: boolean; id?: string; children: React.ReactNode; className?: string;
}> = ({ baslik, ikon: Ikon, alt, capalar, arac, genis, id, children, className }) => (
  <section className={`sbk-blok ${genis ? 'is-genis' : ''} ${className || ''}`} id={id}>
    <header className="sbk-blok-h">
      <div className="sbk-blok-t">
        {Ikon && <span className="sbk-blok-ic"><Ikon aria-hidden /></span>}
        <div>
          <h3>{baslik}</h3>
          {alt && <p>{alt}</p>}
        </div>
      </div>
      {arac && <div className="sbk-blok-arac">{arac}</div>}
    </header>
    <div className="sbk-blok-g">{children}</div>
    <DersteCapa capalar={capalar} />
  </section>
);

export const Kpi: React.FC<{
  ad: string; deger: React.ReactNode; birim?: string; yil?: number | string; kaynak?: string; konum?: string;
  not?: React.ReactNode; seri?: SeriNokta[]; ton?: 'ok' | 'warn' | 'bad'; ipucu?: string; ek?: string[];
}> = ({ ad, deger, birim, yil, kaynak, konum, not, seri, ton, ipucu, ek }) => (
  <div className={`sbk-kpi ${ton ? `is-${ton}` : ''}`} title={ipucu}>
    <span className="sbk-kpi-ad">{ad}</span>
    <span className="sbk-kpi-d">
      <b data-num>{deger}</b>
      {birim && <small>{birim}</small>}
      <Atif id={kaynak} konum={konum} />
      {ek && ek.length > 0 && <EkAtif ids={ek} />}
    </span>
    <span className="sbk-kpi-alt">
      {yil != null && <span>{yil}</span>}
      {not && <span>{not}</span>}
    </span>
    {seri && seri.length > 2 && <Kivilcim seri={seri} />}
  </div>
);

export const Rozet: React.FC<{ ton?: 'accent' | 'ok' | 'warn' | 'bad' | 'ai' | 'clinic' | 'nötr'; children: React.ReactNode }> = ({ ton = 'nötr', children }) => (
  <span className={`sbk-rozet t-${ton === 'nötr' ? 'n' : ton}`}>{children}</span>
);

/* ===============================================================================================================
 * Grafikler (tek seri vurgu rengi; iki seri vurgu + nötr). Üzerine gelince ipucu, klavyeyle gezinme, tablo görünümü.
 * =============================================================================================================== */

function useGenislik<T extends HTMLElement>(): [React.RefObject<T | null>, number] {
  const ref = useRef<T>(null);
  const [w, setW] = useState(0);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    setW(el.clientWidth);
    if (typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => setW(el.clientWidth));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, w];
}

// Yalnız tek yıllık noktalar ("2002-2003" gibi dönem değerleri eksende yer tutmaz)
const sirali = (s: SeriNokta[]) => [...s].filter((x) => typeof x.deger === 'number' && isFinite(x.deger) && /^\d{4}$/.test(String(x.yil))).sort((a, b) => Number(a.yil) - Number(b.yil));

function guzelOlcek(min: number, max: number, adim = 4) {
  if (min === max) { const d = Math.abs(min) || 1; min -= d * 0.5; max += d * 0.5; }
  const ham = (max - min) / adim;
  const us = Math.pow(10, Math.floor(Math.log10(ham)));
  const k = [1, 2, 2.5, 5, 10].find((x) => x * us >= ham) || 10;
  const a = k * us;
  const lo = Math.floor(min / a) * a;
  const hi = Math.ceil(max / a) * a;
  const t: number[] = [];
  for (let v = lo; v <= hi + a / 2; v += a) t.push(+v.toFixed(6));
  return { lo, hi, t };
}

/** Küçük eğilim çizgisi (gösterge kutusunda); süs değil — son yönü gösterir, ipucu yok */
export const Kivilcim: React.FC<{ seri: SeriNokta[] }> = ({ seri }) => {
  // Yalnız son kesintisiz dönem (ör. 2013→2025); arada yıllarca veri yoksa eğilim çizgisi yanıltmasın
  const tum = sirali(seri);
  let bas = tum.length - 1;
  while (bas > 0 && Number(tum[bas].yil) - Number(tum[bas - 1].yil) <= 2) bas--;
  const s = tum.slice(bas).slice(-12);
  if (s.length < 3) return null;
  const W = 96, H = 26;
  const vs = s.map((x) => x.deger);
  const mn = Math.min(...vs), mx = Math.max(...vs);
  const y = (v: number) => (mx === mn ? H / 2 : H - 3 - ((v - mn) / (mx - mn)) * (H - 6));
  const x = (i: number) => 2 + (i / (s.length - 1)) * (W - 4);
  const d = s.map((p, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.deger).toFixed(1)}`).join('');
  return (
    <svg className="sbk-kivilcim" viewBox={`0 0 ${W} ${H}`} aria-hidden>
      <path d={d} />
      <circle cx={x(s.length - 1)} cy={y(s[s.length - 1].deger)} r={2.6} />
    </svg>
  );
};

export interface CizgiSeri { ad: string; seri: SeriNokta[]; ton?: 'vurgu' | 'notr' }

/** Yıllara göre çizgi grafiği: 1–2 seri, tek y ekseni, artı imleci + ipucu, son değere doğrudan etiket */
export const CizgiGrafik: React.FC<{ seriler: CizgiSeri[]; birim?: string; yukseklik?: number; baslik: string; ondalik?: number; sifirdan?: boolean }> = ({
  seriler, birim, yukseklik = 210, baslik, ondalik, sifirdan,
}) => {
  const [ref, w] = useGenislik<HTMLDivElement>();
  const [tablo, setTablo] = useState(false);
  const [imlec, setImlec] = useState<number | null>(null);
  const ss = seriler.map((s) => ({ ...s, seri: sirali(s.seri) })).filter((s) => s.seri.length);
  const yillar = [...new Set(ss.flatMap((s) => s.seri.map((p) => Number(p.yil))))].sort((a, b) => a - b);
  if (!ss.length || !yillar.length) return null;
  const tum = ss.flatMap((s) => s.seri.map((p) => p.deger));
  const { lo, hi, t } = guzelOlcek(sifirdan ? Math.min(0, ...tum) : Math.min(...tum), Math.max(...tum));
  const sol = 44, sag = 56, ust = 12, alt = 26;
  const W = Math.max(w, 260), H = yukseklik;
  const x = (yil: number) => (yillar.length === 1 ? sol + (W - sol - sag) / 2 : sol + ((yil - yillar[0]) / (yillar[yillar.length - 1] - yillar[0])) * (W - sol - sag));
  const y = (v: number) => ust + (1 - (v - lo) / (hi - lo || 1)) * (H - ust - alt);
  const xEtiketAdim = Math.max(1, Math.ceil(yillar.length / Math.max(2, Math.floor((W - sol - sag) / 46))));
  const fmt = (v: number) => sayi(v, ondalik);
  const yakin = (px: number) => yillar.reduce((b, yl) => (Math.abs(x(yl) - px) < Math.abs(x(b) - px) ? yl : b), yillar[0]);
  const imlecYil = imlec;
  const tusa = (e: React.KeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    const i = imlecYil == null ? yillar.length - 1 : yillar.indexOf(imlecYil);
    const j = Math.min(yillar.length - 1, Math.max(0, i + (e.key === 'ArrowRight' ? 1 : -1)));
    setImlec(yillar[j]);
  };
  return (
    <figure className="sbk-grafik">
      <figcaption className="sbk-grafik-h">
        <span>{baslik}{birim && <small> · {birim}</small>}</span>
        <span className="sbk-grafik-arac">
          {ss.length > 1 && (
            <span className="sbk-lejant">
              {ss.map((s) => <span key={s.ad} className={s.ton === 'notr' ? 'is-notr' : ''}><i aria-hidden />{s.ad}</span>)}
            </span>
          )}
          <button type="button" className="sbk-ikon-btn" onClick={() => setTablo((v) => !v)} aria-pressed={tablo} title={tablo ? 'Grafiği göster' : 'Tablo olarak göster'}>
            <Table2 aria-hidden />
          </button>
        </span>
      </figcaption>
      {tablo ? (
        <div className="sbk-tablo-kap">
          <table className="sbk-tablo">
            <thead><tr><th>Yıl</th>{ss.map((s) => <th key={s.ad}>{s.ad}</th>)}</tr></thead>
            <tbody>
              {yillar.slice().reverse().map((yl) => (
                <tr key={yl}><td>{yl}</td>{ss.map((s) => { const p = s.seri.find((q) => Number(q.yil) === yl); return <td key={s.ad} data-num>{p ? fmt(p.deger) : '—'}</td>; })}</tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div ref={ref} className="sbk-grafik-g">
          {w > 0 && (
            <svg
              width={W} height={H} role="img" tabIndex={0} onKeyDown={tusa}
              aria-label={`${baslik}: ${ss.map((s) => `${s.ad} ${s.seri[0].yil} yılında ${fmt(s.seri[0].deger)}, ${s.seri[s.seri.length - 1].yil} yılında ${fmt(s.seri[s.seri.length - 1].deger)}`).join('; ')}`}
              onPointerMove={(e) => { const r = (e.currentTarget as SVGSVGElement).getBoundingClientRect(); setImlec(yakin(e.clientX - r.left)); }}
              onPointerLeave={() => setImlec(null)}
              onBlur={() => setImlec(null)}
            >
              {t.map((v) => (
                <g key={v} className="sbk-eksen">
                  <line x1={sol} x2={W - sag + 8} y1={y(v)} y2={y(v)} />
                  <text x={sol - 6} y={y(v)} dy="0.32em" textAnchor="end">{sayi(v)}</text>
                </g>
              ))}
              {yillar.map((yl, i) => (i % xEtiketAdim === 0 || i === yillar.length - 1) && (
                <text key={yl} className="sbk-eksen-x" x={x(yl)} y={H - 6} textAnchor="middle">{yl}</text>
              ))}
              {imlecYil != null && <line className="sbk-imlec" x1={x(imlecYil)} x2={x(imlecYil)} y1={ust} y2={H - alt} />}
              {ss.map((s) => {
                // Yıllık seride boşluk (ör. 2002 → 2013) varsa çizgi kesilir: aradaki yıllar uydurulmuş gibi görünmesin
                const adimlar = s.seri.slice(1).map((p, i) => Number(p.yil) - Number(s.seri[i].yil)).sort((m, n) => m - n);
                const tipik = adimlar.length ? adimlar[Math.floor(adimlar.length / 2)] : 1;
                const d = s.seri.map((p, i) => {
                  const kopuk = i > 0 && Number(p.yil) - Number(s.seri[i - 1].yil) > tipik * 1.5;
                  return `${i === 0 || kopuk ? 'M' : 'L'}${x(Number(p.yil)).toFixed(1)},${y(p.deger).toFixed(1)}`;
                }).join('');
                const son = s.seri[s.seri.length - 1];
                return (
                  <g key={s.ad} className={`sbk-seri ${s.ton === 'notr' ? 'is-notr' : ''}`}>
                    <path d={d} />
                    {s.seri.map((p) => (
                      <circle key={String(p.yil)} cx={x(Number(p.yil))} cy={y(p.deger)} r={Number(p.yil) === imlecYil ? 5 : s.seri.length > 14 ? 0 : 3.5} />
                    ))}
                    <text className="sbk-son" x={x(Number(son.yil)) + 8} y={y(son.deger)} dy="0.32em">{fmt(son.deger)}</text>
                  </g>
                );
              })}
            </svg>
          )}
          {imlecYil != null && w > 0 && (
            <div className="sbk-ipucu" style={{ left: Math.min(Math.max(x(imlecYil), 70), W - 70), top: 4 }} role="status">
              <b>{imlecYil}</b>
              {ss.map((s) => { const p = s.seri.find((q) => Number(q.yil) === imlecYil); return p ? <span key={s.ad}>{ss.length > 1 && <i className={s.ton === 'notr' ? 'is-notr' : ''} aria-hidden />}{ss.length > 1 ? `${s.ad}: ` : ''}<b data-num>{fmt(p.deger)}</b>{birim ? ` ${birim}` : ''}</span> : null; })}
            </div>
          )}
        </div>
      )}
    </figure>
  );
};

/** Yatay çubuk listesi (büyüklük karşılaştırması). Değer metni mürekkep renginde, çubuk vurgu renginde. */
export const CubukListe: React.FC<{
  kalemler: { ad: React.ReactNode; deger: number; etiket?: string; ikinci?: number; anahtar?: string; ipucu?: string; not?: string }[];
  birim?: string; ikinciAd?: string; birinciAd?: string; ondalik?: number; enCok?: number;
}> = ({ kalemler, birim, ikinciAd, birinciAd, ondalik, enCok }) => {
  const mx = enCok ?? Math.max(...kalemler.flatMap((k) => [k.deger, k.ikinci ?? 0]), 0.0001);
  return (
    <div className="sbk-cubuk">
      {ikinciAd && (
        <div className="sbk-lejant">
          <span><i aria-hidden />{birinciAd}</span>
          <span className="is-notr"><i aria-hidden />{ikinciAd}</span>
        </div>
      )}
      {kalemler.map((k, i) => (
        <div className="sbk-cubuk-s" key={k.anahtar || i} title={k.ipucu || `${typeof k.ad === 'string' ? k.ad : ''}: ${sayi(k.deger, ondalik)}${birim ? ` ${birim}` : ''}`}>
          <span className="sbk-cubuk-ad">{k.ad}{k.not && <small className="sbk-cubuk-not">{k.not}</small>}</span>
          <span className="sbk-cubuk-izler">
            <span className="sbk-cubuk-iz"><i style={{ width: `${(k.deger / mx) * 100}%` }} /><b data-num>{k.etiket ?? sayi(k.deger, ondalik)}{birim && !k.etiket ? <small> {birim}</small> : null}</b></span>
            {k.ikinci != null && (
              <span className="sbk-cubuk-iz is-notr"><i style={{ width: `${(k.ikinci / mx) * 100}%` }} /><b data-num>{sayi(k.ikinci, ondalik)}</b></span>
            )}
          </span>
        </div>
      ))}
    </div>
  );
};

/* ===============================================================================================================
 * Ders paneli: sınav istatistiği, desteler, kazanımlar, spotlar
 * =============================================================================================================== */

const kazanimYolu = (kurul: number, anahtar: string) => `${pathFor('kazanimlar')}?${kurul !== 1 ? `kurul=${kurul}&` : ''}konu=${encodeURIComponent(anahtar)}`;
export const kazanimBag = kazanimYolu;

export const DersPaneli: React.FC<{ b?: BolumBaglanti; onSina?: () => void }> = ({ b, onSina }) => {
  const [acikKz, setAcikKz] = useState<string | null>(null);
  if (!b) return null;
  // Yalnız öğretim yılı biçimindekiler ("2023-2024"); "Kategorisiz", "Bütünleme" gibi etiketler çubuğa girmez
  const yillar = Object.entries(b.yillar).filter(([y]) => /^20\d\d-20\d\d$/.test(y)).sort((a, c) => c[0].localeCompare(a[0])).slice(0, 6).reverse();
  const yMax = Math.max(1, ...yillar.map(([, n]) => n));
  const konular = Object.entries(b.konu_dagilimi).slice(0, 6);
  const anaDesteler = b.desteler.filter((d) => !d.ek);
  const ekDesteler = b.desteler.filter((d) => d.ek);
  return (
    <div className="sbk-ders">
      <section className="sbk-ders-k sbk-sinav-ozet">
        <h3><Target aria-hidden /> Sınavda</h3>
        <p className="sbk-sinav-n"><b data-num>{b.soru_sayisi}</b> çıkmış soru bu bölümün konularından</p>
        {yillar.length > 0 && (
          <div className="sbk-yil-cubuk" aria-label="Sınav yılına göre soru sayısı">
            {yillar.map(([y, n]) => (
              <span key={y} title={`${y}: ${n} soru`}>
                <i style={{ height: `${Math.max(8, (n / yMax) * 100)}%` }} />
                <small>{y.replace(/^20(\d\d)-20(\d\d)$/, '$1-$2')}</small>
              </span>
            ))}
          </div>
        )}
        {konular.length > 0 && (
          <ul className="sbk-konu-l">
            {konular.map(([k, n]) => <li key={k}><span>{k}</span><b data-num>{n}</b></li>)}
          </ul>
        )}
        {onSina && b.havuz > 0 && (
          <button type="button" className="sbk-btn is-dolu" onClick={onSina}><Crosshair aria-hidden /> Kendini sına</button>
        )}
      </section>

      {(anaDesteler.length > 0 || ekDesteler.length > 0) && (
        <section className="sbk-ders-k">
          <h3><GraduationCap aria-hidden /> Öğren desteleri</h3>
          <ul className="sbk-deste-l">
            {[...anaDesteler, ...ekDesteler].slice(0, 6).map((d) => (
              <li key={d.id}>
                <IcBag to={desteYolu(d.id)} className="sbk-deste-a" title={d.baslik}>
                  <span className="sbk-deste-t">{d.kisa}</span>
                  <span className="sbk-deste-m">{d.ders} · {d.slayt} slayt{d.pdf ? ' · PDF' : ''}{d.ek ? ' · ilişkili' : ''}</span>
                  <ChevronRight aria-hidden />
                </IcBag>
              </li>
            ))}
          </ul>
        </section>
      )}

      {b.kazanimlar.length > 0 && (
        <section className="sbk-ders-k">
          <h3><BookOpenCheck aria-hidden /> Kazanımlar</h3>
          <ul className="sbk-kz-l">
            {b.kazanimlar.map((k) => {
              const acik = acikKz === k.anahtar;
              return (
                <li key={`${k.kurul}-${k.anahtar}`} className={acik ? 'is-acik' : ''}>
                  <button type="button" onClick={() => setAcikKz(acik ? null : k.anahtar)} aria-expanded={acik}>
                    <span><small>Kurul {k.kurul} · {k.ders}</small>{k.konu}</span>
                    <span className="sbk-kz-n" title="Kazanım sayısı">{k.kazanimlar.length}</span>
                    <ChevronDown aria-hidden />
                  </button>
                  {acik && (
                    <div className="sbk-kz-ic">
                      <ol>{k.kazanimlar.slice(0, 8).map((z) => <li key={z.id}>{z.metin}</li>)}</ol>
                      <IcBag to={kazanimYolu(k.kurul, k.anahtar)} className="sbk-bag">Kazanımlarda aç <ArrowRight aria-hidden /></IcBag>
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {b.spotlar.length > 0 && (
        <section className="sbk-ders-k">
          <h3><Crosshair aria-hidden /> Sınav spotları</h3>
          <ul className="sbk-spot-l">
            {b.spotlar.slice(0, 4).map((s) => (
              <li key={s.id}>
                <IcBag to={`${pathFor('spots')}?id=${encodeURIComponent(s.id)}`} className="sbk-spot-a">
                  <b>{s.baslik}</b>
                  <span><MiniSatir metin={s.spot} /></span>
                </IcBag>
              </li>
            ))}
          </ul>
          {b.spotlar.length > 4 && <IcBag to={pathFor('spots')} className="sbk-bag">Tüm spotlar <ArrowRight aria-hidden /></IcBag>}
        </section>
      )}
    </div>
  );
};

const MiniSatir: React.FC<{ metin: string }> = ({ metin }) => <>{satirIci(metin.replace(/\n+/g, ' '))}</>;

/* ===============================================================================================================
 * Kendini sına: bölümün çıkmış sorularından tek tek; cevap anında açıklama + çıkmışlarda aç
 * =============================================================================================================== */

const SINA_ANAHTAR = 'medsoru_saglik_sina_v1';
const okuSina = (): Record<string, string> => { try { return JSON.parse(localStorage.getItem(SINA_ANAHTAR) || '{}') || {}; } catch { return {}; } };
const yazSina = (m: Record<string, string>) => { try { localStorage.setItem(SINA_ANAHTAR, JSON.stringify(m)); } catch { /* özel pencere */ } };

const karistir = <T,>(a: T[], tohum: number) => {
  const r = a.slice();
  let s = tohum || 1;
  for (let i = r.length - 1; i > 0; i--) {
    s = (s * 9301 + 49297) % 233280;
    const j = Math.floor((s / 233280) * (i + 1));
    [r[i], r[j]] = [r[j], r[i]];
  }
  return r;
};

export const KendiniSina: React.FC<{ bolum: BolumId; baslik: string; toplam: number }> = ({ bolum, baslik, toplam }) => {
  const [sorular, setSorular] = useState<SinavSorusu[] | null>(null);
  const [tohum, setTohum] = useState(0);
  const [i, setI] = useState(0);
  const [cevaplar, setCevaplar] = useState<Record<string, string>>(okuSina);
  const [konu, setKonu] = useState('');
  useEffect(() => {
    let iptal = false;
    setSorular(null); setI(0); setKonu('');
    bolumSorulari(bolum).then((s) => { if (!iptal) setSorular(s); });
    return () => { iptal = true; };
  }, [bolum]);
  const konular = useMemo(() => {
    const m = new Map<string, number>();
    for (const q of sorular || []) if (q.konu) m.set(q.konu, (m.get(q.konu) || 0) + 1);
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [sorular]);
  const liste = useMemo(() => {
    const l = (sorular || []).filter((q) => !konu || q.konu === konu);
    return tohum ? karistir(l, tohum) : l;
  }, [sorular, konu, tohum]);
  const q = liste[Math.min(i, Math.max(0, liste.length - 1))];
  const sec = useCallback((id: string, k: string) => {
    setCevaplar((p) => {
      if (p[id]) return p;
      const n = { ...p, [id]: k };
      yazSina(n);
      return n;
    });
  }, []);
  const sifirla = () => {
    const n = { ...cevaplar };
    for (const s of liste) delete n[s.id];
    setCevaplar(n); yazSina(n); setI(0);
  };
  const cozulen = liste.filter((s) => cevaplar[s.id]);
  const dogru = cozulen.filter((s) => cevaplar[s.id] === s.dogru).length;

  if (!sorular) return <div className="sbk-sina is-yuk" aria-busy="true"><span className="ui-skel" style={{ height: 160, display: 'block', borderRadius: 12 }} /></div>;
  if (!liste.length || !q) return null;
  const secilen = cevaplar[q.id];
  return (
    <section className="sbk-sina" id="sbk-sina" aria-label={`${baslik}: çıkmış sorularla kendini sına`}>
      <header className="sbk-sina-h">
        <div>
          <h3><Crosshair aria-hidden /> Kendini sına</h3>
          <p>{baslik} konularından {toplam} çıkmış sorunun en sağlam {sorular.length} tanesi · çözülen {cozulen.length}, doğru {dogru}</p>
        </div>
        <div className="sbk-sina-arac">
          {konular.length > 1 && (
            <select value={konu} onChange={(e) => { setKonu(e.target.value); setI(0); }} aria-label="Konuya göre süz" className="sbk-sec">
              <option value="">Tüm konular ({sorular.length})</option>
              {konular.map(([k, n]) => <option key={k} value={k}>{k} ({n})</option>)}
            </select>
          )}
          <button type="button" className="sbk-ikon-btn" onClick={() => { setTohum(Date.now() % 100000); setI(0); }} title="Karıştır" aria-label="Soruları karıştır"><Shuffle aria-hidden /></button>
          <button type="button" className="sbk-ikon-btn" onClick={sifirla} title="Cevapları sıfırla" aria-label="Bu listedeki cevapları sıfırla"><RotateCcw aria-hidden /></button>
        </div>
      </header>
      <div className="sbk-ilerleme" aria-hidden><i style={{ width: `${((i + 1) / liste.length) * 100}%` }} /></div>
      <article className="sbk-soru">
        <p className="sbk-soru-m">
          <span>Soru {i + 1} / {liste.length}</span>
          {q.yil && /\d{4}/.test(q.yil) && <Rozet>{q.yil}</Rozet>}
          {q.kurul ? <Rozet>Kurul {q.kurul}</Rozet> : null}
          {q.konu && <Rozet ton="clinic">{q.konu}</Rozet>}
        </p>
        <MiniMetin metin={q.kok} className="sbk-soru-kok" />
        <div className="sbk-secenek" role="group" aria-label="Seçenekler">
          {q.secenekler.map((o) => {
            const durum = !secilen ? '' : o.k === q.dogru ? 'is-dogru' : o.k === secilen ? 'is-yanlis' : 'is-soluk';
            return (
              <button key={o.k} type="button" className={durum} onClick={() => sec(q.id, o.k)} disabled={!!secilen} aria-pressed={secilen === o.k}>
                <span className="sbk-secenek-k">{o.k}</span>
                <span>{o.t}</span>
                {secilen && o.k === q.dogru && <Check aria-label="Doğru cevap" />}
                {secilen && o.k === secilen && o.k !== q.dogru && <X aria-label="Senin cevabın" />}
              </button>
            );
          })}
        </div>
        {secilen && (
          <div className={`sbk-aciklama ${secilen === q.dogru ? 'is-dogru' : 'is-yanlis'}`} role="status">
            <b>{secilen === q.dogru ? 'Doğru.' : `Yanlış — doğru cevap ${q.dogru}.`}</b>
            {q.aciklama && <MiniMetin metin={q.aciklama} />}
            <IcBag to={`${pathFor('past_exams')}/${encodeURIComponent(q.id)}`} className="sbk-bag">Çıkmış sorularda aç (şık analizi, tartışma) <ArrowRight aria-hidden /></IcBag>
          </div>
        )}
        <footer className="sbk-soru-f">
          <button type="button" className="sbk-btn" onClick={() => setI((x) => Math.max(0, x - 1))} disabled={i === 0}><ChevronLeft aria-hidden /> Önceki</button>
          <button type="button" className="sbk-btn is-dolu" onClick={() => setI((x) => Math.min(liste.length - 1, x + 1))} disabled={i >= liste.length - 1}>Sonraki <ChevronRight aria-hidden /></button>
        </footer>
      </article>
    </section>
  );
};
