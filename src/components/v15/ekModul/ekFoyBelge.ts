import type { EkModul, HocaSet, HocaSoru } from './ekVeri';

/**
 * Çalışma föyünün saf (React'sız) kısmı: konu → soru listesi ve basılacak HTML belgesi. Hem ekran (EkFoy.tsx, "PDF oluştur")
 * hem de hazır PDF betiği (scripts/ek_modul/foy_pdf.mts) aynı belgeyi kullanır.
 */
export type Tur = 'bosluk' | 'dy' | 'cs';
export const TUR_AD: Record<Tur, string> = { bosluk: 'Boşluk doldurma', dy: 'Doğru mu, yanlış mı?', cs: 'Çoktan seçmeli' };
export const TUR_SIRA: Tur[] = ['bosluk', 'dy', 'cs'];

/** Konunun soruları türe göre; aynı metin/kök yinelenirse bir kez alınır */
export function foySorulari(m: EkModul, konuId: string): Record<Tur, HocaSoru[]> {
  const out: Record<Tur, HocaSoru[]> = { bosluk: [], dy: [], cs: [] };
  const k = m.foy?.konular.find((x) => x.id === konuId);
  if (!k || !m.hoca) return out;
  const gorulen = new Set<string>();
  m.hoca.setler.forEach((s) => {
    const nolar = new Set(k.sorular[s.id] || []);
    s.sorular.forEach((q: any) => {
      if (!nolar.has(q.no)) return;
      const anahtar = `${s.tur}|${q.metin || q.kok}|${q.secenekler ? Object.values(q.secenekler).join('|') : ''}`;
      if (gorulen.has(anahtar)) return;
      gorulen.add(anahtar);
      out[s.tur].push({ ...q, k: `${s.id}-${q.no}` });
    });
  });
  (Object.keys(out) as Tur[]).forEach((t) => { out[t] = out[t].map((q, i) => ({ ...q, no: i + 1 })); });
  return out;
}
export const sanalSet = (konu: string, tur: Tur, sorular: HocaSoru[]): HocaSet => ({ id: `foy-${konu}-${tur}`, ad: TUR_AD[tur], tur, aciklama: '', sorular });

/* ——— PDF belgesi ——— */
const e = (s: string) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const kalin = (s: string) => e(s).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
const FOY_CSS = `
@page { size: A4; margin: 15mm 15mm 16mm; }
* { box-sizing: border-box; } html { font: 10.2pt/1.5 Lato, 'Noto Sans', 'Liberation Sans', Arial, sans-serif; color: #1E2A2E; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; } h1, h2, h3, p, ul, ol { margin: 0; padding: 0; } b { font-weight: 800; }
.kapak { height: 262mm; padding: 14mm 12mm; border-radius: 8mm; background: #F4EEE2; display: flex; flex-direction: column; break-after: page; }
.kapak .u { font: 800 9pt Lato, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #2F5D50; }
.kapak img { width: 100%; border-radius: 7mm; margin: 10mm 0; }
.kapak h1 { font: 900 32pt/1.08 Lato, sans-serif; } .kapak .a { font: 500 14pt Lato, sans-serif; color: #2F5D50; margin-top: 3mm; }
.kapak p { margin-top: 5mm; color: #46524f; max-width: 130mm; } .kapak .d { margin-top: auto; font: 900 12pt Lato, sans-serif; color: #2F5D50; text-align: right; }
.konu { break-before: page; } .konu:first-of-type { break-before: auto; }
.ust { display: flex; gap: 5mm; align-items: center; margin-bottom: 4mm; }
.no { flex: none; width: 14mm; height: 14mm; border-radius: 4mm; background: #2F5D50; color: #fff; display: grid; place-items: center; font: 900 14pt Lato, sans-serif; }
.ust small { display: block; font: 800 7.6pt Lato, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #D9865B; }
.ust h2 { font: 900 17pt/1.15 Lato, sans-serif; }
.iki { display: grid; grid-template-columns: 78mm 1fr; gap: 5mm; align-items: start; margin-bottom: 5mm; }
.iki img { width: 100%; border-radius: 4mm; display: block; }
.bilgi { padding: 4mm 5mm; border-radius: 4mm; background: #EEF3EE; }
.bilgi h3, .bol h3 { font: 900 9.4pt Lato, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #2F5D50; margin-bottom: 1.6mm; }
.bilgi li { list-style: none; position: relative; padding-left: 4mm; margin-bottom: .9mm; font-size: 9.3pt; line-height: 1.42; }
.bilgi li::before { content: ""; position: absolute; left: .4mm; top: .6em; width: 1.5mm; height: 1.5mm; border-radius: 50%; background: #D9865B; }
.bol { margin-bottom: 5mm; } .bol h3 { display: flex; align-items: center; gap: 2.5mm; color: #1E2A2E; padding-bottom: 1.4mm; border-bottom: .5mm solid #E4D8C3; margin-bottom: 2.4mm; break-after: avoid; }
.bol h3 i { font-style: normal; display: inline-grid; place-items: center; width: 6mm; height: 6mm; border-radius: 50%; background: #D9865B; color: #fff; font-size: 8.5pt; letter-spacing: 0; }
.bol.dy h3 i { background: #2F5D50; } .bol.cs h3 i { background: #24384F; }
.bos li, .dyl li { list-style: none; break-inside: avoid; display: flex; gap: 2.5mm; margin-bottom: 1.7mm; }
.bos li > b, .dyl li > b, .csl .s > p > b { flex: none; min-width: 6mm; color: #2F5D50; }
.bos u { text-decoration: none; display: inline-block; min-width: 26mm; border-bottom: .35mm solid #1E2A2E; margin: 0 1mm; }
.dyl li span { flex: 1; } .dyl li em { flex: none; font-style: normal; display: flex; gap: 1.6mm; }
.dyl li em i { font-style: normal; width: 6.2mm; height: 6.2mm; border-radius: 50%; border: .35mm solid #7a8582; display: grid; place-items: center; font: 800 7.6pt Lato, sans-serif; color: #55615e; }
.csl { columns: 2; column-gap: 8mm; } .csl .s { break-inside: avoid; margin-bottom: 3.2mm; }
.csl .s > p { display: flex; gap: 2mm; font-weight: 700; } .csl ol { list-style: none; padding-left: 8mm; margin-top: .8mm; font-size: 9.6pt; }
.csl ol li b { color: #55615e; margin-right: 1.2mm; }
.anahtar { break-before: page; } .anahtar h2 { font: 900 17pt Lato, sans-serif; margin-bottom: 4mm; }
.ak { break-inside: avoid; margin-bottom: 4mm; padding: 3.5mm 4.5mm; border-radius: 3.5mm; background: #F7F3EA; font-size: 9.2pt; }
.ak h3 { font: 900 10.4pt Lato, sans-serif; color: #2F5D50; margin-bottom: 1.2mm; } .ak p { margin-bottom: .8mm; } .ak p b { color: #D9865B; }
`;

