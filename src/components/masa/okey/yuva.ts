/** Istaka yuva deposu: kat × sütun görünmez ızgara; diziliş istemcide (sessionStorage, oda kodu + el no) tutulur, sunucudaki ele uzlaşır. */
export interface YuvaDurum { sutun: number; kat: number; d: (number | null)[] }

const anahtarYap = (kod: string, elNo: number) => `medsoru_masa_yuva_${kod}_${elNo}`;

export function yuvaOku(kod: string, elNo: number): YuvaDurum | null {
  try {
    const y = JSON.parse(sessionStorage.getItem(anahtarYap(kod, elNo)) || 'null');
    return y && Array.isArray(y.d) && y.sutun > 0 && y.kat > 0 && y.d.length === y.sutun * y.kat ? y : null;
  } catch { return null; }
}
export function yuvaYaz(kod: string, elNo: number, y: YuvaDurum) {
  try { sessionStorage.setItem(anahtarYap(kod, elNo), JSON.stringify(y)); } catch { /* yok */ }
}

const ilkBos = (d: (number | null)[]) => d.indexOf(null);

/** Eli ızgaraya uzlaştırır: fazlası atılır, eksiği (ipucu yuvası boşsa oraya, değilse ilk boşa) eklenir. Değişiklik yoksa aynı nesne döner. */
export function uzlas(y: YuvaDurum | null, el: number[], sutun: number, kat: number, ipucu?: number): YuvaDurum {
  let d: (number | null)[];
  let degisti = false;
  if (!y) { d = new Array(sutun * kat).fill(null); degisti = true; }
  else if (y.sutun !== sutun || y.kat !== kat) {
    d = new Array(sutun * kat).fill(null);
    const tasan: number[] = [];
    y.d.forEach((id, i) => {
      if (id === null) return;
      const r = Math.floor(i / y.sutun), c = i % y.sutun;
      if (r < kat && c < sutun) d[r * sutun + c] = id; else tasan.push(id);
    });
    for (const id of tasan) { const b = ilkBos(d); if (b >= 0) d[b] = id; }
    degisti = true;
  } else d = y.d;
  const elde = new Set(el);
  const var_ = new Set<number>();
  let kopya = degisti ? d : null;
  const yaz = () => (kopya ||= d.slice());
  d.forEach((id, i) => {
    if (id === null) return;
    if (!elde.has(id) || var_.has(id)) yaz()[i] = null; else var_.add(id);
  });
  for (const id of el) {
    if (var_.has(id)) continue;
    const k = yaz();
    const hedef = ipucu !== undefined && ipucu >= 0 && ipucu < k.length && k[ipucu] === null ? ipucu : ilkBos(k);
    if (hedef >= 0) k[hedef] = id;
    var_.add(id);
  }
  return kopya ? { sutun, kat, d: kopya } : y!;
}

/** Tek taşı yuvaya sokar: dolu yuvada komşular aynı katta en yakın boşluğa doğru kayar (önce sağa, olmazsa sola); kat doluysa ilk boşa. */
function sok(d: (number | null)[], sutun: number, hedef: number, id: number) {
  if (d[hedef] === null) { d[hedef] = id; return; }
  const bas = Math.floor(hedef / sutun) * sutun, son = bas + sutun - 1;
  let b = -1;
  for (let i = hedef + 1; i <= son; i++) if (d[i] === null) { b = i; break; }
  if (b >= 0) { for (let i = b; i > hedef; i--) d[i] = d[i - 1]; d[hedef] = id; return; }
  for (let i = hedef - 1; i >= bas; i--) if (d[i] === null) { b = i; break; }
  if (b >= 0) { for (let i = b; i < hedef; i++) d[i] = d[i + 1]; d[hedef] = id; return; }
  const bos = ilkBos(d);
  if (bos >= 0) d[bos] = id;
}

/** Taş(lar)ı hedef yuvadan başlayarak yan yana yerleştirir */
export function tasi(y: YuvaDurum, ids: number[], hedef: number): YuvaDurum {
  const d = y.d.map((id) => (id !== null && ids.includes(id) ? null : id));
  const katSon = Math.floor(hedef / y.sutun) * y.sutun + y.sutun - 1;
  const bas = Math.max(Math.floor(hedef / y.sutun) * y.sutun, Math.min(hedef, katSon - ids.length + 1));
  ids.forEach((id, k) => sok(d, y.sutun, Math.min(bas + k, katSon), id));
  return { ...y, d };
}

/** Grupları aralarında birer boş yuvayla dizer (sığmazsa bitişik); grup katlar arasında bölünmez */
export function diz(y: YuvaDurum, gruplar: number[][]): YuvaDurum {
  const dene = (bosluk: number): (number | null)[] | null => {
    const d: (number | null)[] = new Array(y.d.length).fill(null);
    let i = 0;
    for (const g of gruplar) {
      if (!g.length) continue;
      const kalan = y.sutun - (i % y.sutun);
      if (g.length <= y.sutun && g.length > kalan) i += kalan;
      if (i + g.length > d.length) return null;
      for (const id of g) d[i++] = id;
      if (i % y.sutun) i += bosluk;
    }
    return d;
  };
  const duz = () => { const d: (number | null)[] = new Array(y.d.length).fill(null); gruplar.flat().forEach((id, i) => { if (i < d.length) d[i] = id; }); return d; };
  return { ...y, d: dene(1) ?? dene(0) ?? duz() };
}

/** Bitişik (arada boş yuva olmayan, aynı kattaki) taş grupları */
export function gruplar(y: YuvaDurum): number[][] {
  const out: number[][] = [];
  let g: number[] = [];
  y.d.forEach((id, i) => {
    if (i % y.sutun === 0 && g.length) { out.push(g); g = []; }
    if (id === null) { if (g.length) { out.push(g); g = []; } } else g.push(id);
  });
  if (g.length) out.push(g);
  return out;
}
export const komsuGrup = (y: YuvaDurum, id: number): number[] => gruplar(y).find((g) => g.includes(id)) ?? [id];
export const yuvaSirasi = (y: YuvaDurum, ids: number[]): number[] => y.d.filter((id): id is number => id !== null && ids.includes(id));
