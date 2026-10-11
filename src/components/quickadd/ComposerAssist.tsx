import React, { useEffect, useMemo, useRef, useState } from 'react';
import { CornerDownLeft, Sparkles, Wand2 } from 'lucide-react';
import { ApiService } from '../../services/api';

/**
 * Tam ekran yazmada öneri çubuğu + cümle tamamlama (telefon).
 *
 *  - Kullanıcı yazmayı BIRAKINCA (600 ms) yazdığı metne benzeyen çıkmış soru kökleri istenir; yazılan son
 *    kelimeler bu köklerde aranır ve kökün devamı (cümle sonuna kadar) olası tamamlama olur. Yaygın soru
 *    kalıpları ("…aşağıdakilerden hangisidir?") yedek kaynaktır. Yapay zekâ çağrısı yok; yerel ve hızlı.
 *  - En iyi tamamlama, metnin hemen ardında soluk ipucu metni (hint) olarak görünür (textarea'nın arkasındaki
 *    ayna katman). Çubuktaki "Ekle", ipucuna dokunmak ya da Tab/→ kabul eder → metnin sonuna eklenir.
 *  - Düzeltme önerisi: baş harf, çift boşluk, soru kalıbında eksik "?".
 *  Klavye açık/kapalı fark etmez: çubuk kompozörün altında, klavye açıkken klavyenin hemen üstündedir.
 */

const TEMPLATES = [
  'aşağıdakilerden hangisidir?',
  'aşağıdakilerden hangisi yanlıştır?',
  'aşağıdakilerden hangisi doğrudur?',
  'aşağıdakilerden hangisi değildir?',
  'en olası tanı hangisidir?',
  'ilk yapılması gereken hangisidir?',
  'en sık görülen bulgu hangisidir?',
  'tedavisinde ilk tercih edilen ilaç hangisidir?',
  'ile ilgili aşağıdakilerden hangisi yanlıştır?',
  'ifadelerden hangileri doğrudur?',
];

