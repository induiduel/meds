/**
 * Taş Masası kabuğunun ortak parçaları: yaprak (kipli pencere), onay, bildirim, avatar, oyun çizimleri, konfeti, skor tablosu.
 * Renkler `.mk` kökünde tanımlıdır (styles/masa/kabuk.css); siteden renk devralınmaz.
 */
import React, { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, motion } from 'motion/react';
import { Bot, Crown, X } from 'lucide-react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { VARSAYILAN_RENKLER, type Ceza, type OdaGorunum, type OyunTur, type Tas, type UnoKart } from '../../services/masa/tipler';
import { azHareket } from './ortak';
import { TasGorsel } from './okey/Tas';
import { KartGorsel } from './uno/Kart';

/* ---------------- metin yardımcıları ---------------- */

/** İşaretli puan: +12 · −7 · 0 (gerçek eksi işareti) */
export const puanYaz = (n: number) => (n > 0 ? `+${n}` : n < 0 ? `−${Math.abs(n)}` : '0');
export const tasMi = (tur: OyunTur) => tur !== 'uno';
export const birim = (tur: OyunTur) => (tur === 'uno' ? 'kart' : 'taş');
/** Bot adındaki "(bot)" eki rozetle gösterilir, metinden düşülür */
export const sadeAd = (ad: string) => ad.replace(/\s*\(bot\)$/i, '');

export const TEMA_BILGI: Record<string, { ad: string; aciklama: string }> = {
  klasik: { ad: 'Klasik', aciklama: 'Yeşil keçe, ahşap ıstaka' },
  kitty: { ad: 'Hello Kitty', aciklama: 'Pembe, fiyonklu, şeker tonları' },
  stitch: { ad: 'Stitch', aciklama: 'Okyanus mavisi, tropik yapraklar' },
  buyucu: { ad: 'Harry Potter', aciklama: 'Parşömen, altın yaldız, gece mavisi' },
};

export const CEZA_BILGI: Record<string, { ad: string; sinif: string; ne: string }> = {
  islek: { ad: 'İşlek taşı işlemedi', sinif: 'is-islek', ne: 'Masadaki bir pere uyan (uca eklenen ya da seriyi bölen) taşı varken taş çekti ya da eli devretti.' },
  per: { ad: 'Açabileceği peri bekletti', sinif: 'is-per', ne: 'Elinde açılabilecek bir per varken taş çekti ya da eli devretti.' },
  islekAtti: { ad: 'İşlek taş attı', sinif: 'is-islek', ne: 'Masadaki bir pere işlenebilecek taşı yere attı.' },
  okeyAtti: { ad: 'Okey attı', sinif: 'is-okey', ne: 'Okey (joker) taşını yere attı.' },
  acmadi: { ad: 'Açamadı', sinif: 'is-per', ne: 'El bittiğinde perlerini açmamıştı.' },
  uno: { ad: 'UNO demedi', sinif: 'is-uno', ne: 'Tek kartı kalınca UNO demedi ve yakalandı: 2 kart çekti.' },
};
export const cezaBilgi = (c: Ceza) => CEZA_BILGI[c.tur] || { ad: c.aciklama || 'Ceza', sinif: 'is-diger', ne: c.aciklama || '' };

/* ---------------- hata sınırı ---------------- */

export class HataSiniri extends React.Component<{ yedek: React.ReactNode | ((sifirla: () => void) => React.ReactNode); children: React.ReactNode }, { hata: boolean }> {
  state = { hata: false };
  static getDerivedStateFromError() { return { hata: true }; }
  componentDidCatch(e: unknown) { console.error('[masa] bileşen hatası', e); }
  render() {
    if (!this.state.hata) return this.props.children;
    const y = this.props.yedek;
    return typeof y === 'function' ? y(() => this.setState({ hata: false })) : y;
  }
}

/* ---------------- örnek taş / kart (masa ajanlarının çizimleri; çökerse sade yedek) ---------------- */

export function TasOrnek({ s, r, renkler, tema = 'klasik', boy = 34, okey, kapali }: { s: number; r: 0 | 1 | 2 | 3; renkler?: readonly string[]; tema?: string; boy?: number; okey?: { s: number; r: 0 | 1 | 2 | 3 }; kapali?: boolean }) {
  const rk = (renkler || VARSAYILAN_RENKLER) as string[];
  const tas: Tas = { id: -1 - s * 4 - r, s, r };
  return (
    <HataSiniri yedek={<span className="mk-tas-yedek" style={{ color: rk[r], width: boy, height: boy * 1.36 }}>{s || '★'}</span>}>
      <TasGorsel tas={tas} renkler={rk} tema={tema} boy={boy} okey={okey} kapali={kapali} />
    </HataSiniri>
  );
}

