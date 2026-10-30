/**
 * Soru dışa aktarıcı · DOCX yazıcısı (WordprocessingML, JSZip; ek bağımlılık yok).
 * İki yerleşim kipi:
 *   sayfa kipi  ızgara (1/2/4/8) ve "arkada"/"sayfa altı" çözümlü akış: her ölçülmüş sayfa sabit yükseklikli bir
 *               tablodur (önizlemedeki ölçek --k aynen yazı boyutuna uygulanır), sayfalar arası küçük sayfa sonu paragrafı
 *   akış kipi   serbest akış ve sondaki çözümler: Word'ün kendi sütun akışı (düzenlenebilir), bloklar bölünmez
 * Kenar boşluğu, çerçeve (pgBorders), alt bilgi (sayfa no), başlık, renk şeridi/zemin/etiket, doğru şık işareti,
 * yazma satırları, cevap anahtarı ve cevap kâğıdı Word öğeleriyle karşılanır.
 */
import JSZip from 'jszip';
import {
  cozumBos, cozumIcerik, etiketler, harfMetni, numaraMetni, parcala, KOLON_ARA, MIN_K,
  type Belge, type Blok, type HS, type Sayfa,
} from './belge';
import { ALT_MM, BASLIK_MM, GRUP_MM, SERIT_MM, YAZI, sayfaOlcu, type Ayar } from './ayar';
import { kaynakAdi } from './kaynak';