const fold = (s: string) =>
  s.toLocaleLowerCase('tr-TR').replace(/[.,;:!?()"'“”‘’«»\[\]]/g, '').replace(/\s+/g, ' ').trim();

/** Yazılan metnin sonu ile kaynak metindeki eşleşmenin devamı. */
function continuations(typed: string, sources: string[], max = 3): string[] {
  const endsWithSpace = /\s$/.test(typed);
  const tw = fold(typed).split(' ').filter(Boolean);
  if (tw.length === 0) return [];
  const partial = endsWithSpace ? '' : tw[tw.length - 1];
  const done = endsWithSpace ? tw : tw.slice(0, -1);
  const out: { text: string; k: number; i: number }[] = [];
  sources.forEach((src, si) => {
    const sw = src.split(/\s+/).filter(Boolean);
    const sf = sw.map(fold);
    for (let k = Math.min(4, done.length); k >= (partial ? 0 : 1); k--) {
      const ctx = done.slice(done.length - k);
      if (k === 0 && partial.length < 3) break;
      for (let i = 0; i + k < sw.length + (partial ? 0 : 1); i++) {
        let ok = true;
        for (let j = 0; j < k; j++) if (sf[i + j] !== ctx[j]) { ok = false; break; }
        if (!ok) continue;
        let rest: string[] = [];
        const at = i + k;
        let lead = '';
        if (partial) {
          const w = sf[at];
          if (!w || !w.startsWith(partial)) continue;
          if (w === partial) {
            // Son kelime tam yazılmış (ardında boşluk yok): sonraki kelimeden, boşlukla devam et
            rest = sw.slice(at + 1);
            lead = ' ';
          } else {
            rest = [sw[at].slice(partial.length), ...sw.slice(at + 1)];
          }
        } else {
          rest = sw.slice(at);
        }
        // cümle sonuna kadar, en çok 12 kelime
        const cut: string[] = [];
        for (const t of rest) {
          cut.push(t);
          if (/[?.!]$/.test(t) || cut.length >= 12) break;
        }
        let text = cut.join(' ');
        if (lead && text) text = lead + text;
        else if (!partial && text) text = (endsWithSpace ? '' : ' ') + text;
        if (text.trim().length >= 2) out.push({ text, k: k + (partial ? 0.5 : 0), i: si });
        return; // bu kaynaktan en uzun bağlamlı tek eşleşme yeter
      }
    }
  });
  out.sort((a, b) => b.k - a.k || a.i - b.i);
  const seen = new Set<string>();
  return out.filter((o) => { const f = fold(o.text); if (seen.has(f)) return false; seen.add(f); return true; }).slice(0, max).map((o) => o.text);
}

/** Basit yazım düzeltmeleri: düzeltilmiş metin + kullanıcıya gösterilecek "önce → sonra" listesi; yoksa null. */
function fixText(s: string): { text: string; changes: string[] } | null {
  const changes: string[] = [];
  let t = s;
  if (/[ \t]{2,}/.test(t)) { t = t.replace(/[ \t]{2,}/g, ' '); changes.push('çift boşluk → tek boşluk'); }
  const sp = t.match(/(\S+)\s+([?.!,;:])/);
  if (sp) { t = t.replace(/\s+([?.!,;:])/g, '$1'); changes.push(`${sp[1]} ${sp[2]} → ${sp[1]}${sp[2]}`); }
  const first = t.match(/^(\s*)(\p{Ll}\S*)/u);
  if (first) {
    const w = first[2];
    const W = w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1);
    t = first[1] + W + t.slice(first[0].length);
    changes.push(`${w} → ${W}`);
  }
  const q = t.trimEnd().match(/(\S+)$/);
  if (q && /^(hangisidir|hangisi|hangileridir|hangileri|nedir|değildir|yanlıştır|doğrudur|hangisinde|hangisine)$/i.test(q[1])) {
    t = t.trimEnd() + '?';
    changes.push(`${q[1]} → ${q[1]}?`);
  }
  return changes.length ? { text: t, changes } : null;
}

export const ComposerAssist: React.FC<{
  active: boolean;
  value: string;
  onChange: (v: string) => void;
  textareaId: string;
  committeeId?: string;
}> = ({ active, value, onChange, textareaId, committeeId }) => {
  const [sources, setSources] = useState<string[]>([]);
  const [paused, setPaused] = useState(false);
  const [box, setBox] = useState<{ top: number; left: number; width: number; height: number; scroll: number } | null>(null);
  const mirrorRef = useRef<HTMLDivElement>(null);
  const reqId = useRef(0);

  // Yazmayı bırakınca (600 ms) kaynak kökleri getir
  useEffect(() => {
    setPaused(false);
    if (!active) return;
    const t = window.setTimeout(() => {
      setPaused(true);
      const q = value.trim();
      if (q.split(/\s+/).length < 2) { setSources([]); return; }
      const id = ++reqId.current;
      ApiService.findSimilarPastQuestions(q, committeeId)
        .then((r) => { if (id === reqId.current) setSources((r || []).slice(0, 8).map((x) => String(x.stem || x.title || ''))); })
        .catch(() => { if (id === reqId.current) setSources([]); });
    }, 600);
    return () => window.clearTimeout(t);
  }, [value, active, committeeId]);

  const options = useMemo(() => {
    if (!paused || !value.trim()) return [];
    const fromPast = continuations(value, sources, 3);
    const fromTpl = continuations(value, TEMPLATES, 3);
    const all = [...fromPast, ...fromTpl];
    const seen = new Set<string>();
    return all.filter((t) => { const f = fold(t); if (seen.has(f)) return false; seen.add(f); return true; }).slice(0, 3);
  }, [paused, value, sources]);
  const fix = useMemo(() => (paused ? fixText(value) : null), [paused, value]);
  const ghost = options[0] || '';

  // Ayna katmanı textarea'nın üstüne hizala (konum, boyut, kaydırma)
  useEffect(() => {
    if (!active) { setBox(null); return; }
    const ta = document.getElementById(textareaId) as HTMLTextAreaElement | null;
    if (!ta) return;
    const measure = () => setBox({ top: ta.offsetTop, left: ta.offsetLeft, width: ta.offsetWidth, height: ta.offsetHeight, scroll: ta.scrollTop });
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(ta);
    ta.addEventListener('scroll', measure);
    // Tab ya da imleç sondayken → ile ipucunu kabul et
    const onKey = (e: KeyboardEvent) => {
      const g = (ta.dataset.ghost || '');
      if (!g) return;
      const atEnd = ta.selectionStart === ta.value.length && ta.selectionEnd === ta.value.length;
      if (e.key === 'Tab' || (e.key === 'ArrowRight' && atEnd)) {
        e.preventDefault();
        onChange(ta.value + g);
      }
    };
    ta.addEventListener('keydown', onKey);
    return () => { ro.disconnect(); ta.removeEventListener('scroll', measure); ta.removeEventListener('keydown', onKey); };
  }, [active, textareaId, onChange]);

  // Kabul kısayolu için ipucunu textarea'ya iliştir
  useEffect(() => {
    const ta = document.getElementById(textareaId) as HTMLTextAreaElement | null;
    if (ta) ta.dataset.ghost = active ? ghost : '';
  }, [ghost, active, textareaId]);

  if (!active) return null;
  const accept = (t: string) => {
    onChange(value + t);
    const ta = document.getElementById(textareaId) as HTMLTextAreaElement | null;
    ta?.focus();
    window.setTimeout(() => ta && ta.setSelectionRange(ta.value.length, ta.value.length), 0);
  };

  return (
    <>
      {box && ghost && (
        <div
          ref={mirrorRef}
          className="ca-mirror"
          aria-hidden
          style={{ top: box.top, left: box.left, width: box.width, height: box.height }}
        >
          <div style={{ transform: `translateY(${-box.scroll}px)` }}>
            <span className="ca-typed">{value}</span>
            <button type="button" tabIndex={-1} className="ca-ghost" onPointerDown={(e) => { e.preventDefault(); accept(ghost); }}>{ghost}</button>
          </div>
        </div>
      )}
      <div className={`ca-bar ${options.length || fix ? 'is-on' : ''}`} role="toolbar" aria-label="Yazım önerileri">
        {fix && (
          <button type="button" className="ca-chip is-fix" onPointerDown={(e) => e.preventDefault()} onClick={() => onChange(fix.text)} title={`Düzelt: ${fix.changes.join(', ')}`}>
            <Wand2 aria-hidden />
            <span className="ca-fix-l">Düzelt</span>
            <span className="ca-fix-d">{fix.changes.slice(0, 2).join(' · ')}{fix.changes.length > 2 ? ` +${fix.changes.length - 2}` : ''}</span>
          </button>
        )}
        {options.map((t, i) => (
          <button key={t} type="button" className={`ca-chip ${i === 0 ? 'is-top' : ''}`} onPointerDown={(e) => e.preventDefault()} onClick={() => accept(t)}>
            {i === 0 ? <CornerDownLeft aria-hidden /> : <Sparkles aria-hidden />}
            <span>…{t.trim()}</span>
          </button>
        ))}
      </div>
    </>
  );
};
