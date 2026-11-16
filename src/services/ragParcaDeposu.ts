/**
 * RAG parça deposu — kalıcılık katmanı (yalnız okuma/yazma; parçalama, tokenizer, BM25 burada YOK).
 *
 * Biçim (2026-11-16): `data/local_rag_chunks.jsonl` — satır başına bir parça nesnesi (JSONL).
 * Eski biçim: `data/local_rag_chunks.json` — tek satırlık dev JSON dizisi (~130 MB). Geçiş kuralı:
 *   - `.jsonl` VARSA esas odur (mtime'a bakılmaz); eski `.json` yok sayılır.
 *   - `.jsonl` yoksa eski `.json` okunur; ilk kayıtta `.jsonl` yazılır. Eski `.json` SİLİNMEZ (sonraki turda arşivlenir).
 * Okuma akışla (satır satır) yapılır: tek 130 MB `JSON.parse` + dev string yok; bozuk satır atlanır ve sayılır.
 * Yazma akışla `.jsonl.<pid>.tmp` → fsync → rename; yazılan satır sayısı ≠ parça sayısı ise rename yapılmaz.
 * Güvenlik freni: 0 parça ya da mevcut satır sayısının %50'sinin altı (mevcut ≥ 1000) yazılmaz; kaçış MEDS_RAG_BUDAMA_ZORLA=1.
 *
 * Bu modülün içe aktarımı yan etkisizdir (izleyici/zamanlayıcı yok) — sınama betikleri doğrudan kullanabilir.
 * Python eşi: scripts/rag_parca_deposu.py (aynı kural).
 */
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { StringDecoder } from 'string_decoder';
import { veriOlayi } from './veriGunlugu';

export const RAG_JSONL_ADI = 'local_rag_chunks.jsonl';
export const RAG_JSON_ESKI_ADI = 'local_rag_chunks.json';

export interface RagDosyalari { jsonl: string; eskiJson: string }

export function ragDosyalari(dataDir: string): RagDosyalari {
  return { jsonl: path.join(dataDir, RAG_JSONL_ADI), eskiJson: path.join(dataDir, RAG_JSON_ESKI_ADI) };
}

/** Okunacak dosya: `.jsonl` varsa o (kural), yoksa eski `.json`, ikisi de yoksa null. */
export function ragOkunacakDosya(dataDir: string): { yol: string; bicim: 'jsonl' | 'json' } | null {
  const d = ragDosyalari(dataDir);
  if (fs.existsSync(d.jsonl)) return { yol: d.jsonl, bicim: 'jsonl' };
  if (fs.existsSync(d.eskiJson)) return { yol: d.eskiJson, bicim: 'json' };
  return null;
}

export interface OkumaSonucu { parcalar: any[]; bozukSatir: number; dosya: string | null; bicim: 'jsonl' | 'json' | null }

function bozukRaporla(dosya: string, bozuk: number, ornekSatirlar: number[]) {
  if (bozuk > 0) veriOlayi('uyari', 'rag-yukleme', `${bozuk} bozuk satır atlandı`, { dosya, ornekSatirlar });
}

/**
 * Akışla okuma (sunucu açılışı). `nefes` verilirse her satırdan sonra çağrılır — çağıran zaman dilimli
 * düzenle (ör. 20 ms) olay döngüsüne nefes aldırır.
 */
export async function ragParcalariOku(dataDir: string, nefes?: () => Promise<void>): Promise<OkumaSonucu> {
  const hedef = ragOkunacakDosya(dataDir);
  if (!hedef) return { parcalar: [], bozukSatir: 0, dosya: null, bicim: null };
  if (hedef.bicim === 'json') {
    // Eski biçim yalnız geçişte bir kez okunur (ilk kayıtta .jsonl yazılır)
    const list = JSON.parse(await fs.promises.readFile(hedef.yol, 'utf-8'));
    return { parcalar: Array.isArray(list) ? list : (list?.chunks || []), bozukSatir: 0, dosya: hedef.yol, bicim: 'json' };
  }
  const parcalar: any[] = [];
  let bozuk = 0; let no = 0; const ornek: number[] = [];
  const rl = readline.createInterface({ input: fs.createReadStream(hedef.yol, { encoding: 'utf-8', highWaterMark: 1 << 20 }), crlfDelay: Infinity });
  for await (const satir of rl) {
    no++;
    if (!satir.trim()) continue;
    try {
      const p = JSON.parse(satir);
      if (p && typeof p === 'object' && p.id) parcalar.push(p); else throw new Error('kimliksiz');
    } catch { bozuk++; if (ornek.length < 10) ornek.push(no); }
    if (nefes) await nefes();
  }
  bozukRaporla(hedef.yol, bozuk, ornek);
  return { parcalar, bozukSatir: bozuk, dosya: hedef.yol, bicim: 'jsonl' };
}

