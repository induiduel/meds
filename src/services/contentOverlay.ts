/**
 * Canlı içerik katmanı (server-only).
 *
 * src/data altındaki paket verisi (sözlük, kartlar, hastalıklar, Öğren desteleri, örnek sorular) ön yüze
 * derlemede gömülür; Oracle'da da imajın içinde durur. Yönetim panelinden yapılan değişiklik oraya yazılırsa
 * hem ziyaretçiye yansımaz hem bir sonraki dağıtımda silinir. Bu yüzden panel değişiklikleri data/content
 * altına (kalıcı birim) yazılır.
 *
 * KAYIT DÜZEYİNDE FARK (2026-10-28, H-katman): katman eskiden dosyanın TAM KOPYASIYDI ve kaynağı tamamen
 * gölgeliyordu — kopya oluştuktan sonra src/data'ya eklenen kayıtlar (ör. yeni k2p desteleri) sunucuda hiç
 * görünmüyordu. Artık katman yalnız farkı tutar:
 *
 *   data/content/<rel>.fark.json   { surum:1, bicim:'dizi'|'nesne'|'tam', anahtar, kayitlar:{id:kayıt},
 *                                    silinen:[id], taban:{id: kaynaktaki kaydın sha1'i | null}, tam? }
 *   data/content/_birlesik/<rel>   kaynak + fark birleşimi (önbellek; kaynak ya da fark değişince yeniden üretilir)
 *
 * Okuyan (resolveContent) birleşik dosyanın yolunu alır: kaynakta olup farkta olmayan her kayıt görünür.
 * Yazan (writableContent) yine data/content/<rel> TAM yolunu alır (mevcut yazıcılar değişmeden çalışsın);
 * yazılan tam dosya, kilit bırakılınca birleşik tabana göre karşılaştırılıp farka çevrilir ve silinir.
 *
 * Dağıtım: deploy/oracle/content-overlay-sync.sh farkları yerel src/data'ya kayıt kayıt uygular
 * (scripts/icerik_katman.py uygula). Denetim: scripts/icerik_katman.py denetle.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { kilitliMi } from './yonetim16/atomikJson.ts';

let SRC = '';
let DIR = '';
const IDS_FILE = () => path.join(DIR, '_ids.json');
const BIRLESIK = '_birlesik';
const FARK_EK = '.fark.json';

/** Katmanı kullanan türler → src/data'ya göre dosya (örnek sorular klasördür) */
export const CONTENT_FILES: Record<string, string> = {
  glossary: 'medical_glossary.json',
  cards: 'question_cards.json',
  diseases: 'diseases.json',
  decks: 'interactive_learning_decks.json',
  ornek: 'ornek_sorular',
  summaries: 'lectureSummariesCatalog.json',
};

export function initContentOverlay(rootDir: string, dataDir: string) {
  SRC = path.join(rootDir, 'src', 'data');
  DIR = path.join(dataDir, 'content');
  // Açılışta bekleyen tam kopyaları (eski biçim ya da yarıda kalan yazım) farka çevir
  try { for (const rel of tamKopyalar()) donustur(rel); } catch (e: any) { console.warn('[katman] açılış dönüşümü:', e?.message); }
}

function relOf(file: string): string | null {
  if (!SRC) return null;
  const rel = path.relative(SRC, path.resolve(file));
  return rel && !rel.startsWith('..') && !path.isAbsolute(rel) ? rel : null;
}

type Fark = {
  surum: 1;
  bicim: 'dizi' | 'nesne' | 'tam';
  anahtar?: string;
  kayitlar: Record<string, any>;
  silinen: string[];
  taban: Record<string, string | null>;
  tam?: any;
};

const tamYol = (rel: string) => path.join(DIR, rel);
const farkYol = (rel: string) => path.join(DIR, rel + FARK_EK);
const birlesikYol = (rel: string) => path.join(DIR, BIRLESIK, rel);
const mtimeOf = (p: string) => { try { return fs.statSync(p).mtimeMs; } catch { return 0; } };
const sha = (v: unknown) => crypto.createHash('sha1').update(JSON.stringify(v)).digest('hex');
const okuJson = (p: string) => JSON.parse(fs.readFileSync(p, 'utf8'));

function atomikYaz(p: string, metin: string) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  const tmp = `${p}.${process.pid}.${Math.random().toString(36).slice(2, 8)}.tmp`;
  fs.writeFileSync(tmp, metin, 'utf8');
  fs.renameSync(tmp, p);
}