export function foyBelge(m: EkModul, konuIdleri: string[], anahtarli: boolean, gorseller: Record<string, string>): string {
  const konular = m.basliklar.flatMap((b) => b.konular.map((k) => ({ ...k, baslikNo: b.no, baslikAd: b.baslik }))).filter((k) => konuIdleri.includes(k.id));
  const govde: string[] = [];
  const anahtar: string[] = [];
  if (konular.length > 1) {
    govde.push(`<section class="kapak"><div class="u">${e(m.ozet.tur)} · Kurul ${m.ozet.kurul}</div>${gorseller[m.ozet.kapak] ? `<img src="${gorseller[m.ozet.kapak]}" alt="">` : ''}
      <h1>${e(m.ozet.ad)}</h1><div class="a">Çalışma föyü</div><p>Çalışma soruları konu konu düzenlendi: önce bilmen gerekenleri oku, sonra boşlukları doldur, doğru–yanlışları işaretle, soruları çöz.${anahtarli ? ' Cevap anahtarı sonda.' : ''}</p><div class="d">MeDSor</div></section>`);
  }
  konular.forEach((k) => {
    const f = m.foy?.konular.find((x) => x.id === k.id);
    const s = foySorulari(m, k.id);
    const b: string[] = [`<section class="konu"><div class="ust"><div class="no">${e(k.id)}</div><div><small>${k.baslikNo}. ${e(k.baslikAd)}</small><h2>${e(k.baslik)}</h2></div></div>`];
    b.push(`<div class="iki">${gorseller[k.gorsel] ? `<img src="${gorseller[k.gorsel]}" alt="">` : '<span></span>'}<div class="bilgi"><h3>Bilmen gerekenler</h3><ul>${(f?.bilgiler || []).map((x) => `<li>${kalin(x)}</li>`).join('')}</ul></div></div>`);
    if (s.bosluk.length) b.push(`<div class="bol"><h3><i>1</i>Boşlukları doldur</h3><ol class="bos">${s.bosluk.map((q: any) => `<li><b>${q.no}.</b><span>${e(q.metin).split('____').join('<u>&nbsp;</u>')}</span></li>`).join('')}</ol></div>`);
    if (s.dy.length) b.push(`<div class="bol dy"><h3><i>2</i>Doğru mu, yanlış mı?</h3><ol class="dyl">${s.dy.map((q: any) => `<li><b>${q.no}.</b><span>${e(q.metin)}</span><em><i>D</i><i>Y</i></em></li>`).join('')}</ol></div>`);
    if (s.cs.length) b.push(`<div class="bol cs"><h3><i>3</i>Çoktan seçmeli</h3><div class="csl">${s.cs.map((q: any) => `<div class="s"><p><b>${q.no}.</b><span>${e(q.kok)}</span></p><ol>${Object.entries(q.secenekler as Record<string, string>).map(([h, v]) => `<li><b>${h})</b>${e(v)}</li>`).join('')}</ol></div>`).join('')}</div></div>`);
    govde.push(`${b.join('')}</section>`);
    anahtar.push(`<div class="ak"><h3>${e(k.id)} · ${e(k.baslik)}</h3>`
      + (s.bosluk.length ? `<p><b>Boşluk:</b> ${s.bosluk.map((q: any) => `${q.no}. ${e(q.cevap)}`).join(' · ')}</p>` : '')
      + (s.dy.length ? `<p><b>Doğru–yanlış:</b> ${s.dy.map((q: any) => `${q.no}-${q.dogru ? 'D' : 'Y'}`).join(' · ')}</p>` : '')
      + (s.cs.length ? `<p><b>Çoktan seçmeli:</b> ${s.cs.map((q: any) => `${q.no}-${q.dogru}`).join(' · ')}</p>` : '') + '</div>');
  });
  if (anahtarli) govde.push(`<section class="anahtar"><h2>Cevap anahtarı</h2>${anahtar.join('')}</section>`);
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>${e(m.ozet.ad)} — Çalışma föyü</title><style>${FOY_CSS}</style></head><body>${govde.join('')}</body></html>`;
}


/* ——— çözümlü soru kitapçığı: hocanın setleri kendi sırasıyla, her sorunun altında cevap ve sesli çözümün metni ——— */
const COZ_CSS = `
.set { break-before: page; } .set h2 { font: 900 17pt/1.15 Lato, sans-serif; margin-bottom: 1mm; } .set > p { color: #55615e; margin-bottom: 4mm; }
.q { break-inside: avoid; padding: 2.6mm 0 2.8mm; border-bottom: .3mm solid #E4D8C3; }
.q > p { display: flex; gap: 2.5mm; } .q > p > b { flex: none; min-width: 7mm; color: #2F5D50; }
.q ol { list-style: none; padding-left: 9.5mm; margin-top: .8mm; display: grid; grid-template-columns: 1fr 1fr; gap: .4mm 6mm; font-size: 9.6pt; }
.q ol li b { color: #55615e; margin-right: 1.2mm; } .q ol li.d { font-weight: 800; color: #2F5D50; } .q ol li.d b { color: #2F5D50; }
.q .c { margin: 1.4mm 0 0 9.5mm; padding: 2mm 3mm; border-radius: 2.5mm; background: #EEF3EE; font-size: 9.2pt; line-height: 1.45; }
.q .c b { color: #D9865B; } .bos u { text-decoration: none; border-bottom: .35mm solid #1E2A2E; padding: 0 1mm; font-weight: 800; color: #2F5D50; }
`;
export function cozumluBelge(m: EkModul, gorseller: Record<string, string>): string {
  const setler = m.hoca?.setler || [];
  const toplam = setler.reduce((t, s) => t + s.sorular.length, 0);
  const govde = [`<section class="kapak"><div class="u">${e(m.ozet.tur)} · Kurul ${m.ozet.kurul}</div>${gorseller[m.ozet.kapak] ? `<img src="${gorseller[m.ozet.kapak]}" alt="">` : ''}
    <h1>${e(m.ozet.ad)}</h1><div class="a">Çözümlü çalışma soruları</div><p>Hocanın ${toplam} çalışma sorusu kendi sırasıyla: ${setler.map((s) => `${e(s.ad)} (${s.sorular.length})`).join(', ')}. Her sorunun altında cevabı ve kısa çözümü var; aynı çözümleri sitede sesli dinleyebilirsin.</p><div class="d">MeDSor</div></section>`];
  setler.forEach((s) => {
    const q = s.sorular.map((x: any) => {
      let kok: string;
      let alt = '';
      let cevap: string;
      if (s.tur === 'bosluk') {
        const p = String(x.metin).split('____');
        const c = String(x.cevap).split(/\s*,\s*/);
        kok = p.map((t, k) => e(t) + (k < p.length - 1 ? `<u>${e(p.length - 1 === 1 ? x.cevap : c.length === p.length - 1 ? c[k] : '…')}</u>` : '')).join('');
        cevap = `<b>Cevap:</b> ${e(x.cevap)}`;
      } else if (s.tur === 'dy') {
        kok = e(x.metin);
        cevap = `<b>${x.dogru ? 'Doğru' : 'Yanlış'}.</b>`;
      } else {
        kok = e(x.kok);
        alt = `<ol>${Object.entries(x.secenekler as Record<string, string>).map(([h, v]) => `<li${h === x.dogru ? ' class="d"' : ''}><b>${h})</b>${e(v)}</li>`).join('')}</ol>`;
        cevap = `<b>Cevap ${x.dogru}.</b>`;
      }
      return `<div class="q"><p><b>${x.no}.</b><span class="${s.tur === 'bosluk' ? 'bos' : ''}">${kok}</span></p>${alt}<div class="c">${cevap} ${e(x.cozum || '')}</div></div>`;
    }).join('');
    govde.push(`<section class="set"><h2>${e(s.ad)}</h2><p>${e(s.aciklama)} · ${s.sorular.length} soru</p>${q}</section>`);
  });
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>${e(m.ozet.ad)} — Çözümlü çalışma soruları</title><style>${FOY_CSS}${COZ_CSS}</style></head><body>${govde.join('')}</body></html>`;
}
