/**
 * Sesli ders ek kipleri (v15 tasarım dalı):
 *  - S06 CdSesliKitap: sesli kitap kipi (kapak, ses dalgası, uyku zamanlayıcısı, sade dinleme)
 *  - S07 CdMasa: üç bölmeli masa (≥1200px) — solda bölümler + Vurgularım, ortada PDF, sağda metin
 *  - S18 CdBolumSonu: bölüm bitince "Bölüm bitti" kutusu, 3 soruyla pekiştir, "Devam (5 sn)"
 *  - U12 CdYanKapsul: ses çalarken yan menüde küçük oynatıcı
 *  - S10 cdAiIste + CdAiPanel: seçim çubuğundaki "Açıkla / Soru üret" (yalnız kullanıcı tıklamasıyla,
 *    mevcut /api/ai/general-chat ucu; otomatik çağrı yok — AGENTS kural 20)
 * Çizim katmanına (kural 18) dokunmaz.
 */
import React, { useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { Check, Clock, Pause, Play, SkipBack, SkipForward, Star, Text, X } from 'lucide-react';
import {
  cdAralik, cdAtla, cdBolumAtla, cdCumleAraligi, cdDurum, cdDuraklat, cdHizDongu, cdParagrafa, cdSar, cdToggle,
  fmtSure, useCd, type CdCikmisKonum, type CdDetay,
} from './canliDersStore';
import { cdCikmisAc, CdCikmisPencereKok } from './CdCikmisChip';
import { useYildizliParagraflar } from '../../services/yildizliParagrafStore';
import { linkClick, navigateTo, pathFor } from '../../router';
import { ApiService } from '../../services/api';
import './cdSesliEk.css';

/* ---------------- ortak: o an okunan cümle ---------------- */
function paragrafBul(d: CdDetay, i: number) {
  for (const b of d.bolumler) for (const p of b.paragraflar) if (p.i === i) return p;
  return null;
}
export function useOkunanCumle(detay: CdDetay | null): string {
  const aktif = useCd((s) => (detay && s.key === detay.key ? s.aktif : -1));
  const cumle = useCd((s) => (detay && s.key === detay.key ? s.cumle : -1));
  return useMemo(() => {
    if (!detay || aktif < 0) return '';
    const p = paragrafBul(detay, aktif);
    if (!p) return '';
    const r = cumle >= 0 ? cdCumleAraligi(aktif, cumle) : null;
    return (r ? p.metin.slice(r[0], r[1]) : p.metin).trim();
  }, [detay, aktif, cumle]);
}

/* ---------------- uyku zamanlayıcısı (S06) ---------------- */
type Uyku = { bitis: number | null; bolumSonu: boolean };
let uyku: Uyku = { bitis: null, bolumSonu: false };
const uykuDinle = new Set<() => void>();
const uykuAyarla = (u: Uyku) => { uyku = u; uykuDinle.forEach((f) => f()); };
let uykuSaat: number | null = null;
function uykuKur(dk: number | 'bolum' | null) {
  if (uykuSaat) { window.clearInterval(uykuSaat); uykuSaat = null; }
  if (dk === null) return uykuAyarla({ bitis: null, bolumSonu: false });
  if (dk === 'bolum') return uykuAyarla({ bitis: null, bolumSonu: true });
  uykuAyarla({ bitis: Date.now() + dk * 60000, bolumSonu: false });
  // Yalnız kullanıcının kurduğu zamanlayıcı: süre dolunca sesi durdurur (LLM/ağ çağrısı yok)
  uykuSaat = window.setInterval(() => {
    if (uyku.bitis && Date.now() >= uyku.bitis) { cdDuraklat(); uykuKur(null); } else uykuAyarla({ ...uyku });
  }, 1000);
}
const useUyku = () => useSyncExternalStore((f) => { uykuDinle.add(f); return () => void uykuDinle.delete(f); }, () => uyku);

function UykuSecici() {
  const u = useUyku();
  const [acik, setAcik] = useState(false);
  const kalan = u.bitis ? Math.max(0, Math.ceil((u.bitis - Date.now()) / 60000)) : 0;
  const etiket = u.bolumSonu ? 'Uyku: bölüm sonunda' : u.bitis ? `Uyku: ${kalan} dk` : 'Uyku zamanlayıcısı';
  return (
    <span className="cdk-uyku">
      <button type="button" className={`cdk-chip${u.bitis || u.bolumSonu ? ' is-on' : ''}`} aria-expanded={acik} onClick={() => setAcik((x) => !x)}>
        <Clock aria-hidden /> {etiket}
      </button>
      {acik && (
        <span className="cdk-uyku-menu" role="menu">
          {[15, 30, 45].map((dk) => (
            <button key={dk} type="button" role="menuitem" onClick={() => { uykuKur(dk); setAcik(false); }}>{dk} dk</button>
          ))}
          <button type="button" role="menuitem" onClick={() => { uykuKur('bolum'); setAcik(false); }}>Bölüm sonunda</button>
          {(u.bitis || u.bolumSonu) && <button type="button" role="menuitem" onClick={() => { uykuKur(null); setAcik(false); }}>Kapat</button>}
        </span>
      )}
    </span>
  );
}

/* ---------------- S06 sesli kitap ---------------- */
function Dalga({ oran, calar }: { oran: number; calar: boolean }) {
  const n = 48;
  const boy = useMemo(() => Array.from({ length: n }, (_, k) => 0.25 + 0.75 * Math.abs(Math.sin(k * 1.7) * Math.cos(k * 0.43))), []);
  return (
    <div className={`cdk-dalga${calar ? ' is-calar' : ''}`} aria-hidden>
      {boy.map((h, k) => <i key={k} className={k / n < oran ? 'is-gecti' : ''} style={{ height: `${Math.round(h * 100)}%`, animationDelay: `${(k % 7) * 90}ms` }} />)}
    </div>
  );
}

export function CdSesliKitap({ detay, onMetin, onBasla }: { detay: CdDetay; onMetin: () => void; onBasla: () => void }) {
  const bu = useCd((s) => s.key === detay.key);
  const t = useCd((s) => (s.key === detay.key ? Math.floor(s.t) : 0));
  const dur = useCd((s) => (s.key === detay.key ? s.dur : 0));
  const calar = useCd((s) => s.key === detay.key && s.playing);
  const rate = useCd((s) => s.rate);
  const bolum = useCd((s) => (s.key === detay.key ? s.bolum : -1));
  const cumle = useOkunanCumle(detay);
  const oran = dur > 0 ? t / dur : 0;
  const ara = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!bu || !dur) return;
    const r = e.currentTarget.getBoundingClientRect();
    cdAtla(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * dur);
  };
  return (
    <section className="cdk" aria-label="Sesli kitap">
      <div className="cdk-kapak" aria-hidden><span>{String(detay.no || '').slice(0, 6) || '♪'}</span></div>
      <div className="cdk-bas">
        <small>{detay.brans || 'Sesli ders'}{detay.hoca ? ` · ${detay.hoca}` : ''}</small>
        <h2>{detay.baslik}</h2>
        {bolum >= 0 && <span>Bölüm {bolum + 1}{detay.bolumler[bolum]?.baslik ? ` · ${detay.bolumler[bolum].baslik}` : ''}</span>}
      </div>
      <p className="cdk-cumle" aria-live="polite">{cumle ? `“${cumle}”` : 'Dinlemeye başlamak için oynat.'}</p>
      <div className="cdk-ilerleme">
        <div className="cdk-dalga-kap" onClick={ara} role="presentation"><Dalga oran={oran} calar={calar} /></div>
        <div className="cdk-sure"><span>{fmtSure(t)}</span><span>{fmtSure(dur)}</span></div>
      </div>
      <div className="cdk-tus">
        <button type="button" className="cdk-ince" onClick={() => cdSar(-15)} disabled={!bu} aria-label="15 saniye geri">−15</button>
        <button type="button" className="cdk-ib" onClick={() => cdBolumAtla(-1)} disabled={!bu} aria-label="Önceki bölüm"><SkipBack aria-hidden /></button>
        <button type="button" className="cdk-oyn" onClick={() => (bu ? cdToggle() : onBasla())} aria-label={calar ? 'Duraklat' : 'Oynat'}>
          {calar ? <Pause aria-hidden /> : <Play aria-hidden />}
        </button>
        <button type="button" className="cdk-ib" onClick={() => cdBolumAtla(1)} disabled={!bu} aria-label="Sonraki bölüm"><SkipForward aria-hidden /></button>
        <button type="button" className="cdk-ince" onClick={() => cdSar(15)} disabled={!bu} aria-label="15 saniye ileri">+15</button>
      </div>
      <div className="cdk-alt">
        <button type="button" className="cdk-chip" onClick={() => cdHizDongu()} aria-label="Oynatma hızı">{rate.toLocaleString('tr-TR')}×</button>
        <UykuSecici />
        <button type="button" className="cdk-chip" onClick={onMetin}><Text aria-hidden /> Metin</button>
      </div>
      <CdCikmisPencereKok />
    </section>
  );
}

