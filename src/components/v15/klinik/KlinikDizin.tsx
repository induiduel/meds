import React from 'react';
import { ChevronRight } from 'lucide-react';
import { linkClick, navigateTo } from '../../../router';
import { useAkis } from '../../../utils/appearance';
import '../../../styles/v18/dizin.css';

/**
 * Klinik dizin (H676, Figma "MeDSor v15 · Minimal" › Klinik/Dizin satırı). Merkez sayfalarının karo + kart ızgarası
 * yerine: harfli bölüm başlığı ("A · KAYNAKLAR", sayaç), numaralı satırlar (01…), çerçeveli simge, ad + tek satır
 * açıklama, sağda eş aralıklı meta. Satır gerçek bağlantıdır (`href` + uygulama içi gezinme); bağlantısız satır div.
 */
export interface DizinOge {
  id: string;
  ad: string;
  ne?: string;
  url?: string;
  ikon?: React.ElementType;
  meta?: string;
  etiket?: string;
  /** Kapalı/boş satır: soluk gösterilir ama bağlantı korunur (açıklama nedenini söyler) */
  soluk?: boolean;
}

export function KlinikDizin({ harf, baslik, ogeler, baslangic = 1, id }: { harf?: string; baslik: string; ogeler: DizinOge[]; baslangic?: number; id?: string }) {
  const akis = useAkis();
  if (!ogeler.length) return null;
  const hid = id ?? `kd-${baslik.toLocaleLowerCase('tr-TR').replace(/[^a-zçğıöşü0-9]+/g, '-')}`;
  // H687 · v18 Akış: numaralı satır listesi yerine solda yapışkan bölüm rayı + sağda simge karolu kart ızgarası
  if (akis) {
    return (
      <section className="akd" aria-labelledby={hid}>
        <header className="akd-ray">
          <h2 id={hid} className="akd-h">{baslik}</h2>
          <span className="akd-say">{ogeler.length} öge</span>
        </header>
        <ul className="akd-l" role="list">
          {ogeler.map((o) => {
            const I = o.ikon;
            const ic = (
              <>
                <span className="akd-ust">
                  {I ? <span className="akd-ic" aria-hidden><I /></span> : <span />}
                  {o.meta && <span className="akd-meta">{o.meta}</span>}
                </span>
                <b className="akd-ad">{o.ad}{o.etiket && <span className="akd-et">{o.etiket}</span>}</b>
                {o.ne && <span className="akd-ne">{o.ne}</span>}
              </>
            );
            return (
              <li key={o.id} className={o.soluk ? 'is-soluk' : undefined}>
                {o.url ? <a className="akd-k" href={o.url} onClick={linkClick(() => navigateTo(o.url!))}>{ic}</a> : <div className="akd-k">{ic}</div>}
              </li>
            );
          })}
        </ul>
      </section>
    );
  }
  return (
    <section className="kd" aria-labelledby={hid}>
      <h2 id={hid} className="kd-h">
        <span>{harf ? `${harf} · ` : ''}{baslik}</span>
        <span className="kd-say" aria-hidden>{String(ogeler.length).padStart(2, '0')}</span>
      </h2>
      <ul className="kd-l" role="list">
        {ogeler.map((o, i) => {
          const I = o.ikon;
          const ic = (
            <>
              <span className="kd-no" aria-hidden>{String(baslangic + i).padStart(2, '0')}</span>
              {I && <span className="kd-ic" aria-hidden><I /></span>}
              <span className="kd-t">
                <b>{o.ad}{o.etiket && <span className="v15-tag is-a">{o.etiket}</span>}</b>
                {o.ne && <span>{o.ne}</span>}
              </span>
              {o.meta && <span className="kd-meta">{o.meta}</span>}
              {o.url && <ChevronRight className="kd-ok" aria-hidden />}
            </>
          );
          return (
            <li key={o.id} className={o.soluk ? 'is-soluk' : undefined}>
              {o.url ? <a className="kd-s" href={o.url} onClick={linkClick(() => navigateTo(o.url!))}>{ic}</a> : <div className="kd-s">{ic}</div>}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
