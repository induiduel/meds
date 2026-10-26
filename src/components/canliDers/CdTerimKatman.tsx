/** Sesli ders PDF terim yardımcısı (2026-10-26, scripts/sesli_anlatim/terim_sozlugu.py).
 *  Yardımcı açıkken slayttaki terimlerin altı ince kesikli çizilir ve çok hafif sarı işaretlenir; dokununca terimin
 *  açıklaması kelimenin hemen üstünde ya da altında (sayfadaki yerine göre sola/sağa yaslı) açılır. Aynı terimler
 *  konuşmacı metninde paragrafın altında yazılı durur (seslendirilmez). Kapalıyken PDF'te hiçbir işaret yoktur. */
import React, { useMemo, useSyncExternalStore } from 'react';
import { Eye, Info } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '../ui/radix';
import type { CdDetay, CdTerim, CdTerimSayfa } from './canliDersStore';

// ── küçük kalıcı tercih deposu ────────────────────────────────────────────────────────────────────────────────
function tercih(anahtar: string, varsayilan: boolean) {
  const dinleyen = new Set<() => void>();
  let deger = varsayilan;
  try { const v = localStorage.getItem(anahtar); if (v !== null) deger = v === '1'; } catch { /* özel kip */ }
  return {
    ayarla(v: boolean) {
      deger = v;
      try { localStorage.setItem(anahtar, v ? '1' : '0'); } catch { /* özel kip */ }
      dinleyen.forEach((f) => f());
    },
    use(): boolean {
      return useSyncExternalStore((f) => { dinleyen.add(f); return () => { dinleyen.delete(f); }; }, () => deger, () => varsayilan);
    },
  };
}

const terimT = tercih('cd-terim-yardimci', false);
export const terimYardimciAyarla = terimT.ayarla;
export const useTerimYardimci = terimT.use;

/** PDF görünüm anahtarları (kullanıcı isteği 2026-10-26): görünümü sadeleştirmek için tek tek kapatılır */
export const PDF_GORUNUM = [
  { id: 'resim', ad: 'Canlı resim işaretçisi', acik: 'Resimler çizilir, vurgulanır ve yakınlaştırılır' },
  { id: 'tablo', ad: 'Tablo işaretçisi', acik: 'Tablolar (resim ya da metin) çizilir, boyanır ve yakınlaştırılır' },
  { id: 'iliski', ad: 'Kelime ilişki kurucusu', acik: 'Kelimeler ve metinler arasındaki ilişki oklarla gösterilir' },
  { id: 'metin', ad: 'Metin vurgusu', acik: 'Okunan satır ve kelime PDF üstünde takip edilir' },
  { id: 'not', ad: 'Öğrenci/hoca vurgusu', acik: 'Öğrenci notu ve hoca anlatımından gelen önemli yerler işaretlenir' },
] as const;
export type PdfGorunumId = typeof PDF_GORUNUM[number]['id'];
const gorunumT = Object.fromEntries(PDF_GORUNUM.map((g) => [g.id, tercih(`cd-pdf-${g.id}`, true)])) as Record<PdfGorunumId, ReturnType<typeof tercih>>;
export function usePdfGorunum(): Record<PdfGorunumId, boolean> {
  const r = gorunumT.resim.use(), t = gorunumT.tablo.use(), i = gorunumT.iliski.use(), m = gorunumT.metin.use(), n = gorunumT.not.use();
  return useMemo(() => ({ resim: r, tablo: t, iliski: i, metin: m, not: n }), [r, t, i, m, n]);
}

export const TERIM_TUR: Record<CdTerim['k'], string> = {
  terim: 'Tıbbi terim', latince: 'Latince / yabancı', karisan: 'Karıştırılabilir', kisaltma: 'Kısaltma',
};

/** PDF çubuğu: ⓘ terim yardımcısı */
export function TerimDugme() {
  const acik = useTerimYardimci();
  return (
    <button type="button" className={`cd-cik-btn cd-trm-btn${acik ? ' is-on' : ''}`} aria-pressed={acik}
      onClick={() => terimYardimciAyarla(!acik)}
      title={acik ? 'Terim yardımcısı açık: işaretli terime dokun, anlamı açılsın' : 'Terim yardımcısı: slayttaki terimleri işaretle, dokununca anlamını göster'}
      aria-label="Terim yardımcısı">
      <Info aria-hidden /> <span className="cd-cik-ad">Terimler</span>
    </button>
  );
}

/** PDF çubuğu: görünüm anahtarları */
export function PdfGorunumDugme() {
  const g = usePdfGorunum();
  const kapali = PDF_GORUNUM.filter((x) => !g[x.id]).length;
  return (
    <Popover>
      <PopoverTrigger asChild>
        <button type="button" className={`cd-cik-btn cd-gor-btn${kapali ? ' is-on' : ''}`} aria-label="PDF görünümü" title="PDF görünümü: işaretçileri aç/kapat">
          <Eye aria-hidden /> <span className="cd-cik-ad">Görünüm{kapali ? ` · ${kapali} kapalı` : ''}</span>
        </button>
      </PopoverTrigger>
      <PopoverContent className="cd-gor-panel" aria-label="PDF görünümü">
        <div className="cd-gor-bas">PDF görünümü</div>
        {PDF_GORUNUM.map((x) => (
          <label key={x.id} className="cd-gor-oge">
            <span className="cd-gor-m"><b>{x.ad}</b><small>{x.acik}</small></span>
            <input type="checkbox" role="switch" className="cd-gor-sw" checked={g[x.id]} onChange={(e) => gorunumT[x.id].ayarla(e.target.checked)} />
          </label>
        ))}
      </PopoverContent>
    </Popover>
  );
}