/* ---------------- S07 üç bölmeli masa ---------------- */
export const MASA_SORGU = '(min-width: 1200px)';
export function useMasaUygun(): boolean {
  const [v, setV] = useState(() => typeof window !== 'undefined' && window.matchMedia(MASA_SORGU).matches);
  useEffect(() => {
    const m = window.matchMedia(MASA_SORGU);
    const f = () => setV(m.matches);
    m.addEventListener('change', f);
    return () => m.removeEventListener('change', f);
  }, []);
  return v;
}

export function CdMasa({ detay, orta, sag, onParagraf }: { detay: CdDetay; orta: React.ReactNode; sag: React.ReactNode; onParagraf: (i: number) => void }) {
  const bolum = useCd((s) => (s.key === detay.key ? s.bolum : -1));
  useCd((s) => s.zs); // zamanlama değişince başlangıç saatleri yenilensin
  const yildizli = useYildizliParagraflar();
  const benim = yildizli.filter((y) => y.kaynak === 'canli_ders' && y.meta?.dersKey === detay.key);
  const git = (i: number) => { if (cdDurum().key === detay.key) cdParagrafa(i, false); onParagraf(i); };
  return (
    <div className="cdm">
      <aside className="cdm-sol" aria-label="Bölümler ve vurgularım">
        <h3>Bölümler</h3>
        <ol className="cdm-bolumler">
          {detay.bolumler.map((b, bi) => {
            const i0 = b.paragraflar[0]?.i;
            const t0 = i0 != null ? cdAralik(i0)?.[0] : undefined;
            return (
              <li key={bi}>
                <button type="button" className={bi === bolum ? 'is-on' : ''} aria-current={bi === bolum ? 'true' : undefined} onClick={() => i0 != null && git(i0)}>
                  <span>{b.baslik || `Bölüm ${bi + 1}`}</span>
                  {t0 != null && <small>{fmtSure(Math.floor(t0))}</small>}
                </button>
              </li>
            );
          })}
        </ol>
        <h3>Vurgularım</h3>
        {benim.length ? (
          <ul className="cdm-vurgu">
            {benim.map((y) => {
              const i = Number(y.meta?.paragrafIndex);
              const t0 = Number.isFinite(i) ? cdAralik(i)?.[0] : undefined;
              return (
                <li key={y.id}>
                  <button type="button" onClick={() => Number.isFinite(i) && git(i)}>
                    <Star aria-hidden />
                    <span>{y.metin.length > 90 ? `${y.metin.slice(0, 88)}…` : y.metin}</span>
                    {t0 != null && <small>{fmtSure(Math.floor(t0))}</small>}
                  </button>
                </li>
              );
            })}
          </ul>
        ) : <p className="cdm-bos">Metinde bir paragrafı yıldızlayınca ya da seçip "Spot yap" deyince burada görünür.</p>}
      </aside>
      <div className="cdm-orta">{orta}</div>
      <div className="cdm-sag">{sag}</div>
    </div>
  );
}

