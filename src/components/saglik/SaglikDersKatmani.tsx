import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight, FileQuestion, Presentation, TriangleAlert, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { elementZoom } from '../../utils/uiZoom';
import { dersEslesmeleri, terimAraligi, terimleriBul, type DersDizin, type DersEslesme } from './saglikDers';
import '../../styles/saglik-ders.css';

/**
 * "Ders slaytında geçiyor" katmanı — Sağlık Bakanlığı sekmesinin TÜM içeriğinde (kart, madde, tablo, açıklama, havuz…)
 * çalışır. React'in çizdiği DOM'a dokunmaz: metin düğümleri okunur, eşleşen sayı CSS Custom Highlight ile vurgulanır
 * (`::highlight(sbk-ders)`), "!" düğmeleri ayrı bir katmanda sayının sağ üstüne konur. Dokununca slayt cümlesi
 * (sayı vurgulu) sayfanın en üstündeki balonda açılır; "Slayta git" Öğren'de o slaytı açar, çıkmış soruda "Soruyu aç".
 * Üç tür işaret: aynı değer (sarı), aynı gösterge ve yıl için slaytta farklı değer (turuncu, ⚠), slaytta / çıkmışta geçen
 * terim (noktalı alt çizgi; dokununca balon — her bölümde ilk geçtiği yerde).
 *
 * Bağlam: değerin bulunduğu blok (madde, tablo hücresi, gösterge kutusu…) + üst maddelerin etiketleri + `data-ders-ad`
 * (gösterge kutusu/satır adı) + tablo satır ve sütun başlığı. Eşleştirme kuralları saglikDers.ts'tedir.
 */

const BLOK = 'li, p, td, th, dd, dt, .sbk-kpi, .sbk-satir-ust, h4, .sbk-karsi-s, figcaption, summary, blockquote, .sbk-gosterge-l > button, .sbk-deger-l > div';
// Taranmayan yerler: kaynakça, gezinti, düğme benzeri küçük denetimler, atıf numaraları, sınav soruları, katmanın kendisi
const ATLA = [
  '.sbk-atif', '.sbk-kaynakca', '.sbk-altnav', '.sbk-dizin', '.sbk-gez', '.sbk-sonraki', '.sbk-giris', '.sbk-bolum-h', '.sbk-cip-l', '.sbk-cip', '.sbk-seg', '.sbk-btn', '.sbk-ikon-btn', '.sbk-tk-b',
  '.sbk-kpi-gecmis', '.sbk-satir-gecmis', '.sbk-link-btn', '.sbk-rozet', '.sbk-sina', '.sbk-ders-katman', '.sbk-capa', '.sbk-kivilcim',
  'svg', 'input', 'select', 'textarea', 'code', '[aria-hidden="true"]', '.sbk-gizli',
].join(',');
const KAYDIRAN = '.sbk-tablo-kap, .sbk-asi-kap, .sbk-gosterge-l, .sbk-havuz-nav, .sbk-okunur-kartlar';
const VURGU = 'sbk-ders';
const VURGU_F = 'sbk-ders-f';
const VURGU_T = 'sbk-ders-t';
/** Terim her bölümde (kart/blok) yalnız ilk geçtiği yerde işaretlenir */
const BOLUM = '.sbk-blok, .sbk-gecmis, .sbk-kavram, section';
/** Düğme/bağlantı içindeki terim işaretlenmez (dokunuş düğmenin kendi işine gider) */
const ETKILESIMLI = 'button, a, summary, [role="button"], label, input, select';

interface Isaret { anahtar: string; x: number; y: number; e: DersEslesme[]; farkli: boolean }
interface TerimKutu { x: number; y: number; w: number; h: number; e: DersEslesme[]; anahtar: string }
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