function girinti(p: string): number {
  try {
    const fd = fs.openSync(p, 'r');
    const buf = Buffer.alloc(200);
    fs.readSync(fd, buf, 0, 200, 0);
    fs.closeSync(fd);
    const m = buf.toString('utf8').match(/\n( +)\S/);
    return m ? m[1].length : 0;
  } catch { return 2; }
}

const ANAHTARLAR = ['id', 'deckId', 'key', 'slug'];
/** Dizi kayıtlarının kimlik alanı: her kayıtta var ve benzersiz olan ilk aday */
function diziAnahtari(...diziler: any[][]): string | null {
  for (const k of ANAHTARLAR) {
    let ok = true;
    for (const d of diziler) {
      const gor = new Set<string>();
      for (const x of d) {
        const v = x && typeof x === 'object' ? x[k] : undefined;
        if (v === undefined || v === null || v === '' || gor.has(String(v))) { ok = false; break; }
        gor.add(String(v));
      }
      if (!ok) break;
    }
    if (ok) return k;
  }
  return null;
}

function haritala(veri: any, f: Fark): Map<string, any> {
  if (f.bicim === 'dizi') return new Map((veri as any[]).map((x) => [String(x[f.anahtar!]), x]));
  return new Map(Object.entries(veri || {}));
}

/** Kaynağa farkı uygular (kaynakta olup farkta olmayan kayıtlar olduğu gibi kalır) */
export function farkUygula(kaynak: any, f: Fark | null): any {
  if (!f) return kaynak;
  if (f.bicim === 'tam') return f.tam;
  const sil = new Set(f.silinen || []);
  const k = f.kayitlar || {};
  if (f.bicim === 'dizi' && Array.isArray(kaynak)) {
    const a = f.anahtar!;
    const gorulen = new Set<string>();
    const out: any[] = [];
    for (const x of kaynak) {
      const id = String(x?.[a]);
      gorulen.add(id);
      if (sil.has(id)) continue;
      out.push(Object.prototype.hasOwnProperty.call(k, id) ? k[id] : x);
    }
    for (const [id, x] of Object.entries(k)) if (!gorulen.has(id)) out.push(x);
    return out;
  }
  if (f.bicim === 'nesne' && kaynak && typeof kaynak === 'object' && !Array.isArray(kaynak)) {
    const out: Record<string, any> = {};
    for (const [id, x] of Object.entries(kaynak)) {
      if (sil.has(id)) continue;
      out[id] = Object.prototype.hasOwnProperty.call(k, id) ? k[id] : x;
    }
    for (const [id, x] of Object.entries(k)) if (!(id in out) && !sil.has(id)) out[id] = x;
    return out;
  }
  return kaynak; // biçim uyuşmuyor: kaynak kazanır (fark denetimde uyarı verir)
}

function farkOku(rel: string): Fark | null {
  try { return okuJson(farkYol(rel)); } catch { return null; }
}

function eskiIds(rel: string): string[] | null {
  const entity = Object.entries(CONTENT_FILES).find(([, r]) => r === rel)?.[0];
  if (!entity) return null;
  try {
    const ids = okuJson(IDS_FILE())?.[entity];
    return ids && typeof ids === 'object' ? Object.keys(ids) : null;
  } catch { return null; }
}

/**
 * data/content/<rel> tam kopyasını farka çevirir ve siler.
 * Taban = kaynak + önceki fark (yazıcının okuduğu birleşik hâl). Tam kopya kaynaktan ESKİYSE (eski biçim katman
 * ya da kaynak sonradan güncellenmiş) kaynakta sonradan eklenen kayıtlar "silindi" sayılmaz; _ids.json'da iz
 * varsa yalnız oradaki kayıtlar fark olur.
 */