/* ---------------- S18 bölüm sonu ---------------- */
const DUR_KEY = 'medsoru_cd_bolum_sonu_dur';
const durOku = () => { try { return localStorage.getItem(DUR_KEY) === '1'; } catch { return false; } };
const durDinle = new Set<() => void>();
export function cdBolumSonuDurAyarla(v: boolean) { try { localStorage.setItem(DUR_KEY, v ? '1' : '0'); } catch { /* yok */ } durDinle.forEach((f) => f()); }
export const useCdBolumSonuDur = () => useSyncExternalStore((f) => { durDinle.add(f); return () => void durDinle.delete(f); }, durOku);

function bolumSorulari(d: CdDetay, bi: number): CdCikmisKonum[] {
  const b = d.bolumler[bi];
  if (!b || !d.cikmisKonum?.length) return [];
  const iler = new Set(b.paragraflar.map((p) => p.i));
  const gor = new Set<string>();
  return d.cikmisKonum.filter((q) => iler.has(q.p) && q.dogrulandi !== false && !gor.has(q.id) && gor.add(q.id)).slice(0, 3);
}

export function CdBolumSonu({ detay }: { detay: CdDetay }) {
  const dur = useCdBolumSonuDur();
  const [biten, setBiten] = useState<number | null>(null);
  const [say, setSay] = useState(5);
  const onceki = useRef<{ b: number; t: number }>({ b: -1, t: 0 });
  const b = useCd((s) => (s.key === detay.key ? s.bolum : -1));

  useEffect(() => {
    const s = cdDurum();
    const o = onceki.current;
    onceki.current = { b, t: s.t };
    // Doğal geçiş: çalarken bir sonraki bölüme sürekli zamanla geçildi (atlama/sarma değil)
    if (s.key !== detay.key || !s.playing || o.b < 0 || b !== o.b + 1) return;
    if (s.t - o.t > 60 || s.t < o.t) return;
    const r0 = cdAralik(detay.bolumler[b]?.paragraflar[0]?.i ?? -1);
    if (!r0 || Math.abs(s.t - r0[0]) > 2) return;
    if (uyku.bolumSonu) { cdDuraklat(); uykuKur(null); return; }
    if (!dur) return; // varsayılan: bölüm arasında otomatik durma yok
    cdDuraklat();
    setBiten(o.b);
    setSay(5);
  }, [b, detay, dur]);

  useEffect(() => {
    if (biten === null || dur) return;
    if (say <= 0) { setBiten(null); if (!cdDurum().playing) cdToggle(); return; }
    const id = window.setTimeout(() => setSay((x) => x - 1), 1000);
    return () => window.clearTimeout(id);
  }, [biten, say, dur]);

  if (biten === null) return null;
  const bb = detay.bolumler[biten];
  const r0 = cdAralik(bb?.paragraflar[0]?.i ?? -1);
  const r1 = cdAralik(detay.bolumler[biten + 1]?.paragraflar[0]?.i ?? -1);
  const sure = r0 && r1 ? Math.max(0, Math.round(r1[0] - r0[0])) : 0;
  const sorular = bolumSorulari(detay, biten);
  const sira = detay.bolumler[biten + 1]?.baslik;
  const devam = () => { setBiten(null); if (!cdDurum().playing) cdToggle(); };
  return createPortal(
    <div className="cdbs" role="dialog" aria-label={`Bölüm ${biten + 1} bitti`}>
      <div className="cdbs-kutu">
        <button type="button" className="cdbs-x" onClick={() => setBiten(null)} aria-label="Kapat"><X aria-hidden /></button>
        <span className="cdbs-ik" aria-hidden><Check /></span>
        <b>Bölüm {biten + 1} bitti</b>
        <p>
          {bb?.baslik ? `${bb.baslik} · ` : ''}{sure ? `${Math.floor(sure / 60)} dk ${sure % 60} sn dinledin.` : ''}
          {sira ? ` Sıradaki: ${sira}.` : ''}
        </p>
        <div className="cdbs-tus">
          {sorular.length > 0 && (
            <button type="button" className="cdbs-ikincil" onClick={() => { setBiten(null); cdCikmisAc(sorular); }}>
              {sorular.length} soruyla pekiştir
            </button>
          )}
          <button type="button" className="cdbs-ana" onClick={devam}>{dur ? 'Devam' : `Devam (${say} sn)`}</button>
        </div>
        <label className="cdbs-anahtar">
          <input type="checkbox" checked={dur} onChange={(e) => cdBolumSonuDurAyarla(e.target.checked)} />
          <span>Bölüm sonlarında dur</span>
        </label>
      </div>
    </div>,
    document.body,
  );
}