/** Eşzamanlı okuma (alt süreç derleyicileri: queryIntel, hastalık grafiği, NotebookLM). Parça parça okur, dev string kurmaz. */
export function ragParcalariOkuSync(dataDir: string): OkumaSonucu {
  const hedef = ragOkunacakDosya(dataDir);
  if (!hedef) return { parcalar: [], bozukSatir: 0, dosya: null, bicim: null };
  if (hedef.bicim === 'json') {
    const list = JSON.parse(fs.readFileSync(hedef.yol, 'utf-8'));
    return { parcalar: Array.isArray(list) ? list : (list?.chunks || []), bozukSatir: 0, dosya: hedef.yol, bicim: 'json' };
  }
  const parcalar: any[] = [];
  let bozuk = 0; let no = 0; const ornek: number[] = [];
  const isle = (satir: string) => {
    no++;
    if (!satir.trim()) return;
    try {
      const p = JSON.parse(satir);
      if (p && typeof p === 'object' && p.id) parcalar.push(p); else throw new Error('kimliksiz');
    } catch { bozuk++; if (ornek.length < 10) ornek.push(no); }
  };
  const fd = fs.openSync(hedef.yol, 'r');
  try {
    const buf = Buffer.alloc(1 << 20);
    const dec = new StringDecoder('utf8');
    let kalan = '';
    for (;;) {
      const n = fs.readSync(fd, buf, 0, buf.length, null);
      if (n <= 0) break;
      const metin = kalan + dec.write(buf.subarray(0, n));
      const satirlar = metin.split('\n');
      kalan = satirlar.pop() as string;
      for (const s of satirlar) isle(s);
    }
    kalan += dec.end();
    if (kalan) isle(kalan);
  } finally { fs.closeSync(fd); }
  bozukRaporla(hedef.yol, bozuk, ornek);
  return { parcalar, bozukSatir: bozuk, dosya: hedef.yol, bicim: 'jsonl' };
}

/** Diskteki mevcut kayıt sayısı (fren için): jsonl'de boş olmayan satır, eski json'da dizi uzunluğu (bilinmiyorsa -1). */
export function ragMevcutSayi(dataDir: string): number {
  const d = ragDosyalari(dataDir);
  if (fs.existsSync(d.jsonl)) {
    const fd = fs.openSync(d.jsonl, 'r');
    try {
      const buf = Buffer.alloc(1 << 20);
      let n = 0; let son = 10; let okunan: number;
      while ((okunan = fs.readSync(fd, buf, 0, buf.length, null)) > 0) {
        for (let i = 0; i < okunan; i++) if (buf[i] === 10) n++;
        son = buf[okunan - 1];
      }
      return son === 10 ? n : n + 1;
    } finally { fs.closeSync(fd); }
  }
  // Eski json yalnız geçişte; boyutundan kaba tahmin yerine fren uygulanmaz (dev JSON'u yeniden ayrıştırmamak için)
  return -1;
}

/** Fren: yazılmamalıysa gerekçe döner. */
export function ragFrenGerekcesi(yeni: number, mevcut: number): string | null {
  if (process.env.MEDS_RAG_BUDAMA_ZORLA === '1') return null;
  if (yeni === 0) return 'yazılacak parça sayısı 0';
  if (mevcut >= 1000 && yeni < mevcut * 0.5) return `yazılacak ${yeni} parça, mevcut ${mevcut} satırın %50'sinin altında`;
  return null;
}

export interface YazmaSonucu { yazildi: boolean; satir: number; bayt: number; gerekce?: string }

