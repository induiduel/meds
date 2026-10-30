/**
 * Soru dışa aktarıcı · PPTX yazıcısı (PresentationML, JSZip; ek bağımlılık yok).
 * Ölçülmüş her sayfa bir slayttır: kenar, çerçeve, başlık, bant, ızgara hücreleri (metin kutusu) ya da akış sütunları,
 * cevap şeridi ve alt bilgi aynı mm konumlarına yerleşir. Yazı boyutu önizlemedeki ölçeği (--k) kullanır; kutular
 * "taşarsa küçült" (normAutofit) işaretlidir, PowerPoint düzenlemede kendisi sığdırır.
 */
import JSZip from 'jszip';
import { cozumBos, cozumIcerik, etiketler, harfMetni, numaraMetni, parcala, KOLON_ARA, ANAHTAR_H, OPTIK_H, OPTIK_W, type Belge, type Blok, type HS, type Sayfa } from './belge';
import { ALT_MM, BASLIK_MM, GRUP_MM, SERIT_MM, YAZI, sayfaOlcu, type Ayar } from './ayar';
import { coreXml, karis, xml } from './docx';
import { kaynakAdi } from './kaynak';

const EMU = (mm: number) => Math.round(mm * 36000);
const hex = (c: string) => (/^#?[0-9a-f]{6}/i.exec(c)?.[0] || '#111827').replace('#', '').toUpperCase();
const DAIRE: Record<string, string> = { A: 'Ⓐ', B: 'Ⓑ', C: 'Ⓒ', D: 'Ⓓ', E: 'Ⓔ', F: 'Ⓕ' };
const NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"';

interface RO { fs: number; b?: boolean; renk?: string; vurgu?: string }
let FONT = 'Arial';
const rPr = (o: RO, tag = 'a:rPr') =>
  `<${tag} lang="tr-TR" sz="${Math.max(100, Math.round(o.fs * 100))}"${o.b ? ' b="1"' : ''} dirty="0">${o.renk ? `<a:solidFill><a:srgbClr val="${hex(o.renk)}"/></a:solidFill>` : ''}${o.vurgu ? `<a:highlight><a:srgbClr val="${o.vurgu}"/></a:highlight>` : ''}<a:latin typeface="${xml(FONT)}"/><a:cs typeface="${xml(FONT)}"/></${tag}>`;
const r = (t: string, o: RO) => (t ? `<a:r>${rPr(o)}<a:t>${xml(t)}</a:t></a:r>` : '');
const zengin = (t: string, o: RO) => parcala(t).map((p) => (p.br ? `<a:br>${rPr(o)}</a:br>` : r(p.t, { ...o, b: o.b || p.b }))).join('');
const TAB = '<a:r><a:rPr lang="tr-TR" dirty="0"/><a:t>\t</a:t></a:r>';

interface PO { satir: number; once?: number; sonra?: number; ind?: number; algn?: 'l' | 'ctr' | 'r' | 'just'; tab?: { pos: number; algn: 'l' | 'r' }[] }
const p = (icerik: string, o: PO, son: RO) =>
  `<a:p><a:pPr${o.ind ? ` marL="${o.ind}" indent="${-o.ind}"` : ''}${o.algn ? ` algn="${o.algn}"` : ''}><a:lnSpc><a:spcPct val="${Math.round((o.satir / 1.2) * 100000)}"/></a:lnSpc><a:spcBef><a:spcPts val="${Math.round((o.once || 0) * 100)}"/></a:spcBef><a:spcAft><a:spcPts val="${Math.round((o.sonra || 0) * 100)}"/></a:spcAft><a:buNone/>${o.tab ? `<a:tabLst>${o.tab.map((t) => `<a:tab pos="${t.pos}" algn="${t.algn}"/>`).join('')}</a:tabLst>` : ''}</a:pPr>${icerik}${rPr(son, 'a:endParaRPr')}</a:p>`;

/* ---------------------------------------------------------------------------
 * Blok paragrafları
 * ------------------------------------------------------------------------- */
function soruP(h: HS, a: Ayar, k: number, wMm: number): string[] {
  const fs = a.punto * k;
  const sat = a.satir;
  const par = a.paragraf * k;
  const out: string[] = [];
  const et = etiketler(h, a);
  const etP = () => p(et.map((e, i) => (i ? r('  ·  ', { fs: fs * 0.74, renk: '9CA3AF' }) : '') + r(e.ad, { fs: fs * 0.74, b: true, renk: e.renkli && h.renk ? h.renk : '64748B' })).join(''), { satir: sat, sonra: par }, { fs: fs * 0.74 });
  if (et.length && a.etiketYeri === 'ust') out.push(etP());
  const numRenk = h.renk && (a.renkStil === 'numara' || a.renkStil === 'etiket') ? h.renk : a.vurgu;
  out.push(p(r(numaraMetni(h.no, a) + ' ', { fs, b: true, renk: numRenk }) + zengin(h.q.stem, { fs, b: a.kokKalin }), { satir: sat, sonra: par, algn: a.iki ? 'just' : undefined }, { fs }));
  const ind = EMU(Math.min(7, wMm * 0.1));
  const sik = (x: { key: string; text: string }) => {
    const dg = a.dogruIsaret && x.key === h.dogru;
    const harf = dg && a.isaretStil === 'daire' && DAIRE[x.key] ? DAIRE[x.key] : harfMetni(x.key, a);
    const o: RO = { fs, b: dg, renk: dg && a.isaretStil !== 'zemin' && a.isaretStil !== 'tik' ? a.vurgu : undefined, vurgu: dg && a.isaretStil === 'zemin' ? karis(a.vurgu, 0.22) : undefined };
    return r(harf, { fs, b: true, renk: dg && a.isaretStil === 'daire' ? a.vurgu : undefined }) + TAB + zengin(x.text, o) + (dg && a.isaretStil === 'tik' ? r(' ✓', { fs, b: true, renk: a.vurgu }) : '');
  };
  const ara = a.paragraf * 0.6 * k;
  if (a.secenekDuzen === 'yan') {
    out.push(p(h.secenek.map((x, i) => (i ? r('     ', { fs }) : '') + sik(x).replace(TAB, r(' ', { fs }))).join(''), { satir: sat, sonra: 0 }, { fs }));
  } else if (a.secenekDuzen === 'iki') {
    const yarim = EMU(wMm / 2);
    for (let i = 0; i < h.secenek.length; i += 2) {
      const b = h.secenek[i + 1];
      out.push(p(sik(h.secenek[i]) + (b ? TAB + sik(b) : ''), { satir: sat, sonra: ara, ind, tab: [{ pos: ind, algn: 'l' }, { pos: yarim, algn: 'l' }, { pos: yarim + ind, algn: 'l' }] }, { fs }));
    }
  } else {
    for (const x of h.secenek) out.push(p(sik(x), { satir: sat, sonra: ara, ind, tab: [{ pos: ind, algn: 'l' }] }, { fs }));
  }
  if (et.length && a.etiketYeri === 'alt') out.push(etP());
  if (a.yazmaSatiri > 0) {
    const n = Math.max(8, Math.floor(wMm / (fs * 0.3528 * 0.5)));
    for (let i = 0; i < a.yazmaSatiri; i++) out.push(p(r('_'.repeat(n), { fs, renk: 'C7CBD1' }), { satir: sat * 1.1, sonra: 0 }, { fs }));
  }
  if (a.cozumYeri === 'altinda') {
    const c = cozumIcerik(h, a);
    if (!cozumBos(c)) out.push(...cozumP(h, a, k * 0.9, wMm, false));
  }
  return sonBosluk(out, a.soruArasi * k);
}

function cozumP(h: HS, a: Ayar, k: number, wMm: number, numarali: boolean): string[] {
  const c = cozumIcerik(h, a);
  if (numarali && !c.harf) c.harf = h.dogru || '—';
  const fs = a.punto * k;
  const sat = a.satir;
  const out: string[] = [];
  const bas = (numarali ? r(numaraMetni(h.no, a) + '  ', { fs, b: true, renk: h.renk || a.vurgu }) : '') + (c.harf ? r(`Cevap: ${c.harf}`, { fs, b: true, renk: a.vurgu }) : '');
  if (bas) out.push(p(bas, { satir: sat, sonra: 1.5 * k }, { fs }));
  if (c.aciklama) out.push(p(zengin(c.aciklama, { fs }), { satir: sat, sonra: 1.5 * k, algn: a.iki ? 'just' : undefined }, { fs }));
  const ind = EMU(Math.min(9, wMm * 0.12));
  for (const x of c.siklar) out.push(p(r(harfMetni(x.k, a), { fs, b: true, renk: x.dogru ? a.vurgu : undefined }) + TAB + zengin(x.t, { fs, renk: x.dogru ? a.vurgu : undefined }), { satir: sat, sonra: k, ind, tab: [{ pos: ind, algn: 'l' }] }, { fs }));
  if (c.kaynak) out.push(p(r(c.kaynak, { fs: fs * 0.88, renk: '6B7280' }), { satir: sat }, { fs }));
  return out;
}
/** Bloğun son paragrafına bloklar arası boşluk (mm → pt) */
const sonBosluk = (l: string[], mm: number) => {
  if (!l.length) return l;
  l[l.length - 1] = l[l.length - 1].replace(/<a:spcAft><a:spcPts val="\d+"\/><\/a:spcAft>/, `<a:spcAft><a:spcPts val="${Math.round(mm * 2.835 * 100)}"/></a:spcAft>`);
  return l;
};
const blokP = (b: Blok, a: Ayar, wMm: number): string[] =>
  b.t === 'soru' ? soruP(b.h, a, b.k, wMm)
    : b.t === 'cozum' ? sonBosluk(cozumP(b.h, a, b.k, wMm, true), a.soruArasi * b.k)
      : [p(r(b.ad, { fs: a.punto * 1.12, b: true, renk: b.renk || a.vurgu }), { satir: 1.15, sonra: a.soruArasi * 1.4 }, { fs: a.punto })];

/* ---------------------------------------------------------------------------
 * Şekiller
 * ------------------------------------------------------------------------- */
class Slayt {
  private id = 1;
  sekil: string[] = [];
  kutu(x: number, y: number, w: number, h: number, paras: string[], o: { ic?: number; dolgu?: string; cizgi?: { renk: string; kalin: number; kesik?: boolean }; yuvarlak?: boolean; anchor?: 't' | 'ctr' | 'b'; sigdir?: boolean; don?: number } = {}) {
    const id = ++this.id;
    const ic = EMU(o.ic || 0);
    const geom = o.yuvarlak ? '<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst></a:prstGeom>' : '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>';
    const fill = o.dolgu ? `<a:solidFill><a:srgbClr val="${o.dolgu}"/></a:solidFill>` : '<a:noFill/>';
    const ln = o.cizgi ? `<a:ln w="${Math.round(o.cizgi.kalin * 12700)}"><a:solidFill><a:srgbClr val="${hex(o.cizgi.renk)}"/></a:solidFill>${o.cizgi.kesik ? '<a:prstDash val="dash"/>' : ''}</a:ln>` : '<a:ln><a:noFill/></a:ln>';
    const govde = paras.length ? paras.join('') : '<a:p><a:endParaRPr lang="tr-TR" dirty="0"/></a:p>';
    this.sekil.push(`<p:sp><p:nvSpPr><p:cNvPr id="${id}" name="Kutu ${id}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm${o.don ? ` rot="${Math.round(o.don * 60000)}"` : ''}><a:off x="${EMU(x)}" y="${EMU(y)}"/><a:ext cx="${EMU(Math.max(0.5, w))}" cy="${EMU(Math.max(0.5, h))}"/></a:xfrm>${geom}${fill}${ln}</p:spPr><p:txBody><a:bodyPr wrap="square" lIns="${ic}" tIns="${ic}" rIns="${ic}" bIns="${ic}" anchor="${o.anchor || 't'}" rtlCol="0">${o.sigdir ? '<a:normAutofit/>' : '<a:noAutofit/>'}</a:bodyPr><a:lstStyle/>${govde}</p:txBody></p:sp>`);
  }
  dortgen(x: number, y: number, w: number, h: number, dolgu: string) { this.kutu(x, y, w, h, [], { dolgu: hex(dolgu) }); }
  xml(): string {
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld ${NS}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>${this.sekil.join('')}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>`;
  }
}

function slaytKur(pg: Sayfa, a: Ayar, no: number, toplam: number, b: Belge): Slayt {
  const s = new Slayt();
  const { w: PW, h: PH } = sayfaOlcu(a);
  const ic = a.cerceve ? a.cerceveIc + a.cerceveKalin * 0.35 : 0;
  const x0 = a.kenar[3] + ic;
  let y = a.kenar[0] + ic;
  if (a.filigran.trim()) s.kutu(0, PH / 2 - 25, PW, 50, [p(r(a.filigran.trim(), { fs: Math.min(PW, PH) / 7 * 2.835, b: true, renk: karis(a.metinRenk, 0.07) }), { satir: 1, algn: 'ctr' }, { fs: 20 })], { anchor: 'ctr', don: -32 });
  if (a.cerceve && pg.tur !== 'kapak') s.kutu(a.kenar[3], a.kenar[0], PW - a.kenar[1] - a.kenar[3], PH - a.kenar[0] - a.kenar[2], [], { cizgi: { renk: a.cerceveRenk, kalin: a.cerceveKalin, kesik: a.cerceveStil === 'dashed' || a.cerceveStil === 'dotted' }, yuvarlak: a.cerceveYaricap > 0 });

  if (pg.tur === 'kapak') {
    const W = PW - a.kenar[1] - a.kenar[3] - 12;
    const dersler = [...new Set(b.hs.map((h) => h.q.ders))];
    const kaynaklar = [...new Set(b.hs.map((h) => kaynakAdi(h.q.kaynak)))];
    s.kutu(a.kenar[3] + 6, a.kenar[0], W, PH - a.kenar[0] - a.kenar[2], [
      p(r(kaynaklar.join(' · ').toLocaleUpperCase('tr'), { fs: 9, b: true, renk: a.vurgu }), { satir: 1.2, sonra: 14 }, { fs: 9 }),
      p(r(a.baslik || 'Soru kitapçığı', { fs: 30, b: true, renk: a.metinRenk }), { satir: 1.1, sonra: 8 }, { fs: 30 }),
      a.altBaslik ? p(r(a.altBaslik, { fs: 13, renk: '4B5563' }), { satir: 1.2, sonra: 16 }, { fs: 13 }) : '',
      p(r(`${b.hs.length}`, { fs: 17, b: true, renk: a.vurgu }) + r(' soru     ', { fs: 9, renk: '6B7280' }) + r(`${dersler.length}`, { fs: 17, b: true, renk: a.vurgu }) + r(' ders', { fs: 9, renk: '6B7280' }), { satir: 1.2, sonra: 12 }, { fs: 9 }),
      dersler.length ? p(r(dersler.slice(0, 14).join(' · '), { fs: 9.5, renk: '374151' }), { satir: 1.3, sonra: 16 }, { fs: 9.5 }) : '',
      a.adSoyad ? p(r('Ad Soyad  ______________________________', { fs: 10 }), { satir: 1.6, sonra: 6 }, { fs: 10 }) : '',
      p(r(new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) + (a.altMetin ? ` · ${a.altMetin}` : ''), { fs: 8.5, renk: '9CA3AF' }), { satir: 1.2, once: 10 }, { fs: 8.5 }),
    ].filter(Boolean), { anchor: 'ctr' });
    return s;
  }

  const g = pg.g;
  if (g.baslik) {
    const sag = a.adSoyad || a.tarih ? Math.min(60, g.w * 0.42) : 0;
    s.kutu(x0, y, g.w - sag, BASLIK_MM - 1, [
      p(r(a.baslik, { fs: Math.min(16, a.punto * 1.45), b: true, renk: a.vurgu }), { satir: 1.1 }, { fs: 12 }),
      a.altBaslik ? p(r(a.altBaslik, { fs: Math.max(7, a.punto * 0.8), renk: '4B5563' }), { satir: 1.1 }, { fs: 8 }) : '',
    ].filter(Boolean), { anchor: 'b' });
    if (sag) s.kutu(x0 + g.w - sag, y, sag, BASLIK_MM - 1, [a.adSoyad ? p(r('Ad Soyad: _______________', { fs: Math.max(7, a.punto * 0.78), renk: '374151' }), { satir: 1.3 }, { fs: 8 }) : '', a.tarih ? p(r('Tarih: _______________', { fs: Math.max(7, a.punto * 0.78), renk: '374151' }), { satir: 1.3 }, { fs: 8 }) : ''].filter(Boolean), { anchor: 'b' });
    s.dortgen(x0, y + BASLIK_MM - 0.45, g.w, 0.4, a.vurgu);
    y += BASLIK_MM;
  }
  if (pg.bant) {
    s.dortgen(x0, y + GRUP_MM / 2 - 1.3, 2.6, 2.6, pg.bant.renk || a.vurgu);
    s.kutu(x0 + 5, y, g.w - 5, GRUP_MM - 0.4, [p(r(pg.bant.ad, { fs: Math.max(8, a.punto * 1.05), b: true, renk: a.vurgu }), { satir: 1.1 }, { fs: 10 })], { anchor: 'ctr' });
    s.dortgen(x0, y + GRUP_MM - 0.3, g.w, 0.2, '#D1D5DB');
    y += GRUP_MM;
  }
  const gy = y;
  if (pg.izgara && pg.hucre) {
    const { sut, sat, cw, ch } = pg.izgara;
    pg.hucre.forEach((bl, i) => {
      const c = i % sut;
      const rr = Math.floor(i / sut);
      const hx = x0 + c * (cw + a.hucreAralik);
      const hy = gy + rr * (ch + a.hucreAralik);
      if (!bl) { if (a.hucreCerceve) s.kutu(hx, hy, cw, ch, [], { cizgi: { renk: '#CBD5E1', kalin: 0.7 }, yuvarlak: true }); return; }
      const h = bl.t === 'grup' ? null : bl.h;
      const serit = !!(h?.renk && a.renkStil === 'serit');
      const ic2 = a.hucreCerceve ? 3 : 0;
      const zemin = h?.renk && a.renkStil === 'zemin' ? karis(h.renk, 0.09) : undefined;
      if (a.hucreCerceve || zemin) s.kutu(hx, hy, cw, ch, [], { cizgi: a.hucreCerceve ? { renk: '#CBD5E1', kalin: 0.7 } : undefined, yuvarlak: true, dolgu: zemin });
      if (serit) s.dortgen(hx + ic2, hy + ic2, 1.2, ch - ic2 * 2, h!.renk!);
      const sol = serit ? 3.8 : 0;
      const icW = cw - ic2 * 2 - sol;
      s.kutu(hx + ic2 + sol, hy + ic2, icW, ch - ic2 * 2, blokP(bl, a, icW), { sigdir: true });
    });
  } else if (pg.kolon) {
    const kw = pg.kolonW!;
    pg.kolon.forEach((kol, i) => {
      const kx = x0 + i * (kw + KOLON_ARA);
      if (i && a.sutunCizgi) s.dortgen(kx - KOLON_ARA / 2 - 0.1, gy, 0.2, g.h, '#9CA3AF');
      s.kutu(kx, gy, kw, g.h, kol.flatMap((bl) => blokP(bl, a, kw)), { sigdir: true });
    });
  } else if (pg.anahtar) {
    const sut = pg.anahtarSut || 8;
    const cw = (g.w - (sut - 1) * 1.2) / sut;
    pg.anahtar.forEach((x, i) => {
      const c = i % sut;
      const rr = Math.floor(i / sut);
      s.kutu(x0 + c * (cw + 1.2), gy + rr * ANAHTAR_H, cw, ANAHTAR_H - 1.2, [p(r(String(x.no), { fs: Math.max(8, a.punto * 0.92), b: true }) + TAB + r(x.harf, { fs: Math.max(8, a.punto * 0.92), b: true, renk: a.vurgu }), { satir: 1, tab: [{ pos: EMU(cw - 4), algn: 'r' }] }, { fs: 9 })], { ic: 1, anchor: 'ctr', cizgi: { renk: '#D1D5DB', kalin: 0.6 }, dolgu: x.renk ? karis(x.renk, 0.1) : undefined });
    });
  } else if (pg.optik) {
    const sut = pg.optikSut || 4;
    const sat = Math.ceil(pg.optik.length / sut);
    pg.optik.forEach((n, i) => {
      const c = Math.floor(i / sat);
      const rr = i % sat;
      s.kutu(x0 + c * (OPTIK_W + 5), gy + rr * OPTIK_H, OPTIK_W, OPTIK_H, [p(r(String(n).padStart(3, ' '), { fs: 8, b: true }) + r('   Ⓐ  Ⓑ  Ⓒ  Ⓓ  Ⓔ', { fs: 10.5, renk: '6B7280' }), { satir: 1 }, { fs: 8 })], { anchor: 'ctr' });
    });
  }
  y += g.h;
  if (pg.serit) {
    s.dortgen(x0, y, g.w, 0.2, '#9CA3AF');
    s.kutu(x0, y + 0.8, g.w, SERIT_MM - 1, [p(r('Cevaplar · ', { fs: Math.max(6.5, a.punto * 0.72), b: true, renk: a.vurgu }) + r(pg.serit.map((x) => `${x.no}-${x.harf}`).join('   '), { fs: Math.max(6.5, a.punto * 0.72), renk: '374151' }), { satir: 1.3 }, { fs: 7 })]);
    y += SERIT_MM;
  }
  if (a.sayfaNo || a.altMetin.trim()) {
    s.kutu(x0, y, g.w, ALT_MM, [p(r(a.altMetin, { fs: Math.max(6.5, a.punto * 0.72), renk: '6B7280' }) + TAB + (a.sayfaNo ? r(`${no} / ${toplam}`, { fs: Math.max(6.5, a.punto * 0.72), renk: '6B7280' }) : ''), { satir: 1, tab: [{ pos: EMU(g.w), algn: 'r' }] }, { fs: 7 })], { anchor: 'b' });
  }
  return s;
}

const TEMA = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="MeDSor"><a:themeElements><a:clrScheme name="MeDSor"><a:dk1><a:srgbClr val="111827"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="1F2937"/></a:dk2><a:lt2><a:srgbClr val="F3F4F6"/></a:lt2><a:accent1><a:srgbClr val="2563EB"/></a:accent1><a:accent2><a:srgbClr val="DC2626"/></a:accent2><a:accent3><a:srgbClr val="059669"/></a:accent3><a:accent4><a:srgbClr val="D97706"/></a:accent4><a:accent5><a:srgbClr val="7C3AED"/></a:accent5><a:accent6><a:srgbClr val="0891B2"/></a:accent6><a:hlink><a:srgbClr val="2563EB"/></a:hlink><a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink></a:clrScheme><a:fontScheme name="MeDSor"><a:majorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="MeDSor"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>`;
const BOS_AGAC = '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree>';
const STIL = '<a:lvl1pPr><a:defRPr/></a:lvl1pPr>';

export async function pptxUret(belge: Belge, a: Ayar): Promise<Blob> {
  FONT = YAZI[a.yazi].ofis;
  const { w, h } = sayfaOlcu(a);
  const kapakVar = belge.sayfalar[0]?.tur === 'kapak';
  const toplam = belge.sayfalar.length - (kapakVar ? 1 : 0);
  const slaytlar = belge.sayfalar.map((pg, i) => slaytKur(pg, a, kapakVar ? i : i + 1, toplam, belge).xml());
  const REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';
  const zip = new JSZip();
  zip.file('[Content_Types].xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/><Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/><Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>${slaytlar.map((_, i) => `<Override PartName="/ppt/slides/slide${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>`).join('')}<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>`);
  zip.file('_rels/.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${REL}/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="${REL}/extended-properties" Target="docProps/app.xml"/></Relationships>`);
  zip.file('docProps/core.xml', coreXml(a.baslik));
  zip.file('docProps/app.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>MeDSor</Application><Slides>${slaytlar.length}</Slides></Properties>`);
  zip.file('ppt/presentation.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation ${NS} saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>${slaytlar.map((_, i) => `<p:sldId id="${256 + i}" r:id="rIdS${i + 1}"/>`).join('')}</p:sldIdLst><p:sldSz cx="${EMU(w)}" cy="${EMU(h)}"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle>${STIL}</p:defaultTextStyle></p:presentation>`);
  zip.file('ppt/_rels/presentation.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${REL}/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="${REL}/theme" Target="theme/theme1.xml"/><Relationship Id="rId3" Type="${REL}/presProps" Target="presProps.xml"/><Relationship Id="rId4" Type="${REL}/viewProps" Target="viewProps.xml"/><Relationship Id="rId5" Type="${REL}/tableStyles" Target="tableStyles.xml"/>${slaytlar.map((_, i) => `<Relationship Id="rIdS${i + 1}" Type="${REL}/slide" Target="slides/slide${i + 1}.xml"/>`).join('')}</Relationships>`);
  zip.file('ppt/presProps.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr ${NS}/>`);
  zip.file('ppt/viewProps.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr ${NS}><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr><p:gridSpacing cx="76200" cy="76200"/></p:viewPr>`);
  zip.file('ppt/tableStyles.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>`);
  zip.file('ppt/theme/theme1.xml', TEMA);
  zip.file('ppt/slideMasters/slideMaster1.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster ${NS}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>${BOS_AGAC}</p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle>${STIL}</p:titleStyle><p:bodyStyle>${STIL}</p:bodyStyle><p:otherStyle>${STIL}</p:otherStyle></p:txStyles></p:sldMaster>`);
  zip.file('ppt/slideMasters/_rels/slideMaster1.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${REL}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="${REL}/theme" Target="../theme/theme1.xml"/></Relationships>`);
  zip.file('ppt/slideLayouts/slideLayout1.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout ${NS} type="blank" preserve="1"><p:cSld name="Boş">${BOS_AGAC}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>`);
  zip.file('ppt/slideLayouts/_rels/slideLayout1.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${REL}/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>`);
  slaytlar.forEach((x, i) => {
    zip.file(`ppt/slides/slide${i + 1}.xml`, x);
    zip.file(`ppt/slides/_rels/slide${i + 1}.xml.rels`, `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${REL}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>`);
  });
  return zip.generateAsync({ type: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.presentationml.presentation', compression: 'DEFLATE' });
}