/* ---------------- U12 yan menü kapsülü ---------------- */
export function CdYanKapsul() {
  const key = useCd((s) => s.key);
  const baslik = useCd((s) => s.baslik);
  const calar = useCd((s) => s.playing);
  const oran = useCd((s) => (s.dur > 0 ? Math.min(1, s.t / s.dur) : 0));
  if (!key) return null;
  const href = pathFor('canli_ders', key);
  return (
    <div className={`cdy${calar ? ' is-calar' : ''}`}>
      <button type="button" className="cdy-oyn" onClick={() => cdToggle()} aria-label={calar ? 'Duraklat' : 'Oynat'}>
        {calar ? <Pause aria-hidden /> : <Play aria-hidden />}
      </button>
      <a className="cdy-t" href={href} onClick={linkClick(() => navigateTo(href))} title={baslik}>
        <small>{calar ? 'Şimdi çalınıyor' : 'Duraklatıldı'}</small>
        <b>{baslik}</b>
      </a>
      <i className="cdy-bar" style={{ width: `${Math.round(oran * 100)}%` }} aria-hidden />
    </div>
  );
}

/* ---------------- S10 Açıkla / Soru üret (yalnız tıklamayla) ---------------- */
type AiDurum = { tur: 'acikla' | 'soru'; metin: string; yanit: string | null; hata: string | null } | null;
let ai: AiDurum = null;
const aiDinle = new Set<() => void>();
const aiAyarla = (d: AiDurum) => { ai = d; aiDinle.forEach((f) => f()); };

