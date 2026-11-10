/**
 * Kural sayfalarının görsel anlatım parçaları: taş tanıtımı, tur akışı, Pişti sahneleri, Go / Çizgi Yarışı / XOX şemaları.
 * Şemalar motor kurallarını resimler (services/masa/motor/*); kural değişirse metinle birlikte güncellenir.
 */
import React from 'react';
import { Check, X } from 'lucide-react';
import { PISTI_RENK_SIMGE, degerYazi, type PistiRenk } from '../../../services/masa/motor/pisti';
import { OYUNCU_SINIR, OYUN_ADI, type OyunTur } from '../../../services/masa/tipler';
import { OyunResmi, TasOrnek } from '../kabukOrtak';
import { kategoriAdi, oyuncuYazi } from '../oyunKatalog';
import { Kart as PistiKartGorsel } from '../pisti/Kart';
import type { T } from './ortak';
import '../../../styles/masa/pisti.css';
import '../../../styles/masa/kurallar-gorsel.css';

const Alt = ({ ad, iyi }: { ad: React.ReactNode; iyi?: boolean }) => (
  <figcaption>{iyi !== undefined && (iyi ? <Check size={15} /> : <X size={15} />)} <span>{ad}</span></figcaption>
);
const sinif = (iyi?: boolean) => `mk-ornek mk-sema${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`;

/* ---------------- oyun künyesi ---------------- */

/** Kural sayfasının başı: oyunun çizimi, kaç kişi, neyle oynanır, amaç */
export function Kunye({ tur, malzeme, amac }: { tur: OyunTur; malzeme: string; amac: string }) {
  return (
    <header className="mk-kunye">
      <span className="mk-kunye-resim"><OyunResmi tur={tur} /></span>
      <div className="mk-kunye-metin">
        <h2>{OYUN_ADI[tur]}</h2>
        <div className="mk-kunye-cipler">
          <span>{kategoriAdi(tur)}</span>
          <span>{oyuncuYazi(OYUNCU_SINIR[tur])}</span>
          <span>{malzeme}</span>
          <span className="is-amac">Amaç: {amac}</span>
        </div>
      </div>
    </header>
  );
}

/* ---------------- okey taşları ---------------- */

const SEKIL = ['daire', 'baklava', 'üçgen', 'kare'];

/** "Taşları tanı": 1–13, dört renk + şekil, her taştan iki tane */
export function TasTanitim({ rk, ek }: { rk: string[]; ek?: React.ReactNode }) {
  return (
    <div className="mk-tanit" role="group" aria-label="Taşları tanı">
      <div className="mk-tanit-satir">
        <span className="mk-tanit-ad"><b>Sayılar</b>1’den 13’e</span>
        <div className="mk-tanit-taslar is-kaydir">{Array.from({ length: 13 }, (_, i) => <TasOrnek key={i} s={i + 1} r={2} renkler={rk} boy={23} />)}</div>
      </div>
      <div className="mk-tanit-satir">
        <span className="mk-tanit-ad"><b>Dört renk</b>her rengin kendi şekli var</span>
        <div className="mk-tanit-taslar">
          {([0, 1, 2, 3] as const).map((r) => (
            <span key={r} className="mk-tanit-tas"><TasOrnek s={7} r={r} renkler={rk} boy={30} /><small>{SEKIL[r]}</small></span>
          ))}
        </div>
      </div>
      <div className="mk-tanit-satir">
        <span className="mk-tanit-ad"><b>İkişer tane</b>13 sayı × 4 renk × 2</span>
        <div className="mk-tanit-taslar">
          <TasOrnek s={9} r={0} renkler={rk} boy={30} /><TasOrnek s={9} r={0} renkler={rk} boy={30} />
          <span className="mk-tanit-esit">= 104 taş</span>
        </div>
      </div>
      {ek}
    </div>
  );
}

/** TasTanitim'e eklenen satır (okey, joker gibi özel taşlar) */
export function TanitSatir({ ad, alt, children }: { ad: string; alt: string; children: React.ReactNode }) {
  return (
    <div className="mk-tanit-satir">
      <span className="mk-tanit-ad"><b>{ad}</b>{alt}</span>
      <div className="mk-tanit-taslar">{children}</div>
    </div>
  );
}

/** Etiketli taş dizisi: zincir uçları, masa–el ayrımı gibi anlatımlar için */
export function TasDizi({ t, rk, etiket, ad, iyi }: { t: T[]; rk: string[]; etiket?: Record<number, string>; ad: string; iyi?: boolean }) {
  return (
    <figure className={sinif(iyi)}>
      <div className="mk-dizi">
        {t.map(([s, r], i) => (
          <span key={i} className={`mk-dizi-tas${etiket?.[i] ? ' is-etiketli' : ''}`}>
            <TasOrnek s={s} r={r} renkler={rk} boy={30} />
            <small>{etiket?.[i] || ' '}</small>
          </span>
        ))}
      </div>
      <Alt ad={ad} iyi={iyi} />
    </figure>
  );
}

