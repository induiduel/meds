/**
 * Yönetim v16 — atomik JSON yazıcı (server-only).
 * Dosya başına tek yazıcı kilidi (söz zinciri) + aynı klasörde geçici dosya + fsync + rename + isteğe bağlı yedek.
 * Büyük dosyalarda (pastQuestions 96 MB, desteler 86 MB) yarım yazım / eşzamanlı ezme riskini kaldırır.
 * Mevcut yazma yollarına bağlamak: fs.writeFileSync(f, JSON.stringify(x)) → await atomikJsonYaz(f, x).
 */
import fs from 'fs';
import path from 'path';

const kilitler = new Map<string, Promise<unknown>>();

/** Aynı dosyaya yazan işleri sıraya koyar */
export function dosyaKilidi<T>(file: string, is: () => Promise<T> | T): Promise<T> {
  const key = path.resolve(file);
  const onceki = kilitler.get(key) || Promise.resolve();
  const sonraki = onceki.catch(() => {}).then(is);
  kilitler.set(key, sonraki);
  sonraki.finally(() => { if (kilitler.get(key) === sonraki) kilitler.delete(key); }).catch(() => {});
  return sonraki;
}

export type AtomikSecenek = {
  /** Yazmadan önce eski dosyanın kaç yedeği tutulsun (0 = yedek yok). Varsayılan 2. Yedek: <klasör>/_yedek/<ad>.<zaman>.json */
  yedek?: number;
  /** Yedek klasörü (varsayılan <dosya klasörü>/_yedek). data/content altındaki dosyalarda katman DIŞINA verin: eşitleme betiği oradaki her .json'u çeker. */
  yedekKlasoru?: string;
  girinti?: number;
  /** Boş dizi/nesne yazımını reddet (CLAUDE.md: boş sonuçla veri ezilmez). Varsayılan true */
  bosYazma?: boolean;
};

function bosMu(v: unknown) {
  return v == null || (Array.isArray(v) && v.length === 0) || (typeof v === 'object' && !Array.isArray(v) && Object.keys(v as object).length === 0);
}

function yedekle(file: string, n: number, klasor?: string) {
  if (n <= 0 || !fs.existsSync(file)) return;
  const dir = klasor || path.join(path.dirname(file), '_yedek');
  fs.mkdirSync(dir, { recursive: true });
  const ad = path.basename(file, '.json');
  fs.copyFileSync(file, path.join(dir, `${ad}.${new Date().toISOString().replace(/[:.]/g, '-')}.json`));
  const eski = fs.readdirSync(dir).filter((f) => f.startsWith(`${ad}.`) && f.endsWith('.json')).sort();
  for (const f of eski.slice(0, Math.max(0, eski.length - n))) fs.rmSync(path.join(dir, f), { force: true });
}

function yazSenkron(file: string, veri: unknown, o: AtomikSecenek) {
  if (o.bosYazma !== false && bosMu(veri)) throw new Error(`atomikJson: boş veri yazımı reddedildi (${path.basename(file)})`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const metin = JSON.stringify(veri, null, o.girinti ?? 2);
  const tmp = `${file}.${process.pid}.${Math.random().toString(36).slice(2, 8)}.tmp`;
  const fd = fs.openSync(tmp, 'w');
  try {
    fs.writeSync(fd, metin);
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
  try {
    yedekle(file, o.yedek ?? 2, o.yedekKlasoru);
    fs.renameSync(tmp, file);
  } catch (e) {
    fs.rmSync(tmp, { force: true });
    throw e;
  }
}

/** Kilitli atomik yazım */
export function atomikJsonYaz(file: string, veri: unknown, o: AtomikSecenek = {}): Promise<void> {
  return dosyaKilidi(file, () => yazSenkron(file, veri, o));
}

/** Kilit içinde oku → değiştir → yaz (okuma-yazma yarışı yok). fn eski değeri alır (dosya yoksa undefined). */
export function atomikJsonGuncelle<T>(file: string, fn: (eski: T | undefined) => T | Promise<T>, o: AtomikSecenek = {}): Promise<T> {
  return dosyaKilidi(file, async () => {
    let eski: T | undefined;
    try { eski = JSON.parse(fs.readFileSync(file, 'utf8')); } catch { eski = undefined; }
    const yeni = await fn(eski);
    yazSenkron(file, yeni, o);
    return yeni;
  });
}

/** Kilit beklemeden senkron yazım (yalnız tek yazıcının garanti olduğu yerlerde; açılış göçleri vb.) */
export function atomikJsonYazSenkron(file: string, veri: unknown, o: AtomikSecenek = {}) {
  yazSenkron(file, veri, o);
}

/** Dosyaya şu an kilitli bir yazım sürüyor mu (canlı katman dönüştürücüsü yazımın ortasına girmesin) */
export function kilitliMi(file: string): boolean {
  return kilitler.has(path.resolve(file));
}
