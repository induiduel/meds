import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight, Presentation, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { cumleAraligi, dersEslesmeleri, type DersDizin, type DersEslesme } from './saglikDers';

/**
 * "Ders slaytında geçiyor" katmanı — Sağlık Bakanlığı sekmesinin TÜM içeriğinde (kart, madde, tablo, açıklama, havuz…)
 * çalışır. React'in çizdiği DOM'a dokunmaz: metin düğümleri okunur, eşleşen sayı CSS Custom Highlight ile vurgulanır
 * (`::highlight(sbk-ders)`), "!" düğmeleri ayrı bir katmanda sayının sağ üstüne konur. Dokununca slayt cümlesi
 * (sayı vurgulu) sayfanın en üstündeki balonda açılır; "Slayta git" Öğren'de o slaytı açar.
 *
 * Bağlam: değerin bulunduğu blok (madde, tablo hücresi, gösterge kutusu…) + üst maddelerin etiketleri + `data-ders-ad`
 * (gösterge kutusu/satır adı) + tablo satır ve sütun başlığı. Eşleştirme kuralları saglikDers.ts'tedir.
 */

const BLOK = 'li, p, td, th, dd, dt, .sbk-kpi, .sbk-satir-ust, h4, .sbk-karsi-s, figcaption, summary, blockquote, .sbk-gosterge-l > button, .sbk-deger-l > div';
// Taranmayan yerler: kaynakça, gezinti, düğme benzeri küçük denetimler, atıf numaraları, sınav soruları, katmanın kendisi
const ATLA = [
  '.sbk-atif', '.sbk-kaynakca', '.sbk-nav', '.sbk-altnav', '.sbk-cip-l', '.sbk-cip', '.sbk-seg', '.sbk-btn', '.sbk-ikon-btn', '.sbk-tk-b',
  '.sbk-kpi-gecmis', '.sbk-satir-gecmis', '.sbk-link-btn', '.sbk-rozet', '.sbk-sina', '.sbk-ders-katman', '.sbk-capa', '.sbk-kivilcim',
  'svg', 'input', 'select', 'textarea', 'code', '[aria-hidden="true"]', '.sbk-gizli',
].join(',');
const KAYDIRAN = '.sbk-tablo-kap, .sbk-asi-kap, .sbk-gosterge-l, .sbk-havuz-nav, .sbk-okunur-kartlar';
const VURGU = 'sbk-ders';

interface Isaret { anahtar: string; x: number; y: number; e: DersEslesme[] }
interface Parca { dugum: Text; bas: number; son: number }

const highlightVar = () => typeof CSS !== 'undefined' && 'highlights' in CSS && typeof (window as any).Highlight === 'function';

/** Bloğun metni: alt bloklar (iç içe liste) hariç; kalın parçalar **…** ile işaretli (değer seçimi için) */
function blokMetni(blok: Element): { duz: string; isaretli: string; parcalar: Parca[] } {
  const parcalar: Parca[] = [];
  let duz = '';
  let isaretli = '';
  const w = document.createTreeWalker(blok, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => {
      const p = (n as Text).parentElement;
      if (!p || p.closest(ATLA)) return NodeFilter.FILTER_REJECT;
      // İç içe liste/blok: kendi bloğunda işlenir
      const ic = p.closest(BLOK);
      if (ic && ic !== blok && blok.contains(ic)) return NodeFilter.FILTER_REJECT;
      if (p.closest('ul, ol') && p.closest('ul, ol') !== blok.closest('ul, ol') && blok.contains(p.closest('ul, ol'))) return NodeFilter.FILTER_REJECT;
      return (n as Text).data.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    },
  });
  for (let n = w.nextNode() as Text | null; n; n = w.nextNode() as Text | null) {
    if (duz) { duz += ' '; isaretli += ' '; }
    const kalin = !!n.parentElement?.closest('strong, b, mark');
    parcalar.push({ dugum: n, bas: duz.length, son: duz.length + n.data.length });
    duz += n.data;
    isaretli += kalin && /\d/.test(n.data) ? `**${n.data.replace(/\*/g, '')}**` : n.data.replace(/\*\*|==/g, '');
  }
  return { duz, isaretli, parcalar };
}

const etiket = (s: string) => (/^\s*([^:]{2,80}):/.exec(s)?.[1] || '').trim();

