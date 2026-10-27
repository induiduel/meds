/**
 * Ödül kutlaması: kuyruktaki her ödül için tam ekran kart — madalya açılışı, sayaç, parçacık efekti.
 * Efekt seçilebilir (kilitle açılır): konfeti (varsayılan), mitoz (hücreler bölünerek dağılır), ATP sentaz (dönen rotordan
 * fırlayan ATP molekülleri). En üst seviye ödüllerde altın halka + ışın. Hareket azaltma tercihinde parçacık yok.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { kutlamaKapat, kutlamalariAtla, sayi, useBasarim, type Odul } from '../../services/basarimIstemci';
import { AtpIkon, Ikon } from './ortak';

type Efekt = 'konfeti' | 'mitoz' | 'sentaz' | 'kalp' | 'asklepios';

const hareketAz = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

function Parcacik({ efekt, renk, ust }: { efekt: Efekt; renk: string; ust: boolean }) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const c = ref.current;
    if (!c || hareketAz()) return;
    const ctx = c.getContext('2d');
    if (!ctx) return;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const boyut = () => { c.width = c.clientWidth * dpr; c.height = c.clientHeight * dpr; };
    boyut();
    window.addEventListener('resize', boyut);
    const W = () => c.width, H = () => c.height;
    const css = getComputedStyle(document.documentElement);
    const palet = [renk, css.getPropertyValue('--color-accent').trim() || '#0A84FF', '#FFD60A', '#30D158', '#FF375F', '#BF5AF2'];
    type P = { x: number; y: number; vx: number; vy: number; r: number; a: number; va: number; renk: string; omur: number; tur: number; bol?: boolean };
    const ps: P[] = [];
    const cx = W() / 2, cy = H() * 0.42;
    const say = (ust ? 1.6 : 1) * (efekt === 'konfeti' ? 140 : efekt === 'mitoz' ? 26 : efekt === 'kalp' ? 34 : efekt === 'asklepios' ? 46 : 36);
    for (let i = 0; i < say; i++) {
      const aci = Math.random() * Math.PI * 2;
      const hiz = (efekt === 'konfeti' ? 6 + Math.random() * 9 : 2 + Math.random() * 4) * dpr;
      ps.push({
        x: cx, y: cy, vx: Math.cos(aci) * hiz, vy: Math.sin(aci) * hiz - (efekt === 'konfeti' ? 6 * dpr : 0),
        r: (efekt === 'konfeti' ? 4 + Math.random() * 5 : efekt === 'mitoz' ? 10 + Math.random() * 10 : 9) * dpr,
        a: Math.random() * 6, va: (Math.random() - 0.5) * 0.3, renk: palet[i % palet.length], omur: 0, tur: i % 3,
      });
    }
    let kare = 0;
    let raf = 0;
    const atp = (p: P) => {
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
      ctx.fillStyle = p.renk; ctx.globalAlpha *= 0.95;
      ctx.beginPath(); ctx.arc(-p.r, 0, p.r * 0.55, 0, 7); ctx.fill();
      for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.arc(p.r * 0.2 + k * p.r * 0.75, 0, p.r * 0.32, 0, 7); ctx.fill(); }
      ctx.restore();
    };
    const ciz = () => {
      kare++;
      ctx.clearRect(0, 0, W(), H());
      if (efekt === 'asklepios' && kare < 190) {
        // Asklepios Asası: altın asa belirir, yılan alttan yukarı dolanarak tırmanır, sonra söner
        const alfa = kare < 150 ? Math.min(1, kare / 20) : Math.max(0, 1 - (kare - 150) / 40);
        const boy = 120 * dpr, ust = cy - boy, alt = cy + boy;
        // kart ortada ve opak: asalar kartın iki yanında (dar ekranda kenar boşluğunda) çizilir
        const yan = Math.max(18 * dpr, Math.min(cx - 34 * dpr, (190 + 52) * dpr));
        for (const cx of [W() / 2 - yan, W() / 2 + yan]) {
        ctx.save(); ctx.globalAlpha = alfa;
        const asa = ctx.createLinearGradient(cx - 6 * dpr, 0, cx + 6 * dpr, 0);
        asa.addColorStop(0, '#8A6A00'); asa.addColorStop(0.5, '#FFE58A'); asa.addColorStop(1, '#8A6A00');
        ctx.fillStyle = asa; ctx.beginPath(); ctx.roundRect?.(cx - 5 * dpr, ust - 10 * dpr, 10 * dpr, boy * 2 + 20 * dpr, 5 * dpr); ctx.fill();
        const ilerle = Math.min(1, Math.max(0, (kare - 12) / 70));
        const adim = 140, sar = 3.2;
        const nokta = (i: number) => { const t = i / adim; const y = alt - t * boy * 1.9; return { x: cx + Math.sin(t * Math.PI * 2 * sar) * 26 * dpr * (1 - t * 0.25), y, on: Math.cos(t * Math.PI * 2 * sar) > 0 }; };
        const son = Math.floor(adim * ilerle);
        // önce asanın arkasında kalan parçalar, sonra öndekiler (dolanma derinliği)
        for (const katman of [false, true]) {
          for (let i = 1; i <= son; i++) {
            const a = nokta(i - 1), b = nokta(i);
            if (b.on !== katman) continue;
            ctx.strokeStyle = katman ? '#22C55E' : '#166534'; ctx.lineWidth = (katman ? 9 : 7) * dpr * (1 - (i / adim) * 0.35); ctx.lineCap = 'round';
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
        if (son > 2) {
          const h = nokta(son), o = nokta(son - 2);
          const aci = Math.atan2(h.y - o.y, h.x - o.x);
          ctx.save(); ctx.translate(h.x, h.y); ctx.rotate(aci); ctx.fillStyle = '#15803D';
          ctx.beginPath(); ctx.ellipse(4 * dpr, 0, 10 * dpr, 6.5 * dpr, 0, 0, 7); ctx.fill();
          ctx.fillStyle = '#FDE047'; ctx.beginPath(); ctx.arc(8 * dpr, -2.5 * dpr, 1.6 * dpr, 0, 7); ctx.fill();
          if (kare % 30 < 12) { ctx.strokeStyle = '#EF4444'; ctx.lineWidth = 1.5 * dpr; ctx.beginPath(); ctx.moveTo(13 * dpr, 0); ctx.lineTo(19 * dpr, -2 * dpr); ctx.moveTo(13 * dpr, 0); ctx.lineTo(19 * dpr, 2 * dpr); ctx.stroke(); }
          ctx.restore();
        }
        ctx.restore();
        }
      }
      if (efekt === 'sentaz' && kare < 140) {
        // dönen F0 rotoru
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(kare * 0.12); ctx.strokeStyle = renk; ctx.lineWidth = 3 * dpr; ctx.globalAlpha = Math.max(0, 1 - kare / 140);
        for (let k = 0; k < 8; k++) { ctx.rotate(Math.PI / 4); ctx.beginPath(); ctx.moveTo(70 * dpr, 0); ctx.lineTo(96 * dpr, 0); ctx.stroke(); }
        ctx.restore();
      }
      let canli = 0;
      for (const p of ps) {
        p.omur++;
        if (efekt === 'konfeti') { p.vy += 0.25 * dpr; p.vx *= 0.985; p.vy *= 0.985; }
        else if (efekt === 'mitoz') { p.vx *= 0.97; p.vy = p.vy * 0.97 + 0.04 * dpr; }
        else if (efekt === 'kalp') { p.vx *= 0.97; p.vy = p.vy * 0.97 - 0.06 * dpr; }
        else if (efekt === 'asklepios') { if (kare < 70) { p.omur = 0; continue; } p.vx *= 0.96; p.vy = p.vy * 0.96 - 0.05 * dpr; }
        else { const aci = Math.atan2(p.vy, p.vx) + 0.025; const h = Math.hypot(p.vx, p.vy) * 1.004; p.vx = Math.cos(aci) * h; p.vy = Math.sin(aci) * h; }
        p.x += p.vx; p.y += p.vy; p.a += p.va;
        const alfa = Math.max(0, 1 - p.omur / (efekt === 'konfeti' ? 170 : 150));
        if (alfa <= 0 || p.y > H() + 40) continue;
        canli++;
        ctx.globalAlpha = alfa;
        if (efekt === 'konfeti') {
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.renk;
          if (p.tur === 0) ctx.fillRect(-p.r, -p.r / 2.5, p.r * 2, p.r / 1.25);
          else if (p.tur === 1) { ctx.beginPath(); ctx.arc(0, 0, p.r / 1.6, 0, 7); ctx.fill(); }
          else { ctx.beginPath(); ctx.moveTo(0, -p.r); ctx.lineTo(p.r, p.r); ctx.lineTo(-p.r, p.r); ctx.fill(); }
          ctx.restore();
        } else if (efekt === 'asklepios') {
          // Işıltı: dört köşeli yıldız (yeşil / altın)
          const z = p.r * 0.55 * (0.7 + 0.3 * Math.sin(p.omur * 0.3));
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.tur === 0 ? '#E5B000' : p.tur === 1 ? '#4ADE80' : '#BBF7D0';
          ctx.beginPath(); ctx.moveTo(0, -z); ctx.quadraticCurveTo(0, 0, z, 0); ctx.quadraticCurveTo(0, 0, 0, z); ctx.quadraticCurveTo(0, 0, -z, 0); ctx.quadraticCurveTo(0, 0, 0, -z); ctx.fill();
          ctx.restore();
        } else if (efekt === 'kalp') {
          // Kalp: atım ritmiyle büyüyüp küçülür (EKG gibi çift vuruş)
          const faz = (p.omur % 50) / 50;
          const atim = 1 + (faz < 0.12 ? faz * 2.2 : faz < 0.24 ? (0.24 - faz) * 2.2 : faz < 0.34 ? (faz - 0.24) * 1.6 : faz < 0.44 ? (0.44 - faz) * 1.6 : 0);
          const z = p.r * 0.9 * atim;
          ctx.save(); ctx.translate(p.x, p.y); ctx.scale(z / 10, z / 10); ctx.fillStyle = p.tur === 0 ? '#FF375F' : p.tur === 1 ? '#FF6B81' : p.renk;
          ctx.beginPath(); ctx.moveTo(0, 3); ctx.bezierCurveTo(-10, -5, -5, -12, 0, -6); ctx.bezierCurveTo(5, -12, 10, -5, 0, 3); ctx.fill();
          ctx.restore();
        } else if (efekt === 'mitoz') {
          // hücre: zar + çekirdek; 40. karede ikiye bölünür
          if (!p.bol && p.omur === 40 && ps.length < 140) {
            p.bol = true; p.r *= 0.72;
            ps.push({ ...p, vx: -p.vy * 0.8, vy: p.vx * 0.8, omur: 40, bol: true });
          }
          const ayrim = p.omur > 28 && p.omur < 40 ? (p.omur - 28) / 12 : 0;
          ctx.strokeStyle = p.renk; ctx.fillStyle = p.renk; ctx.lineWidth = 2 * dpr;
          ctx.beginPath(); ctx.ellipse(p.x, p.y, p.r * (1 + ayrim * 0.6), p.r * (1 - ayrim * 0.25), p.a, 0, 7); ctx.stroke();
          ctx.globalAlpha = alfa * 0.25; ctx.fill(); ctx.globalAlpha = alfa;
          ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 0.32, 0, 7); ctx.fill();
        } else atp(p);
      }
      ctx.globalAlpha = 1;
      if (canli > 0 || kare < (efekt === 'asklepios' ? 190 : 140)) raf = requestAnimationFrame(ciz);
    };
    raf = requestAnimationFrame(ciz);
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', boyut); };
  }, [efekt, renk, ust]);
  return <canvas ref={ref} className={`bs-k-tuval${efekt === 'asklepios' ? ' is-ust-katman' : ''}`} aria-hidden />;
}

/** 0'dan hedefe sayar. */
function Sayac({ hedef, sure = 900 }: { hedef: number; sure?: number }) {
  const [v, setV] = useState(hareketAz() ? hedef : 0);
  useEffect(() => {
    if (hareketAz()) { setV(hedef); return; }
    let raf = 0; const t0 = performance.now();
    const f = (t: number) => { const x = Math.min(1, (t - t0) / sure); setV(Math.round(hedef * (1 - Math.pow(1 - x, 3)))); if (x < 1) raf = requestAnimationFrame(f); };
    raf = requestAnimationFrame(f);
    return () => cancelAnimationFrame(raf);
  }, [hedef, sure]);
  return <>{sayi(v)}</>;
}