export function donustur(rel: string): boolean {
  const tam = tamYol(rel);
  if (!fs.existsSync(tam) || kilitliMi(tam)) return false;
  const src = path.join(SRC, rel);
  let yeni: any;
  try { yeni = okuJson(tam); } catch { return false; } // yazım sürüyor ya da bozuk: dokunma
  const kaynak = fs.existsSync(src) ? okuJson(src) : undefined;
  const eski = farkOku(rel);
  const bayat = !!kaynak && mtimeOf(src) > mtimeOf(tam) + 1000;

  let f: Fark;
  const diziMi = Array.isArray(yeni) && (kaynak === undefined || Array.isArray(kaynak));
  const nesneMi = !Array.isArray(yeni) && yeni && typeof yeni === 'object' && kaynak && typeof kaynak === 'object' && !Array.isArray(kaynak)
    && Object.values(yeni).every((v) => v && typeof v === 'object') && Object.values(kaynak).every((v) => v && typeof v === 'object');
  const anahtar = diziMi ? diziAnahtari(yeni, Array.isArray(kaynak) ? kaynak : []) : null;
  const uygunEski = eski && eski.bicim !== 'tam' && (eski.bicim === (diziMi ? 'dizi' : 'nesne')) && (!diziMi || eski.anahtar === anahtar);

  if (kaynak === undefined || (!anahtar && !nesneMi)) {
    f = { surum: 1, bicim: 'tam', kayitlar: {}, silinen: [], taban: {}, tam: yeni };
  } else {
    f = uygunEski
      ? { surum: 1, bicim: eski!.bicim, anahtar: eski!.anahtar, kayitlar: { ...eski!.kayitlar }, silinen: [...(eski!.silinen || [])], taban: { ...(eski!.taban || {}) } }
      : { surum: 1, bicim: diziMi ? 'dizi' : 'nesne', ...(diziMi ? { anahtar: anahtar! } : {}), kayitlar: {}, silinen: [], taban: {} };
    const tabanVeri = farkUygula(kaynak, uygunEski ? eski : null);
    const yM = haritala(yeni, f), tM = haritala(tabanVeri, f), kM = haritala(kaynak, f);
    const sil = new Set(f.silinen);
    const izli = bayat && !uygunEski ? eskiIds(rel) : null;
    for (const [id, x] of yM) {
      if (izli && !izli.includes(id)) continue;
      const tx = tM.get(id);
      if (tx !== undefined && JSON.stringify(tx) === JSON.stringify(x)) continue;
      sil.delete(id);
      const kx = kM.get(id);
      if (kx !== undefined && JSON.stringify(kx) === JSON.stringify(x)) { delete f.kayitlar[id]; delete f.taban[id]; continue; }
      f.kayitlar[id] = x;
      if (!(id in f.taban)) f.taban[id] = kx === undefined ? null : sha(kx);
    }
    if (!bayat) {
      for (const id of tM.keys()) {
        if (yM.has(id)) continue;
        delete f.kayitlar[id];
        if (kM.has(id)) { sil.add(id); if (!(id in f.taban)) f.taban[id] = sha(kM.get(id)); } else delete f.taban[id];
      }
    } else if (!izli) {
      console.warn(`[katman] ${rel}: tam kopya kaynaktan eski — silme kaydedilmedi, yalnız değişen kayıtlar alındı`);
    }
    f.silinen = [...sil];
  }

  const bos = f.bicim !== 'tam' && !Object.keys(f.kayitlar).length && !f.silinen.length;
  if (bos) fs.rmSync(farkYol(rel), { force: true });
  else atomikYaz(farkYol(rel), JSON.stringify(f, null, 1));
  fs.rmSync(tam, { force: true });
  fs.rmSync(birlesikYol(rel), { force: true });
  return true;
}

/** Tam kopya olarak duran katman dosyaları (src/data'ya göre yol) */
function tamKopyalar(): string[] {
  const out: string[] = [];
  const gez = (d: string, onek: string) => {
    let ls: fs.Dirent[] = [];
    try { ls = fs.readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of ls) {
      if (e.name === BIRLESIK || e.name.startsWith('_') && !onek) continue;
      const r = onek ? `${onek}/${e.name}` : e.name;
      if (e.isDirectory()) gez(path.join(d, e.name), r);
      else if (e.name.endsWith('.json') && !e.name.endsWith(FARK_EK)) out.push(r);
    }
  };
  gez(DIR, '');
  return out;
}

const bekleyen = new Map<string, NodeJS.Timeout>();
function sonraDonustur(rel: string, deneme = 0) {
  if (bekleyen.has(rel)) clearTimeout(bekleyen.get(rel)!);
  bekleyen.set(rel, setTimeout(() => {
    bekleyen.delete(rel);
    try {
      if (fs.existsSync(tamYol(rel)) && !donustur(rel) && deneme < 40) sonraDonustur(rel, deneme + 1);
    } catch (e: any) { console.warn(`[katman] ${rel} farka çevrilemedi:`, e?.message); }
  }, 1500));
}