/** Üst maddelerin etiketleri, gösterge adı, tablo satır/sütun başlığı; `ad`: değerin adı (gösterge / satır / sütun) */
function baglamMetni(blok: Element): { baglam: string; ad: string } {
  const parca: string[] = [];
  let ad = blok.closest<HTMLElement>('[data-ders-ad]')?.dataset.dersAd || '';
  if (ad) parca.push(ad);
  if (blok.matches('td, th')) {
    const tr = blok.closest('tr');
    const tablo = blok.closest('table');
    const i = tr ? Array.from(tr.children).indexOf(blok) : -1;
    const satirBas = tr?.firstElementChild && tr.firstElementChild !== blok ? tr.firstElementChild.textContent || '' : '';
    const sutunBas = i >= 0 ? tablo?.querySelector('thead tr')?.children[i]?.textContent || '' : '';
    parca.push(satirBas, sutunBas);
    if (!ad) ad = satirBas.replace(/\s+/g, ' ').trim();
  }
  // Üst madde(ler): kendi ilk satırlarının etiketi ("Anne ölüm oranı: …" → "Anne ölüm oranı"; "Yıllara göre")
  let li = blok.parentElement?.closest('li');
  let say = 0;
  while (li && say < 3) {
    const ilk = li.firstElementChild;
    // Bloğun kendi satırı (ör. gösterge satırının üst kısmı) üst madde sayılmaz: kendi değerleri bağlama karışırdı
    if (ilk && !ilk.contains(blok)) {
      const t = (!ilk.matches('ul, ol') ? ilk.textContent : '') || '';
      parca.push(etiket(t) || t.slice(0, 60));
    }
    li = li.parentElement?.closest('li');
    say++;
  }
  return { baglam: parca.filter(Boolean).join(' ').replace(/\s+/g, ' ').trim(), ad };
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
  const soruAc = (id: string) => {
    onClose();
    navigateTo(`${pathFor('past_exams')}/${encodeURIComponent(id)}`);
  };
  const farkli = e.find((x) => x.tur === 'farkli');
  const terim = e.find((x) => x.tur === 'terim')?.terim;
  const slaytlar = e.filter((x) => !x.cumle.q);
  const sorular = e.filter((x) => x.cumle.q);
  const baslik = farkli ? 'Ders slaytında farklı değer' : terim ? 'Derste geçen terim' : slaytlar.length ? 'Ders slaytında geçiyor' : 'Çıkmış soruda geçiyor';
  const Oge: React.FC<{ x: DersEslesme }> = ({ x }) => {
    const t = x.cumle.t;
    const r: [number, number] | null = x.tur === 'terim' && x.terim ? terimAraligi(t, x.terim) : [x.sa, x.sb];
    return (
      <div className="sbk-ders-pop-o">
        <small>{x.cumle.q ? `Çıkmış soru${x.cumle.qy ? ` · ${x.cumle.qy}` : ''}${x.cumle.qk ? ` · Kurul ${x.cumle.qk}` : ''}` : `${x.deste} · Slayt ${x.cumle.s}`}{x.cumle.b ? ` · ${x.cumle.b}` : ''}</small>
        <q>{r && r[1] > r[0] ? <>{t.slice(0, r[0])}<mark className="sbk-ders-m">{t.slice(r[0], r[1])}</mark>{t.slice(r[1])}</> : t}</q>
        {x.cumle.q ? (
          <button type="button" className="sbk-ders-git" onClick={() => soruAc(x.cumle.q!)}>Soruyu aç <ArrowRight aria-hidden /></button>
        ) : (
          <button type="button" className="sbk-ders-git" onClick={() => git(x.cumle.d, x.cumle.s)}>Slayta git <ArrowRight aria-hidden /></button>
        )}
      </div>
    );
  };
  return createPortal(
    <div ref={ref} className={`sbk-ders-pop is-sabit ${farkli ? 'is-farkli' : ''}`} role="dialog" aria-label={baslik} style={{ top: ust, right: sag }}>
      <div className="sbk-ders-pop-u">
        <span className="sbk-ders-pop-t">{farkli ? <TriangleAlert aria-hidden /> : <Presentation aria-hidden />} {baslik}</span>
        <button type="button" className="sbk-ders-pop-x" onClick={onClose} aria-label="Kapat"><X aria-hidden /></button>
      </div>
      {farkli && (
        <p className="sbk-ders-pop-f">
          Bu sayfada <b>{farkli.ham}</b>{farkli.yil ? ` (${farkli.yil})` : ''}, ders slaytında <b>{farkli.slaytDeger?.replace('.', ',')}</b> yazıyor.
          {' '}Sayfadaki değer resmî kaynaktandır (sonradan güncellenmiş olabilir); sınav ders slaytına göre hazırlanır, slayttaki değeri bilin.
        </p>
      )}
      {terim && (
        <p className="sbk-ders-pop-f is-terim">
          <b>{terim.t}</b> · {terim.n} slayt cümlesinde{terim.nq ? `, ${terim.nq} çıkmış soruda` : ''} geçiyor.
        </p>
      )}
      {slaytlar.slice(0, 3).map((x, i) => <Oge key={`s${i}`} x={x} />)}
      {slaytlar.length > 3 && <small className="sbk-muted">+{slaytlar.length - 3} slayt daha</small>}
      {sorular.length > 0 && <span className="sbk-ders-pop-ara"><FileQuestion aria-hidden /> Çıkmış soruda</span>}
      {sorular.slice(0, 2).map((x, i) => <Oge key={`q${i}`} x={x} />)}
      {sorular.length > 2 && <small className="sbk-muted">+{sorular.length - 2} çıkmış soru daha</small>}
    </div>,
    document.body,
  );
};

