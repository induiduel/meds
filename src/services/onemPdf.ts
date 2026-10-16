/**
 * Patoloji · Sınav için en önemliler — PDF motoru (tarayıcıda jsPDF, Türkçe karakterli Liberation fontu).
 *
 * Beş düzen:
 *  - liste   : ayrıntılı liste (puan rozeti, etiketler, seçilen ayrıntılar, sorular)
 *  - kompakt : son tekrar için sık dizilmiş hap bilgiler (1–2 sütun)
 *  - bosluk  : kalın anahtar terimler boş bırakılır, numaralı cevaplar anahtarda
 *  - soru    : soru kitapçığı (örnek + çıkmış), optik daireler, cevap anahtarı
 *  - kart    : kesilip ortadan katlanan kartlar (ön yarı başlık, arka yarı bilgi)
 * Düzen: sayfa boyu (A4 / A5 / tablet / Letter), yön, sütun, yazı boyu, satır aralığı, kenar boşluğu, sıralama.
 * Görünüm: renkli / gri / mürekkep tasarrufu (dolgusuz), kapak, sayfa numaralı ve tıklanabilir içindekiler,
 * PDF yer imleri (ders başına), üst bilgi (sayfadaki ders), "s / N" alt bilgisi, işaret kutuları, not alanı.
 * Maddeler çağıran tarafta süzülür (OnemPdfPenceresi); burada yalnız içerik ve görünüm.
 */
import { setupPdfFonts } from './drive';

export type OnemPdfMod = 'liste' | 'kompakt' | 'bosluk' | 'soru' | 'kart';

export interface OnemPdfMadde {
  id: string; puan: number; baslik: string; bilgi: string; alt?: string[]; tur: string;
  alinti: { sayfa: number; metin: string }[]; neden: string; detay: string;
  ornek_soru?: { kok: string; secenekler: Record<string, string>; dogru: string; aciklama?: string } | null;
  cikmis?: string[]; kaynak?: 'metin' | 'tablo' | 'sekil'; klinik?: boolean; sinavUygun?: boolean; kategori?: string;
  ornek26?: { kok: string; secenekler: Record<string, string>; dogru: string; aciklama?: string }[];
}
export interface OnemPdfDers {
  kod: string; no: number; baslik: string; pdf: string; ozet: string; neden_onemli: string; maddeler: OnemPdfMadde[];
  cikmis?: Record<string, { sinav: string; kok: string; secenekler: Record<string, string>; dogru: string }>;
  sinavAdaylari?: { id: string; sira: number; gerekce: string }[]; soruSayisi?: number;
}
export interface OnemPdfSecenek {
  mod: OnemPdfMod;
  /** kapakta başlığın altındaki satır (ör. "21) Glomerüler Hastalıklar" ya da "33 ders") */
  baslik: string;
  filtreOzeti: string[];
  ozet: boolean; adaylarKutusu: boolean; alt: boolean; alinti: boolean; neden: boolean; detay: boolean;
  ornekSoru: boolean; cikmis: boolean;
  anahtar: 'ders' | 'son' | 'yok';
  sayfa: 'a4' | 'a5' | 'tablet' | 'letter'; yon: 'dikey' | 'yatay'; sutun: 1 | 2;
  yazi: 'kucuk' | 'normal' | 'buyuk'; aralik: 'sik' | 'normal' | 'rahat'; kenar: 'dar' | 'normal' | 'genis';
  siralama: 'puan' | 'slayt';
  renk: 'renkli' | 'gri' | 'murekkep';
  kapak: boolean; icindekiler: boolean; yeniSayfa: boolean; numara: boolean; isaretKutusu: boolean; notAlani: boolean; optik: boolean;
}
export interface OnemPdfEk {
  /** "öğrendim" işaretli madde kimlikleri (işaret kutusu dolu çizilir) */
  ogrenilen?: Set<string>;
  ilerleme?: (oran: number) => void;
  iptal?: () => boolean;
}

export const MOD_AD: Record<OnemPdfMod, string> = {
  liste: 'Ayrıntılı liste', kompakt: 'Kompakt özet', bosluk: 'Boşluk doldurma', soru: 'Soru kitapçığı', kart: 'Kesilebilir kartlar',
};
const MOD_NOT: Record<OnemPdfMod, string> = {
  liste: 'Her madde puan rozeti, bilgi türü ve sınav etiketleriyle; seçtiğin ayrıntılar maddenin altında.',
  kompakt: 'Son tekrar için sık dizilmiş hap bilgiler: solda puan, yanında tek cümle bilgi.',
  bosluk: 'Kalın yazılan anahtar terimler boş bırakıldı. Boşlukları doldur, numaralı cevaplar anahtarda.',
  soru: 'Örnek ve çıkmış sorular. Şıkları işaretle, sonra cevap anahtarından kontrol et.',
  kart: 'Kesik çizgilerden kes, ortadaki çizgiden arkaya katla: ön yüzde başlık, kartı alttan çevirince bilgi.',
};

type RGB = [number, number, number];
const BANT_R: Record<number, RGB> = { 9: [200, 38, 45], 8: [214, 112, 10], 7: [30, 79, 216], 6: [124, 58, 237], 5: [13, 138, 128], 4: [120, 132, 146] };
const BANT_G: Record<number, RGB> = { 9: [25, 25, 25], 8: [62, 62, 62], 7: [86, 86, 86], 6: [106, 106, 106], 5: [126, 126, 126], 4: [146, 146, 146] };
const BANT_AD: Record<number, string> = { 9: '90–100', 8: '80–89', 7: '70–79', 6: '60–69', 5: '50–59', 4: '0–49' };
const BANT_NOT: Record<number, string> = { 9: 'Olmazsa olmaz', 8: 'Çok sık sorulur', 7: 'Sık sorulur', 6: 'Bilinmeli', 5: 'Destekleyici', 4: 'Ayrıntı' };
const TUR_AD: Record<string, string> = { tanim: 'TANIM', en_sik: 'EN SIK', karakteristik: 'KARAKTERİSTİK', sayi: 'SAYI', eslesme: 'EŞLEŞME', mekanizma: 'MEKANİZMA', siniflama: 'SINIFLAMA', tuzak: 'TUZAK', tani_tedavi: 'TANI' };
const INK: RGB = [14, 26, 38], INK2: RGB = [70, 84, 100], INK3: RGB = [118, 130, 144], LINE: RGB = [214, 220, 227], FIELD: RGB = [243, 245, 248], BEYAZ: RGB = [255, 255, 255];
/** önceki sözcüğe boşluksuz yapışan belirteçler (kalın sözcük sonrası noktalama) */
const YAPIS = /^[,.;:!?)\]’'”]/;
const bantOf = (p: number) => Math.max(4, Math.min(9, Math.floor(p / 10)));
const soft = (c: RGB, k = 0.12): RGB => c.map((v) => Math.round(255 - (255 - v) * k)) as RGB;
const ilkSayfa = (m: OnemPdfMadde) => Math.min(...m.alinti.map((a) => a.sayfa), 9999);
const bekle = () => new Promise<void>((r) => setTimeout(r, 0));
/** PDF yer imi metni UTF-16BE (BOM'lu) yazılır; yoksa Türkçe harfler bozulur */
const utf16 = (s: string) => {
  let r = 'þÿ';
  for (const ch of s) { const c = ch.codePointAt(0) || 32; if (c <= 0xffff) r += String.fromCharCode(c >> 8, c & 0xff); }
  return r;
};

