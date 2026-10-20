#!/usr/bin/env node
/**
 * Son Prova özet PDF'i: partın konuşma metninde atıf yapılan slayt sayfalarını kaynak ders PDF'lerinden kırpar, ders ve
 * sayfa sırasıyla tek PDF'te birleştirir; her sayfanın üstüne "Branş N) Ders · slayt S" şeridi ekler (etiket.py).
 * Girdi: meds_temp/son_prova/cikti/<key>/kirp.json (derle.py). Çıktı: data/son_prova/pdf/<key>.pdf + <key>.json (ad, sayfa).
 * Kullanım: node scripts/son_prova/pdf_kirp.mjs <kirp.json> [...]
 */
import fs from 'fs';
import path from 'path';
import os from 'os';
import { execFileSync } from 'child_process';
import { PDFDocument } from 'pdf-lib';

const MEDS = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const DRIVE = path.join(process.env.MEDS_DOWNLOADS_DIR || path.resolve(MEDS, '..', 'meds_downloads'), 'drive_root');

async function kirp(girdi) {
  const k = JSON.parse(fs.readFileSync(girdi, 'utf8'));
  const etiketPdf = path.join(os.tmpdir(), `sp-etiket-${process.pid}.pdf`);
  execFileSync('python3', [path.join(MEDS, 'scripts/son_prova/etiket.py'), girdi, etiketPdf]);
  const etiketDoc = await PDFDocument.load(fs.readFileSync(etiketPdf));
  fs.unlinkSync(etiketPdf);
  const out = await PDFDocument.create();
  out.setTitle(k.ad.replace(/\.pdf$/, ''));
  out.setAuthor('MeDSor Son Prova');
  out.setSubject('Konuşma metninde geçen ders slaytları (kaynak: fakülte ders PDF\'leri)');
  const kaynak = {};
  for (const [kod, rel] of Object.entries(k.kaynaklar)) {
    if (rel.startsWith('@metin:')) {
      // PDF'i paylaşılmamış ders: slayt metninden sayfalar (metin_pdf.py), sayfa numaraları aynı
      const gecici = path.join(os.tmpdir(), `sp-metin-${process.pid}-${kod}.pdf`);
      const ad = k.sayfalar.find((x) => x.kod === kod)?.etiket.replace(/ · slayt \d+$/, '') || kod;
      execFileSync('python3', [path.join(MEDS, 'scripts/son_prova/metin_pdf.py'), path.resolve(MEDS, '..', rel.slice(7)), gecici, ad]);
      kaynak[kod] = await PDFDocument.load(fs.readFileSync(gecici));
      fs.unlinkSync(gecici);
      continue;
    }
    kaynak[kod] = await PDFDocument.load(fs.readFileSync(path.join(DRIVE, rel)), { ignoreEncryption: true });
  }
  const etiketler = await out.embedPdf(etiketDoc, k.sayfalar.map((_, i) => i));
  // Her kaynaktan sayfalar TEK copyPages çağrısıyla alınır: ortak yazı tipi/resim nesneleri bir kez kopyalanır
  const kopya = new Map();
  for (const kod of Object.keys(kaynak)) {
    const src = kaynak[kod];
    const ss = k.sayfalar.filter((x) => x.kod === kod).map((x) => x.s);
    for (const s of ss) if (s < 1 || s > src.getPageCount()) throw new Error(`${kod}:${s} sayfa yok (${src.getPageCount()})`);
    const ps = await out.copyPages(src, ss.map((s) => s - 1));
    ss.forEach((s, i) => kopya.set(`${kod}:${s}`, ps[i]));
  }
  for (let i = 0; i < k.sayfalar.length; i++) {
    const s = k.sayfalar[i];
    const p = kopya.get(`${s.kod}:${s.s}`);
    out.addPage(p);
    const mb = p.getMediaBox();
    const cb = p.getCropBox();
    const kutu = cb && cb.width > 0 ? cb : mb;
    const band = Math.max(18, kutu.width * 0.03);
    // slaytın üstüne boş bant: kutu yukarı uzatılır, slayt içeriği yerinde kalır
    p.setMediaBox(kutu.x, kutu.y, kutu.width, kutu.height + band);
    p.setCropBox(kutu.x, kutu.y, kutu.width, kutu.height + band);
    p.drawPage(etiketler[i], { x: kutu.x, y: kutu.y + kutu.height, width: kutu.width, height: band });
  }
  const hedef = path.join(MEDS, k.cikti);
  fs.mkdirSync(path.dirname(hedef), { recursive: true });
  const bayt = await out.save({ useObjectStreams: true });
  fs.writeFileSync(hedef, bayt);
  fs.writeFileSync(hedef.replace(/\.pdf$/, '.json'), JSON.stringify({ name: k.ad, pages: k.sayfalar.length, bayt: bayt.length }));
  console.log(`${path.basename(hedef)}: ${k.sayfalar.length} sayfa, ${(bayt.length / 1048576).toFixed(1)} MB`);
}

for (const g of process.argv.slice(2)) await kirp(g);