/* ---------------- tur akışı ---------------- */

export interface AkisAdim { ikon: React.ReactNode; ad: string; metin: string; /** önceki adımla bağ: 'sonra' ok, 'yada' seçenek */ bag?: 'sonra' | 'yada' }

/** Bir turun adımları: simge + başlık + tek cümle; adımlar okla ya da "ya da" ile bağlanır */
export function Akis({ baslik = 'Bir tur nasıl geçer', adimlar }: { baslik?: string; adimlar: AkisAdim[] }) {
  return (
    <div className="mk-akis-kutu">
      <span className="mk-akis-baslik">{baslik}</span>
      <ol className="mk-akis">
        {adimlar.map((a, i) => (
          <li key={a.ad} className={i > 0 ? `is-${a.bag || 'sonra'}` : ''}>
            {i > 0 && <i className="mk-akis-bag" aria-hidden="true">{a.bag === 'yada' ? 'ya da' : '→'}</i>}
            <span className="mk-akis-adim">
              <span className="mk-akis-ikon" aria-hidden="true">{a.ikon}</span>
              <b>{a.ad}</b>
              <span>{a.metin}</span>
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}

/* ---------------- Pişti ---------------- */

type PK = [PistiRenk, number];
const pk = ([renk, d]: PK, i: number) => ({ id: -1 - i, renk, d });
const pkYazi = ([renk, d]: PK) => `${degerYazi(d)}${PISTI_RENK_SIMGE[renk]}`;

/** Yerdeki kart(lar) + attığın kart → sonuç */
export function PistiSahne({ yer, at, sonuc, ad, iyi }: { yer: PK[]; at: PK; sonuc: string; ad: string; iyi?: boolean }) {
  return (
    <figure className={sinif(iyi)} aria-label={`Yerde ${yer.map(pkYazi).join(', ') || 'kart yok'}; atılan ${pkYazi(at)}: ${sonuc}`}>
      <div className="mk-pisti">
        <span className="mk-pisti-grup">
          <span className="mk-pisti-yer">
            {yer.length ? yer.map((k, i) => <PistiKartGorsel key={i} kart={pk(k, i)} style={{ marginLeft: i ? 'calc(var(--pk-w) * -.62)' : 0 }} />) : <span className="mk-pisti-bos" />}
          </span>
          <small>Yerde</small>
        </span>
        <b className="mk-pisti-arti" aria-hidden="true">+</b>
        <span className="mk-pisti-grup"><PistiKartGorsel kart={pk(at, 9)} /><small>Attığın</small></span>
        <b className="mk-pisti-sonuc">{sonuc}</b>
      </div>
      <Alt ad={ad} iyi={iyi} />
    </figure>
  );
}

/** Puan getiren kartlar */
export function PistiPuanlar() {
  const kartlar: [PK, string, string][] = [[['maca', 1], '+1', 'Her As'], [['kupa', 11], '+1', 'Her Vale'], [['sinek', 2], '+2', 'Sinek 2'], [['karo', 10], '+3', 'Karo 10']];
  return (
    <div className="mk-ornekler">
      {kartlar.map(([k, puan, ad], i) => (
        <figure key={ad} className="mk-ornek mk-sema">
          <div className="mk-pisti"><PistiKartGorsel kart={pk(k, i)} /><b className="mk-pisti-sonuc">{puan}</b></div>
          <Alt ad={ad} />
        </figure>
      ))}
    </div>
  );
}

/* ---------------- Go ---------------- */

type GoTas = [number, number, 'S' | 'B', boolean?];
/** o: özgürlük · h: buraya oyna · x: konamaz · ko: ko noktası · aS / aB: siyahın / beyazın alanı */
type GoIsaret = [number, number, 'o' | 'h' | 'x' | 'ko' | 'aS' | 'aB'];

/** Küçük Go tahtası (varsayılan 5×5); taşlar kesişimlerde, işaretler anlatılan kuralı gösterir. Soluk taş: alınacak / alınmış taş */
export function GoSema({ n = 5, taslar, isaret = [], ad, iyi }: { n?: number; taslar: GoTas[]; isaret?: GoIsaret[]; ad: string; iyi?: boolean }) {
  const H = 20, K = 15, boy = K * 2 + H * (n - 1);
  const p = (i: number) => K + i * H;
  return (
    <figure className={sinif(iyi)}>
      <svg className="mk-go" viewBox={`0 0 ${boy} ${boy}`} width={boy * 1.15} height={boy * 1.15} role="img" aria-label={ad}>
        <rect width={boy} height={boy} rx="6" fill="#ddb065" stroke="#6b4a22" strokeWidth="2" />
        {Array.from({ length: n }, (_, i) => (
          <g key={i} stroke="#2a1c0c" strokeWidth="1" strokeOpacity=".75"><line x1={p(0)} x2={p(n - 1)} y1={p(i)} y2={p(i)} /><line y1={p(0)} y2={p(n - 1)} x1={p(i)} x2={p(i)} /></g>
        ))}
        {isaret.filter((m) => m[2] === 'aS' || m[2] === 'aB').map(([x, y, tur], i) => (
          <rect key={`a${i}`} x={p(x) - 4} y={p(y) - 4} width="8" height="8" rx="1.5" fill={tur === 'aS' ? '#111' : '#fff'} stroke={tur === 'aS' ? 'none' : '#333'} strokeWidth=".8" />
        ))}
        {taslar.map(([x, y, r, soluk], i) => (
          <circle key={`t${i}`} cx={p(x)} cy={p(y)} r="8.6" fill={r === 'S' ? '#141414' : '#f6f3ea'} stroke={soluk ? '#c0392b' : '#000'} strokeOpacity={soluk ? 1 : 0.35} strokeWidth={soluk ? 1.6 : 1} strokeDasharray={soluk ? '3 2' : undefined} opacity={soluk ? 0.5 : 1} />
        ))}
        {isaret.map(([x, y, tur], i) => {
          if (tur === 'o') return <circle key={i} cx={p(x)} cy={p(y)} r="3.6" fill="#2bd17e" stroke="#0b5c34" strokeWidth="1" />;
          if (tur === 'h') return <g key={i}><circle cx={p(x)} cy={p(y)} r="7.6" fill="rgba(255,216,74,.35)" stroke="#8a5a00" strokeWidth="1.6" strokeDasharray="3 2" /><path d={`M${p(x) - 3.5} ${p(y)}h7M${p(x)} ${p(y) - 3.5}v7`} stroke="#5c3b00" strokeWidth="1.6" strokeLinecap="round" /></g>;
          if (tur === 'x') return <path key={i} d={`M${p(x) - 5} ${p(y) - 5}l10 10M${p(x) + 5} ${p(y) - 5}l-10 10`} stroke="#c0392b" strokeWidth="2.6" strokeLinecap="round" />;
          if (tur === 'ko') return <rect key={i} x={p(x) - 5} y={p(y) - 5} width="10" height="10" fill="none" stroke="#c0392b" strokeWidth="2" />;
          return null;
        })}
      </svg>
      <Alt ad={ad} iyi={iyi} />
    </figure>
  );
}

/** Go şemalarındaki işaretlerin açıklaması */
export function GoLejant() {
  return (
    <ul className="mk-lejant" aria-label="Şema işaretleri">
      <li><i className="mk-lj is-o" /> özgürlük</li>
      <li><i className="mk-lj is-h" /> buraya oynanır</li>
      <li><i className="mk-lj is-x" /> konamaz</li>
      <li><i className="mk-lj is-soluk" /> alınan taş</li>
      <li><i className="mk-lj is-alan" /> çevrili alan</li>
    </ul>
  );
}

/* ---------------- Çizgi Yarışı ---------------- */

type Nokta = [number, number];
const KIRMIZI = '#e4572e', MAVI = '#2563eb';

export function Zar({ n, renk }: { n: number; renk?: string }) {
  const yer: Record<number, [number, number][]> = { 1: [[12, 12]], 2: [[7, 7], [17, 17]], 3: [[7, 7], [12, 12], [17, 17]], 4: [[7, 7], [17, 7], [7, 17], [17, 17]], 5: [[7, 7], [17, 7], [12, 12], [7, 17], [17, 17]], 6: [[7, 6], [17, 6], [7, 12], [17, 12], [7, 18], [17, 18]] };
  return (
    <svg className="mk-zar" viewBox="0 0 24 24" width="30" height="30" role="img" aria-label={`Zar ${n}`}>
      <rect x="1.5" y="1.5" width="21" height="21" rx="5" fill="#fffaf0" stroke={renk || '#c9bfa6'} strokeWidth="2" />
      {(yer[n] || []).map(([x, y], i) => <circle key={i} cx={x} cy={y} r="2" fill="#1d2b2a" />)}
    </svg>
  );
}

/**
 * Çizgi Yarışı pisti: üstte mavi kale, altta kırmızı kale, ortada kesik orta çizgi.
 * Yollar [sütun, satır] hücreleriyle verilir; `plan` o turda atılacak adımları kesik çizgiyle gösterir.
 */
export function CizgiSema({ kirmizi, mavi, plan, zarlar, ad, iyi, sutun = 3, satir = 10 }: {
  kirmizi: Nokta[]; mavi: Nokta[]; plan?: { renk: 'k' | 'm'; yol: Nokta[] }; zarlar?: React.ReactNode; ad: string; iyi?: boolean; sutun?: number; satir?: number;
}) {
  const H = 15, K = 5, w = K * 2 + sutun * H, h = K * 2 + satir * H;
  const c = ([x, y]: Nokta) => `${K + x * H + H / 2},${K + y * H + H / 2}`;
  const cizgi = (yol: Nokta[], renk: string, kesik?: boolean) => (
    <g>
      <polyline points={yol.map(c).join(' ')} fill="none" stroke={renk} strokeWidth={kesik ? 3 : 5} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={kesik ? '1 6' : undefined} />
      {(() => { const [x, y] = c(yol[yol.length - 1]).split(',').map(Number); return <circle cx={x} cy={y} r={kesik ? 4 : 4.6} fill={kesik ? '#fdfaf2' : renk} stroke={renk} strokeWidth="2" />; })()}
    </g>
  );
  return (
    <figure className={sinif(iyi)}>
      <div className="mk-cizgi">
        <svg viewBox={`0 0 ${w} ${h}`} width={w * 1.25} height={h * 1.25} role="img" aria-label={ad}>
          <rect width={w} height={h} rx="5" fill="#fdfaf2" stroke="#7aa3c9" strokeWidth="1.5" />
          <rect x={K} y={K} width={sutun * H} height={H} fill={MAVI} opacity=".18" />
          <rect x={K} y={K + (satir - 1) * H} width={sutun * H} height={H} fill={KIRMIZI} opacity=".18" />
          {Array.from({ length: satir + 1 }, (_, i) => <line key={`y${i}`} x1={K} x2={w - K} y1={K + i * H} y2={K + i * H} stroke="#7aa3c9" strokeWidth=".6" strokeOpacity=".7" />)}
          {Array.from({ length: sutun + 1 }, (_, i) => <line key={`x${i}`} y1={K} y2={h - K} x1={K + i * H} x2={K + i * H} stroke="#7aa3c9" strokeWidth=".6" strokeOpacity=".7" />)}
          <line x1={K - 3} x2={w - K + 3} y1={K + (satir / 2) * H} y2={K + (satir / 2) * H} stroke="#1d2b2a" strokeWidth="1.6" strokeDasharray="5 3" opacity=".6" />
          {cizgi(mavi, MAVI)}
          {cizgi(kirmizi, KIRMIZI)}
          {plan && cizgi(plan.yol, plan.renk === 'k' ? KIRMIZI : MAVI, true)}
        </svg>
        {zarlar && <div className="mk-cizgi-yan">{zarlar}</div>}
      </div>
      <Alt ad={ad} iyi={iyi} />
    </figure>
  );
}

/* ---------------- XOX ---------------- */

/** XOX tahtası: satırlar "X.O" biçiminde; `dizi` kazanan çizginin iki ucu [satır, sütun] */
export function XoxSema({ satirlar, dizi, ad, iyi }: { satirlar: string[]; dizi?: [Nokta, Nokta]; ad: string; iyi?: boolean }) {
  const n = satirlar.length, H = 22, K = 5, boy = K * 2 + n * H;
  const o = (i: number) => K + i * H + H / 2;
  return (
    <figure className={sinif(iyi)}>
      <svg viewBox={`0 0 ${boy} ${boy}`} width={Math.min(150, boy * 1.2)} height={Math.min(150, boy * 1.2)} role="img" aria-label={ad} fill="none" strokeLinecap="round">
        <rect width={boy} height={boy} rx="7" fill="#fffaf0" />
        {Array.from({ length: n - 1 }, (_, i) => (
          <g key={i} stroke="#3b3b3b" strokeOpacity=".45" strokeWidth="1.6"><line x1={K + (i + 1) * H} x2={K + (i + 1) * H} y1={K + 2} y2={boy - K - 2} /><line y1={K + (i + 1) * H} y2={K + (i + 1) * H} x1={K + 2} x2={boy - K - 2} /></g>
        ))}
        {satirlar.flatMap((s, r) => [...s].map((h, k) => (
          h === 'X' ? <path key={`${r}-${k}`} d={`M${o(k) - 5.5} ${o(r) - 5.5}l11 11M${o(k) + 5.5} ${o(r) - 5.5}l-11 11`} stroke="#c2410c" strokeWidth="3.4" />
            : h === 'O' ? <circle key={`${r}-${k}`} cx={o(k)} cy={o(r)} r="6.2" stroke="#1d4ed8" strokeWidth="3.2" /> : null
        )))}
        {dizi && <line x1={o(dizi[0][1])} y1={o(dizi[0][0])} x2={o(dizi[1][1])} y2={o(dizi[1][0])} stroke="#111" strokeOpacity=".75" strokeWidth="3" />}
      </svg>
      <Alt ad={ad} iyi={iyi} />
    </figure>
  );
}
