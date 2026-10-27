/** Ders PDF'inin bağımsız HTML'i (uygulama stilinden yalıtılmış): tarayıcıda iframe'e, Node'da Chrome'a verilir — iki yol aynı çıktıyı üretir. */
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import DersPdfBelge from './DersPdfBelge';
import type { PdfAkis } from './dersPdfAkis';

export function dersPdfHtml(akis: PdfAkis, kod: string, css: string, onizleme = false): string {
  const govde = renderToStaticMarkup(React.createElement(DersPdfBelge, { akis, kod }));
  const on = onizleme ? '@media screen { body { background: #d8dce3; margin: 0; padding: 16px 0; } .dpdf { width: 960px; margin: 0 auto; padding: 28px 36px; background: #fff; box-shadow: 0 2px 20px rgba(0,0,0,.2); } }' : '';
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>${akis.baslik.replace(/</g, '&lt;')}</title><style>${css}${on}</style></head><body>${govde}</body></html>`;
}
