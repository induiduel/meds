import React, { useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { Eraser, Highlighter, Pen, Plus, Search, Share2, Trash2, Type, Undo2, X } from 'lucide-react';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/notlarim.css';

/**
 * v15 · Notlarım (tasarım sistemi v15 › K "Not / kalem / renklendirme"). Yeni sayfa: /notlarim (Menü › Ben).
 * Her not: başlık, metin, renk etiketi ve kalem/fosforlu çizim katmanı. Kayıt cihazda; anahtarlar userKvSync
 * SYNC_PATTERNS'te olduğu için giriş yapan öğrencinin hesabına eşitlenir (başka cihazda da açılır).
 * Çizim anahtarı nota ayrıdır (medsoru_notlarim_cizim:<id>) — liste küçük kalır, 2 MB sınırı not başına uygulanır.
 * Çizgiler 1000 birim genişliğe göre saklanır; her ekran boyutunda aynı yerde durur.
 */
interface Not { id: string; baslik: string; metin: string; renk: string; at: number }
interface Cizgi { r: string; w: number; f?: 1; p: number[] }
type Arac = 'yaz' | 'kalem' | 'fosfor' | 'silgi';

const KEY = 'medsoru_notlarim_v1';
const CKEY = (id: string) => `medsoru_notlarim_cizim:${id}`;
const OLAY = 'medsoru:notlarim';
const RENKLER = ['none', 'red', 'amber', 'green', 'blue', 'violet'] as const;
const RENK_AD: Record<string, string> = { none: 'Renksiz', red: 'Kırmızı', amber: 'Sarı', green: 'Yeşil', blue: 'Mavi', violet: 'Mor' };
/** kalem mürekkepleri: koyu metin rengi + palet tonları (CSS değişkeni adları; çizimde hesaplanır) */
const MUREKKEP = ['ink', 'red', 'blue', 'green', 'amber'] as const;

const oku = (): Not[] => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } };
let ham: string | null = null; let onb: Not[] = [];
const anlik = () => { const h = (() => { try { return localStorage.getItem(KEY); } catch { return null; } })(); if (h !== ham) { ham = h; onb = oku(); } return onb; };
const abone = (f: () => void) => {
  const g = (e: Event) => { if (!(e instanceof StorageEvent) || e.key === KEY) f(); };
  window.addEventListener(OLAY, g); window.addEventListener('storage', g);
  return () => { window.removeEventListener(OLAY, g); window.removeEventListener('storage', g); };
};
const yaz = (n: Not[]) => { try { localStorage.setItem(KEY, JSON.stringify(n)); } catch { /* dolu */ } window.dispatchEvent(new Event(OLAY)); };
const cizimOku = (id: string): Cizgi[] => { try { return JSON.parse(localStorage.getItem(CKEY(id)) || '[]'); } catch { return []; } };
const cizimYaz = (id: string, c: Cizgi[]) => { try { if (c.length) localStorage.setItem(CKEY(id), JSON.stringify(c)); else localStorage.removeItem(CKEY(id)); } catch { /* dolu */ } };
const fold = (s: string) => s.toLocaleLowerCase('tr-TR');
const tarihYaz = (t: number) => new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });

export default function NotlarimV15() {
  const notlar = useSyncExternalStore(abone, anlik, anlik);
  // açık not adreste (?not=<id>): üst bardaki Geri ve tarayıcı geri tuşu listeye döner
  const notParam = () => new URLSearchParams(location.search).get('not');
  const [acikId, setAcikId0] = useState<string | null>(notParam);
  useEffect(() => { const f = () => setAcikId0(notParam()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  const setAcikId = (id: string | null) => {
    if (id === acikId) return;
    try { if (id) history.pushState(history.state, '', `${location.pathname}?not=${id}`); else history.back(); } catch { /* yok */ }
    setAcikId0(id);
  };
  const [ara, setAra] = useState('');
  const acik = notlar.find((n) => n.id === acikId) || null;
  useV15Baslik({ baslik: acik ? (acik.baslik || 'Başlıksız not') : 'Notlarım', alt: acik ? 'Notlarım' : `${notlar.length} not`, ...(acik ? { geri: '/notlarim' } : {}) });

  const sirali = useMemo(() => [...notlar].sort((a, b) => b.at - a.at).filter((n) => !ara || fold(`${n.baslik} ${n.metin}`).includes(fold(ara))), [notlar, ara]);
  const yeni = () => {
    const n: Not = { id: `n${Date.now().toString(36)}`, baslik: '', metin: '', renk: 'none', at: Date.now() };
    yaz([n, ...notlar]); setAcikId(n.id);
  };
  const guncelle = (id: string, d: Partial<Not>) => yaz(anlik().map((n) => (n.id === id ? { ...n, ...d, at: Date.now() } : n)));
  const sil = (id: string) => {
    if (!confirm('Bu not silinsin mi?')) return;
    cizimYaz(id, []); yaz(anlik().filter((n) => n.id !== id)); setAcikId(null);
  };

  if (acik) return <Duzenleyici not={acik} guncelle={(d) => guncelle(acik.id, d)} sil={() => sil(acik.id)} kapat={() => setAcikId(null)} />;

  return (
    <div className="nt15">
      <h1 className="sr-only">Notlarım</h1>
      <div className="nt15-ust">
        <label className="o15-ara nt15-ara"><Search aria-hidden /><input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Notlarda ara" aria-label="Notlarda ara" /></label>
        <button type="button" className="v15-btn" onClick={yeni}><Plus aria-hidden />Yeni not</button>
      </div>
      {!notlar.length ? (
        <div className="v15-card nt15-bos">
          <Pen aria-hidden />
          <b>Henüz notun yok</b>
          <p>Ders çalışırken aklına geleni yaz, kalemle çiz ya da fosforluyla işaretle. Notların hesabına kaydedilir; telefonda yazdığını bilgisayarda açabilirsin.</p>
          <button type="button" className="v15-btn" onClick={yeni}><Plus aria-hidden />İlk notu yaz</button>
        </div>
      ) : !sirali.length ? (
        <p className="b15-bos v15-card">"{ara}" geçen not yok.</p>
      ) : (
        <ul className="nt15-izgara">
          {sirali.map((n) => (
            <li key={n.id}>
              <button type="button" className={`v15-card nt15-kart is-${n.renk}`} onClick={() => setAcikId(n.id)}>
                <b>{n.baslik || 'Başlıksız not'}</b>
                <span>{n.metin.slice(0, 160) || (localStorage.getItem(CKEY(n.id)) ? 'Çizim' : 'Boş not')}</span>
                <small>{tarihYaz(n.at)}</small>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Duzenleyici({ not, guncelle, sil, kapat }: { not: Not; guncelle: (d: Partial<Not>) => void; sil: () => void; kapat: () => void }) {
  const [arac, setArac] = useState<Arac>('yaz');
  const [murekkep, setMurekkep] = useState<(typeof MUREKKEP)[number]>('ink');
  const [kalin, setKalin] = useState(3);
  const [cizgiler, setCizgiler] = useState<Cizgi[]>(() => cizimOku(not.id));
  const kap = useRef<HTMLDivElement>(null);
  const tuval = useRef<HTMLCanvasElement>(null);
  const aktif = useRef<Cizgi | null>(null);

  useEffect(() => { cizimYaz(not.id, cizgiler); }, [cizgiler, not.id]);

  const renkCoz = (r: string) => {
    const cs = getComputedStyle(document.documentElement);
    const m: Record<string, string> = { ink: '--color-ink', red: '--color-bad', blue: '--color-accent', green: '--color-ok', amber: '--color-warn' };
    return cs.getPropertyValue(m[r] || '--color-ink').trim() || '#222';
  };
  const ciz = () => {
    const c = tuval.current, el = kap.current; if (!c || !el) return;
    const dpr = window.devicePixelRatio || 1;
    // tuval mutlak konumlu ve kabın yüksekliğini alır; scrollHeight kullanılmaz (tuval kendi boyunu katıp sonsuz büyüyordu)
    const w = el.clientWidth, h = el.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
    const g = c.getContext('2d'); if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    const k = w / 1000;
    for (const s of [...cizgiler, ...(aktif.current ? [aktif.current] : [])]) {
      if (s.p.length < 2) continue;
      g.globalAlpha = s.f ? 0.32 : 1; g.strokeStyle = renkCoz(s.r); g.lineWidth = s.w * k * (s.f ? 6 : 1); g.lineCap = 'round'; g.lineJoin = 'round';
      g.beginPath(); g.moveTo(s.p[0] * k, s.p[1] * k);
      for (let i = 2; i < s.p.length; i += 2) g.lineTo(s.p[i] * k, s.p[i + 1] * k);
      if (s.p.length === 2) g.lineTo(s.p[0] * k + 0.1, s.p[1] * k);
      g.stroke();
    }
    g.globalAlpha = 1;
  };
  useEffect(ciz);
  // metin uzayınca kap büyür: tuvali yeniden boyutla
  useEffect(() => { const el = kap.current; if (!el) return; const ro = new ResizeObserver(() => ciz()); ro.observe(el); return () => ro.disconnect(); });
  useEffect(() => { const f = () => ciz(); window.addEventListener('resize', f); return () => window.removeEventListener('resize', f); });

  const nokta = (e: React.PointerEvent) => {
    const r = kap.current!.getBoundingClientRect(); const k = 1000 / r.width;
    return [Math.round((e.clientX - r.left) * k), Math.round((e.clientY - r.top) * k)];
  };
  const bas = (e: React.PointerEvent) => {
    if (arac === 'yaz') return;
    e.preventDefault(); (e.target as Element).setPointerCapture(e.pointerId);
    const [x, y] = nokta(e);
    if (arac === 'silgi') { silNokta(x, y); return; }
    aktif.current = { r: murekkep, w: kalin, p: [x, y], ...(arac === 'fosfor' ? { f: 1 as const } : {}) };
    ciz();
  };
  const surukle = (e: React.PointerEvent) => {
    if (arac === 'yaz' || !(e.buttons & 1)) return;
    const [x, y] = nokta(e);
    if (arac === 'silgi') { silNokta(x, y); return; }
    const a = aktif.current; if (!a) return;
    const n = a.p.length; if (Math.abs(a.p[n - 2] - x) + Math.abs(a.p[n - 1] - y) < 2) return;
    a.p.push(x, y); ciz();
  };
  const birak = () => { const a = aktif.current; aktif.current = null; if (a) setCizgiler((c) => [...c, a]); };
  const silNokta = (x: number, y: number) => setCizgiler((c) => {
    const kalan = c.filter((s) => { for (let i = 0; i < s.p.length; i += 2) if (Math.hypot(s.p[i] - x, s.p[i + 1] - y) < 14 + s.w * (s.f ? 3 : 1)) return false; return true; });
    return kalan.length === c.length ? c : kalan;
  });
  const paylas = async () => {
    const metin = `${not.baslik || 'Not'}\n\n${not.metin}`.trim();
    try { if (navigator.share) await navigator.share({ title: not.baslik || 'Not', text: metin }); else await navigator.clipboard.writeText(metin); } catch { /* vazgeçti */ }
  };

  const AR: [Arac, string, React.ElementType][] = [['yaz', 'Yaz', Type], ['kalem', 'Kalem', Pen], ['fosfor', 'Fosforlu', Highlighter], ['silgi', 'Silgi', Eraser]];
  return (
    <div className="nt15 nt15-d">
      <div className="nt15-arac v15-card" role="toolbar" aria-label="Araçlar">
        {AR.map(([id, ad, Ic]) => (
          <button key={id} type="button" className={`nt15-ab${arac === id ? ' is-on' : ''}`} aria-pressed={arac === id} onClick={() => setArac(id)} title={ad}><Ic aria-hidden /><span>{ad}</span></button>
        ))}
        <span className="nt15-ayir" aria-hidden />
        {(arac === 'kalem' || arac === 'fosfor') && (
          <>
            {MUREKKEP.map((m) => <button key={m} type="button" className={`nt15-mr is-${m}${murekkep === m ? ' is-on' : ''}`} aria-label={`Renk: ${m === 'ink' ? 'Siyah' : RENK_AD[m]}`} aria-pressed={murekkep === m} onClick={() => setMurekkep(m)} />)}
            <select className="nt15-kalin" value={kalin} onChange={(e) => setKalin(Number(e.target.value))} aria-label="Kalınlık">
              <option value={2}>İnce</option><option value={3}>Orta</option><option value={6}>Kalın</option>
            </select>
          </>
        )}
        <button type="button" className="nt15-ab" onClick={() => setCizgiler((c) => c.slice(0, -1))} disabled={!cizgiler.length} title="Geri al"><Undo2 aria-hidden /><span>Geri al</span></button>
      </div>

      <div className={`v15-card nt15-kagit is-${not.renk}`}>
        <div className="nt15-renk" role="radiogroup" aria-label="Not rengi">
          {RENKLER.map((r) => <button key={r} type="button" role="radio" aria-checked={not.renk === r} aria-label={RENK_AD[r]} className={`nt15-rk is-${r}${not.renk === r ? ' is-on' : ''}`} onClick={() => guncelle({ renk: r })} />)}
          <span className="nt15-bosluk" />
          <button type="button" className="v15-ib" onClick={paylas} aria-label="Paylaş"><Share2 aria-hidden /></button>
          <button type="button" className="v15-ib" onClick={sil} aria-label="Notu sil"><Trash2 aria-hidden /></button>
          <button type="button" className="v15-ib" onClick={kapat} aria-label="Kapat"><X aria-hidden /></button>
        </div>
        <div ref={kap} className={`nt15-yuzey${arac !== 'yaz' ? ' is-ciz' : ''}`}
          onPointerDown={bas} onPointerMove={surukle} onPointerUp={birak} onPointerCancel={birak}>
          <input className="nt15-baslik" value={not.baslik} onChange={(e) => guncelle({ baslik: e.target.value.slice(0, 120) })} placeholder="Başlık" aria-label="Başlık" readOnly={arac !== 'yaz'} />
          <textarea className="nt15-metin" value={not.metin} onChange={(e) => guncelle({ metin: e.target.value })} placeholder="Yazmaya başla…" aria-label="Not metni" readOnly={arac !== 'yaz'}
            ref={(t) => { if (t) { t.style.height = 'auto'; t.style.height = `${t.scrollHeight}px`; } }} />
          <canvas ref={tuval} className="nt15-tuval" aria-hidden />
        </div>
        <p className="v15-cap nt15-not">{tarihYaz(not.at)} · {arac === 'yaz' ? 'Kalemle çizmek için üstten Kalem\'i seç.' : arac === 'silgi' ? 'Silmek istediğin çizginin üstünden geç.' : 'Parmağınla ya da kalemle çiz.'}</p>
      </div>
    </div>
  );
}
