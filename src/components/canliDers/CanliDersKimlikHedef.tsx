/**
 * Kimlik bağlantısı (/k/<kimlik> → /canliders/<anahtar>#k1-03-c0142) ile açılan sesli derste hedefe kaydırma.
 *  - #k1-03-p010 → 10. paragraf (v2 numarası 1'den; bölüm başlıkları sayılmaz → p.i = 9)
 *  - #k1-03-b02  → 2. bölüm
 *  - #k1-03-c0142 → cümle: /api/k metni paragraflarda aranır, paragraf kaydırılır ve cümle işaretlenir
 * Oynatma kendiliğinden başlamaz; "Buradan dinle" düğmesi o paragraftan çalar. Stil: styles/kurul-suzgec.css.
 */
import React, { useEffect, useState } from 'react';
import { Play, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { cdDurum, cdOynat, cdParagrafa, type CdDetay } from './canliDersStore';
import '../../styles/kurul-suzgec.css';

const KIMLIK = /^#(k\d-\d{2})-([bpc])(\d{2,4})$/i;
const bosluk = (s: string) => s.replace(/\s+/g, ' ').trim();

/** Paragraf öğesindeki metin parçasını <mark> ile sarar; sarılamazsa (öğe sınırı) yalnız paragraf vurgulanır. */
function cumleIsaretle(p: HTMLElement, metin: string): HTMLElement | null {
  const hedef = bosluk(metin);
  const dugumler: Text[] = [];
  const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) dugumler.push(n as Text);
  // Düz metin + her karakterin hangi düğümden geldiği (boşluklar teke indirilir)
  let duz = '';
  const harita: Array<[Text, number]> = [];
  for (const d of dugumler) {
    const s = d.data;
    for (let i = 0; i < s.length; i++) {
      const c = /\s/.test(s[i]) ? ' ' : s[i];
      if (c === ' ' && duz.endsWith(' ')) continue;
      duz += c; harita.push([d, i]);
    }
  }
  const bas = duz.indexOf(hedef);
  if (bas < 0) return null;
  const [d0, o0] = harita[bas];
  const [d1, o1] = harita[bas + hedef.length - 1];
  try {
    const r = document.createRange();
    r.setStart(d0, o0);
    r.setEnd(d1, o1 + 1);
    const m = document.createElement('mark');
    m.className = 'kimlik-cumle';
    if (d0 === d1) r.surroundContents(m);
    else { m.appendChild(r.extractContents()); r.insertNode(m); }
    return m;
  } catch { return null; }
}

function isaretKaldir(m: HTMLElement | null) {
  const ust = m?.parentNode;
  if (!m || !ust) return;
  while (m.firstChild) ust.insertBefore(m.firstChild, m);
  ust.removeChild(m);
  (ust as HTMLElement).normalize?.();
}

export default function CanliDersKimlikHedef({ detay, kok }: { detay: CdDetay | null; kok: React.RefObject<HTMLElement | null> }) {
  const [dinle, setDinle] = useState<number | null>(null);

  useEffect(() => {
    if (!detay) return;
    const m = KIMLIK.exec(location.hash);
    if (!m) return;
    let iptal = false;
    let isaret: HTMLElement | null = null;
    const zaman: number[] = [];
    // Kullanıcı kendisi kaydırınca hedefi tutmayı bırak
    let kullanici = false;
    const birak = () => { kullanici = true; };
    ['wheel', 'touchstart', 'keydown'].forEach((t) => window.addEventListener(t, birak, { once: true, passive: true }));
    const vurgula = (el: HTMLElement) => {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Açılışta oynatıcının kaldığı paragrafı izlemesi / tur sayfayı başa çekebiliyor: kısa süre hedefi görünür tut
      for (const ms of [700, 1500, 2600]) {
        zaman.push(window.setTimeout(() => {
          if (kullanici || !el.isConnected) return;
          const r = el.getBoundingClientRect();
          if (r.bottom < 0 || r.top > innerHeight) el.scrollIntoView({ behavior: 'auto', block: 'center' });
        }, ms));
      }
      el.classList.remove('kimlik-vurgu');
      void el.offsetWidth;
      el.classList.add('kimlik-vurgu');
      zaman.push(window.setTimeout(() => el.classList.remove('kimlik-vurgu'), 2800));
    };
    const paragraf = (i: number) => kok.current?.querySelector<HTMLElement>(`.cd-p[data-i="${i}"]`) || null;
    const tumP = () => [...detay.bolumler.flatMap((b) => b.paragraflar)];
    const n = Number(m[3]);
    const tur = m[2].toLowerCase();

    const calis = async () => {
      if (tur === 'b') {
        const s = kok.current?.querySelectorAll<HTMLElement>('.cd-bolum')[n - 1];
        if (s) vurgula(s);
        const ilk = detay.bolumler[n - 1]?.paragraflar[0];
        if (ilk) setDinle(ilk.i);
        return;
      }
      if (tur === 'p') {
        const p = tumP()[n - 1];
        const el = p ? paragraf(p.i) : null;
        if (p && el) { vurgula(el); setDinle(p.i); }
        return;
      }
      // Cümle: metni sunucudan al, paragraflarda ara
      const r = await safeJsonFetch<{ metin?: string }>(`/api/k/${encodeURIComponent(location.hash.slice(1).toLowerCase())}`);
      if (iptal || !r.ok || !r.data?.metin) return;
      const hedef = bosluk(r.data.metin);
      const p = tumP().find((x) => bosluk(x.metin).includes(hedef));
      const el = p ? paragraf(p.i) : null;
      if (!p || !el) return;
      isaret = cumleIsaretle(el, hedef);
      vurgula(el);
      setDinle(p.i);
      zaman.push(window.setTimeout(() => { isaretKaldir(isaret); isaret = null; }, 12000));
    };
    // Metin listesi çizildikten sonra (PDF bölmesi ve düzen otursun)
    zaman.push(window.setTimeout(() => { void calis(); }, 450));
    return () => {
      iptal = true; zaman.forEach((t) => clearTimeout(t)); isaretKaldir(isaret);
      ['wheel', 'touchstart', 'keydown'].forEach((t) => window.removeEventListener(t, birak));
    };
  }, [detay, kok]);

  if (dinle == null || !detay) return null;
  return (
    <div className="kh-dinle" role="status">
      <button
        type="button"
        className="kh-dinle-ana"
        onClick={() => {
          if (cdDurum().key !== detay.key) cdOynat(detay, undefined, { oynat: false });
          cdParagrafa(dinle);
          setDinle(null);
        }}
      >
        <Play aria-hidden /> Buradan dinle
      </button>
      <button type="button" className="kh-dinle-kapat" onClick={() => setDinle(null)} aria-label="Kapat"><X aria-hidden /></button>
    </div>
  );
}