export function KartOrnek({ renk, deger, tema = 'klasik', boy = 46, kapali }: { renk?: UnoKart['renk']; deger?: UnoKart['deger']; tema?: string; boy?: number; kapali?: boolean }) {
  const kart: UnoKart | undefined = deger ? { id: -1, renk: renk ?? null, deger } : undefined;
  return (
    <HataSiniri yedek={<span className="mk-kart-yedek" style={{ width: boy, height: boy * 1.5 }}>{deger || ''}</span>}>
      <KartGorsel kart={kart} tema={tema} boy={boy} kapali={kapali} />
    </HataSiniri>
  );
}

/* ---------------- yaprak ---------------- */

/** Kipli pencere: telefonda alttan yaprak, geniş ekranda ortada; `tam` = tam sayfa. Gövdeye taşınır (site kabuğunun üstünde). */
export function Yaprak({ ac, kapat, baslik, children, tam, genis, alt, tema }: {
  ac: boolean; kapat: () => void; baslik: React.ReactNode; children: React.ReactNode; tam?: boolean; genis?: boolean; alt?: React.ReactNode; tema?: string;
}) {
  const kutu = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ac) return;
    lockScroll();
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); kapat(); } };
    window.addEventListener('keydown', tus);
    const t = setTimeout(() => kutu.current?.focus({ preventScroll: true }), 30);
    return () => { unlockScroll(); window.removeEventListener('keydown', tus); clearTimeout(t); };
  }, [ac]); // eslint-disable-line react-hooks/exhaustive-deps
  if (typeof document === 'undefined') return null;
  const az = azHareket();
  return createPortal(
    <AnimatePresence>
      {ac && (
        <motion.div className={`mk mk-yaprak-kok${tam ? ' is-tam' : ''}`} data-tema={tema} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.16 }}>
          <div className="mk-yaprak-perde" onClick={kapat} />
          <motion.div
            ref={kutu} className={`mk-yaprak${genis ? ' is-genis' : ''}`} role="dialog" aria-modal="true" tabIndex={-1}
            initial={az ? false : { y: 28, scale: 0.98 }} animate={{ y: 0, scale: 1 }} exit={az ? undefined : { y: 20 }}
            transition={{ type: 'spring', stiffness: 420, damping: 34 }}
          >
            <header className="mk-yaprak-bas">
              <h2>{baslik}</h2>
              <button type="button" className="mk-ikon-dugme" onClick={kapat} aria-label="Kapat"><X size={20} /></button>
            </header>
            <div className="mk-yaprak-govde">{children}</div>
            {alt && <footer className="mk-yaprak-alt">{alt}</footer>}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body,
  );
}

export function Onay({ ac, kapat, baslik, metin, onayAd, tehlike, onay }: { ac: boolean; kapat: () => void; baslik: string; metin: React.ReactNode; onayAd: string; tehlike?: boolean; onay: () => void }) {
  return (
    <Yaprak ac={ac} kapat={kapat} baslik={baslik} alt={
      <>
        <button type="button" className="mk-dugme is-soluk" onClick={kapat}>Vazgeç</button>
        <button type="button" className={`mk-dugme ${tehlike ? 'is-tehlike' : 'is-ana'}`} onClick={() => { kapat(); onay(); }}>{onayAd}</button>
      </>
    }>
      <p className="mk-onay-metin">{metin}</p>
    </Yaprak>
  );
}

/* ---------------- bildirim ---------------- */