/** Akışla atomik yazım: tmp → fsync → rename. Hata/uyuşmazlıkta eski dosya yerinde kalır. */
export async function ragParcalariYaz(dataDir: string, parcalar: Iterable<any>, adet: number): Promise<YazmaSonucu> {
  const { jsonl } = ragDosyalari(dataDir);
  const fren = ragFrenGerekcesi(adet, ragMevcutSayi(dataDir));
  if (fren) {
    veriOlayi('hata', 'rag-kayit', `RAG parça kaydı durduruldu: ${fren}; eski dosya korundu`, { dosya: jsonl, kacis: 'MEDS_RAG_BUDAMA_ZORLA=1' });
    return { yazildi: false, satir: 0, bayt: 0, gerekce: fren };
  }
  const tmp = `${jsonl}.${process.pid}.tmp`;
  const fh = await fs.promises.open(tmp, 'w');
  let satir = 0; let bayt = 0;
  try {
    let tampon: string[] = []; let tamponUzun = 0;
    const bosalt = async () => {
      if (!tampon.length) return;
      const b = Buffer.from(tampon.join(''), 'utf-8');
      await fh.write(b);
      bayt += b.length; tampon = []; tamponUzun = 0;
    };
    for (const p of parcalar) {
      const s = JSON.stringify(p) + '\n';
      tampon.push(s); tamponUzun += s.length; satir++;
      if (tamponUzun >= 1 << 20) await bosalt(); // ~1 MB'lık parçalar; aralarda döngü serbest
    }
    await bosalt();
    await fh.sync();
  } catch (e) {
    await fh.close().catch(() => {});
    await fs.promises.unlink(tmp).catch(() => {});
    throw e;
  }
  await fh.close();
  if (satir !== adet) {
    await fs.promises.unlink(tmp).catch(() => {});
    const g = `yazılan satır ${satir} ≠ bellekteki parça ${adet}`;
    veriOlayi('hata', 'rag-kayit', `RAG parça kaydı iptal: ${g}; eski dosya korundu`, { dosya: jsonl });
    return { yazildi: false, satir, bayt, gerekce: g };
  }
  await fs.promises.rename(tmp, jsonl);
  return { yazildi: true, satir, bayt };
}

/** Eşzamanlı eşi (NotebookLM gibi küçük eşzamanlı yazarlar için) — aynı fren ve atomiklik. */
export function ragParcalariYazSync(dataDir: string, parcalar: any[]): YazmaSonucu {
  const { jsonl } = ragDosyalari(dataDir);
  const fren = ragFrenGerekcesi(parcalar.length, ragMevcutSayi(dataDir));
  if (fren) {
    veriOlayi('hata', 'rag-kayit', `RAG parça kaydı durduruldu: ${fren}; eski dosya korundu`, { dosya: jsonl, kacis: 'MEDS_RAG_BUDAMA_ZORLA=1' });
    return { yazildi: false, satir: 0, bayt: 0, gerekce: fren };
  }
  const tmp = `${jsonl}.${process.pid}.tmp`;
  const fd = fs.openSync(tmp, 'w');
  let satir = 0; let bayt = 0;
  try {
    let tampon: string[] = []; let uz = 0;
    const bosalt = () => { if (!tampon.length) return; const b = Buffer.from(tampon.join(''), 'utf-8'); fs.writeSync(fd, b); bayt += b.length; tampon = []; uz = 0; };
    for (const p of parcalar) { const s = JSON.stringify(p) + '\n'; tampon.push(s); uz += s.length; satir++; if (uz >= 1 << 20) bosalt(); }
    bosalt();
    fs.fsyncSync(fd);
  } catch (e) {
    fs.closeSync(fd); try { fs.unlinkSync(tmp); } catch { /* yok */ }
    throw e;
  }
  fs.closeSync(fd);
  if (satir !== parcalar.length) {
    try { fs.unlinkSync(tmp); } catch { /* yok */ }
    veriOlayi('hata', 'rag-kayit', `RAG parça kaydı iptal: satır ${satir} ≠ parça ${parcalar.length}`, { dosya: jsonl });
    return { yazildi: false, satir, bayt, gerekce: 'satır uyuşmazlığı' };
  }
  fs.renameSync(tmp, jsonl);
  return { yazildi: true, satir, bayt };
}
