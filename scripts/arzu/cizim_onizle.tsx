/** Arzu katmanı çizimlerini büyük boyutta statik HTML olarak üretir (göz denetimi): npx tsx scripts/arzu/cizim_onizle.tsx <çıktı.html> */
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { writeFileSync } from 'node:fs';
import { TavsanZiplayan, TilkiYuruyen, TilkiOturan, KittyVeBatman } from '../../src/components/arzu/cizimler';
import { readFileSync } from 'node:fs';
const css = readFileSync(new URL('../../src/styles/arzu.css', import.meta.url), 'utf8');
const b = (el: React.ReactElement, cls: string) => `<div class="${cls}" style="position:static;display:inline-block;margin:16px;background:#fff;border-radius:12px;padding:12px;animation:none;transform:none;left:auto;bottom:auto">${renderToStaticMarkup(el)}</div>`;
const html = `<!doctype html><meta charset="utf-8"><style>body{background:#f4f6fa;font-family:sans-serif}${css}</style>
<h3>Tavşan (koşar)</h3>${b(<TavsanZiplayan width={420} />, 'ar-yaratik ar-tavsan is-kosar')}${b(<TavsanZiplayan width={420} />, 'ar-yaratik ar-tavsan is-durur')}
<h3>Tilki (koşar / selam)</h3>${b(<TilkiYuruyen width={420} />, 'ar-yaratik ar-tilki is-kosar')}${b(<TilkiYuruyen width={420} />, 'ar-yaratik ar-tilki is-selam')}
<h3>Oturan</h3>${b(<TilkiOturan width={300} />, 'ar-yoldas is-oturur')}${b(<TilkiOturan width={300} />, 'ar-yoldas is-uyur')}
<h3>Çift</h3>${b(<KittyVeBatman width={440} />, '')}`;
writeFileSync(process.argv[2], html);
console.log('yazildi');
