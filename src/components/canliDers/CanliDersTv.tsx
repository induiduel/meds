/**
 * Canlı ders · TV kumandası. TV tarayıcısı (Tizen, webOS, Android/Google TV, Fire TV, Bravia, Vidaa…) ya da ?tv=1 ile
 * açılınca ders ekranında kumanda tuşları çalışır ve ilk açılışta kısa bir tanıtım gösterilir (sonra "Kumanda" düğmesiyle).
 */
import React, { useEffect, useRef, useState } from 'react';
import { Tv, X } from 'lucide-react';

const TV_UA = /smart-?tv|smarttv|tizen|web0s|webos|netcast|bravia|hbbtv|vidaa|viera|philipstv|roku|crkey|aft[a-z]{1,3}\b|googletv|android tv|\btv\b|appletv|tvos/i;
const TV_KEY = 'medsoru_canli_ders_tv';
const TANITIM_KEY = 'medsoru_canli_ders_tv_tanitim_v1';

/** TV mi? ?tv=1 açar (cihazda kalır), ?tv=0 kapatır */
export const cdTvMi = (() => {
  let v: boolean | null = null;
  return () => {
    if (v != null) return v;
    try {
      const q = new URLSearchParams(location.search).get('tv');
      if (q === '1' || q === '0') localStorage.setItem(TV_KEY, q);
      const k = localStorage.getItem(TV_KEY);
      v = k ? k === '1' : TV_UA.test(navigator.userAgent);
    } catch { v = TV_UA.test(navigator.userAgent || ''); }
    return v;
  };
})();

/** Kumanda tuşu → eylem. key adları + eski TV keyCode'ları (LG/Samsung/HbbTV) */
export type TvEylem = 'oynat' | 'duraklat' | 'degistir' | 'geri' | 'ileri' | 'geriCok' | 'ileriCok' | 'oncekiBolum' | 'sonrakiBolum';
export function cdTvTus(e: KeyboardEvent, tv: boolean): TvEylem | null {
  const k = e.key;
  const c = e.keyCode;
  if (k === 'MediaPlayPause' || c === 179 || c === 10252 || c === 463) return 'degistir';
  if (k === 'MediaPlay' || c === 415 || c === 250) return 'oynat';
  if (k === 'MediaPause' || c === 19) return 'duraklat';
  if (k === 'MediaStop' || c === 413 || c === 178) return 'duraklat';
  if (k === 'MediaRewind' || c === 412 || c === 227) return 'geriCok';
  if (k === 'MediaFastForward' || c === 417 || c === 228) return 'ileriCok';
  if (k === 'MediaTrackPrevious' || k === 'ChannelDown' || c === 177 || c === 428 || c === 424) return 'oncekiBolum';
  if (k === 'MediaTrackNext' || k === 'ChannelUp' || c === 176 || c === 427 || c === 425) return 'sonrakiBolum';
  if (k === 'ArrowLeft') return 'geri';
  if (k === 'ArrowRight') return 'ileri';
  if (!tv) return null;
  if (k === 'Enter' || c === 13) return 'degistir';
  return null;
}

const TUSLAR: [string, string][] = [
  ['OK / ⏯', 'Oynat · duraklat (düğmedeyken: düğmeye bas)'],
  ['◀  ▶', '10 sn geri · ileri'],
  ['⏪  ⏩', '30 sn geri · ileri (her zaman)'],
  ['▲  ▼', 'Düğmelere geç (hız, ses, tam ekran…); orada ◀ ▶ ile gez'],
  ['Geri', 'Düğmelerden çık, sarmaya dön · pencereyi kapat'],
  ['CH+ / CH−  ⏭ ⏮', 'Sonraki · önceki bölüm'],
];