interface Bildirim { id: number; metin: string; tur: 'bilgi' | 'hata' | 'iyi' }
let bildirimler: Bildirim[] = [];
let bildirimNo = 0;
const bildirimAbone = new Set<() => void>();
const bildirimYay = () => bildirimAbone.forEach((f) => f());
/** Kısa süreli bildirim (aynı metin art arda yinelenmez) */
export function bildir(metin: string, tur: Bildirim['tur'] = 'bilgi', ms = 3000) {
  if (!metin || bildirimler.some((b) => b.metin === metin)) return;
  const id = ++bildirimNo;
  bildirimler = [...bildirimler.slice(-2), { id, metin, tur }];
  bildirimYay();
  setTimeout(() => { bildirimler = bildirimler.filter((b) => b.id !== id); bildirimYay(); }, ms);
}
export function Bildirimler() {
  const liste = useSyncExternalStore((f) => { bildirimAbone.add(f); return () => { bildirimAbone.delete(f); }; }, () => bildirimler, () => bildirimler);
  if (typeof document === 'undefined') return null;
  return createPortal(
    <div className="mk mk-bildirimler" role="status" aria-live="polite">
      <AnimatePresence>
        {liste.map((b) => (
          <motion.div key={b.id} layout="position" className={`mk-bildirim is-${b.tur}`} initial={{ opacity: 0, y: -14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }}>
            {b.metin}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>,
    document.body,
  );
}

/* ---------------- avatar ---------------- */

const AVATAR_TON = ['#c2410c', '#0f766e', '#7c3aed', '#be185d', '#1d4ed8', '#4d7c0f', '#b45309', '#0e7490'];
export function Avatar({ ad, foto, bot, id, boy = 36, tac }: { ad: string; foto?: string; bot?: boolean; id?: string; boy?: number; tac?: boolean }) {
  const anahtar = id || ad;
  let h = 0;
  for (let i = 0; i < anahtar.length; i++) h = (h * 31 + anahtar.charCodeAt(i)) >>> 0;
  const harf = sadeAd(ad).trim().slice(0, 1).toLocaleUpperCase('tr-TR') || '?';
  return (
    <span className="mk-avatar" style={{ width: boy, height: boy, fontSize: boy * 0.44, background: bot ? '#3b4a4a' : AVATAR_TON[h % AVATAR_TON.length] }} aria-hidden="true">
      {foto && !bot ? <img src={foto} alt="" loading="lazy" /> : bot ? <Bot size={boy * 0.56} /> : harf}
      {tac && <i className="mk-avatar-tac"><Crown size={Math.max(11, boy * 0.34)} /></i>}
    </span>
  );
}

/* ---------------- oyun çizimleri (özgün, küçük SVG) ---------------- */

const tasCiz = (x: number, y: number, don: number, sayi: string, renk: string, k: number) => (
  <g key={k} transform={`translate(${x} ${y}) rotate(${don})`}>
    <rect x="-17" y="-24" width="34" height="48" rx="6" fill="#0003" transform="translate(1.5 3)" />
    <rect x="-17" y="-24" width="34" height="48" rx="6" fill="#f7f0de" stroke="#d9cba8" />
    <text x="0" y="1" textAnchor="middle" fontSize={sayi.length > 2 ? 15 : 20} fontWeight="800" fill={renk} fontFamily="inherit">{sayi}</text>
    <circle cx="0" cy="13" r="3.2" fill="none" stroke={renk} strokeWidth="1.6" />
  </g>
);
const kartCiz = (x: number, y: number, don: number, renk: string, sayi: string, k: number) => (
  <g key={k} transform={`translate(${x} ${y}) rotate(${don})`}>
    <rect x="-18" y="-27" width="36" height="54" rx="6" fill="#0003" transform="translate(1.5 3)" />
    <rect x="-18" y="-27" width="36" height="54" rx="6" fill="#fff" />
    <rect x="-15" y="-24" width="30" height="48" rx="4" fill={renk} />
    <ellipse cx="0" cy="0" rx="10" ry="16" fill="#fff" transform="rotate(24)" />
    <text x="0" y="7" textAnchor="middle" fontSize="19" fontWeight="900" fill={renk} fontFamily="inherit">{sayi}</text>
  </g>
);
export function OyunResmi({ tur }: { tur: OyunTur }) {
  return (
    <svg className="mk-oyun-resim" viewBox="0 0 132 84" aria-hidden="true">
      {tur === 'yedili' && [tasCiz(38, 44, -12, '5', '#1f6feb', 0), tasCiz(66, 40, 0, '6', '#1f6feb', 1), tasCiz(94, 44, 12, '7', '#1f6feb', 2)]}
      {tur === 'takim' && [
        tasCiz(30, 46, -8, '9', '#d62839', 0), tasCiz(54, 40, 4, '9', '#1d1d1f', 1),
        <path key="b" d="M62 14c8-8 20-8 28 0" fill="none" stroke="#f3c74f" strokeWidth="3" strokeLinecap="round" strokeDasharray="2 6" />,
        tasCiz(80, 40, -4, '9', '#1f6feb', 2), tasCiz(104, 46, 8, '9', '#e8a400', 3),
      ]}
      {tur === 'yuzbir' && [
        tasCiz(34, 46, -10, '12', '#d62839', 0), tasCiz(98, 46, 10, '13', '#d62839', 2), tasCiz(66, 40, 0, '101', '#1d1d1f', 1),
        <path key="y" d="M66 4l2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9-4.3-4.1 5.9-.8z" fill="#f3c74f" />,
      ]}
      {tur === 'uno' && [kartCiz(38, 44, -16, '#d8323c', '7', 0), kartCiz(66, 40, 0, '#f2b417', '2', 1), kartCiz(94, 44, 16, '#2a6fdb', '9', 2)]}
    </svg>
  );
}

/* ---------------- konfeti (tuval; ~90 parça, kendiliğinden biter) ---------------- */

export function Konfeti({ renkler = ['#f3c74f', '#f6efdf', '#e4572e', '#2ec4b6', '#ff8fab'], adet = 90 }: { renkler?: string[]; adet?: number }) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const c = ref.current;
    if (!c || azHareket()) return;
    const kap = c.parentElement!;
    const olcek = Math.min(2, window.devicePixelRatio || 1);
    const w = kap.clientWidth, h = kap.clientHeight;
    c.width = w * olcek; c.height = h * olcek;
    const g = c.getContext('2d');
    if (!g) return;
    g.scale(olcek, olcek);
    const p = Array.from({ length: adet }, (_, i) => {
      const a = -Math.PI / 2 + (Math.random() - 0.5) * 1.9, hiz = 5 + Math.random() * 9;
      return { x: w / 2 + (Math.random() - 0.5) * 60, y: h * 0.42, vx: Math.cos(a) * hiz, vy: Math.sin(a) * hiz - 3, d: Math.random() * 6.28, vd: (Math.random() - 0.5) * 0.4, b: 5 + Math.random() * 6, r: renkler[i % renkler.length] };
    });
    let kare = 0, id = 0;
    const ciz = () => {
      g.clearRect(0, 0, w, h);
      kare++;
      const sol = Math.max(0, 1 - Math.max(0, kare - 110) / 50);
      for (const q of p) {
        q.vy += 0.24; q.vx *= 0.985; q.x += q.vx; q.y += q.vy; q.d += q.vd;
        g.save(); g.globalAlpha = sol; g.translate(q.x, q.y); g.rotate(q.d); g.fillStyle = q.r;
        g.fillRect(-q.b / 2, -q.b / 3, q.b, q.b * 0.62); g.restore();
      }
      if (kare < 160) id = requestAnimationFrame(ciz); else g.clearRect(0, 0, w, h);
    };
    id = requestAnimationFrame(ciz);
    return () => cancelAnimationFrame(id);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  return <canvas ref={ref} className="mk-konfeti" aria-hidden="true" />;
}

/** 0'dan hedefe sayan sayaç (az hareket tercihinde anında) */
export function useSayac(hedef: number, sure = 900, gecikme = 0) {
  const [d, setD] = useState(azHareket() ? hedef : 0);
  useEffect(() => {
    if (azHareket()) { setD(hedef); return; }
    let id = 0;
    const t0 = performance.now() + gecikme;
    const adim = (t: number) => {
      const k = Math.min(1, Math.max(0, (t - t0) / sure));
      setD(Math.round(hedef * (1 - (1 - k) ** 3)));
      if (k < 1) id = requestAnimationFrame(adim);
    };
    id = requestAnimationFrame(adim);
    return () => cancelAnimationFrame(id);
  }, [hedef, sure, gecikme]);
  return d;
}

/* ---------------- skor tablosu (oyuncular × eller) ---------------- */

export function SkorTablo({ oda }: { oda: OdaGorunum }) {
  const sirali = [...oda.oyuncular].sort((a, b) => (oda.skor[b.id] || 0) - (oda.skor[a.id] || 0));
  if (!oda.eller.length) return <p className="mk-bos">Henüz tamamlanan el yok. İlk el bitince puanlar burada görünür.</p>;
  return (
    <div className="mk-skor-kaydir">
      <table className="mk-skor">
        <thead>
          <tr>
            <th scope="col">Oyuncu</th>
            {oda.eller.map((e) => <th key={e.no} scope="col">{e.no}. el</th>)}
            <th scope="col">Toplam</th>
          </tr>
        </thead>
        <tbody>
          {sirali.map((o) => (
            <tr key={o.id} className={o.id === oda.ben ? 'is-ben' : ''}>
              <th scope="row">
                <span className="mk-skor-ad">{sadeAd(o.ad)}{o.id === oda.ben && <em>sen</em>}{o.takim && <i className={`mk-takim-nokta is-${o.takim}`}>{o.takim}</i>}</span>
              </th>
              {oda.eller.map((e) => {
                const p = e.puanlar[o.id];
                return <td key={e.no} className={e.kazananlar.includes(o.id) ? 'is-kazanan' : p < 0 ? 'is-eksi' : ''}>{p === undefined ? '–' : puanYaz(p)}</td>;
              })}
              <td className="mk-skor-toplam">{puanYaz(oda.skor[o.id] || 0)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
