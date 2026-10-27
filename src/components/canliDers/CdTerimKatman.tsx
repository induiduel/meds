/** Sesli ders PDF terim yardımcısı (2026-10-26, scripts/sesli_anlatim/terim_sozlugu.py).
 *  Yardımcı açıkken slayttaki terimlerin altı ince kesikli çizilir ve çok hafif sarı işaretlenir; dokununca terimin
 *  açıklaması kelimenin hemen üstünde ya da altında (sayfadaki yerine göre sola/sağa yaslı) açılır. Aynı terimler
 *  konuşmacı metninde paragrafın altında yazılı durur (seslendirilmez). Kapalıyken PDF'te hiçbir işaret yoktur. */
import { navigateTo } from '../../router';
import { isFavoriteCard, toggleFavoriteCard } from '../../services/studyStore';
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
  { id: 'cikmis', ad: 'Çıkmış soru işaretleri', acik: 'Doğrulanmış çıkmışı olan slaytta çip görünür; dokununca soru açılır' },
] as const;
export type PdfGorunumId = typeof PDF_GORUNUM[number]['id'];
const gorunumT = Object.fromEntries(PDF_GORUNUM.map((g) => [g.id, tercih(`cd-pdf-${g.id}`, true)])) as Record<PdfGorunumId, ReturnType<typeof tercih>>;
export function usePdfGorunum(): Record<PdfGorunumId, boolean> {
  const r = gorunumT.resim.use(), t = gorunumT.tablo.use(), i = gorunumT.iliski.use(), m = gorunumT.metin.use(), n = gorunumT.not.use(), c = gorunumT.cikmis.use();
  return useMemo(() => ({ resim: r, tablo: t, iliski: i, metin: m, not: n, cikmis: c }), [r, t, i, m, n, c]);
}
export const pdfGorunumAyarla = (id: PdfGorunumId, v: boolean) => gorunumT[id].ayarla(v);

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
      {x.acilim && <p className="cd-trm-acilim"><b>{x.acilim}</b></p>}
      {x.a && x.a !== x.acilim && <p>{x.a}</p>}
      {x.f && <p className="cd-trm-f">Karıştırılan: <b>{x.f}</b></p>}
      <KartEylem x={x} />
    </>
  );
}

/** Terim kartı eylemleri (tasarım S20): Sözlükte aç · Karta ekle (favori ezber kartları, studyStore) */
function KartEylem({ x }: { x: CdTerim }) {
  const id = `cd-terim:${x.t}`;
  const [kartta, setKartta] = React.useState(() => isFavoriteCard(id));
  return (
    <div className="cd-trm-eylem">
      <button type="button" onClick={() => navigateTo(`/sozluk?terim=${encodeURIComponent(x.t)}`)}>Sözlükte aç</button>
      <button type="button" className={kartta ? 'is-on' : ''} aria-pressed={kartta}
        onClick={() => { toggleFavoriteCard({ id, front: x.t, back: [x.acilim, x.a].filter(Boolean).join(' — ') || x.t, group: 'Sesli ders terimleri' }); setKartta(isFavoriteCard(id)); }}>
        {kartta ? 'Kartlarımda' : 'Karta ekle'}
      </button>
    </div>
  );
}

/** Terim ve kısaltma katmanlarını tek haritada birleştirir (PDF katmanı ve paragraf altı listesi aynı veriyi kullanır). */
export function cdTerimKatmani(terim?: CdDetay['terim'], kisaltma?: CdDetay['kisaltma']): Record<string, Record<string, CdTerimSayfa>> | null {
  if (!terim && !kisaltma) return null;
  const out: Record<string, Record<string, CdTerimSayfa>> = {};
  const ekle = (kaynak?: CdDetay['terim']) => {
    for (const [dosya, sayfalar] of Object.entries(kaynak || {})) {
      for (const [no, sy] of Object.entries(sayfalar || {})) {
        const hedef = ((out[dosya] ||= {})[no] ||= { bos: sy.bos, t: [] });
        for (const x of sy.t || []) if (!hedef.t.some((y) => y.t === x.t)) hedef.t.push(x);
      }
    }
  };
  ekle(terim);
  ekle(kisaltma);
  return Object.keys(out).length ? out : null;
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

// Python terim_sozlugu.py ile aynı katlama ve ek kuralı: kısa terim (≤4) birebir; uzun terimde kalan yalnız Türkçe ek dizisi
const KATLA: Record<string, string> = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', â: 'a', î: 'i', û: 'u' };
const katla = (w: string) => w.toLocaleLowerCase('tr').replace(/[çğıöşüâîû]/g, (c) => KATLA[c]).split(/['’]/)[0];
const EK = /^(?:y?(?:i|u|a|e)?(?:n|m|miz|niz|ler|lar|si|su|leri|lari)?(?:in|un|nin|nun|i|u|a|e|ye|ya|de|da|te|ta|den|dan|ten|tan|le|la|yle|yla|dir|dur|tir|tur|ki|ken|li|lu|siz|suz|lik|luk|sel|sal|ce|ca)?){0,3}$/;
const TOK = /[\p{L}\p{N}]+(?:[-'’][\p{L}\p{N}]+)*/gu;
const uyar = (p: string, w: string) => w === p || (p.length > 4 && w.startsWith(p) && w.length - p.length <= 7 && EK.test(w.slice(p.length)));

/** Konuşmacı metninde paragrafın altı: dersin terimlerinden bu paragrafta (ekli hâli dahil) geçenler (seslendirilmez) */
export function CdParagrafTerimleri({ detay, metin }: { detay: CdDetay; i?: number; metin: string }) {
  const acik = useTerimYardimci();
  const katman = useMemo(() => cdTerimKatmani(detay.terim, detay.kisaltma), [detay.terim, detay.kisaltma]);
  const tum = useMemo(() => {
    const m = new Map<string, { x: CdTerim; p: string[] }>();
    for (const d of Object.values(katman || {})) for (const sy of Object.values(d)) for (const x of sy.t) {
      const p = (x.t.match(TOK) || []).map(katla).filter(Boolean);
      const k = p.join(' ');
      if (p.length && !m.has(k)) m.set(k, { x, p });
    }
    return [...m.values()];
  }, [katman]);
  const liste = useMemo(() => {
    if (!acik || !tum.length) return [];
    const w = (metin.match(TOK) || []).map(katla);
    const out: CdTerim[] = [];
    for (const { x, p } of tum) {
      for (let i = 0; i + p.length <= w.length; i++) {
        if (p.every((q, j) => uyar(q, w[i + j]))) { out.push(x); break; }
      }
    }
    return out;
  }, [acik, tum, metin]);
  if (!acik || !liste.length) return null;
  return (
    <dl className="cd-p-trm" aria-label="Bu paragraftaki terimler (seslendirilmez)">
      {liste.map((x) => (
        <div key={x.t} className="cd-p-trm-oge">
          <dt>{x.t}<span className={`cd-trm-tur is-${x.k}`}>{TERIM_TUR[x.k]}</span></dt>
          <dd>{x.acilim && <b>{x.acilim}{x.a && x.a !== x.acilim ? '. ' : ''}</b>}{x.a !== x.acilim ? x.a : ''}{x.f && <i> Karıştırılan: {x.f}.</i>}</dd>
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
