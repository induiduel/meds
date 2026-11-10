/**
 * Çalışma föyünün hazır PDF'i: ekrandaki "PDF oluştur" ile AYNI belge (src/components/v15/ekModul/ekFoyBelge.ts), bütün konular,
 * cevap anahtarlı → public/ek_moduller/<modül>/pdf/<modül>-calisma-foyu.pdf (başsız Chrome).
 * Kullanım (çalışma dizini meds/): npx tsx scripts/ek_modul/foy_pdf.mts yuruyus-kampcilik [konu,konu… | --cozumlu]
 * --cozumlu: hocanın setleri kendi sırasıyla, cevap + çözüm metni → <modül>-cozumlu-sorular.pdf
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { cozumluBelge, foyBelge } from '../../src/components/v15/ekModul/ekFoyBelge';

const modul = process.argv[2];
const kok = path.resolve('src/data/ek_moduller', modul);
const oku = (ad: string) => JSON.parse(readFileSync(path.join(kok, ad), 'utf8'));
const ozet = JSON.parse(readFileSync(path.resolve('src/data/ek_moduller/index.json'), 'utf8')).moduller.find((m: any) => m.id === modul);
const basliklar = readdirSync(kok).filter((f) => /^b\d+\.json$/.test(f)).map(oku).sort((a, b) => a.no - b.no);
const m: any = { ozet, basliklar, hoca: oku('hoca_sorulari.json'), foy: oku('foy.json') };
const konular = basliklar.flatMap((b: any) => b.konular);
const cozumlu = process.argv[3] === '--cozumlu';
const secili = process.argv[3] && !cozumlu ? process.argv[3].split(',') : konular.map((k: any) => k.id);
const gorselKok = path.resolve('public/ek_moduller', modul);
const gorseller: Record<string, string> = {};
[ozet.kapak, ...konular.map((k: any) => k.gorsel)].forEach((d: string) => { gorseller[d] = pathToFileURL(path.join(gorselKok, d)).href; });
const html = path.join(tmpdir(), `foy-${modul}.html`);
writeFileSync(html, cozumlu ? cozumluBelge(m, gorseller) : foyBelge(m, secili, true, gorseller));
const hedef = path.join(gorselKok, 'pdf', cozumlu ? `${modul}-cozumlu-sorular.pdf` : `${modul}-calisma-foyu${process.argv[3] ? `-${secili.join('-')}` : ''}.pdf`);
mkdirSync(path.dirname(hedef), { recursive: true });
execFileSync('google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files', `--print-to-pdf=${hedef}`, pathToFileURL(html).href], { stdio: 'ignore', timeout: 180000 });
console.log(hedef);