export function cdAiIste(tur: 'acikla' | 'soru', metin: string, ders: string) {
  const m = metin.trim().slice(0, 600);
  aiAyarla({ tur, metin: m, yanit: null, hata: null });
  const message = tur === 'acikla'
    ? `"${ders}" dersindeki şu cümleyi tıp öğrencisine kısa, maddeli ve sade Türkçe ile açıkla: "${m}"`
    : `"${ders}" dersindeki şu bilgiden, yalnız bu bilgiye dayanan, 5 şıklı tek bir çoktan seçmeli soru yaz; doğru cevabı ve kısa gerekçesini ekle: "${m}"`;
  void ApiService.sendGeneralAiChat({ message, mode: tur === 'acikla' ? 'explain' : 'general', provider: 'auto', allowCloudFallback: true, timeoutMs: 45000 })
    .then((r) => { if (ai?.metin !== m) return; aiAyarla({ tur, metin: m, yanit: r.success ? (r.reply || '') : null, hata: r.success ? null : (r.error || 'Yanıt alınamadı.') }); })
    .catch(() => { if (ai?.metin === m) aiAyarla({ tur, metin: m, yanit: null, hata: 'Bağlantı hatası.' }); });
}

export function CdAiPanel() {
  const d = useSyncExternalStore((f) => { aiDinle.add(f); return () => void aiDinle.delete(f); }, () => ai);
  if (!d) return null;
  return createPortal(
    <div className="cdai" role="dialog" aria-label={d.tur === 'acikla' ? 'Açıklama' : 'Üretilen soru'}>
      <div className="cdai-bas">
        <b>{d.tur === 'acikla' ? 'Açıkla' : 'Soru üret'}</b>
        <button type="button" onClick={() => aiAyarla(null)} aria-label="Kapat"><X aria-hidden /></button>
      </div>
      <blockquote>{d.metin}</blockquote>
      {d.hata ? <p className="cdai-hata">{d.hata}</p>
        : d.yanit === null ? <p className="cdai-bekle"><span className="cd-spin" aria-hidden /> Yapay zekâ yanıtlıyor…</p>
          : <div className="cdai-yanit">{d.yanit}</div>}
      <small>Yapay zekâ yanıtıdır; ders notuyla karşılaştırarak kullan.</small>
    </div>,
    document.body,
  );
}