const BASLIK: Record<Odul['t'], string> = { hedef: 'Hedef tamamlandı', basarim: 'Başarım açıldı', siralama: 'Sıralama ödülü', baslangic: 'Hoş geldin', harcama: 'Kilit açıldı', yonetici: 'Yönetici hediyesi' };

export function KutlamaKatmani() {
  const { kutlama, tanim, durum } = useBasarim();
  const o = kutlama[0];
  const dugme = useRef<HTMLButtonElement>(null);
  const bilgi = useMemo(() => {
    if (!o) return null;
    const b = o.ref ? tanim.basarimlar.find((x) => x.id === o.ref) : undefined;
    const h = o.ref ? tanim.hedefler.find((x) => x.id === o.ref) : undefined;
    const seviye = Number(o.id.split(':').pop()) || 0;
    const renk = b?.renk || (o.t === 'siralama' ? '#F59E0B' : o.ust ? '#EAB308' : 'var(--color-accent)');
    return { ikon: b?.ikon || h?.ikon || (o.t === 'siralama' ? 'trophy' : 'crown'), renk, seviye, ad: (b?.ad || h?.ad || o.ad.split(' · ')[0]), aciklama: b?.aciklama };
  }, [o, tanim]);
  const efekt: Efekt = durum?.secili.efekt === 'efekt_mitoz' ? 'mitoz' : durum?.secili.efekt === 'efekt_sentaz' ? 'sentaz' : durum?.secili.efekt === 'efekt_kalp' ? 'kalp' : durum?.secili.efekt === 'efekt_asklepios' ? 'asklepios' : 'konfeti';

  useEffect(() => {
    if (!o) return;
    dugme.current?.focus({ preventScroll: true });
    try { if (o.a > 0 || o.ust) navigator.vibrate?.([30, 40, 60]); } catch { /* */ }
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape' || e.key === 'Enter') { e.preventDefault(); kutlamaKapat(); } };
    window.addEventListener('keydown', tus);
    return () => window.removeEventListener('keydown', tus);
  }, [o?.id]);

  if (!o || !bilgi) return null;
  const renkCss = bilgi.renk.startsWith('var(') ? bilgi.renk : bilgi.renk;
  const parlakRenk = bilgi.renk.startsWith('#') ? bilgi.renk : '#0A84FF';
  return createPortal(
    <div className={`bs-k${o.ust ? ' is-ust' : ''}`} role="dialog" aria-modal="true" aria-labelledby="bs-k-ad" key={o.id} style={{ '--bs-renk': renkCss } as React.CSSProperties}>
      <div className="bs-k-perde" onClick={kutlamaKapat} />
      <Parcacik efekt={efekt} renk={parlakRenk} ust={!!o.ust} />
      <div className="bs-k-kart">
        <div className="bs-k-madalya" aria-hidden>
          {o.ust && <span className="bs-k-isin" />}
          <span className="bs-k-halka" />
          <span className="bs-k-yuz"><Ikon ad={bilgi.ikon} /></span>
          {bilgi.seviye > 0 && o.t !== 'siralama' && <span className="bs-k-seviye">{bilgi.seviye}</span>}
        </div>
        <p className="bs-k-ust-yazi">{o.ust ? `${BASLIK[o.t]} · en üst seviye` : BASLIK[o.t]}</p>
        <h2 id="bs-k-ad" className="bs-k-ad">{o.t === 'siralama' ? o.ad : bilgi.ad}</h2>
        {o.t !== 'siralama' && bilgi.seviye > 0 && <p className="bs-k-alt">{bilgi.seviye}. seviye{bilgi.aciklama ? ` · ${bilgi.aciklama}` : ''}</p>}
        <div className="bs-k-odul">
          {o.p > 0 && <span className="bs-k-p"><b>+<Sayac hedef={o.p} /></b> puan</span>}
          {o.a > 0 && <span className="bs-k-a"><AtpIkon boyut={20} canli /><b>+<Sayac hedef={o.a} sure={1200} /></b> mol ATP</span>}
        </div>
        {o.a > 0 && durum && durum.atp.tavan != null && durum.atp.kuyrukta > 0 && (
          <p className="bs-k-not">Günlük {durum.atp.tavan} mol sınırı dolduysa ATP kuyruğa alınır, sonraki günlerde hesabına geçer.</p>
        )}
        <div className="bs-k-eylem">
          {kutlama.length > 1 && <button type="button" className="bs-k-atla" onClick={kutlamalariAtla}>Hepsini geç ({kutlama.length - 1})</button>}
          <button ref={dugme} type="button" className="bs-k-devam" onClick={kutlamaKapat}>{kutlama.length > 1 ? 'Sıradaki' : 'Harika'}</button>
        </div>
      </div>
    </div>,
    document.body,
  );
}