function Kart({ x }: { x: CdTerim }) {
  return (
    <>
      <div className="cd-trm-kart-bas">
        <b>{x.t}</b>
        <span className={`cd-trm-tur is-${x.k}`}>{TERIM_TUR[x.k]}</span>
      </div>
      <p>{x.a}</p>
      {x.f && <p className="cd-trm-f">Karıştırılan: <b>{x.f}</b></p>}
    </>
  );
}

/** Sayfa katmanı (pageOverlay içinde): yalnız yardımcı açıkken */
export const CdTerimKatman = React.memo(function CdTerimKatman({ sayfa, gizle }: { sayfa: CdTerimSayfa; gizle?: boolean }) {
  const acik = useTerimYardimci();
  if (!acik || gizle || !sayfa.t.length) return null;
  return (
    <div className="cd-trm-kat">
      {sayfa.t.flatMap((x, i) => x.b.map((b, j) => {
        const orta = (b[0] + b[2]) / 2;
        return (
          <Popover key={`${i}-${j}`}>
            <PopoverTrigger asChild>
              <button type="button" className={`cd-trm is-${x.k}`} aria-label={`${x.t}: anlamını göster`}
                style={{ left: `${b[0] * 100}%`, top: `${b[1] * 100}%`, width: `${(b[2] - b[0]) * 100}%`, height: `${(b[3] - b[1]) * 100}%` }} />
            </PopoverTrigger>
            {/* üstte yer varsa kelimenin üstünde, yoksa altında; sayfanın sağındaki kelimede sağa, solundakinde sola yaslı */}
            <PopoverContent className="cd-trm-kart" side={b[1] > 0.3 ? 'top' : 'bottom'} align={orta > 0.6 ? 'end' : orta < 0.4 ? 'start' : 'center'}
              sideOffset={6} aria-label={x.t}>
              <Kart x={x} />
            </PopoverContent>
          </Popover>
        );
      }))}
    </div>
  );
});

const kucuk = (s: string) => s.toLocaleLowerCase('tr');

/** Konuşmacı metninde paragrafın altı: o paragrafın slayt(lar)ındaki ve paragrafta geçen terimler (seslendirilmez) */
export function CdParagrafTerimleri({ detay, i, metin }: { detay: CdDetay; i: number; metin: string }) {
  const acik = useTerimYardimci();
  const liste = useMemo(() => {
    const es = detay.pdf?.paragraflar[i];
    if (!detay.terim || !es) return [];
    const yerler = new Set<string>([`${es.dosya || 0}:${es.sayfa}`]);
    (es.sayfalar || []).forEach((s, c) => yerler.add(`${es.dosyalar?.[c] ?? es.dosya ?? 0}:${s}`));
    const m = kucuk(metin);
    const out = new Map<string, CdTerim>();
    for (const y of yerler) {
      const [d, s] = y.split(':');
      for (const x of detay.terim[d]?.[s]?.t || []) {
        const ilk = kucuk(x.t).split(/\s+/)[0];
        const kok = ilk.length > 5 ? ilk.slice(0, Math.max(5, ilk.length - 2)) : ilk;
        if (m.includes(kok) && !out.has(kucuk(x.t))) out.set(kucuk(x.t), x);
      }
    }
    return [...out.values()];
  }, [detay.terim, detay.pdf, i, metin]);
  if (!acik || !liste.length) return null;
  return (
    <dl className="cd-p-trm" aria-label="Bu paragraftaki terimler (seslendirilmez)">
      {liste.map((x) => (
        <div key={x.t} className="cd-p-trm-oge">
          <dt>{x.t}<span className={`cd-trm-tur is-${x.k}`}>{TERIM_TUR[x.k]}</span></dt>
          <dd>{x.a}{x.f && <i> Karıştırılan: {x.f}.</i>}</dd>
        </div>
      ))}
    </dl>
  );
}

/** Ders başlığı: her görünümde (metin, PDF, tam ekran) erişilen ⓘ terim düğmesi */
export function TerimBaslikDugme() {
  const acik = useTerimYardimci();
  return (
    <button type="button" className={`cd-btn is-ikon cd-trm-bas${acik ? ' is-on' : ''}`} aria-pressed={acik}
      onClick={() => terimYardimciAyarla(!acik)} aria-label="Terim yardımcısı"
      title={acik ? 'Terim yardımcısı açık (kapat)' : 'Terim yardımcısı: slayttaki terimlerin anlamını göster'}>
      <Info aria-hidden />
    </button>
  );
}

/** ⋯ Ders seçenekleri menüsü: terim yardımcısı + PDF görünüm anahtarları (açılır pencere değil, satır içi) */
export function PdfAyarlarMenu({ terimVar }: { terimVar: boolean }) {
  const g = usePdfGorunum();
  const t = useTerimYardimci();
  return (
    <div className="cd-gor-menu" role="group" aria-label="PDF görünümü">
      <div className="cd-gor-bas">PDF görünümü</div>
      {terimVar && (
        <label className="cd-gor-oge">
          <span className="cd-gor-m"><b>Terim yardımcısı</b><small>Terimler işaretlenir, dokununca anlamı açılır</small></span>
          <input type="checkbox" role="switch" className="cd-gor-sw" checked={t} onChange={(e) => terimYardimciAyarla(e.target.checked)} />
        </label>
      )}
      {PDF_GORUNUM.map((x) => (
        <label key={x.id} className="cd-gor-oge">
          <span className="cd-gor-m"><b>{x.ad}</b><small>{x.acik}</small></span>
          <input type="checkbox" role="switch" className="cd-gor-sw" checked={g[x.id]} onChange={(e) => gorunumT[x.id].ayarla(e.target.checked)} />
        </label>
      ))}
    </div>
  );
}