const tw = (mm: number) => Math.max(0, Math.round(mm * 56.6929));
const hp = (pt: number) => Math.max(2, Math.round(pt * 2));
const hex = (c: string) => (/^#?[0-9a-f]{6}/i.exec(c)?.[0] || '#111827').replace('#', '').toUpperCase();
/** iki rengi karıştırır (açık zemin tonları için) */
export function karis(c: string, oran: number, zemin = 'FFFFFF'): string {
  const a = hex(c), b = hex(zemin);
  const p = (h: string, i: number) => parseInt(h.slice(i, i + 2), 16);
  return [0, 2, 4].map((i) => Math.round(p(a, i) * oran + p(b, i) * (1 - oran)).toString(16).padStart(2, '0')).join('').toUpperCase();
}
export const xml = (t: string) =>
  String(t ?? '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F￾￿]/g, '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const DAIRE: Record<string, string> = { A: 'Ⓐ', B: 'Ⓑ', C: 'Ⓒ', D: 'Ⓓ', E: 'Ⓔ', F: 'Ⓕ' };

interface RunO { b?: boolean; i?: boolean; renk?: string; fs: number; shd?: string; alt?: boolean; /** çerçeve rengi (etiket "çizgi" biçimi) */ bdr?: string }
const rPr = (o: RunO) =>
  `<w:rPr>${o.b ? '<w:b/><w:bCs/>' : ''}${o.i ? '<w:i/><w:iCs/>' : ''}${o.renk ? `<w:color w:val="${hex(o.renk)}"/>` : ''}<w:sz w:val="${hp(o.fs)}"/><w:szCs w:val="${hp(o.fs)}"/>${o.bdr ? `<w:bdr w:val="single" w:sz="4" w:space="1" w:color="${hex(o.bdr)}"/>` : ''}${o.shd ? `<w:shd w:val="clear" w:color="auto" w:fill="${o.shd}"/>` : ''}</w:rPr>`;
const run = (t: string, o: RunO) => `<w:r>${rPr(o)}<w:t xml:space="preserve">${xml(t)}</w:t></w:r>`;
const zengin = (t: string, o: RunO) => parcala(t).map((p) => (p.br ? `<w:r>${rPr(o)}<w:br/></w:r>` : run(p.t, { ...o, b: o.b || p.b }))).join('');

/** Word "auto" satır aralığı yazı tipinin tek satır yüksekliğiyle çarpılır (CSS ise puntoyla); yazı tipine göre bölünür */
const TEK_SATIR: Record<string, number> = { Arial: 1.15, 'Times New Roman': 1.15, Georgia: 1.14, Calibri: 1.22, 'Courier New': 1.13 };
let SATIR_F = 1.15;
const satirTw = (x: number) => Math.round((240 * x) / SATIR_F);

interface ParaO {
  after?: number; before?: number; satir?: number; tamH?: number; ind?: [number, number]; keep?: boolean; jc?: 'left' | 'center' | 'right' | 'both';
  sol?: { renk: string; kalin: number }; alt?: { renk: string; stil: string; kalin: number }; ust?: { renk: string; stil: string };
  shd?: string; tab?: { pos: number; al: 'left' | 'right'; lider?: 'underscore' | 'none' }[]; vurgulu?: boolean;
}
function pPr(o: ParaO): string {
  const bd = [
    o.ust ? `<w:top w:val="${o.ust.stil}" w:sz="4" w:space="2" w:color="${hex(o.ust.renk)}"/>` : '',
    o.sol ? `<w:left w:val="single" w:sz="${o.sol.kalin}" w:space="6" w:color="${hex(o.sol.renk)}"/>` : '',
    o.alt ? `<w:bottom w:val="${o.alt.stil}" w:sz="${o.alt.kalin}" w:space="2" w:color="${hex(o.alt.renk)}"/>` : '',
  ].join('');
  const sp = o.tamH != null
    ? `<w:spacing w:before="0" w:after="0" w:line="${Math.max(20, tw(o.tamH))}" w:lineRule="exact"/>`
    : `<w:spacing w:before="${Math.round((o.before || 0) * 20)}" w:after="${Math.round((o.after || 0) * 20)}" w:line="${satirTw(o.satir || 1)}" w:lineRule="auto"/>`;
  return `<w:pPr>${o.keep ? '<w:keepNext/><w:keepLines/>' : '<w:keepLines/>'}${bd ? `<w:pBdr>${bd}</w:pBdr>` : ''}${o.shd ? `<w:shd w:val="clear" w:color="auto" w:fill="${o.shd}"/>` : ''}${o.tab ? `<w:tabs>${o.tab.map((t) => `<w:tab w:val="${t.al}" w:pos="${t.pos}"${t.lider && t.lider !== 'none' ? ` w:leader="${t.lider}"` : ''}/>`).join('')}</w:tabs>` : ''}${sp}${o.ind ? `<w:ind w:left="${o.ind[0]}" w:hanging="${o.ind[1]}"/>` : ''}${o.jc ? `<w:jc w:val="${o.jc}"/>` : ''}</w:pPr>`;
}
const para = (icerik: string, o: ParaO = {}) => `<w:p>${pPr(o)}${icerik}</w:p>`;
/** Sayfa/bölüm sonu için neredeyse yüksekliksiz paragraf */
const MINIK = '<w:pPr><w:spacing w:before="0" w:after="0" w:line="20" w:lineRule="exact"/><w:rPr><w:sz w:val="2"/></w:rPr></w:pPr>';
const SAYFA_SONU = `<w:p>${MINIK}<w:r><w:rPr><w:sz w:val="2"/></w:rPr><w:br w:type="page"/></w:r></w:p>`;
const BOS_P = `<w:p>${MINIK}</w:p>`;
const PAYLIK = 4; // mm: sayfa sonu paragrafı + yazı işlemcilerin satır yuvarlaması için ayrılan pay
/** Sabit sayfa kipinde yazı işlemcinin (Word/LibreOffice) satır kırma ölçüsü tarayıcıdan biraz geniştir; sınırına dek
 *  doldurulmuş hücre, sabit yükseklikli satırı sonraki sayfaya iter (her sayfa ikiye bölünür). Ölçek ve satır payı bunu önler. */
const OFIS_K = 0.93;
const SATIR_PAY = 0.97;

const stilAd = (s: string) => (s === 'solid' ? 'single' : s === 'dashed' ? 'dashed' : s === 'dotted' ? 'dotted' : s === 'double' ? 'double' : 'single');
const tabloKenarYok = '<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>';
const hucreKenar = (renk = 'CBD5E1', sz = 6) => `<w:tcBorders><w:top w:val="single" w:sz="${sz}" w:color="${renk}"/><w:left w:val="single" w:sz="${sz}" w:color="${renk}"/><w:bottom w:val="single" w:sz="${sz}" w:color="${renk}"/><w:right w:val="single" w:sz="${sz}" w:color="${renk}"/></w:tcBorders>`;
/** mar: dört kenar iç boşluğu; yan: yalnız sol/sağ (sabit yükseklikli satırda LibreOffice üst/alt boşluğu satır yüksekliğine ekler) */
const tc = (w: number, icerik: string, o: { kenar?: boolean; mar?: number; yan?: number; vAlign?: string; shd?: string } = {}) =>
  `<w:tc><w:tcPr><w:tcW w:w="${w}" w:type="dxa"/>${o.kenar ? hucreKenar() : ''}${o.shd ? `<w:shd w:val="clear" w:color="auto" w:fill="${o.shd}"/>` : ''}${o.mar != null || o.yan != null ? `<w:tcMar><w:top w:w="${o.mar ?? 0}" w:type="dxa"/><w:left w:w="${o.mar ?? o.yan}" w:type="dxa"/><w:bottom w:w="${o.mar ?? 0}" w:type="dxa"/><w:right w:w="${o.mar ?? o.yan}" w:type="dxa"/></w:tcMar>` : ''}${o.vAlign ? `<w:vAlign w:val="${o.vAlign}"/>` : ''}</w:tcPr>${icerik || BOS_P}</w:tc>`;
const tablo = (gen: number[], satirlar: string[], o: { ind?: number } = {}) =>
  `<w:tbl><w:tblPr><w:tblW w:w="${gen.reduce((x, y) => x + y, 0)}" w:type="dxa"/>${o.ind ? `<w:tblInd w:w="${o.ind}" w:type="dxa"/>` : ''}${tabloKenarYok}<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar><w:tblLook w:val="0000"/></w:tblPr><w:tblGrid>${gen.map((g) => `<w:gridCol w:w="${g}"/>`).join('')}</w:tblGrid>${satirlar.join('')}</w:tbl>`;
const tr = (hucreler: string, h?: number, kesin = true) =>
  `<w:tr><w:trPr><w:cantSplit/>${h != null ? `<w:trHeight w:val="${tw(h)}" w:hRule="${kesin ? 'exact' : 'atLeast'}"/>` : ''}</w:trPr>${hucreler}</w:tr>`;

/* ---------------------------------------------------------------------------
 * Bloklar
 * ------------------------------------------------------------------------- */
function blokOrtak(h: HS, a: Ayar): Partial<ParaO> {
  if (!h.renk) return {};
  if (a.renkStil === 'serit') return { sol: { renk: h.renk, kalin: 24 } };
  if (a.renkStil === 'zemin') return { shd: karis(h.renk, 0.09) };
  return {};
}

/** Etiketler: hap/kutu/köşe → zemin dolgusu; çizgi → yalnız kenarlık; düz → ayraçlı metin. Renk `belge.ts::etiketler` ile ortak */
function etiketRuns(h: HS, a: Ayar, fs: number): string {
  const efs = fs * a.etiketBoyut;
  const ozel = a.etiketRenk === 'ozel';
  return etiketler(h, a).map((e, i) => {
    const metin = ozel && !e.renkli ? a.etiketMetin : karis(e.renk, 0.8, '000000');
    const zemin = ozel && !e.renkli ? hex(a.etiketZemin) : karis(e.renk, 0.14);
    const ayrac = i ? (a.etiketSekil === 'duz' ? run(' · ', { fs: efs, renk: '9CA3AF' }) : run('  ', { fs: efs })) : '';
    if (a.etiketSekil === 'duz') return ayrac + run(e.ad, { fs: efs, b: a.etiketKalin, renk: metin });
    if (a.etiketSekil === 'cizgi') return ayrac + run(` ${e.ad} `, { fs: efs, b: a.etiketKalin, renk: metin, bdr: ozel && !e.renkli ? a.etiketMetin : karis(e.renk, 0.55) });
    return ayrac + run(` ${e.ad} `, { fs: efs, b: a.etiketKalin, renk: metin, shd: zemin });
  }).join('');
}

function cozumParas(h: HS, a: Ayar, k: number, w: number, kutu: boolean, baslikNo: boolean): string[] {
  const c = cozumIcerik(h, a);
  if (baslikNo && !c.harf) c.harf = h.dogru || '—';
  const fs = a.punto * k * (kutu ? 0.9 : 1);
  const ortak: ParaO = kutu ? { sol: { renk: a.vurgu, kalin: 18 }, shd: karis(a.vurgu, 0.07) } : blokOrtak(h, a);
  const sat = a.satir;
  const out: string[] = [];
  if (baslikNo) out.push(para(run(numaraMetni(h.no, a) + '  ', { fs, b: true, renk: a.vurgu }) + (c.harf ? run(`Cevap: ${c.harf}`, { fs, b: true, renk: a.vurgu }) : ''), { ...ortak, keep: true, satir: sat, after: 1.5 * k }));
  else if (c.harf) out.push(para(run(`Cevap: ${c.harf}`, { fs, b: true, renk: a.vurgu }), { ...ortak, keep: true, satir: sat, after: 1.5 * k }));
  if (c.aciklama) out.push(para(zengin(c.aciklama, { fs }), { ...ortak, keep: true, satir: sat, after: 1.5 * k, jc: a.iki ? 'both' : undefined }));
  const ind = Math.min(tw(9), Math.round(w * 0.12));
  for (const x of c.siklar) out.push(para(run(harfMetni(x.k, a), { fs, b: true, renk: x.dogru ? a.vurgu : undefined }) + '<w:r><w:tab/></w:r>' + zengin(x.t, { fs, renk: x.dogru ? a.vurgu : undefined }), { ...ortak, keep: true, satir: sat, after: 1 * k, ind: [ind, ind], tab: [{ pos: ind, al: 'left' }] }));
  if (c.kaynak) out.push(para(run(c.kaynak, { fs: fs * 0.88, renk: '6B7280' }), { ...ortak, keep: true, satir: sat }));
  return out;
}

/** Soru bloğu → paragraf/tablo listesi. w: kullanılabilir genişlik (twip) */
function soruParas(h: HS, a: Ayar, k: number, w: number, o: { ayirici?: boolean; hucrede?: boolean } = {}): string[] {
  const fs = a.punto * k;
  const sat = a.satir;
  const ortak = blokOrtak(h, a);
  const par = a.paragraf * k;
  const out: string[] = [];
  const et = etiketRuns(h, a, fs);
  if (et && a.etiketYeri === 'ust') out.push(para(et, { ...ortak, keep: true, satir: sat, after: par }));
  const numara = numaraMetni(h.no, a);
  const noRun = h.renk && a.renkStil === 'numara'
    ? run(` ${numara} `, { fs, b: true, renk: 'FFFFFF', shd: hex(h.renk) }) + run(' ', { fs })
    : run(numara + ' ', { fs, b: true, renk: a.vurgu });
  out.push(para(noRun + zengin(h.q.stem, { fs, b: a.kokKalin }), { ...ortak, keep: true, satir: sat, after: par, jc: a.iki ? 'both' : undefined }));
  const isaretli = (key: string) => a.dogruIsaret && key === h.dogru;
  const sikRuns = (x: { key: string; text: string }) => {
    const dg = isaretli(x.key);
    const harf = dg && a.isaretStil === 'daire' && DAIRE[x.key] ? DAIRE[x.key] : harfMetni(x.key, a);
    const ro: RunO = { fs, b: dg, renk: dg && (a.isaretStil === 'kalin' || a.isaretStil === 'daire') ? a.vurgu : undefined, shd: dg && a.isaretStil === 'zemin' ? karis(a.vurgu, 0.16) : undefined };
    return { harf: run(harf, { fs, b: true, renk: dg && a.isaretStil === 'daire' ? a.vurgu : undefined }), metin: zengin(x.text, ro) + (dg && a.isaretStil === 'tik' ? run(' ✓', { fs, b: true, renk: a.vurgu }) : '') };
  };
  const araSik = a.paragraf * 0.6 * k;
  if (a.secenekDuzen === 'yan') {
    out.push(para(h.secenek.map((x, i) => { const r = sikRuns(x); return (i ? run('     ', { fs }) : '') + r.harf + run(' ', { fs }) + r.metin; }).join(''), { ...ortak, keep: true, satir: sat, after: 0 }));
  } else if (a.secenekDuzen === 'iki') {
    const yarim = Math.floor(w / 2);
    const ind = Math.min(tw(7), Math.round(yarim * 0.18));
    const satirlar: string[] = [];
    for (let i = 0; i < h.secenek.length; i += 2) {
      const hc = [h.secenek[i], h.secenek[i + 1]].map((x) => {
        if (!x) return tc(yarim, '');
        const r = sikRuns(x);
        return tc(yarim, para(r.harf + '<w:r><w:tab/></w:r>' + r.metin, { satir: sat, after: araSik, ind: [ind, ind], tab: [{ pos: ind, al: 'left' }] }));
      });
      satirlar.push(tr(hc.join('')));
    }
    out.push(tablo([yarim, w - yarim], satirlar));
    out.push(para('', { ...ortak, tamH: 0.6 }));
  } else {
    const ind = Math.min(tw(7), Math.round(w * 0.1));
    h.secenek.forEach((x, i) => {
      const r = sikRuns(x);
      out.push(para(r.harf + '<w:r><w:tab/></w:r>' + r.metin, { ...ortak, keep: i < h.secenek.length - 1, satir: sat, after: araSik, ind: [ind, ind], tab: [{ pos: ind, al: 'left' }] }));
    });
  }
  if (et && a.etiketYeri === 'alt') out.push(para(et, { ...ortak, keep: true, satir: sat, before: par }));
  for (let i = 0; i < a.yazmaSatiri; i++) out.push(para('', { ...ortak, tamH: a.punto * a.satir * 1.35 * 0.3528 * k, alt: { renk: 'C7CBD1', stil: 'single', kalin: 4 } }));
  if (a.cozumYeri === 'altinda') {
    const c = cozumIcerik(h, a);
    if (!cozumBos(c)) out.push(...cozumParas(h, a, k, w, true, false));
  }
  // son paragraf: soru arası boşluk + ayraç
  const son = out.length - 1;
  const ayir = (o.ayirici ?? true) && a.ayirici !== 'yok';
  out[son] = out[son].replace(/<w:keepNext\/>/, '').replace(/<w:spacing w:before="(\d+)" w:after="\d+"/, `<w:spacing w:before="$1" w:after="${Math.round(a.soruArasi * k * 56.69)}"`);
  if (ayir) out.push(para('', { tamH: 0.8, alt: { renk: '9CA3AF', stil: stilAd(a.ayirici), kalin: a.ayirici === 'double' ? 6 : 4 } }), para('', { tamH: a.soruArasi * 0.5 * k }));
  return out;
}

/** Katman başlığı: seviyeye göre küçülen punto ve girinti; biçim (çizgi/bant/kutu/sade) paragraf kenarlığı ve zeminle */
const GRUP_OLCEK = [1.28, 1.12, 1.0, 0.92];
function grupPara(b: { ad: string; renk: string | null; seviye?: number; sayi?: number; k?: number }, a: Ayar): string {
  const sv = Math.min(3, b.seviye ?? 0);
  const fs = a.punto * GRUP_OLCEK[sv] * (b.k ?? 1);
  const renk = b.renk || a.vurgu;
  const o: ParaO = { keep: true, satir: 1.15, after: a.soruArasi * 1.4 * (b.k ?? 1), before: sv ? 1 : 2, ind: sv ? [tw(sv * 1.5), 0] : undefined };
  if (a.grupStil === 'cizgi') o.alt = { renk: karis(renk, 0.55), stil: 'single', kalin: sv >= 2 ? 4 : 6 };
  else if (a.grupStil === 'bant') { o.sol = { renk, kalin: 24 }; o.shd = karis(renk, sv >= 2 ? 0.05 : 0.1); }
  else if (a.grupStil === 'kutu') { o.alt = { renk: karis(renk, 0.55), stil: 'single', kalin: 4 }; o.ust = { renk: karis(renk, 0.55), stil: 'single' }; }
  const sayi = a.grupSayi && b.sayi != null ? run(`  ${b.sayi} soru`, { fs: fs * 0.78, b: true, renk: '6B7280' }) : '';
  return para(run(b.ad, { fs, b: true, renk }) + sayi, o);
}

function blokParas(b: Blok, a: Ayar, w: number, o: { hucrede?: boolean } = {}): string[] {
  if (b.t === 'grup') return [grupPara(b, a)];
  if (b.t === 'soru') return [...(b.basliklar || []).map((g) => grupPara({ ...g, k: b.k * 0.86 }, a)), ...soruParas(b.h, a, b.k, w, { ayirici: !o.hucrede, hucrede: o.hucrede })];
  return cozumParas(b.h, a, b.k, w, false, true).map((p, i, arr) => (i === arr.length - 1 ? p.replace(/<w:keepNext\/>/, '').replace(/w:after="\d+"/, `w:after="${Math.round(a.soruArasi * b.k * 56.69)}"`) : p));
}

/* ---------------------------------------------------------------------------
 * Sayfa parçaları
 * ------------------------------------------------------------------------- */
function baslikTablo(a: Ayar, w: number): string {
  const fs = Math.min(16, a.punto * 1.45);
  const sag = Math.round(w * 0.42);
  const sol = para(run(a.baslik, { fs, b: true, renk: a.vurgu }), { satir: 1.1, after: 1 }) + (a.altBaslik ? para(run(a.altBaslik, { fs: Math.max(7, a.punto * 0.8), renk: '4B5563' }), { satir: 1.1 }) : '');
  const alan = (ad: string) => para(run(ad + ' ', { fs: Math.max(7, a.punto * 0.78), renk: '374151' }) + '<w:r><w:tab/></w:r>', { satir: 1.2, after: 2, tab: [{ pos: sag - 60, al: 'right', lider: 'underscore' }] });
  const sagIc = (a.adSoyad ? alan('Ad Soyad:') : '') + (a.tarih ? alan('Tarih:') : '');
  const kenar = `<w:tcBorders><w:bottom w:val="single" w:sz="9" w:color="${hex(a.vurgu)}"/></w:tcBorders>`;
  const hucre = (gen: number, ic: string) => `<w:tc><w:tcPr><w:tcW w:w="${gen}" w:type="dxa"/>${kenar}<w:vAlign w:val="bottom"/></w:tcPr>${ic || BOS_P}</w:tc>`;
  return tablo([w - sag, sag], [tr(hucre(w - sag, sol) + hucre(sag, sagIc), BASLIK_MM - 0.4)]);
}

const bantPara = (ad: string, renk: string | null, a: Ayar) =>
  para(run('■ ', { fs: Math.max(8, a.punto * 1.05), renk: renk || a.vurgu }) + run(ad, { fs: Math.max(8, a.punto * 1.05), b: true, renk: a.vurgu }), { tamH: GRUP_MM, alt: { renk: 'D1D5DB', stil: 'single', kalin: 4 } });

const seritPara = (p: Sayfa, a: Ayar) =>
  para(run('Cevaplar · ', { fs: Math.max(6.5, a.punto * 0.72), b: true, renk: a.vurgu }) + run((p.serit || []).map((x) => `${x.no}-${x.harf}`).join('   '), { fs: Math.max(6.5, a.punto * 0.72), renk: '374151' }), { tamH: SERIT_MM, ust: { renk: '9CA3AF', stil: 'dashed' } });

/** Sayfa kipinde tek sayfa: (başlık) (bant) gövde tablosu (şerit) */
function sabitSayfa(p: Sayfa, a: Ayar): string {
  const W = tw(p.g.w);
  const parca: string[] = [];
  if (p.g.baslik) parca.push(baslikTablo(a, W));
  if (p.bant) parca.push(bantPara(p.bant.ad, p.bant.renk, a));
  const govdeH = p.g.h - PAYLIK;
  if (p.izgara && p.hucre) {
    const { sut, sat, cw } = p.izgara;
    const ch = ((govdeH - (sat - 1) * a.hucreAralik) / sat) * SATIR_PAY;
    const gen: number[] = [];
    for (let c = 0; c < sut; c++) { if (c) gen.push(tw(a.hucreAralik)); gen.push(tw(cw)); }
    const icW = tw(a.hucreCerceve ? cw - 6 : cw);
    const satirlar: string[] = [];
    for (let r = 0; r < sat; r++) {
      if (r) satirlar.push(tr(gen.map((g) => tc(g, '')).join(''), a.hucreAralik));
      const hc: string[] = [];
      for (let c = 0; c < sut; c++) {
        if (c) hc.push(tc(gen[c * 2 - 1], ''));
        const b = p.hucre[r * sut + c];
        const ust = a.hucreCerceve ? para('', { tamH: 3 }) : '';
        hc.push(tc(tw(cw), b ? ust + blokParas(b.t === 'grup' ? b : { ...b, k: b.k * OFIS_K }, a, icW, { hucrede: true }).join('') : '', { kenar: a.hucreCerceve, yan: a.hucreCerceve ? tw(3) : 0 }));
      }
      satirlar.push(tr(hc.join(''), ch));
    }
    parca.push(tablo(gen, satirlar));
  } else if (p.kolon) {
    const kw = p.kolonW!;
    const gen: number[] = [];
    p.kolon.forEach((_, i) => { if (i) gen.push(tw(KOLON_ARA)); gen.push(tw(kw)); });
    const hc = p.kolon.map((c, i) => (i ? tc(gen[i * 2 - 1], '') : '') + tc(tw(kw), c.flatMap((b) => blokParas(b.t === 'grup' ? b : { ...b, k: b.k * OFIS_K }, a, tw(kw))).join(''))).join('');
    parca.push(tablo(gen, [tr(hc, govdeH * SATIR_PAY)]));
  }
  if (p.serit) parca.push(seritPara(p, a));
  return parca.join('');
}

function kapakXml(b: Belge, a: Ayar, w: number): string {
  const dersler = [...new Set(b.hs.map((h) => h.q.ders))];
  const kaynaklar = [...new Set(b.hs.map((h) => kaynakAdi(h.q.kaynak)))];
  const alan = (ad: string) => para(run(ad + ' ', { fs: 10 }) + '<w:r><w:tab/></w:r>', { after: 10, tab: [{ pos: Math.round(w * 0.7), al: 'left', lider: 'underscore' }] });
  return [
    para(run(kaynaklar.join(' · ').toLocaleUpperCase('tr'), { fs: 9, b: true, renk: a.vurgu }), { after: 14 }),
    para(run(a.baslik || 'Soru kitapçığı', { fs: 30, b: true }), { after: 8, satir: 1.05 }),
    a.altBaslik ? para(run(a.altBaslik, { fs: 13, renk: '4B5563' }), { after: 16 }) : '',
    para(run(`${b.hs.length}`, { fs: 17, b: true, renk: a.vurgu }) + run(' soru     ', { fs: 9, renk: '6B7280' }) + run(`${dersler.length}`, { fs: 17, b: true, renk: a.vurgu }) + run(' ders', { fs: 9, renk: '6B7280' }), { after: 12 }),
    dersler.length ? para(run(dersler.slice(0, 14).join(' · ') + (dersler.length > 14 ? ' …' : ''), { fs: 9.5, renk: '374151' }), { after: 16 }) : '',
    para(run(`Her sorunun yalnız bir doğru cevabı vardır.${a.optik ? ' Cevaplarını sondaki cevap kâğıdına işaretle.' : ''}${a.cevapAnahtari ? ' Cevap anahtarı belgenin sonundadır.' : ''}`, { fs: 9, renk: '374151' }), { sol: { renk: a.vurgu, kalin: 24 }, shd: 'F8FAFC', after: 18, satir: 1.5 }),
    a.adSoyad ? alan('Ad Soyad') + alan('Numara') : '',
    a.tarih ? alan('Tarih') : '',
    para(run(new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) + (a.altMetin ? ` · ${a.altMetin}` : ''), { fs: 8.5, renk: '9CA3AF' }), { before: 12 }),
  ].join('');
}

function anahtarXml(sayfalar: Sayfa[], a: Ayar, w: number): string {
  const liste = sayfalar.flatMap((p) => p.anahtar || []);
  const sut = Math.max(1, Math.min(10, sayfalar[0]?.anahtarSut || 8));
  const g = Math.floor(w / sut);
  const satirlar: string[] = [];
  for (let i = 0; i < liste.length; i += sut) {
    satirlar.push(tr(Array.from({ length: sut }, (_, j) => {
      const x = liste[i + j];
      return tc(g, x ? para(run(String(x.no), { fs: Math.max(8, a.punto * 0.92), b: true }) + '<w:r><w:tab/></w:r>' + run(x.harf, { fs: Math.max(8, a.punto * 0.92), b: true, renk: a.vurgu }), { satir: 1, tab: [{ pos: g - 160, al: 'right' }] }) : '', { kenar: !!x, mar: 50, shd: x?.renk ? karis(x.renk, 0.1) : undefined });
    }).join(''), 6.4, false));
  }
  return bantPara('Cevap anahtarı', null, a) + para('', { tamH: 2 }) + tablo(Array(sut).fill(g), satirlar);
}

function optikXml(sayfalar: Sayfa[], a: Ayar, w: number): string {
  const nolar = sayfalar.flatMap((p) => p.optik || []);
  const sut = Math.max(1, Math.min(5, sayfalar[0]?.optikSut || 4));
  const sat = Math.ceil(nolar.length / sut);
  const g = Math.floor(w / sut);
  const satirlar: string[] = [];
  for (let r = 0; r < sat; r++) {
    satirlar.push(tr(Array.from({ length: sut }, (_, c) => {
      const n = nolar[c * sat + r];
      return tc(g, n != null ? para(run(String(n).padStart(3, ' '), { fs: 8, b: true }) + run('   Ⓐ  Ⓑ  Ⓒ  Ⓓ  Ⓔ', { fs: 10.5, renk: '6B7280' }), { satir: 1 }) : '');
    }).join(''), 6.2));
  }
  return bantPara('Cevap kâğıdı', null, a) + para('', { tamH: 2 }) + tablo(Array(sut).fill(g), satirlar);
}

/* ---------------------------------------------------------------------------
 * Bölümler ve paket
 * ------------------------------------------------------------------------- */
interface Bolum { icerik: string; sutun: number; kapak?: boolean; ustBilgi?: boolean; /** önceki bölümle aynı sayfada başlar */ devam?: boolean }

export async function docxUret(belge: Belge, a: Ayar): Promise<Blob> {
  SATIR_F = TEK_SATIR[YAZI[a.yazi].ofis] || 1.15;
  const { w: PW, h: PH } = sayfaOlcu(a);
  const ic = a.cerceve ? a.cerceveIc + a.cerceveKalin * 0.35 : 0;
  const altVar = a.sayfaNo || !!a.altMetin.trim();
  const genis = tw(belge.sayfalar.find((p) => p.tur !== 'kapak')?.g.w || PW - a.kenar[1] - a.kenar[3]);
  const sayfaKipi = a.duzen !== 'akis' || a.cozumYeri === 'arkada' || a.cozumYeri === 'sayfaAlti';
  const bolumler: Bolum[] = [];
  const ss = belge.sayfalar;
  let i = 0;
  while (i < ss.length) {
    const p = ss[i];
    if (p.tur === 'kapak') { bolumler.push({ icerik: kapakXml(belge, a, genis), sutun: 1, kapak: true }); i++; continue; }
    if ((p.tur === 'soru' || (p.tur === 'cozum' && a.cozumYeri === 'arkada')) && sayfaKipi) {
      const parca: string[] = [];
      while (i < ss.length && (ss[i].tur === 'soru' || (ss[i].tur === 'cozum' && a.cozumYeri === 'arkada'))) {
        if (parca.length) parca.push(SAYFA_SONU);
        parca.push(sabitSayfa(ss[i], a));
        i++;
      }
      bolumler.push({ icerik: parca.join(''), sutun: 1, ustBilgi: false });
      continue;
    }
    if (p.tur === 'soru' || p.tur === 'cozum') {
      const tur = p.tur;
      const bloklar: Blok[] = [];
      const ilk = p;
      while (i < ss.length && ss[i].tur === tur) { bloklar.push(...(ss[i].kolon || []).flat()); i++; }
      const kw = tw(ilk.kolonW || ilk.g.w);
      const bas = (ilk.g.baslik && !a.baslikHerSayfa ? baslikTablo(a, genis) : '') + (tur === 'cozum' ? grupPara({ ad: 'Çözümler', renk: null }, a) : '');
      // Akışta ölçek yalnız sütunu aşan blokta küçülür; Word bloğu kendisi böler, ölçeği yumuşat
      const govde = bloklar.flatMap((b) => blokParas(b.t === 'grup' ? b : { ...b, k: Math.max(b.k, (MIN_K + 0.2) * Math.min(1, belge.olcek)) }, a, kw)).join('');
      // başlık tek sütunda, sorular çok sütunda: başlık ayrı bölüm
      if (bas && a.sutun > 1) {
        bolumler.push({ icerik: bas, sutun: 1, ustBilgi: a.baslikHerSayfa });
        bolumler.push({ icerik: govde, sutun: a.sutun, ustBilgi: a.baslikHerSayfa, devam: true });
      } else bolumler.push({ icerik: bas + govde, sutun: a.sutun, ustBilgi: a.baslikHerSayfa });
      continue;
    }
    if (p.tur === 'anahtar') {
      const l: Sayfa[] = [];
      while (i < ss.length && ss[i].tur === 'anahtar') l.push(ss[i++]);
      bolumler.push({ icerik: anahtarXml(l, a, genis), sutun: 1, ustBilgi: a.baslikHerSayfa });
      continue;
    }
    if (p.tur === 'optik') {
      const l: Sayfa[] = [];
      while (i < ss.length && ss[i].tur === 'optik') l.push(ss[i++]);
      bolumler.push({ icerik: optikXml(l, a, genis), sutun: 1, ustBilgi: a.baslikHerSayfa });
      continue;
    }
    i++;
  }

  const kenarlik = a.cerceve
    ? `<w:pgBorders w:offsetFrom="text">${['top', 'left', 'bottom', 'right'].map((y) => `<w:${y} w:val="${stilAd(a.cerceveStil)}" w:sz="${Math.min(96, Math.max(2, Math.round(a.cerceveKalin * 8)))}" w:space="${Math.min(31, Math.round(a.cerceveIc * 2.835))}" w:color="${hex(a.cerceveRenk)}"/>`).join('')}</w:pgBorders>`
    : '';
  const sectPr = (b: Bolum, ilkSayfaNo: boolean, devam: boolean) => {
    const ust = b.ustBilgi && !b.kapak;
    const top = a.kenar[0] + ic + (ust ? BASLIK_MM : 0);
    const bottom = a.kenar[2] + ic + (altVar && !b.kapak ? ALT_MM : 0);
    return `<w:sectPr>${ust ? '<w:headerReference w:type="default" r:id="rIdBas"/>' : ''}${!b.kapak && altVar ? '<w:footerReference w:type="default" r:id="rIdAlt"/>' : ''}<w:type w:val="${devam ? 'continuous' : 'nextPage'}"/><w:pgSz w:w="${tw(PW)}" w:h="${tw(PH)}"${PW > PH ? ' w:orient="landscape"' : ''}/><w:pgMar w:top="${tw(top)}" w:right="${tw(a.kenar[1] + ic)}" w:bottom="${tw(bottom)}" w:left="${tw(a.kenar[3] + ic)}" w:header="${tw(a.kenar[0] + ic)}" w:footer="${tw(Math.max(2, a.kenar[2] + ic))}" w:gutter="0"/>${b.kapak ? '' : kenarlik}${ilkSayfaNo ? '<w:pgNumType w:start="1"/>' : ''}<w:cols w:num="${b.sutun}" w:space="${tw(KOLON_ARA)}"${b.sutun > 1 && a.sutunCizgi ? ' w:sep="1"' : ''}/>${b.kapak ? '<w:vAlign w:val="center"/>' : ''}</w:sectPr>`;
  };
  let govdeXml = '';
  bolumler.forEach((b, j) => {
    const ilkSayfaNo = j > 0 && bolumler[j - 1].kapak === true;
    const devam = !!b.devam;
    if (j < bolumler.length - 1) {
      govdeXml += b.icerik + `<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" w:lineRule="exact"/><w:rPr><w:sz w:val="2"/></w:rPr>${sectPr(b, ilkSayfaNo, devam)}</w:pPr></w:p>`;
    } else {
      govdeXml += b.icerik + sectPr(b, ilkSayfaNo, devam);
    }
  });

  const NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
  const font = YAZI[a.yazi].ofis;
  const docXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${NS}><w:body>${govdeXml}</w:body></w:document>`;
  const stiller = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles ${NS}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="${xml(font)}" w:hAnsi="${xml(font)}" w:cs="${xml(font)}" w:eastAsia="${xml(font)}"/><w:color w:val="${hex(a.metinRenk)}"/><w:sz w:val="${hp(a.punto)}"/><w:szCs w:val="${hp(a.punto)}"/><w:lang w:val="tr-TR"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="${satirTw(a.satir)}" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style><w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style></w:styles>`;
  const ayarlar = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings ${NS}><w:defaultTabStop w:val="709"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>`;
  const altFs = Math.max(6.5, a.punto * 0.72);
  const sagTab = tw(PW - a.kenar[1] - a.kenar[3] - ic * 2);
  const sayfaAlan = belge.sayfalar[0]?.tur === 'kapak'
    ? `<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r>${rPr({ fs: altFs, renk: '6B7280' })}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r>${rPr({ fs: altFs, renk: '6B7280' })}<w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>`
    : `<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r>${rPr({ fs: altFs, renk: '6B7280' })}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r>${rPr({ fs: altFs, renk: '6B7280' })}<w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>${run(' / ', { fs: altFs, renk: '6B7280' })}<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r>${rPr({ fs: altFs, renk: '6B7280' })}<w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r>${rPr({ fs: altFs, renk: '6B7280' })}<w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>`;
  const altXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr ${NS}>${para(run(a.altMetin, { fs: altFs, renk: '6B7280' }) + '<w:r><w:tab/></w:r>' + (a.sayfaNo ? sayfaAlan : ''), { tab: [{ pos: sagTab, al: 'right' }] })}</w:ftr>`;
  const basXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr ${NS}>${baslikTablo(a, sagTab)}</w:hdr>`;

  const zip = new JSZip();
  zip.file('[Content_Types].xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>`);
  zip.file('_rels/.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>`);
  zip.file('docProps/core.xml', coreXml(a.baslik));
  zip.file('docProps/app.xml', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>MeDSor</Application></Properties>`);
  zip.file('word/document.xml', docXml);
  zip.file('word/styles.xml', stiller);
  zip.file('word/settings.xml', ayarlar);
  zip.file('word/header1.xml', basXml);
  zip.file('word/footer1.xml', altXml);
  zip.file('word/_rels/document.xml.rels', `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStil" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdAyar" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rIdBas" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rIdAlt" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>`);
  return zip.generateAsync({ type: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', compression: 'DEFLATE' });
}

export function coreXml(baslik: string): string {
  const t = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${xml(baslik || 'Sorular')}</dc:title><dc:creator>MeDSor</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">${t}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">${t}</dcterms:modified></cp:coreProperties>`;
}