export async function onemPdfOlustur(dersler: OnemPdfDers[], o: OnemPdfSecenek, ek: OnemPdfEk = {}): Promise<{ blob: Blob; sayfa: number }> {
  const { jsPDF } = await import('jspdf');
  const OLCU = { a4: [210, 297], a5: [148, 210], tablet: [157.5, 210], letter: [215.9, 279.4] } as const;
  const yatay = o.yon === 'yatay';
  const doc = new jsPDF({ unit: 'mm', format: [...OLCU[o.sayfa]], orientation: yatay ? 'landscape' : 'portrait', compress: true });
  const W = doc.internal.pageSize.getWidth(), H = doc.internal.pageSize.getHeight();
  const kucukSayfa = Math.min(W, H) < 160;
  const FS = ({ kucuk: 0.88, normal: 1, buyuk: 1.15 } as const)[o.yazi] * (kucukSayfa ? 0.94 : 1);
  const LHK = ({ sik: 0.385, normal: 0.425, rahat: 0.47 } as const)[o.aralik];
  const GK = ({ sik: 0.65, normal: 1, rahat: 1.35 } as const)[o.aralik];
  const M = ({ dar: 9, normal: 14, genis: 20 } as const)[o.kenar] * (kucukSayfa ? 0.8 : 1);
  const CW = W - 2 * M;
  const YH = Math.max(6, M - 3.5); // üst bilgi taban çizgisi
  const UST = YH + 5.5;
  const YF = H - Math.max(5, M - 5); // alt bilgi taban çizgisi
  const BOT = YF - 5;
  const mod = o.mod;
  const cloze = mod === 'bosluk';
  const SUT = mod === 'kart' ? 1 : o.sutun;
  const GAP = 7 * (kucukSayfa ? 0.8 : 1);
  const colW = (CW - (SUT - 1) * GAP) / SUT;

  const gri = o.renk !== 'renkli';
  const mur = o.renk === 'murekkep';
  const BN = gri ? BANT_G : BANT_R;
  const ST: RGB = gri ? [45, 45, 45] : [176, 116, 0];
  const OK: RGB = gri ? [70, 70, 70] : [21, 122, 62];
  const MAVI: RGB = gri ? [70, 70, 70] : [13, 110, 150];

  const { font: F, T: T0 } = await setupPdfFonts(doc);
  // Liberation'da olmayan üst/alt simgeler düz karşılığa çevrilir (yoksa PDF'te kaybolur)
  const SUP: Record<string, string> = { '⁺': '+', '⁻': '−', '⁰': '0', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '★': '*' };
  const T = (x: string) => T0(String(x).replace(/[⁺⁻⁰⁴-⁹₀-₄★]/g, (c) => SUP[c] || c));

  // ---------- sayfa ve sütun akışı
  let col = 0;
  let y = UST;
  let aktifDers = '';
  const sayfaDers: string[] = ['']; // sayfa başına üst bilgi etiketi (dizin = sayfa − 1)
  const ikinciSutun = new Set<number>();
  const kapakVeIcindekiler = new Set<number>();
  const sayfa = () => doc.getNumberOfPages();
  const X = () => M + col * (colW + GAP);
  const yeniSayfa = () => { doc.addPage(); col = 0; y = UST; sayfaDers.push(aktifDers); };
  const sonraki = () => {
    if (col < SUT - 1) { col++; y = UST; ikinciSutun.add(sayfa()); } else yeniSayfa();
  };
  /** sayfa+sütun kimliği: bir öğe bölündüyse "en az şu kadar yükseklik" kuralı uygulanmaz */
  const konum = () => sayfa() * 10 + col;
  const sayfaBasinda = () => col === 0 && y <= UST + 0.01;
  /** h kadar yer yoksa sonraki sütuna/sayfaya geç (sütun başındaysa geçme: sonsuz döngü olmaz) */
  const yer = (h: number) => { if (y + h > BOT && y > UST + 0.01) sonraki(); };

  const font = (b: 'normal' | 'bold' | 'italic', size: number, c: RGB = INK) => { doc.setFont(F, b); doc.setFontSize(size * FS); doc.setTextColor(...c); };
  const lhOf = (size: number) => size * FS * LHK;
  /** dolgulu kutu; mürekkep tasarrufunda dolgu yerine ince çerçeve */
  const kutu = (x: number, yy: number, w: number, h: number, r: number, fill: RGB | null, stroke?: RGB, lw = 0.3) => {
    const f = !!fill && !mur;
    const s = stroke || (mur && fill ? LINE : null);
    if (f) doc.setFillColor(...fill!);
    if (s) { doc.setDrawColor(...s); doc.setLineWidth(lw); }
    if (f || s) doc.roundedRect(x, yy, w, h, r, r, f && s ? 'FD' : f ? 'F' : 'S');
  };
  const cizgi = (x1: number, y1: number, x2: number, y2: number, c: RGB = LINE, lw = 0.2, kesik = false) => {
    doc.setDrawColor(...c); doc.setLineWidth(lw);
    if (kesik) doc.setLineDashPattern([1.1, 1.1], 0);
    doc.line(x1, y1, x2, y2);
    if (kesik) doc.setLineDashPattern([], 0);
  };
  const kisalt = (s: string, w: number) => {
    let t = T(s);
    if (doc.getTextWidth(t) <= w) return t;
    while (t.length > 1 && doc.getTextWidth(t + '…') > w) t = t.slice(0, -1);
    return t.trimEnd() + '…';
  };

  // ---------- zengin metin: **kalın**, boşluk doldurmada kalın = boşluk
  type Tok = { t: string; b: boolean; bos?: string };
  let bosNo = 0;
  let bosCevap: string[] = [];
  const toks = (s: string, bosluk: boolean): Tok[] => {
    const out: Tok[] = [];
    String(s || '').split(/(\*\*[^*]+\*\*)/g).forEach((p) => {
      const b = p.length > 4 && p.startsWith('**') && p.endsWith('**');
      const ic = b ? p.slice(2, -2) : p;
      if (b && bosluk) { out.push({ t: '', b: false, bos: ic.trim() }); return; }
      ic.split(/(\s+)/).forEach((w) => { if (w && !/^\s+$/.test(w)) out.push({ t: T(w), b }); });
    });
    return out;
  };
  /** boşluğun genişliği: cevabın yazı genişliği + numara payı (en az 14 mm) */
  const bosW = (cevap: string) => { doc.setFont(F, 'normal'); return Math.max(14, doc.getTextWidth(T(cevap)) * 1.15 + 6); };
  const tokW = (tk: Tok, it: boolean) => {
    if (tk.bos !== undefined) return bosW(tk.bos);
    doc.setFont(F, tk.b ? 'bold' : it ? 'italic' : 'normal');
    return doc.getTextWidth(tk.t);
  };
  const satirla = (s: string, width: number, size0: number, bosluk = false, it = false) => {
    doc.setFontSize(size0 * FS);
    doc.setFont(F, 'normal');
    const sp = doc.getTextWidth(' ');
    const lines: Tok[][] = []; let cur: Tok[] = []; let w = 0;
    for (const tk of toks(s, bosluk)) {
      const tw = tokW(tk, it);
      const bitisik = cur.length > 0 && YAPIS.test(tk.t);
      if (cur.length && !bitisik && w + sp + tw > width) { lines.push(cur); cur = []; w = 0; }
      w += (cur.length && !bitisik ? sp : 0) + tw; cur.push(tk);
    }
    if (cur.length) lines.push(cur);
    return lines;
  };
  const yukseklik = (s: string, width: number, size: number, bosluk = false) => satirla(s, width, size, bosluk).length * lhOf(size);
  interface ZOpt { bosluk?: boolean; it?: boolean; vurgu?: RGB }
  const zengin = (s: string, dx: number, width: number, size0: number, c: RGB, z: ZOpt = {}) => {
    const size = size0 * FS, lh = lhOf(size0);
    const lines = satirla(s, width, size0, z.bosluk, z.it);
    doc.setFontSize(size);
    doc.setFont(F, 'normal');
    const sp = doc.getTextWidth(' ');
    for (const ln of lines) {
      yer(lh + 0.4);
      let cx = X() + dx;
      const by = y + lh * 0.8;
      ln.forEach((tk, i) => {
        if (i > 0 && YAPIS.test(tk.t)) cx -= sp; // noktalama önceki sözcüğe bitişik
        if (tk.bos !== undefined) {
          const w = bosW(tk.bos);
          const no = ++bosNo;
          bosCevap.push(`**${no})** ${tk.bos}`);
          doc.setFont(F, 'bold'); doc.setFontSize(size * 0.62); doc.setTextColor(...INK3);
          doc.text(String(no), cx + 0.4, by - size * 0.12);
          cizgi(cx + 0.3, by + 0.7, cx + w - 0.3, by + 0.7, INK2, 0.25);
          doc.setFontSize(size);
          cx += w + sp;
          return;
        }
        doc.setFont(F, tk.b ? 'bold' : z.it ? 'italic' : 'normal');
        doc.setTextColor(...(tk.b && z.vurgu ? z.vurgu : c));
        doc.text(tk.t, cx, by);
        cx += doc.getTextWidth(tk.t) + sp;
      });
      y += lh;
    }
    return lines.length * lh;
  };
  const madde = (s: string, dx: number, width: number, size: number, c: RGB, z: ZOpt = {}) => {
    const lh = lhOf(size);
    yer(lh + 0.4);
    doc.setFillColor(...c); doc.circle(X() + dx + 1, y + lh * 0.52, 0.5 * FS, 'F');
    zengin(s, dx + 3.2, width - 3.2, size, c, z);
  };
  /** küçük etiket; mürekkep tasarrufunda zeminsiz */
  const etiketW = (s: string, size = 6.4) => { font('bold', size); return doc.getTextWidth(T(s)) + 3; };
  const etiket = (s: string, x: number, by: number, c: RGB, size = 6.4) => {
    const w = etiketW(s, size);
    if (!mur) { doc.setFillColor(...soft(c, 0.15)); doc.roundedRect(x, by - size * FS * 0.36, w, size * FS * 0.5, 0.8, 0.8, 'F'); }
    else { doc.setDrawColor(...soft(c, 0.5)); doc.setLineWidth(0.2); doc.roundedRect(x, by - size * FS * 0.36, w, size * FS * 0.5, 0.8, 0.8, 'S'); }
    font('bold', size, c); doc.text(T(s), x + 1.5, by);
    return w;
  };
  /** etiket dizisini satırlara böler; kaç satır tuttuğunu döndürür */
  const etiketler = (liste: [string, RGB][], dx: number, maxW: number, by0: number) => {
    let ex = dx, satir = 0;
    for (const [s, c] of liste) {
      const w = etiketW(s);
      if (ex > dx && ex + w > dx + maxW) { satir++; ex = dx; }
      ex += etiket(s, X() + ex, by0 + satir * 3.9 * FS, c) + 1.4;
    }
    return satir + 1;
  };
  const isaret = (x: number, yy: number, s: number, dolu: boolean) => {
    doc.setDrawColor(...INK3); doc.setLineWidth(0.3); doc.roundedRect(x, yy, s, s, 0.6, 0.6, 'S');
    if (dolu) { doc.setDrawColor(...OK); doc.setLineWidth(0.55); doc.line(x + s * 0.2, yy + s * 0.52, x + s * 0.42, yy + s * 0.76); doc.line(x + s * 0.42, yy + s * 0.76, x + s * 0.82, yy + s * 0.24); }
  };

  // ---------- içerik hazırlığı
  const sorulari = (d: OnemPdfDers) => {
    const out: { m: OnemPdfMadde; tur: 'ornek' | 'ornek26' | 'cikmis'; id?: string }[] = [];
    const goruldu = new Set<string>();
    for (const m of d.maddeler) {
      if (o.ornekSoru) for (let i = 0; i < (m.ornek26 || []).length; i++) out.push({ m, tur: 'ornek26', id: String(i) });
      if (o.ornekSoru && m.ornek_soru) out.push({ m, tur: 'ornek' });
      if (o.cikmis) for (const id of m.cikmis || []) {
        if (!d.cikmis?.[id] || goruldu.has(id)) continue;
        goruldu.add(id); out.push({ m, tur: 'cikmis', id });
      }
    }
    return out;
  };
  const sirala = (ms: OnemPdfMadde[]) => o.siralama === 'slayt'
    ? ms.slice().sort((a, b) => ilkSayfa(a) - ilkSayfa(b) || b.puan - a.puan)
    : ms.slice().sort((a, b) => b.puan - a.puan || ilkSayfa(a) - ilkSayfa(b));
  const liste = dersler
    .map((d) => ({ ...d, maddeler: sirala(d.maddeler) }))
    .filter((d) => (mod === 'soru' ? sorulari(d).length > 0 : d.maddeler.length > 0));
  const toplamMadde = liste.reduce((n, d) => n + d.maddeler.length, 0);
  const toplamSoru = liste.reduce((n, d) => n + sorulari(d).length, 0);
  const toplamAday = liste.reduce((n, d) => n + (d.sinavAdaylari || []).filter((a) => d.maddeler.some((m) => m.id === a.id)).length, 0);

  // ---------- kapak
  let sayfaSayisiYeri: { x: number; y: number } | null = null;
  if (o.kapak) {
    kapakVeIcindekiler.add(1);
    if (!mur) { doc.setFillColor(...BN[9]); doc.rect(0, 0, W, 4.5, 'F'); } else cizgi(0, 4.5, W, 4.5, INK, 0.6);
    y = M + 16;
    font('bold', 28, INK); doc.text(T('Patoloji'), M, y); y += 10 * FS;
    font('bold', 15, INK2); doc.text(T('Sınav için en önemliler'), M, y); y += 8 * FS;
    if (o.baslik) { zengin(o.baslik, 0, CW, 11, INK3); y += 1; }
    font('normal', 8.5, INK3);
    doc.text(T(new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) + ' · Kurul 1 Tıbbi Patoloji ders PDF\'leri'), M, y + 3); y += 9;

    // düzen kutusu
    const notH = yukseklik(MOD_NOT[mod], CW - 10, 9) + 11;
    kutu(M, y, CW, notH, 2, soft(ST, 0.1), mur ? INK3 : undefined);
    if (!mur) { doc.setFillColor(...ST); doc.rect(M, y, 1.4, notH, 'F'); }
    font('bold', 7.5, ST); doc.text(T('DÜZEN'), M + 5, y + 5);
    font('bold', 11, INK); doc.text(T(MOD_AD[mod]), M + 17, y + 5.2);
    y += 7.5; zengin(MOD_NOT[mod], 5, CW - 10, 9, INK2); y += 4 * GK;

    // sayılar
    const kutular: [string, string][] = [[String(liste.length), 'ders'], [String(toplamMadde), 'madde'], toplamSoru ? [String(toplamSoru), 'soru'] : [String(toplamAday), 'sınav adayı'], ['', 'sayfa']];
    const kw = (CW - 3 * 3) / 4;
    kutular.forEach(([v, ad], i) => {
      const x = M + i * (kw + 3);
      kutu(x, y, kw, 15, 2, FIELD, mur ? LINE : undefined);
      font('bold', 15, INK); if (v) doc.text(T(v), x + 4, y + 8.2); else sayfaSayisiYeri = { x: x + 4, y: y + 8.2 };
      font('normal', 7.8, INK3); doc.text(T(ad), x + 4, y + 12.6);
    });
    y += 21;

    // bant dağılımı
    if (mod !== 'soru' && toplamMadde) {
      font('bold', 8.5, INK); doc.text(T('Puan dağılımı'), M, y); y += 2.5;
      const say: Record<number, number> = {};
      for (const d of liste) for (const m of d.maddeler) say[bantOf(m.puan)] = (say[bantOf(m.puan)] || 0) + 1;
      let bx = M;
      for (const b of [9, 8, 7, 6, 5, 4]) {
        if (!say[b]) continue;
        const w = (CW * say[b]) / toplamMadde;
        if (!mur) { doc.setFillColor(...BN[b]); doc.rect(bx, y, Math.max(w - 0.4, 0.4), 4, 'F'); }
        else { doc.setDrawColor(...INK2); doc.setLineWidth(0.25); doc.rect(bx, y, Math.max(w - 0.4, 0.4), 4, 'S'); }
        bx += w;
      }
      y += 8;
      let lx = M;
      for (const b of [9, 8, 7, 6, 5, 4]) {
        if (!say[b]) continue;
        const s = `${BANT_AD[b]}: ${say[b]}`;
        font('normal', 7.8, INK2);
        const w = doc.getTextWidth(T(s)) + 7;
        if (lx + w > M + CW) { lx = M; y += 4.6; }
        if (!mur) { doc.setFillColor(...BN[b]); doc.roundedRect(lx, y - 2.5, 3, 3, 0.6, 0.6, 'F'); } else { doc.setDrawColor(...INK2); doc.roundedRect(lx, y - 2.5, 3, 3, 0.6, 0.6, 'S'); }
        doc.text(T(s), lx + 4.2, y);
        lx += w;
      }
      y += 7;
    }

    const blok = (bas: string, satirlar: string[]) => {
      if (!satirlar.length) return;
      font('bold', 8.5, INK); doc.text(T(bas), M, y); y += 2;
      for (const s of satirlar) madde(s, 0, CW, 8.8, INK2, { vurgu: INK });
      y += 3;
    };
    blok('Seçimler', o.filtreOzeti);
    blok('Sınav kuralı (hocanın açıklaması)', [
      'Resimlerden ve tablolardan soru sorulmayacak.',
      'Klinik bulgu sorulmayacak; **prognoz ve tedavi sorulabilir**.',
      'Her ders slaytından **1 soru**; yalnız "Genetik, Pediatrik ve Çevresel Patoloji"den **2 soru**.',
    ]);
    if (mod !== 'soru' && mod !== 'kart') {
      blok('Nasıl okunur', [
        'Sol rozet maddenin **puanıdır** (100 üzerinden); renk puan partını gösterir.',
        '**SINAV ADAYI n** etiketi o dersten çıkabilecek sorunun sıralı adayıdır; 1 = en olası soru.',
        '**TABLO / ŞEKİL / KLİNİK BULGU · SORULMAZ** maddeler bilgi içindir; **PROGNOZ / TEDAVİ** sorulabilir.',
      ]);
    }
  }

  // ---------- içindekiler için yer ayır (sayfa numaraları içerik yazıldıktan sonra doldurulur)
  for (let p = 1; o.kapak && p <= sayfa(); p++) kapakVeIcindekiler.add(p);
  const tocGerek = o.icindekiler && liste.length > 1;
  const tocLh = 6.2 * FS;
  const tocSatirSayfa = Math.max(1, Math.floor((BOT - UST - 14) / tocLh));
  let tocBas = 0;
  if (tocGerek) {
    const n = Math.ceil(liste.length / tocSatirSayfa);
    if (o.kapak) { tocBas = sayfa() + 1; for (let i = 0; i < n; i++) { doc.addPage(); sayfaDers.push(''); } }
    else { for (let i = 1; i < n; i++) { doc.addPage(); sayfaDers.push(''); } tocBas = 1; }
    for (let i = 0; i < n; i++) kapakVeIcindekiler.add(tocBas + i);
  }
  const ilkIcerikSayfasiBos = !o.kapak && !tocGerek;
  const toc: { ad: string; sayfa: number; n: number }[] = [];

  // ---------- ortak parçalar
  const genelAnahtar: string[] = [];
  let soruNo = 0;
  let maddeNo = 0;

  const dersBaslat = (d: OnemPdfDers, ilk: boolean) => {
    aktifDers = `${d.no}) ${d.baslik}`;
    if (ilk && ilkIcerikSayfasiBos) { y = UST; col = 0; }
    else if (o.yeniSayfa || ilk) { if (!sayfaBasinda() || ilk) yeniSayfa(); }
    else { if (y > UST + 0.01) y += 6 * GK; yer(34); }
    if (sayfaBasinda()) sayfaDers[sayfa() - 1] = aktifDers;
    const sz = SUT === 2 ? 11.5 : 13.5;
    const lines = satirla(`**${aktifDers}**`, colW - 9, sz);
    const lh = sz * FS * 0.46;
    const h = lines.length * lh + 6.5;
    yer(h + 14);
    if (mur) { kutu(X(), y, colW, h, 2, null, INK, 0.5); }
    else kutu(X(), y, colW, h, 2, INK);
    const y0 = y;
    lines.forEach((ln, i) => {
      font('bold', sz, mur ? INK : BEYAZ);
      doc.text(ln.map((t) => t.t).join(' '), X() + 4.5, y0 + 4.6 + lh * 0.78 + i * lh);
    });
    try { (doc as any).outline.add(null, utf16(aktifDers), { pageNumber: sayfa() }); } catch { /* yer imi yoksa geç */ }
    toc.push({ ad: aktifDers, sayfa: sayfa(), n: mod === 'soru' ? sorulari(d).length : d.maddeler.length });
    y = y0 + h + 2.2;
    const meta = [
      `Kaynak: ${d.pdf}`,
      mod === 'soru' ? `${sorulari(d).length} soru` : `${d.maddeler.length} madde`,
    ].join(' · ');
    zengin(meta, 0, colW, 7.4, INK3, { it: true });
    y += 2 * GK;
  };

  const ozetYaz = (d: OnemPdfDers) => {
    zengin(d.ozet, 0, colW, 9.3, INK2, { vurgu: INK });
    y += 1.8 * GK;
    const nm = `**Neden önemli:** ${d.neden_onemli}`;
    const nh = yukseklik(nm, colW - 7, 8.8) + 4;
    if (nh < BOT - UST - 4) { yer(nh); kutu(X(), y, colW, nh, 1.6, FIELD); }
    y += 2; zengin(nm, 3.5, colW - 7, 8.8, INK2, { vurgu: INK }); y += 2 + 2.5 * GK;
  };

  const adayKutusu = (d: OnemPdfDers) => {
    const byId = new Map(d.maddeler.map((m) => [m.id, m]));
    const ad = (d.sinavAdaylari || []).filter((a) => byId.has(a.id)).sort((a, b) => a.sira - b.sira);
    if (!ad.length) return;
    const ns = d.soruSayisi || 1;
    const tw = colW - 18;
    const kutuH = 10 + ad.reduce((s, a) => s + yukseklik(byId.get(a.id)!.bilgi, tw, 9, cloze) + yukseklik(a.gerekce, tw, 7.6) + 2.4, 0);
    const kutulu = kutuH < BOT - UST - 4;
    yer(kutulu ? kutuH : 16);
    const y0 = y;
    if (kutulu) kutu(X(), y0, colW, kutuH, 2, soft(ST, 0.08), ST, 0.45);
    y += 5.2; font('bold', 9.4, ST); doc.text(T(`SINAVDA ÇIKABİLECEK — bu slayttan ${ns} soru`), X() + 4, y); y += 2.6;
    for (const a of ad) {
      const m = byId.get(a.id)!;
      yer(8);
      const en = a.sira <= ns;
      kutu(X() + 4, y + 0.5, 8, 4.4, 1, en ? ST : soft(ST, 0.45), mur ? ST : undefined);
      font('bold', 7.4, mur ? ST : BEYAZ); doc.text(T(`${a.sira}`), X() + 8, y + 3.65, { align: 'center' });
      zengin(m.bilgi, 14, tw, 9, INK, { vurgu: BN[9], bosluk: cloze });
      zengin((en ? 'En olası soru. ' : '') + a.gerekce, 14, tw, 7.6, INK2, { it: true });
      y += 2.2;
    }
    if (kutulu) y = Math.max(y, y0 + kutuH);
    y += 3.5 * GK;
  };

  const partBaslik = (b: number, part: number, n: number) => {
    yer(15);
    const gc: RGB = b ? BN[b] : INK2;
    const ad = b ? `${BANT_AD[b]} · ${BANT_NOT[b]}` : 'Slayt sırasıyla (puan rozetli)';
    if (mod === 'kompakt') {
      y += 1.5;
      font('bold', 8.4, gc); doc.text(T(ad), X(), y + 3.2);
      font('bold', 7.6, gc); doc.text(T(`${n}`), X() + colW, y + 3.2, { align: 'right' });
      cizgi(X(), y + 4.8, X() + colW, y + 4.8, gc, 0.45);
      y += 7.5;
      return;
    }
    kutu(X(), y, colW, 7, 1.5, soft(gc, 0.14), mur ? gc : undefined);
    if (!mur) { doc.setFillColor(...gc); doc.rect(X(), y, 1.4, 7, 'F'); }
    font('bold', 7.6, gc); const pw = doc.getTextWidth(T(b ? `PART ${part}` : 'SLAYT'));
    doc.text(T(b ? `PART ${part}` : 'SLAYT'), X() + 4, y + 4.8);
    font('bold', 7.6, gc); const nw = doc.getTextWidth(T(`${n} madde`));
    doc.text(T(`${n} madde`), X() + colW - 3, y + 4.8, { align: 'right' });
    font('bold', 9.2, INK); doc.text(kisalt(ad, colW - pw - nw - 14), X() + pw + 7, y + 4.8);
    y += 7 + 3 * Math.max(GK, 0.8);
  };

  const soruYaz = (kok: string, sec: Record<string, string>, dx: number, onEk: string) => {
    soruNo++;
    const opt = o.optik;
    const harfler = Object.keys(sec);
    const optW = opt ? harfler.length * 5.6 + 2 : 0;
    const w = colW - dx - optW;
    const kokS = `**${onEk} ${soruNo}.** ${kok}`;
    yer(Math.min(yukseklik(kokS, w, 9) + 10, 40));
    const y0 = y;
    zengin(kokS, dx, w, 9, INK);
    if (opt) {
      harfler.forEach((h, i) => {
        const cx = X() + colW - optW + 2 + i * 5.6 + 2.2;
        doc.setDrawColor(...INK3); doc.setLineWidth(0.25); doc.circle(cx, y0 + 2.1, 2.1, 'S');
        font('bold', 6.2, INK3); doc.text(h, cx, y0 + 3.05, { align: 'center' });
      });
    }
    // şıklar: kısaysa iki sütun
    const ent = Object.entries(sec);
    font('normal', 8.6);
    const yarim = (colW - dx - 6) / 2;
    const kisa = ent.every(([k, v]) => doc.getTextWidth(T(`${k}) ${v}`)) < yarim - 3);
    if (kisa && ent.length > 2) {
      for (let i = 0; i < ent.length; i += 2) {
        const lh = lhOf(8.6);
        yer(lh + 0.4);
        const sat = ent.slice(i, i + 2);
        sat.forEach(([k, v], j) => {
          font('normal', 8.6, INK2);
          doc.text(T(`${k}) ${v}`), X() + dx + 4 + j * (yarim + 3), y + lh * 0.8);
        });
        y += lh;
      }
    } else {
      for (const [k, v] of ent) zengin(`${k}) ${v}`, dx + 4, colW - dx - 4, 8.6, INK2);
    }
    y += 1.4 * GK;
  };

  const anahtarYaz = (bas: string, satirlar: string[], akan: boolean) => {
    if (!satirlar.length) return;
    yer(12); y += 2.5 * GK;
    font('bold', 9.4, INK); doc.text(T(bas), X(), y + 3); y += 5.5;
    if (akan) zengin(satirlar.join('   '), 0, colW, 8.2, INK2);
    else for (const a of satirlar) zengin(a, 0, colW, 8.2, INK2, { vurgu: INK });
  };

  const notAlani = () => {
    yer(18); y += 3 * GK;
    font('bold', 8.4, INK3); doc.text(T('Notlar'), X(), y + 3); y += 6;
    for (let i = 0; i < 5; i++) { yer(7.5); y += 7.2; cizgi(X(), y, X() + colW, y, LINE, 0.25); }
    y += 2;
  };

  const adaySiraOf = (d: OnemPdfDers) => new Map((d.sinavAdaylari || []).map((a) => [a.id, a.sira]));
  const etiketListesi = (m: OnemPdfMadde, c: RGB, sira?: number): [string, RGB][] => {
    const l: [string, RGB][] = [[TUR_AD[m.tur] || m.tur.toUpperCase(), c]];
    if (sira) l.push([`SINAV ADAYI ${sira}`, ST]);
    if (m.kaynak === 'tablo') l.push(['TABLO · SORULMAZ', INK3]);
    if (m.kaynak === 'sekil') l.push(['ŞEKİL · SORULMAZ', INK3]);
    if (m.klinik) l.push(['KLİNİK BULGU · SORULMAZ', INK3]);
    if (m.kategori === 'prognoz') l.push(['PROGNOZ · SORULABİLİR', MAVI]);
    if (m.kategori === 'tedavi') l.push(['TEDAVİ · SORULABİLİR', OK]);
    if ((m.cikmis || []).length) l.push([`${m.cikmis!.length} ÇIKMIŞ`, OK]);
    return l;
  };

  /** maddenin altındaki ayrıntılar (liste / kompakt / boşluk ortak) */
  const ayrinti = (d: OnemPdfDers, m: OnemPdfMadde, dx: number, w: number, c: RGB, k: number, anahtar: string[]) => {
    if (o.alt) for (const a of m.alt || []) madde(a, dx, w, 8.6 * k, INK2, { vurgu: c, bosluk: cloze });
    if (o.neden && m.neden) { y += 0.6; zengin(`Neden önemli: ${m.neden}`, dx, w, 7.9 * k, INK3, { it: true }); }
    if (o.alinti) for (const a of m.alinti) { y += 0.4; zengin(`“${a.metin}” — s. ${a.sayfa}`, dx, w, 7.9 * k, INK3, { it: true }); }
    if (o.detay && m.detay) {
      y += 0.8;
      for (const s of String(m.detay).split('\n').map((x) => x.trim()).filter(Boolean)) {
        if (/^[-•]\s+/.test(s)) madde(s.replace(/^[-•]\s+/, ''), dx, w, 8.3 * k, INK2, { vurgu: c });
        else zengin(s, dx, w, 8.3 * k, INK2, { vurgu: c });
      }
    }
    if (o.ornekSoru) for (const q of m.ornek26 || []) {
      y += 1.2;
      soruYaz(q.kok, q.secenekler, dx, 'Soru');
      anahtar.push(`**${soruNo}) ${q.dogru}**${q.aciklama ? ' — ' + q.aciklama : ''}`);
    }
    if (o.ornekSoru && m.ornek_soru) {
      y += 1.2;
      soruYaz(m.ornek_soru.kok, m.ornek_soru.secenekler, dx, 'Soru');
      anahtar.push(`**${soruNo}) ${m.ornek_soru.dogru}**${m.ornek_soru.aciklama ? ' — ' + m.ornek_soru.aciklama : ''}`);
    }
    if (o.cikmis) for (const id of m.cikmis || []) {
      const q = d.cikmis?.[id]; if (!q) continue;
      y += 1.2;
      soruYaz(`(${q.sinav}) ${q.kok}`, q.secenekler, dx, 'Çıkmış');
      anahtar.push(`**${soruNo}) ${q.dogru}** (çıkmış · ${q.sinav})`);
    }
  };

  const maddeListe = (d: OnemPdfDers, m: OnemPdfMadde, sira: number | undefined, anahtar: string[]) => {
    maddeNo++;
    const c = BN[bantOf(m.puan)];
    const bx = 13;
    const kutuPay = o.isaretKutusu ? 6.5 : 0;
    const tw = colW - bx - kutuPay;
    const h0 = yukseklik(m.bilgi, tw, 10, cloze) + 8;
    yer(Math.min(h0, 34));
    const y0 = y, k0 = konum();
    kutu(X(), y0, 10, 7, 1.4, soft(c, 0.16), mur ? c : undefined);
    font('bold', 10, c); doc.text(T(String(m.puan)), X() + 5, y0 + 4.9, { align: 'center' });
    if (o.numara) { font('normal', 6.4, INK3); doc.text(T(`#${maddeNo}`), X() + 5, y0 + 10.2, { align: 'center' }); }
    if (o.isaretKutusu) isaret(X() + colW - 4.4, y0 + 0.4, 4.2, !!ek.ogrenilen?.has(m.id));
    const satir = etiketler(etiketListesi(m, c, sira), bx, tw, y0 + 2.3);
    y = y0 + 3.8 + (satir - 1) * 3.9 * FS;
    const sonuk = m.sinavUygun === false;
    zengin(m.bilgi, bx, tw, 10, sonuk ? INK2 : INK, { vurgu: c, bosluk: cloze });
    ayrinti(d, m, bx + 1, tw - 1, c, 1, anahtar);
    if (konum() === k0) y = Math.max(y, y0 + (o.numara ? 11 : 8));
    yer(3); y += 1.6 * GK; cizgi(X() + bx, y, X() + colW, y); y += 2.6 * GK;
  };

  const maddeKompakt = (d: OnemPdfDers, m: OnemPdfMadde, sira: number | undefined, anahtar: string[]) => {
    maddeNo++;
    const c = BN[bantOf(m.puan)];
    const gx = 8.6;
    const kutuPay = o.isaretKutusu ? 5 : 0;
    const tw = colW - gx - kutuPay;
    const lh = lhOf(9);
    yer(Math.min(yukseklik(m.bilgi, tw, 9, cloze), 18) + 1);
    const y0 = y, k0 = konum();
    font('bold', 8.6, c); doc.text(T(String(m.puan)), X(), y0 + lh * 0.8);
    if (sira) { font('bold', 5.8, ST); doc.text(T(`A${sira}`), X(), y0 + lh * 0.8 + 3); }
    else if (o.numara) { font('normal', 5.8, INK3); doc.text(T(`#${maddeNo}`), X(), y0 + lh * 0.8 + 3); }
    if (o.isaretKutusu) isaret(X() + colW - 3.3, y0 + 0.3, 3.2, !!ek.ogrenilen?.has(m.id));
    zengin(m.bilgi, gx, tw, 9, m.sinavUygun === false ? INK2 : INK, { vurgu: c, bosluk: cloze });
    ayrinti(d, m, gx + 0.4, tw - 0.4, c, 0.94, anahtar);
    if (konum() === k0) y = Math.max(y, y0 + (sira || o.numara ? 4.6 : 0));
    y += 1.7 * GK;
  };

  // kart düzeni: sütun sayısı sayfa genişliğine göre
  const kartSut = CW >= 240 ? 3 : CW >= 115 ? 2 : 1;
  const KG = 4;
  const kw = (CW - (kartSut - 1) * KG) / kartSut;
  const kartOlc = (m: OnemPdfMadde) => {
    const p = 3.2, iw = kw - 2 * p;
    const on = 7 + yukseklik(`**${m.baslik}**`, iw, 10.5);
    let arka = yukseklik(m.bilgi, iw, 8.8);
    if (o.alt) for (const a of m.alt || []) arka += yukseklik(a, iw - 3.2, 7.8);
    const yari = Math.max(on, arka, 14) + 2 * p;
    return { yari, h: 2 * yari };
  };
  const kartCiz = (d: OnemPdfDers, m: OnemPdfMadde, x: number, y0: number, yari: number, sira?: number) => {
    const c = BN[bantOf(m.puan)];
    const p = 3.2, iw = kw - 2 * p;
    doc.setDrawColor(...INK3); doc.setLineWidth(0.25); doc.setLineDashPattern([1.4, 1.2], 0);
    doc.rect(x, y0, kw, 2 * yari, 'S'); doc.setLineDashPattern([], 0);
    if (!mur) { doc.setFillColor(...c); doc.rect(x + 0.15, y0 + 0.15, kw - 0.3, 1.3, 'F'); }
    // ön yarı
    font('bold', 8.6, c); doc.text(T(String(m.puan)), x + p, y0 + p + 3.6);
    let ex = x + p + 7;
    ex += etiket(TUR_AD[m.tur] || m.tur, ex, y0 + p + 3.1, c, 5.8) + 1;
    if (sira) etiket(`ADAY ${sira}`, ex, y0 + p + 3.1, ST, 5.8);
    font('normal', 6.2, INK3); doc.text(T(`${d.no}`), x + kw - p, y0 + p + 3.3, { align: 'right' });
    const keepX = col; col = 0;
    const kx = x - M; // zengin X() + dx ile yazar; kart sütunu tek kolonlu akışta
    const yy = y; y = y0 + p + 6;
    zengin(`**${m.baslik}**`, kx + p, iw, 10.5, INK);
    // katlama çizgisi
    cizgi(x + 2, y0 + yari, x + kw - 2, y0 + yari, INK3, 0.2, true);
    font('normal', 5.4, INK3); doc.text(T('katla'), x + kw - 2, y0 + yari - 0.8, { align: 'right' });
    // arka yarı (katlayınca kartın arkası; alttan çevirince düz okunur)
    y = y0 + yari + p;
    zengin(m.bilgi, kx + p, iw, 8.8, INK, { vurgu: c });
    if (o.alt) for (const a of m.alt || []) madde(a, kx + p, iw, 7.8, INK2, { vurgu: c });
    y = yy; col = keepX;
  };

  // ---------- dersler
  for (let di = 0; di < liste.length; di++) {
    const d = liste[di];
    if (ek.iptal?.()) throw new Error('iptal');
    dersBaslat(d, di === 0);
    const sira = adaySiraOf(d);
    const anahtar: string[] = [];
    bosNo = 0; bosCevap = [];

    if (mod === 'soru') {
      for (const s of sorulari(d)) {
        if (s.tur === 'ornek26') {
          const q = s.m.ornek26![Number(s.id)];
          soruYaz(q.kok, q.secenekler, 0, 'Soru');
          anahtar.push(`**${soruNo}) ${q.dogru}** — ${q.aciklama || s.m.baslik}`);
        } else if (s.tur === 'ornek') {
          soruYaz(s.m.ornek_soru!.kok, s.m.ornek_soru!.secenekler, 0, 'Soru');
          anahtar.push(`**${soruNo}) ${s.m.ornek_soru!.dogru}** — ${s.m.ornek_soru!.aciklama || s.m.baslik}`);
        } else {
          const q = d.cikmis![s.id!];
          soruYaz(`(${q.sinav}) ${q.kok}`, q.secenekler, 0, 'Çıkmış');
          anahtar.push(`**${soruNo}) ${q.dogru}** — konu: ${s.m.baslik}`);
        }
        y += 1.2 * GK;
      }
    } else if (mod === 'kart') {
      if (o.ozet) ozetYaz(d);
      const ms = d.maddeler;
      for (let i = 0; i < ms.length; i += kartSut) {
        const sat = ms.slice(i, i + kartSut);
        const yari = Math.max(...sat.map((m) => kartOlc(m).yari));
        if (y + 2 * yari > BOT && y > UST + 0.01) yeniSayfa();
        sat.forEach((m, j) => kartCiz(d, m, M + j * (kw + KG), y, yari, sira.get(m.id)));
        y += 2 * yari + KG;
      }
    } else {
      if (o.ozet) ozetYaz(d);
      if (o.adaylarKutusu) adayKutusu(d);
      const gruplar = o.siralama === 'slayt'
        ? [{ b: 0, ms: d.maddeler }]
        : [9, 8, 7, 6, 5, 4].map((b) => ({ b, ms: d.maddeler.filter((m) => bantOf(m.puan) === b) }));
      let part = 0;
      for (const { b, ms } of gruplar) {
        if (!ms.length) continue;
        part++;
        partBaslik(b, part, ms.length);
        for (const m of ms) (mod === 'kompakt' ? maddeKompakt : maddeListe)(d, m, sira.get(m.id), anahtar);
      }
    }

    // ders sonu: anahtarlar + not alanı
    const bos = bosCevap.slice();
    if (o.anahtar === 'ders') {
      if (bos.length) anahtarYaz('Boşlukların cevapları', bos, true);
      anahtarYaz('Cevap anahtarı', anahtar, false);
    } else if (o.anahtar === 'son' && (bos.length || anahtar.length)) {
      genelAnahtar.push(`§${aktifDers}`);
      if (bos.length) genelAnahtar.push(`¶${bos.join('   ')}`);
      genelAnahtar.push(...anahtar);
    }
    if (o.notAlani && mod !== 'kart') notAlani();
    ek.ilerleme?.((di + 1) / liste.length);
    await bekle();
  }

  if (o.anahtar === 'son' && genelAnahtar.length) {
    aktifDers = 'Cevap anahtarı';
    yeniSayfa();
    try { (doc as any).outline.add(null, utf16('Cevap anahtarı'), { pageNumber: sayfa() }); } catch { /* yok */ }
    font('bold', 13, INK); doc.text(T('Cevap anahtarı'), X(), y + 4); y += 9;
    for (const a of genelAnahtar) {
      if (a.startsWith('§')) { yer(10); y += 2.5; zengin(`**${a.slice(1)}**`, 0, colW, 9.4, INK); y += 0.6; }
      else if (a.startsWith('¶')) zengin(a.slice(1), 0, colW, 8.2, INK2);
      else zengin(a, 0, colW, 8.2, INK2, { vurgu: INK });
    }
  }

  // ---------- içindekiler (sayfa numaralı, tıklanabilir)
  if (tocGerek) {
    toc.forEach((e, i) => {
      const p = tocBas + Math.floor(i / tocSatirSayfa);
      doc.setPage(p);
      const sat = i % tocSatirSayfa;
      if (sat === 0) {
        font('bold', 14, INK); doc.text(T(i === 0 ? 'İçindekiler' : 'İçindekiler (devam)'), M, UST + 5);
        cizgi(M, UST + 8, M + CW, UST + 8, LINE, 0.3);
      }
      const yy = UST + 14 + sat * tocLh;
      font('bold', 9.6, INK);
      const no = String(e.sayfa);
      const nw = doc.getTextWidth(no);
      font('normal', 7.6, INK3);
      const sayi = `${e.n} ${mod === 'soru' ? 'soru' : 'madde'}`;
      const sw = doc.getTextWidth(T(sayi));
      font('normal', 9.6, INK);
      const ad = kisalt(e.ad, CW - nw - sw - 16);
      doc.text(ad, M, yy);
      const aw = doc.getTextWidth(ad);
      doc.setDrawColor(...LINE); doc.setLineWidth(0.3); doc.setLineDashPattern([0.4, 1.2], 0);
      doc.line(M + aw + 2, yy - 0.6, M + CW - nw - sw - 6, yy - 0.6); doc.setLineDashPattern([], 0);
      font('normal', 7.6, INK3); doc.text(T(sayi), M + CW - nw - 4, yy, { align: 'right' });
      font('bold', 9.6, INK); doc.text(no, M + CW, yy, { align: 'right' });
      doc.link(M, yy - tocLh * 0.7, CW, tocLh, { pageNumber: e.sayfa });
    });
    try {
      const ol = (doc as any).outline;
      ol.add(null, utf16('İçindekiler'), { pageNumber: tocBas });
      ol.root.children.unshift(ol.root.children.pop()); // yer imlerinde en başta
    } catch { /* yok */ }
  }

  // ---------- üst/alt bilgi, sütun çizgisi, kapaktaki sayfa sayısı
  const N = sayfa();
  for (let p = 1; p <= N; p++) {
    doc.setPage(p);
    const kapak = o.kapak && p === 1;
    if (!kapak) {
      font('normal', 7.2, INK3);
      const sol = `Patoloji · Sınav için en önemliler · ${MOD_AD[mod]}`;
      doc.text(kisalt(sol, CW * 0.48), M, YH);
      const sag = kapakVeIcindekiler.has(p) ? '' : sayfaDers[p - 1] || '';
      if (sag) { font('bold', 7.2, INK2); doc.text(kisalt(sag, CW * 0.48), M + CW, YH, { align: 'right' }); }
      cizgi(M, YH + 1.8, M + CW, YH + 1.8, LINE, 0.2);
    }
    font('normal', 7.2, INK3);
    doc.text(T('MeDSor · kaynak: Kurul 1 Tıbbi Patoloji ders PDF\'leri'), M, YF);
    doc.text(T(`${p} / ${N}`), M + CW, YF, { align: 'right' });
    if (ikinciSutun.has(p) && !kapakVeIcindekiler.has(p)) {
      const sx = M + colW + GAP / 2;
      cizgi(sx, UST, sx, BOT, LINE, 0.2);
    }
  }
  if (sayfaSayisiYeri) { doc.setPage(1); font('bold', 15, INK); doc.text(String(N), (sayfaSayisiYeri as { x: number; y: number }).x, (sayfaSayisiYeri as { x: number; y: number }).y); }
  return { blob: doc.output('blob'), sayfa: N };
}