/** Üst maddelerin etiketleri, gösterge adı, tablo satır/sütun başlığı */
function baglamMetni(blok: Element): string {
  const parca: string[] = [];
  const ad = blok.closest<HTMLElement>('[data-ders-ad]')?.dataset.dersAd;
  if (ad) parca.push(ad);
  if (blok.matches('td, th')) {
    const tr = blok.closest('tr');
    const tablo = blok.closest('table');
    const i = tr ? Array.from(tr.children).indexOf(blok) : -1;
    const satirBas = tr?.firstElementChild && tr.firstElementChild !== blok ? tr.firstElementChild.textContent || '' : '';
    const sutunBas = i >= 0 ? tablo?.querySelector('thead tr')?.children[i]?.textContent || '' : '';
    parca.push(satirBas, sutunBas);
  }
  // Üst madde(ler): kendi ilk satırlarının etiketi ("Anne ölüm oranı: …" → "Anne ölüm oranı"; "Yıllara göre")
  let li = blok.parentElement?.closest('li');
  let say = 0;
  while (li && say < 3) {
    const ilk = li.firstElementChild;
    const t = (ilk && !ilk.matches('ul, ol') ? ilk.textContent : '') || '';
    parca.push(etiket(t) || t.slice(0, 60));
    li = li.parentElement?.closest('li');
    say++;
  }
  return parca.filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
}

function kirpildi(r: DOMRect, dugum: Node): boolean {
  const k = dugum.parentElement?.closest(KAYDIRAN);
  if (!k) return false;
  const kr = k.getBoundingClientRect();
  return r.right < kr.left + 2 || r.left > kr.right - 2 || r.bottom < kr.top + 2 || r.top > kr.bottom - 2;
}

const DersBalonu: React.FC<{ dz: DersDizin; e: DersEslesme[]; konum: { top: number; right: number }; onClose: () => void }> = ({ dz, e, konum, onClose }) => {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const dis = (ev: PointerEvent) => {
      const t = ev.target as Element;
      if (!ref.current?.contains(t) && !t.closest?.('.sbk-ders-i-b')) onClose();
    };
    const tus = (ev: KeyboardEvent) => { if (ev.key === 'Escape') onClose(); };
    document.addEventListener('pointerdown', dis);
    document.addEventListener('keydown', tus);
    return () => { document.removeEventListener('pointerdown', dis); document.removeEventListener('keydown', tus); };
  }, [onClose]);
  // Ekrandan taşmasın: alta sığmıyorsa yukarı kaydır
  const [ust, setUst] = useState(konum.top);
  const [sag, setSag] = useState(konum.right);
  useLayoutEffect(() => {
    const h = ref.current?.offsetHeight || 0;
    const w = ref.current?.offsetWidth || 0;
    setUst(Math.max(8, Math.min(konum.top, window.innerHeight - h - 8)));
    // Sol kenardan da taşmasın
    setSag(Math.max(8, Math.min(konum.right, window.innerWidth - w - 8)));
  }, [konum.top, konum.right]);
  const git = (d: string, s: number) => {
    onClose();
    navigateTo(`${pathFor('learn')}/${encodeURIComponent(d)}?slide=${s}`);
  };
  return createPortal(
    <div ref={ref} className="sbk-ders-pop is-sabit" role="dialog" aria-label="Ders slaytında geçiyor" style={{ top: ust, right: sag }}>
      <div className="sbk-ders-pop-u">
        <span className="sbk-ders-pop-t"><Presentation aria-hidden /> Ders slaytında geçiyor</span>
        <button type="button" className="sbk-ders-pop-x" onClick={onClose} aria-label="Kapat"><X aria-hidden /></button>
      </div>
      {e.slice(0, 3).map((x, i) => {
        const r = cumleAraligi(dz, x);
        const t = x.cumle.t;
        return (
          <div key={i} className="sbk-ders-pop-o">
            <small>{x.deste} · Slayt {x.cumle.s}{x.cumle.b ? ` · ${x.cumle.b}` : ''}</small>
            <q>{r ? <>{t.slice(0, r[0])}<mark className="sbk-ders-m">{t.slice(r[0], r[1])}</mark>{t.slice(r[1])}</> : t}</q>
            <button type="button" className="sbk-ders-git" onClick={() => git(x.cumle.d, x.cumle.s)}>
              Slayta git <ArrowRight aria-hidden />
            </button>
          </div>
        );
      })}
      {e.length > 3 && <small className="sbk-muted">+{e.length - 3} slayt daha</small>}
    </div>,
    document.body,
  );
};

