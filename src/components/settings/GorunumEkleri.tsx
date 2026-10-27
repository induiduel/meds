import React, { useEffect, useMemo, useState } from 'react';
import { Check, RotateCcw } from 'lucide-react';
import { FONT_LIST, MOTIFS, useAppearance, type MotifId } from '../../utils/appearance';
import { findPalette, kontrastOrani, ozelVurgu } from '../../utils/palettes';
import './gorunumEkleri.css';

/**
 * Ayarlar › Görünüm ekleri (v15 tasarım sistemi):
 *  V03 Tıbbi motifler — zemin dokusu (data-motif, styles/motifler.css)
 *  V04 Yazı tipleri — arayüz ve okuma yazısı (FONT_LIST; seçilince Google Fonts'tan yüklenir)
 *  W01 Paleti düzenle — temanın o anki paletine özel vurgu; ozelVurgu kontrast kapısından geçirir (≥4.5:1)
 */
type Look = ReturnType<typeof useAppearance>;
const ORNEK = 'Bölünemeyen kalp kası hücrelerinde yük artışı yalnız hipertrofiye yol açar. Hb 13,5 g/dL · K⁺ 4,2 mmol/L';

const hsl = (h: number, s: number, l: number) => {
  const f = (n: number) => { const k = (n + h / 30) % 12, a = (s / 100) * Math.min(l / 100, 1 - l / 100); return Math.round(255 * (l / 100 - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)))).toString(16).padStart(2, '0'); };
  return `#${f(0)}${f(8)}${f(4)}`.toUpperCase();
};
const toHsl = (hex: string): [number, number, number] => {
  const n = parseInt(hex.slice(1), 16); const r = (n >> 16) / 255, g = ((n >> 8) & 255) / 255, b = (n & 255) / 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  if (!d) return [0, 0, Math.round(l * 100)];
  const s = d / (1 - Math.abs(2 * l - 1));
  const h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [Math.round((h * 60 + 360) % 360), Math.round(s * 100), Math.round(l * 100)];
};

export function GorunumEkleri({ look }: { look: Look }) {
  return (
    <>
      <MotifSecimi look={look} />
      <YaziTipleri look={look} />
      <PaletDuzenle look={look} />
    </>
  );
}

function MotifSecimi({ look }: { look: Look }) {
  const cur = look.motif || 'yok';
  return (
    <div className="ge-blok">
      <h3 id="ge-motif-h">Arka plan motifi</h3>
      <div role="radiogroup" aria-labelledby="ge-motif-h" className="ge-motifs">
        {MOTIFS.map((m) => (
          <button key={m.id} type="button" role="radio" aria-checked={cur === m.id} className={`ge-opt ge-motif is-${m.id}`} onClick={() => look.set({ motif: m.id as MotifId })}>
            <b>{m.name}</b><span>{m.hint}</span>
            {cur === m.id && <Check className="ge-tik" strokeWidth={3} aria-hidden />}
          </button>
        ))}
      </div>
      <p className="ge-not">Motif yalnız zemin dokusudur: çok soluk, yazının altında kalır ve okunurluğu değiştirmez. Rengi vurgu renginden gelir.</p>
    </div>
  );
}

function YaziTipleri({ look }: { look: Look }) {
  const [tur, setTur] = useState<'ui' | 'read'>('ui');
  const secili = tur === 'ui' ? look.fontUi || 'jakarta' : look.fontRead || '';
  const liste = FONT_LIST.filter((f) => f.kind === tur);
  // önizleme için seçili sekmedeki yazı tiplerini yükle
  useEffect(() => {
    for (const f of liste) {
      if (!f.g || document.getElementById(`font-${f.id}`)) continue;
      const l = document.createElement('link'); l.id = `font-${f.id}`; l.rel = 'stylesheet';
      l.href = `https://fonts.googleapis.com/css2?family=${f.g}&display=swap`; document.head.appendChild(l);
    }
  }, [tur]); // eslint-disable-line react-hooks/exhaustive-deps
  const sec = (id: string) => look.set(tur === 'ui' ? { fontUi: id === 'jakarta' ? undefined : id } : { fontRead: id || undefined });
  return (
    <div className="ge-blok">
      <h3 id="ge-font-h">Yazı tipleri</h3>
      <div className="ge-fseg" role="tablist" aria-label="Yazı tipi türü">
        <button type="button" role="tab" aria-selected={tur === 'ui'} onClick={() => setTur('ui')}>Arayüz</button>
        <button type="button" role="tab" aria-selected={tur === 'read'} onClick={() => setTur('read')}>Okuma</button>
      </div>
      <div role="radiogroup" aria-labelledby="ge-font-h" className="ge-fonts">
        {tur === 'read' && (
          <button type="button" role="radio" aria-checked={!secili} className="ge-font" onClick={() => sec('')}>
            <span className="ge-font-ust"><span className="ge-font-ip">Okuma yazısı ayarındaki seçim</span>{!secili && <span className="ge-font-bdg">Seçili</span>}</span>
            <b style={{ fontFamily: 'var(--read-font, var(--font-read))' }}>Tasarımın varsayılanı</b>
          </button>
        )}
        {liste.map((f) => (
          <button key={f.id} type="button" role="radio" aria-checked={secili === f.id} className="ge-font" onClick={() => sec(f.id)}>
            <span className="ge-font-ust"><span className="ge-font-ip">{f.hint}</span>{secili === f.id && <span className="ge-font-bdg">Seçili</span>}</span>
            <b style={{ fontFamily: f.family }}>{f.name}</b>
            <span className="ge-font-ornek" style={{ fontFamily: f.family }}>{ORNEK}</span>
          </button>
        ))}
      </div>
      <p className="ge-not">Arayüz yazısı menü, düğme ve kartlarda; okuma yazısı soru kökü, ders anlatımı ve notlarda kullanılır.</p>
    </div>
  );
}