/** Okuma yolu: farkı varsa kaynak + fark birleşimi (önbellek dosyası), yoksa paketteki dosya */
export function resolveContent(file: string): string {
  const rel = relOf(file);
  if (!rel) return file;
  if (fs.existsSync(tamYol(rel))) {
    // Yazım kilidi sürerken yazıcı kendi tam kopyasını okusun
    if (kilitliMi(tamYol(rel))) return tamYol(rel);
    try { donustur(rel); } catch (e: any) { console.warn(`[katman] ${rel} farka çevrilemedi:`, e?.message); return tamYol(rel); }
    if (fs.existsSync(tamYol(rel))) return tamYol(rel);
  }
  const fy = farkYol(rel);
  const fm = mtimeOf(fy);
  if (!fm) return file;
  const by = birlesikYol(rel);
  const bm = mtimeOf(by);
  if (bm && bm >= fm && bm >= mtimeOf(file)) return by;
  try {
    const kaynak = fs.existsSync(file) ? okuJson(file) : undefined;
    const veri = farkUygula(kaynak, farkOku(rel));
    if (veri === undefined) return file;
    const g = girinti(file);
    atomikYaz(by, JSON.stringify(veri, null, g || undefined) + (g ? '\n' : ''));
    return by;
  } catch (e: any) {
    console.warn(`[katman] ${rel} birleştirilemedi:`, e?.message);
    return file;
  }
}

/** Yazma yolu: src/data altındaki her dosya katmana TAM yazılır; ardından farka çevrilir */
export function writableContent(file: string): string {
  const rel = relOf(file);
  if (!rel) return file;
  const o = tamYol(rel);
  fs.mkdirSync(path.dirname(o), { recursive: true });
  sonraDonustur(rel);
  return o;
}

function readIds(): Record<string, Record<string, number>> {
  try { return JSON.parse(fs.readFileSync(IDS_FILE(), 'utf8')) || {}; } catch { return {}; }
}

/** Değişen kayıt kimliklerini not eder (istemci yalnız bu desteleri sunucudan çeker) */
export function markContentChanged(entity: string, ids: string[] = []) {
  if (!DIR || !CONTENT_FILES[entity] || !ids.length) return;
  const all = readIds();
  const now = Date.now();
  all[entity] = { ...(all[entity] || {}) };
  for (const id of ids) all[entity][id] = now;
  fs.mkdirSync(DIR, { recursive: true });
  fs.writeFileSync(IDS_FILE(), JSON.stringify(all, null, 2), 'utf8');
}

/** Tür için katmanda iz var mı (fark ya da henüz çevrilmemiş tam kopya) */
export function katmandaVar(rel: string): boolean {
  return !!DIR && (fs.existsSync(farkYol(rel)) || fs.existsSync(tamYol(rel)));
}

/**
 * Paketten yeni olanlar. Fark dosyası dağıtımda silinince (imaj artık aynı) türü de listeden düşer.
 * decks: farktaki deste kimlikleri; ornek: farkı olan ders dosyaları (k1/k1-01 gibi).
 */
export function contentManifest() {
  const out: Record<string, { at: number; ids?: string[] }> = {};
  const ids = readIds();
  let pruned = false;
  for (const rel of tamKopyalar()) sonraDonustur(rel);
  for (const [entity, rel] of Object.entries(CONTENT_FILES)) {
    if (entity === 'ornek') {
      const o = path.join(DIR, rel);
      const files: string[] = [];
      let at = 0;
      try {
        for (const k of fs.readdirSync(o)) {
          const kd = path.join(o, k);
          if (!fs.statSync(kd).isDirectory()) continue;
          for (const f of fs.readdirSync(kd)) {
            const m = f.match(/^(.*)\.json(?:\.fark\.json)?$/);
            if (!m) continue;
            files.push(`${k}/${m[1]}`);
            at = Math.max(at, mtimeOf(path.join(kd, f)));
          }
        }
      } catch { /* klasör yok */ }
      const uniq = [...new Set(files)];
      if (uniq.length) out.ornek = { at, ids: uniq };
      continue;
    }
    if (!katmandaVar(rel)) {
      if (ids[entity]) { delete ids[entity]; pruned = true; }
      continue;
    }
    const f = farkOku(rel);
    const degisen = f && f.bicim !== 'tam' ? [...Object.keys(f.kayitlar || {}), ...(f.silinen || [])] : Object.keys(ids[entity] || {});
    out[entity] = { at: Math.max(mtimeOf(farkYol(rel)), mtimeOf(tamYol(rel))), ids: entity === 'decks' ? degisen : undefined };
  }
  if (pruned) try { fs.writeFileSync(IDS_FILE(), JSON.stringify(ids, null, 2), 'utf8'); } catch { /* yoksay */ }
  return out;
}
