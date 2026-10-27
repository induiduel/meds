import React, { useMemo, useState } from 'react';
import { FileDown, Repeat, Star, Trash2 } from 'lucide-react';
import { YildizliParagraflarPanel } from '../study/YildizliParagraflarModal';
import { useYildizliSayisi } from '../../services/yildizliParagrafStore';
import { favoriSil, useFavoriler, type Favori } from '../../services/favoriStore';
import { linkClick, navigateTo, pathFor } from '../../router';

const TUR_AD: Record<Favori['tur'], string> = { terim: 'Terim', hastalik: 'Hastalık / kavram', bilgi: 'Bilgi', onemli: 'Önemli nokta', spot: 'Sınav spotu', tablo: 'Tablo', liste: 'Liste' };
const BOLUM_AD: Record<string, string> = { terimler: 'Terimler', hastaliklar: 'Hastalıklar', bilgiler: 'Bilgiler', tablolar: 'Tablolar', listeler: 'Listeler' };
const esc = (t: string) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const konum = (f: Favori) => [`Kurul ${f.kurul}`, f.ders, BOLUM_AD[f.bolum] || f.bolum, f.slayt?.length ? `Slayt s.${f.slayt.join(', ')}` : '', f.adim ? `Öğren adımı ${f.adim}` : ''].filter(Boolean).join(' › ');

/** Metni maddeleştirir: '- ' satırları liste, diğerleri paragraf/alt başlık */
function govdeHtml(m: string) {
  let o = '', acik = false;
  for (const sat of m.split('\n').filter((x) => x.trim())) {
    const mad = /^- (.*)/.exec(sat);
    if (mad) { if (!acik) { o += '<ul>'; acik = true; } o += `<li>${esc(mad[1])}</li>`; }
    else { if (acik) { o += '</ul>'; acik = false; } o += `<p>${esc(sat)}</p>`; }
  }
  return o + (acik ? '</ul>' : '');
}

export function favoriPdfAc(liste: Favori[]) {
  const gruplar = new Map<string, Favori[]>();
  for (const f of liste) gruplar.set(`Kurul ${f.kurul} · ${f.ders}`, [...(gruplar.get(`Kurul ${f.kurul} · ${f.ders}`) || []), f]);
  const govde = [...gruplar].map(([ad, l]) => `<h2>${esc(ad)}</h2>` + l.map((f) => `<section><h3>${f.yildiz ? '★ ' : ''}${f.tekrar ? '↻ ' : ''}${esc(f.baslik)}</h3><div class="k">${esc(TUR_AD[f.tur])} · ${esc(konum(f))}</div>${govdeHtml(f.metin)}</section>`).join('')).join('');
  const html = `<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Favorilerim</title><style>
  body{font:13px/1.5 system-ui,sans-serif;color:#111;margin:24px}h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;border-bottom:2px solid #333;padding-bottom:3px;margin:22px 0 8px}
  section{break-inside:avoid;margin:0 0 12px}h3{font-size:14px;margin:0}.k{color:#555;font-size:11px;margin:1px 0 4px}p{margin:2px 0}ul{margin:2px 0 2px 18px;padding:0}.t{color:#555;margin-bottom:10px}</style></head>
  <body><h1>Favorilerim</h1><div class="t">${liste.length} kayıt · ${new Date().toLocaleDateString('tr-TR')} · ★ yıldızlı, ↻ tekrar edilecek</div>${govde}</body></html>`;
  const fr = document.createElement('iframe');
  fr.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0';
  document.body.appendChild(fr);
  fr.srcdoc = html;
  fr.onload = () => { fr.contentWindow?.focus(); fr.contentWindow?.print(); setTimeout(() => fr.remove(), 60000); };
}

/** Bugün: ★ / ↻ ile işaretlenen kayıtlar; kaynağına gider, PDF'e aktarılır */
export default function FavorilerBugun() {
  const ySay = useYildizliSayisi();
  return (
    <>
      <FavoriListesi />
      {ySay > 0 && (
        <section className="v15-card" aria-label="Yıldızlı paragraflar">
          <YildizliParagraflarPanel inline />
        </section>
      )}
    </>
  );
}

function FavoriListesi() {
  const l = useFavoriler();
  const [suz, setSuz] = useState<'hepsi' | 'yildiz' | 'tekrar'>('hepsi');
  const g = useMemo(() => l.filter((f) => suz === 'hepsi' || f[suz]), [l, suz]);
  if (!l.length) return null;
  return (
    <section className="fvb v15-card" aria-labelledby="fvb-h">
      <header className="fvb-u">
        <h2 id="fvb-h">Favorilerim <small>{l.length}</small></h2>
        <div className="fvb-sec" role="tablist">
          {([['hepsi', 'Hepsi'], ['yildiz', 'Yıldızlı'], ['tekrar', 'Tekrar et']] as const).map(([k, ad]) => <button key={k} type="button" role="tab" aria-selected={suz === k} onClick={() => setSuz(k)}>{ad}</button>)}
        </div>
        <button type="button" className="fvb-pdf" onClick={() => favoriPdfAc(g)} disabled={!g.length}><FileDown aria-hidden />PDF'e aktar</button>
      </header>
      <ul className="fvb-l" role="list">
        {g.map((f) => {
          const url = `${pathFor('ders_detay', f.dersKey)}?b=${f.bolum}`;
          return (
            <li key={f.id}>
              <a href={url} onClick={linkClick(() => navigateTo(url))}>
                <b>{f.yildiz && <Star aria-label="Yıldızlı" />}{f.tekrar && <Repeat aria-label="Tekrar et" />}{f.baslik}</b>
                <small>{TUR_AD[f.tur]} · {konum(f)}</small>
                <span>{f.metin.replace(/\n- /g, ' • ').replace(/\n/g, ' ').slice(0, 160)}</span>
              </a>
              <button type="button" onClick={() => favoriSil(f.id)} aria-label="Favorilerden çıkar"><Trash2 aria-hidden /></button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