/** Vurgular CSS Highlight kayıtlarında tek ad altında toplanır; sayfa katmanı ile "Geçmiş yıllar" penceresinin katmanı
 * aynı anda çalışabildiği için her katman kendi aralıklarını buraya yazar, kayıt hepsinin birleşimidir */
type Turler = { ayni: Range[]; farkli: Range[]; terim: Range[] };
const kayitlar = new Map<number, Turler>();
let sonKatman = 0;
function vurgulariYaz() {
  if (!highlightVar()) return;
  const hl = (CSS as any).highlights;
  const birlesik: Turler = { ayni: [], farkli: [], terim: [] };
  for (const t of kayitlar.values()) { birlesik.ayni.push(...t.ayni); birlesik.farkli.push(...t.farkli); birlesik.terim.push(...t.terim); }
  const H = (window as any).Highlight;
  for (const [ad, l] of [[VURGU, birlesik.ayni], [VURGU_F, birlesik.farkli], [VURGU_T, birlesik.terim]] as const) {
    if (l.length) hl.set(ad, new H(...l)); else hl.delete(ad);
  }
}
const yerelSayfa = () => /\/saglik\/karabuk/.test(window.location.pathname);

export const DersKatmani: React.FC<{ dz: DersDizin | null; kok: HTMLElement | null; tazele: unknown; yerel?: boolean }> = ({ dz, kok, tazele, yerel }) => {
  const katman = useRef<HTMLDivElement>(null);
  const [kimlik] = useState(() => ++sonKatman);
  const [isaretler, setIsaretler] = useState<Isaret[]>([]);
  const [acik, setAcik] = useState<{ anahtar: string; top: number; right: number } | null>(null);
  const terimKutulari = useRef<TerimKutu[]>([]);
  const [yedek, setYedek] = useState<{ x: number; y: number; w: number; h: number; tur: string }[]>([]);
  // Konumlar görünür px'tir (getBoundingClientRect); yazı boyutu/ölçek (CSS zoom) açıkken katmanın kendi px'ine bölünür,
  // yoksa rozetler sayıdan uzaklaşır (telefonda büyük yazıda)
  const [olcek, setOlcek] = useState(1);

  const tara = useCallback(() => {
    const hedef = katman.current?.offsetParent as HTMLElement | null;
    if (!dz || !kok || !hedef) return;
    const kr = hedef.getBoundingClientRect();
    const ilSayfasi = yerel ?? yerelSayfa();
    const bloklar = new Set<Element>();
    const w = document.createTreeWalker(kok, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => ((n as Text).data.trim() && !(n as Text).parentElement?.closest(ATLA) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT),
    });
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const b = (n as Text).parentElement?.closest(BLOK);
      if (b && kok.contains(b)) bloklar.add(b);
    }
    const yeni: Isaret[] = [];
    const tur: Turler = { ayni: [], farkli: [], terim: [] };
    const kutular: { x: number; y: number; w: number; h: number; tur: string }[] = [];
    const tk: TerimKutu[] = [];
    // Terim, bölümünde yalnız ilk geçtiği yerde
    const bolumdeGorulen = new Map<Element, Set<string>>();
    let no = 0;
    const aralik = (parcalar: Parca[], bas: number, son: number) => {
      const p = parcalar.find((x) => bas >= x.bas && son <= x.son);
      if (!p) return null;
      const r = document.createRange();
      try { r.setStart(p.dugum, bas - p.bas); r.setEnd(p.dugum, son - p.bas); } catch { return null; }
      const rects = r.getClientRects();
      const son2 = rects[rects.length - 1];
      if (!son2 || (!son2.width && !son2.height) || kirpildi(son2, p.dugum)) return null;
      return { r, rects: Array.from(rects), son2, dugum: p.dugum };
    };
    for (const b of bloklar) {
      const { duz, isaretli, parcalar } = blokMetni(b);
      if (!duz) continue;
      const sayiAraliklari: [number, number][] = [];
      if (/\d/.test(duz)) {
        const { baglam, ad } = baglamMetni(b);
        const es = dersEslesmeleri(dz, isaretli, baglam, { ad: ad || undefined, yerel: ilSayfasi });
        // Aynı sayı için slaytları tek işarette topla
        const grup = new Map<string, DersEslesme[]>();
        for (const e of es) grup.set(`${e.bas}-${e.son}`, [...(grup.get(`${e.bas}-${e.son}`) || []), e]);
        for (const [, l] of grup) {
          const { bas, son } = l[0];
          const ar = aralik(parcalar, bas, son);
          if (!ar) continue;
          const farkli = l.every((x) => x.tur === 'farkli');
          (farkli ? tur.farkli : tur.ayni).push(ar.r);
          sayiAraliklari.push([bas, son]);
          for (const q of ar.rects) kutular.push({ x: q.left - kr.left, y: q.top - kr.top, w: q.width, h: q.height, tur: farkli ? 'f' : 'a' });
          yeni.push({ anahtar: `${no++}:${l[0].ham}:${l[0].cumle.t.slice(0, 20)}`, x: ar.son2.right - kr.left, y: ar.son2.top - kr.top, e: l, farkli });
        }
      }
      // Terimler (düğme/bağlantı içindekiler hariç; sayı işaretiyle çakışanlar hariç)
      if (!dz.terimler?.length) continue;
      const bolum = b.closest(BOLUM) || kok;
      const gorulen = bolumdeGorulen.get(bolum) || bolumdeGorulen.set(bolum, new Set()).get(bolum)!;
      for (const [bas, son, x] of terimleriBul(dz, duz)) {
        const anahtar = x.a || x.k.join(' ');
        if (gorulen.has(anahtar)) continue;
        if (sayiAraliklari.some(([a2, b2]) => bas < b2 && son > a2)) continue;
        const ar = aralik(parcalar, bas, son);
        if (!ar || ar.dugum.parentElement?.closest(ETKILESIMLI)) continue;
        gorulen.add(anahtar);
        tur.terim.push(ar.r);
        const e: DersEslesme[] = [
          ...x.s.map((n) => dz.cumleler[n]).filter(Boolean).map((c) => ({ tur: 'terim' as const, cumle: c, deste: dz.desteler[c.d] || c.d, bas, son, ham: duz.slice(bas, son), sa: 0, sb: 0, terim: x })),
          ...x.q.map((n) => dz.cumleler[n]).filter(Boolean).map((c) => ({ tur: 'terim' as const, cumle: c, deste: 'Çıkmış soru', bas, son, ham: duz.slice(bas, son), sa: 0, sb: 0, terim: x })),
        ];
        if (!e.length) continue;
        const k = `t${no++}:${anahtar}`;
        for (const q of ar.rects) {
          tk.push({ x: q.left - kr.left, y: q.top - kr.top, w: q.width, h: q.height, e, anahtar: k });
          kutular.push({ x: q.left - kr.left, y: q.top - kr.top, w: q.width, h: q.height, tur: 't' });
        }
        yeni.push({ anahtar: k, x: 0, y: 0, e, farkli: false });
      }
    }
    terimKutulari.current = tk;
    setOlcek(elementZoom(katman.current) || 1);
    kayitlar.set(kimlik, tur);
    if (highlightVar()) { vurgulariYaz(); setYedek([]); } else setYedek(kutular);
    setIsaretler(yeni);
  }, [dz, kok, kimlik, yerel]);

  // İçerik değişince (bölüm, görünüm, açılan ayrıntı), boyut değişince ve iç kaydırmada yeniden tara
  useEffect(() => {
    if (!dz || !kok) return;
    let t = 0;
    // Zamanlayıcı (rAF değil): arka plandaki sekmede rAF durur, işaretler hiç çizilmezdi
    const planla = (gecikme = 120) => { window.clearTimeout(t); t = window.setTimeout(tara, gecikme); };
    planla(60);
    // Açılış canlandırması (pencere kayarak gelir) konumları kaydırır; transform ResizeObserver'a görünmez → bitince yeniden
    const gec = [window.setTimeout(tara, 450), window.setTimeout(tara, 1000)];
    const animBitti = (e: Event) => { if (e.target instanceof Element && e.target.contains(kok)) planla(30); };
    document.addEventListener('transitionend', animBitti, true);
    document.addEventListener('animationend', animBitti, true);
    // Katmanın kendi düğmeleri (geçmiş penceresinde katman taranan kabın içinde) yeniden taramayı tetiklemesin
    const mo = new MutationObserver((l) => { if (l.some((m) => !katman.current?.contains(m.target))) planla(); });
    mo.observe(kok, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['open', 'class', 'hidden'] });
    // Yazı boyutu / ölçek kökteki değişkenlerle (style) değişir; içerik CSS px'te aynı kaldığı için ResizeObserver görmez
    const kokMo = new MutationObserver(() => planla(80));
    kokMo.observe(document.documentElement, { attributes: true, attributeFilter: ['style', 'data-design'] });
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(() => planla()) : null;
    ro?.observe(kok);
    const kaydir = (e: Event) => { if (e.target instanceof Element && e.target !== document.documentElement && kok.contains(e.target)) planla(40); };
    kok.addEventListener('scroll', kaydir, true);
    const boyut = () => planla();
    window.addEventListener('resize', boyut);
    // Terime dokunma: vurgu (Highlight) tıklanamaz → dokunulan nokta terim kutularında aranır
    const tikla = (ev: MouseEvent) => {
      const hedefEl = ev.target as Element | null;
      if (!hedefEl || hedefEl.closest(ETKILESIMLI) || hedefEl.closest('.sbk-ders-katman')) return;
      if (window.getSelection()?.toString()) return;
      const o = katman.current?.offsetParent?.getBoundingClientRect();
      if (!o) return;
      const x = ev.clientX - o.left;
      const y = ev.clientY - o.top;
      const k = terimKutulari.current.find((q) => x >= q.x - 2 && x <= q.x + q.w + 2 && y >= q.y - 2 && y <= q.y + q.h + 2);
      if (!k) return;
      setAcik({ anahtar: k.anahtar, top: o.top + k.y + k.h + 6, right: Math.max(8, window.innerWidth - (o.left + k.x + k.w) - 8) });
    };
    // İmleç terimin üstündeyken el işareti
    let imlec = false;
    const gezin = (ev: PointerEvent) => {
      if (ev.pointerType !== 'mouse') return;
      const o = katman.current?.offsetParent?.getBoundingClientRect();
      if (!o) return;
      const x = ev.clientX - o.left;
      const y = ev.clientY - o.top;
      const ust = terimKutulari.current.some((q) => x >= q.x && x <= q.x + q.w && y >= q.y && y <= q.y + q.h);
      if (ust !== imlec) { imlec = ust; kok.toggleAttribute('data-terim-ust', ust); }
    };
    kok.addEventListener('click', tikla);
    kok.addEventListener('pointermove', gezin, { passive: true });
    return () => {
      window.removeEventListener('resize', boyut);
      window.clearTimeout(t);
      gec.forEach((x) => window.clearTimeout(x));
      document.removeEventListener('transitionend', animBitti, true);
      document.removeEventListener('animationend', animBitti, true);
      mo.disconnect();
      kokMo.disconnect();
      ro?.disconnect();
      kok.removeEventListener('scroll', kaydir, true);
      kok.removeEventListener('click', tikla);
      kok.removeEventListener('pointermove', gezin);
      kok.removeAttribute('data-terim-ust');
      kayitlar.delete(kimlik);
      vurgulariYaz();
    };
  }, [dz, kok, tara, kimlik]);
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
      {yedek.map((k, i) => <span key={i} className={`sbk-ders-yedek is-${k.tur}`} style={{ left: k.x / olcek, top: k.y / olcek, width: k.w / olcek, height: k.h / olcek }} />)}
      {isaretler.filter((x) => !x.anahtar.startsWith('t')).map((x) => (
        <button
          key={x.anahtar} type="button" className={`sbk-ders-i-b ${x.farkli ? 'is-farkli' : ''} ${acik?.anahtar === x.anahtar ? 'is-acik' : ''}`}
          style={{ left: x.x / olcek, top: x.y / olcek }} aria-expanded={acik?.anahtar === x.anahtar}
          title={x.farkli ? 'Ders slaytında bu yıl için farklı değer yazıyor' : x.e.every((e) => e.cumle.q) ? 'Bu bilgi çıkmış soruda da geçiyor' : 'Bu bilgi ders slaytında da geçiyor'}
          aria-label={`${x.e[0].ham}: ${x.farkli ? 'ders slaytında farklı değer' : 'ders slaytında geçiyor'}, ayrıntı`}
          onClick={(ev) => {
            if (acik?.anahtar === x.anahtar) { setAcik(null); return; }
            const r = (ev.currentTarget as HTMLElement).getBoundingClientRect();
            setAcik({ anahtar: x.anahtar, top: r.bottom + 6, right: Math.max(8, window.innerWidth - r.right - 8) });
          }}
        >{x.farkli ? <TriangleAlert aria-hidden /> : <Presentation aria-hidden />}</button>
      ))}
      {acik && secili && dz && <DersBalonu dz={dz} e={secili.e} konum={acik} onClose={() => setAcik(null)} />}
    </div>
  );
};