function PaletDuzenle({ look }: { look: Look }) {
  const pal = findPalette(look.mode, look.palette);
  const baz = look.customAccent || pal.vars.accent;
  const [h0, s0, l0] = toHsl(baz);
  const [hex, setHex] = useState(baz);
  const [metin, setMetin] = useState(baz);
  useEffect(() => { setHex(baz); setMetin(baz); }, [baz]);
  const [h, s, l] = useMemo(() => (hex === baz ? [h0, s0, l0] : toHsl(hex)), [hex, baz, h0, s0, l0]);
  const sonuc = useMemo(() => ozelVurgu(hex, pal.vars, look.mode), [hex, pal, look.mode]);
  const kaydi = sonuc.accent.toUpperCase() !== hex.toUpperCase();
  const oran = kontrastOrani(sonuc.accent, pal.vars.white);
  const degisti = hex.toUpperCase() !== baz.toUpperCase();
  const yaz = (v: string) => { setHex(v.toUpperCase()); setMetin(v.toUpperCase()); };
  return (
    <div className="ge-blok">
      <h3 id="ge-pd-h">Paleti düzenle · {pal.name}</h3>
      <div className="ge-pd">
        <div className="ge-pd-ust">
          <input type="color" className="ge-pd-renk" value={hex} onChange={(e) => yaz(e.target.value)} aria-label="Özel vurgu rengi" />
          <input className="ge-pd-hex" value={metin} spellCheck={false} maxLength={7} aria-label="Renk kodu"
            onChange={(e) => { const v = e.target.value.trim(); setMetin(v); if (/^#[0-9a-f]{6}$/i.test(v)) setHex(v.toUpperCase()); }} />
        </div>
        <label className="ge-pd-k"><span>Ton</span><input type="range" min={0} max={359} value={h} onChange={(e) => yaz(hsl(+e.target.value, s, l))} className="is-ton" /></label>
        <label className="ge-pd-k"><span>Doygunluk</span><input type="range" min={0} max={100} value={s} onChange={(e) => yaz(hsl(h, +e.target.value, l))} /></label>
        <label className="ge-pd-k"><span>Açıklık</span><input type="range" min={5} max={95} value={l} onChange={(e) => yaz(hsl(h, s, +e.target.value))} /></label>
        <div className="ge-pd-on" style={{ background: pal.vars.white, color: pal.vars.ink, borderColor: pal.vars.line }}>
          <span className="ge-pd-btn" style={{ background: sonuc.accent, color: sonuc.on }}>Düğme</span>
          <span style={{ color: sonuc.accent, fontWeight: 600 }}>Bağlantı yazısı</span>
          <span className="ge-pd-chip" style={{ background: sonuc.soft, color: sonuc.accent }}>Seçili</span>
        </div>
        <p className="ge-not">
          Kontrast {oran.toFixed(1)}:1{kaydi ? ` · okunurluk için ${sonuc.accent} tonuna ayarlandı` : ''}. Renk her zemin ve düğme yazısında en az 4,5:1 okunacak biçimde uygulanır.
        </p>
        <div className="ge-pd-eylem">
          <button type="button" className="ge-pd-b" onClick={() => look.set({ customAccent: null })} disabled={!look.customAccent}><RotateCcw aria-hidden />Sıfırla</button>
          <button type="button" className="ge-pd-b is-pri" onClick={() => look.set({ customAccent: hex })} disabled={!degisti && !!look.customAccent}><Check aria-hidden />Uygula</button>
        </div>
      </div>
    </div>
  );
}