export const DersKatmani: React.FC<{ dz: DersDizin | null; kok: HTMLElement | null; tazele: unknown }> = ({ dz, kok, tazele }) => {
  const katman = useRef<HTMLDivElement>(null);
  const [isaretler, setIsaretler] = useState<Isaret[]>([]);
  const [acik, setAcik] = useState<{ anahtar: string; top: number; right: number } | null>(null);
  const rangeler = useRef<Range[]>([]);
  const [yedek, setYedek] = useState<{ x: number; y: number; w: number; h: number }[]>([]);

  const tara = useCallback(() => {
    const hedef = katman.current?.offsetParent as HTMLElement | null;
    if (!dz || !kok || !hedef) return;
    const kr = hedef.getBoundingClientRect();
    const bloklar = new Set<Element>();
    const w = document.createTreeWalker(kok, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (/\d/.test((n as Text).data) && !(n as Text).parentElement?.closest(ATLA) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT),
    });
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const b = (n as Text).parentElement?.closest(BLOK);
      if (b && kok.contains(b)) bloklar.add(b);
    }
    const yeni: Isaret[] = [];
    const rl: Range[] = [];
    const kutular: { x: number; y: number; w: number; h: number }[] = [];
    let no = 0;
    for (const b of bloklar) {
      const { duz, isaretli, parcalar } = blokMetni(b);
      if (!duz || !/\d/.test(duz)) continue;
      const es = dersEslesmeleri(dz, isaretli, baglamMetni(b));
      if (!es.length) continue;
      // Aynı sayı için slaytları tek işarette topla
      const grup = new Map<string, DersEslesme[]>();
      for (const e of es) grup.set(`${e.bas}-${e.son}`, [...(grup.get(`${e.bas}-${e.son}`) || []), e]);
      for (const [, l] of grup) {
        const { bas, son } = l[0];
        const p = parcalar.find((x) => bas >= x.bas && son <= x.son);
        if (!p) continue;
        const r = document.createRange();
        try { r.setStart(p.dugum, bas - p.bas); r.setEnd(p.dugum, son - p.bas); } catch { continue; }
        const rects = r.getClientRects();
        const son2 = rects[rects.length - 1];
        if (!son2 || (!son2.width && !son2.height) || kirpildi(son2, p.dugum)) continue;
        rl.push(r);
        for (const q of Array.from(rects)) kutular.push({ x: q.left - kr.left, y: q.top - kr.top, w: q.width, h: q.height });
        yeni.push({ anahtar: `${no++}:${l[0].ham}:${l[0].cumle.t.slice(0, 20)}`, x: son2.right - kr.left, y: son2.top - kr.top, e: l });
      }
    }
    rangeler.current = rl;
    if (highlightVar()) {
      (CSS as any).highlights.set(VURGU, new (window as any).Highlight(...rl));
      setYedek([]);
    } else setYedek(kutular);
    setIsaretler(yeni);
  }, [dz, kok]);

  // İçerik değişince (bölüm, görünüm, açılan ayrıntı), boyut değişince ve iç kaydırmada yeniden tara
  useEffect(() => {
    if (!dz || !kok) return;
    let t = 0;
    // Zamanlayıcı (rAF değil): arka plandaki sekmede rAF durur, işaretler hiç çizilmezdi
    const planla = (gecikme = 120) => { window.clearTimeout(t); t = window.setTimeout(tara, gecikme); };
    planla(60);
    const mo = new MutationObserver(() => planla());
    mo.observe(kok, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['open', 'class', 'hidden'] });
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(() => planla()) : null;
    ro?.observe(kok);
    const kaydir = (e: Event) => { if (e.target instanceof Element && e.target !== document.documentElement && kok.contains(e.target)) planla(40); };
    kok.addEventListener('scroll', kaydir, true);
    const boyut = () => planla();
    window.addEventListener('resize', boyut);
    return () => {
      window.removeEventListener('resize', boyut);
      window.clearTimeout(t);
      mo.disconnect();
      ro?.disconnect();
      kok.removeEventListener('scroll', kaydir, true);
      if (highlightVar()) (CSS as any).highlights.delete(VURGU);
    };
  }, [dz, kok, tara]);
  useEffect(() => { setAcik(null); }, [tazele]);
  // Sayfa kayınca balon yerinde kalmasın
  useEffect(() => {
    if (!acik) return;
    const f = () => setAcik(null);
    window.addEventListener('scroll', f, { passive: true });
    return () => window.removeEventListener('scroll', f);
  }, [acik]);

  const secili = acik ? isaretler.find((x) => x.anahtar === acik.anahtar) : undefined;
  return (
    <div ref={katman} className="sbk-ders-katman" aria-hidden={false}>
      {yedek.map((k, i) => <span key={i} className="sbk-ders-yedek" style={{ left: k.x, top: k.y, width: k.w, height: k.h }} />)}
      {isaretler.map((x) => (
        <button
          key={x.anahtar} type="button" className={`sbk-ders-i-b ${acik?.anahtar === x.anahtar ? 'is-acik' : ''}`}
          style={{ left: x.x, top: x.y }} aria-expanded={acik?.anahtar === x.anahtar}
          title="Bu bilgi ders slaytında da geçiyor" aria-label={`${x.e[0].ham}: ders slaytında geçiyor, ayrıntı`}
          onClick={(ev) => {
            if (acik?.anahtar === x.anahtar) { setAcik(null); return; }
            const r = (ev.currentTarget as HTMLElement).getBoundingClientRect();
            setAcik({ anahtar: x.anahtar, top: r.bottom + 6, right: Math.max(8, window.innerWidth - r.right - 8) });
          }}
        ><Presentation aria-hidden /></button>
      ))}
      {acik && secili && dz && <DersBalonu dz={dz} e={secili.e} konum={acik} onClose={() => setAcik(null)} />}
    </div>
  );
};
