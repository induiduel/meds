/** Ders PDF'i (yapay zekasız, limitsiz): python scripts/ders_icerik_adim.py ile `adim` yazılmış paketten slayt sırasıyla
 *  "anlatım → özet" akışlı PDF üretir (720×540 pt sayfalar). Kullanım: npx tsx scripts/ders_pdf.mts <key> [çıktı.pdf]
 *  Gerekli: google-chrome (headless --print-to-pdf). */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { renderToStaticMarkup } from 'react-dom/server';
import React from 'react';
import { dersPdfAkisi } from '../src/components/v15/dersPdfAkis';
import DersPdfBelge from '../src/components/v15/DersPdfBelge';

const R = path.resolve(import.meta.dirname, '..');
const key = process.argv[2];
if (!key) { console.error('Kullanım: npx tsx scripts/ders_pdf.mts <key> [çıktı.pdf]'); process.exit(2); }
const paket = JSON.parse(fs.readFileSync(path.join(R, 'src/data/ders_icerik', key + '.json'), 'utf8'));
const deste = JSON.parse(fs.readFileSync(path.join(R, 'src/data/decks/items', `k2p-${key}.json`), 'utf8'));
const akis = dersPdfAkisi({ ...paket, baslik: paket.baslik || deste.title }, deste.slides);
const css = fs.readFileSync(path.join(R, 'src/styles/v15/dersPdf.css'), 'utf8');
const html = `<!doctype html><html lang="tr"><meta charset="utf-8"><title>${akis.baslik}</title><style>${css}</style><body>${renderToStaticMarkup(React.createElement(DersPdfBelge, { akis, kod: key.split('-').slice(0, 2).join('-').toUpperCase() }))}</body></html>`;
const cikti = path.resolve(process.argv[3] || `${key}.pdf`);
const gecici = cikti.replace(/\.pdf$/, '') + '.html';
fs.writeFileSync(gecici, html);
execFileSync('google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', `--print-to-pdf=${cikti}`, 'file://' + gecici], { stdio: 'inherit' });
fs.unlinkSync(gecici);
console.log('PDF:', cikti, `${akis.adimlar.length} adım`);