/** TV'de ders ekranı: ilk açılışta tanıtım + başlıkta "Kumanda" düğmesi */
export function CdTvKumanda() {
  const tv = cdTvMi();
  useCdTvGezinme('ders');
  const [acik, setAcik] = useState(() => { if (!tv) return false; try { return !localStorage.getItem(TANITIM_KEY); } catch { return true; } });
  const tamamRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!acik) return;
    tamamRef.current?.focus();
    const kapat = (e: KeyboardEvent) => {
      if (e.key === 'Escape' || e.key === 'Backspace' || e.key === 'GoBack' || e.keyCode === 461 || e.keyCode === 10009) {
        e.preventDefault(); e.stopPropagation(); bitir();
      }
    };
    document.addEventListener('keydown', kapat, true);
    return () => document.removeEventListener('keydown', kapat, true);
  }, [acik]);
  if (!tv) return null;
  function bitir() {
    try { localStorage.setItem(TANITIM_KEY, '1'); } catch { /* yok */ }
    setAcik(false);
  }
  return (
    <>
      <button type="button" className="cd-btn cd-tv-btn" onClick={() => setAcik(true)} aria-label="Kumanda tuşları" title="Kumanda tuşları">
        <Tv aria-hidden /> <span>Kumanda</span>
      </button>
      {acik && (
        <div className="cd-dlg cd-tv-dlg" role="presentation">
          <div className="cd-dlg-kart is-dar" role="dialog" aria-modal="true" aria-labelledby="cd-tv-b">
            <button type="button" className="cd-dlg-x cd-btn is-ikon" onClick={bitir} aria-label="Kapat"><X aria-hidden /></button>
            <span className="cd-ikon" aria-hidden><Tv /></span>
            <b id="cd-tv-b" className="cd-dlg-baslik">Kumandayla dinle</b>
            <p className="cd-dlg-metin">Dersi TV kumandasıyla yönetebilirsin:</p>
            <ul className="cd-tv-liste">
              {TUSLAR.map(([t, a]) => <li key={t}><kbd>{t}</kbd><span>{a}</span></li>)}
            </ul>
            <div className="cd-dlg-eylem">
              <button ref={tamamRef} type="button" className="cd-btn is-ana" onClick={bitir}>Anladım</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

/* ---------------- tam kumanda erişimi: yön tuşlarıyla odak gezinmesi ---------------- */
const ODAKLANIR = 'a[href], button:not([disabled]), select:not([disabled]), input:not([disabled]):not([type="hidden"]), [tabindex]:not([tabindex="-1"]), [role="slider"]';
const GERI_TUS = (e: KeyboardEvent) => e.key === 'GoBack' || e.key === 'BrowserBack' || e.keyCode === 461 || e.keyCode === 10009 || (e.key === 'Backspace' && !/^(INPUT|TEXTAREA)$/.test((e.target as HTMLElement)?.tagName || ''));

function gorunur(el: HTMLElement) {
  const r = el.getBoundingClientRect();
  if (r.width < 2 || r.height < 2) return false;
  const s = getComputedStyle(el);
  return s.visibility !== 'hidden' && s.display !== 'none' && r.bottom > -200 && r.top < innerHeight + 2000;
}

type Yon = 'sol' | 'sag' | 'yukari' | 'asagi';
/** En yakın odaklanabilir öğeye geç (açık diyalog varsa onun içinde). Bulursa true. */
export function cdOdakGez(yon: Yon): boolean {
  const kap = (document.querySelector('.cd-dlg [role="dialog"], .cd-dlg [role="alertdialog"]') as HTMLElement) || document.body;
  const akt = document.activeElement as HTMLElement | null;
  const simdi = akt && akt !== document.body && kap.contains(akt) ? akt : null;
  const adaylar = [...kap.querySelectorAll<HTMLElement>(ODAKLANIR)].filter((el) => el !== simdi && gorunur(el));
  if (!adaylar.length) return false;
  const r0 = simdi ? simdi.getBoundingClientRect() : new DOMRect(innerWidth / 2, yon === 'yukari' ? innerHeight : yon === 'asagi' ? 0 : innerHeight / 2, 0, 0);
  const cx = r0.left + r0.width / 2, cy = r0.top + r0.height / 2;
  let en: HTMLElement | null = null, enP = Infinity;
  for (const el of adaylar) {
    const r = el.getBoundingClientRect();
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    let ana: number, yan: number;
    if (yon === 'sag') { ana = r.left - r0.right; yan = Math.abs(y - cy); if (x <= cx + 1) continue; }
    else if (yon === 'sol') { ana = r0.left - r.right; yan = Math.abs(y - cy); if (x >= cx - 1) continue; }
    else if (yon === 'asagi') { ana = r.top - r0.bottom; yan = Math.abs(x - cx); if (y <= cy + 1) continue; }
    else { ana = r0.top - r.bottom; yan = Math.abs(x - cx); if (y >= cy - 1) continue; }
    const p = Math.max(0, ana) + yan * (yon === 'sol' || yon === 'sag' ? 3 : 0.6);
    if (p < enP) { enP = p; en = el; }
  }
  if (!en) return false;
  (en as HTMLElement & { focus(o?: { focusVisible?: boolean; preventScroll?: boolean }): void }).focus({ focusVisible: true, preventScroll: true });
  en.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  return true;
}

/**
 * TV'de canlı ders sayfalarında kumanda gezinmesi. 'liste': tüm yön tuşları odak taşır.
 * 'ders': odak bir düğmedeyse yön tuşları düğmeler arasında gezer; odak boştayken ◀▶ sarar (CanliDersDock), ▲▼ düğmelere geçer.
 * Geri: açık pencereyi kapatır; derste odağı bırakıp sarma moduna döner.
 */
export function useCdTvGezinme(mod: 'liste' | 'ders') {
  useEffect(() => {
    if (!cdTvMi()) return;
    document.documentElement.classList.add('cd-tv');
    const on = (e: KeyboardEvent) => {
      if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      // H335: açık bir menünün (⋯ CdTasmaMenu, role="menu") içindeyken yön tuşları, Home/End ve Esc/Geri menünündür;
      // pencere düzeyindeki yakalayıcı onları önce alıp odak gezinmesine/sarmaya çeviriyordu
      if (t?.closest?.('[role="menu"]')) return;
      if (GERI_TUS(e) || e.key === 'Escape') {
        const x = document.querySelector<HTMLElement>('.cd-dlg .cd-dlg-x, .cd-dlg [aria-label="Kapat"]');
        if (x) { e.preventDefault(); e.stopPropagation(); x.click(); return; }
        if (mod === 'ders' && t && t !== document.body) { e.preventDefault(); e.stopPropagation(); t.blur(); return; }
        return;
      }
      const yon: Yon | null = e.key === 'ArrowLeft' ? 'sol' : e.key === 'ArrowRight' ? 'sag' : e.key === 'ArrowUp' ? 'yukari' : e.key === 'ArrowDown' ? 'asagi' : null;
      if (!yon) return;
      if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable) && (yon === 'sol' || yon === 'sag')) return;
      if (t?.getAttribute('role') === 'slider' && (yon === 'sol' || yon === 'sag')) return; // ilerleme çubuğu kendi sarar
      const odakVar = !!t && t !== document.body && t.matches?.(ODAKLANIR);
      if (mod === 'ders' && !odakVar && (yon === 'sol' || yon === 'sag')) return; // sarma (Dock)
      // Derste ilk ▲/▼: önce oynat düğmesine
      const oynat = mod === 'ders' && !odakVar ? document.querySelector<HTMLElement>('.cd-dock .cd-oynat') : null;
      if (oynat) { e.preventDefault(); e.stopPropagation(); oynat.focus({ focusVisible: true } as FocusOptions); return; }
      if (cdOdakGez(yon)) { e.preventDefault(); e.stopPropagation(); }
    };
    window.addEventListener('keydown', on, true);
    return () => { window.removeEventListener('keydown', on, true); document.documentElement.classList.remove('cd-tv'); };
  }, [mod]);
}
